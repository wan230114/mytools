#!/usr/bin/env python3
import argparse
import re
import shlex
from collections import defaultdict
from datetime import datetime

SNAPSHOT_RE = re.compile(r'^\[Now_time\]:\s*([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]+)\s*,\s*used time:\s*(\S+)')
CMD_RE = re.compile(r'^[ \t]*\\?_?[ \t]*(.*\S.*)$')


def parse_log(path):
    snapshots = []
    current_ts = None
    current_cmds = []

    with open(path, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            m = SNAPSHOT_RE.match(line)
            if m:
                if current_ts is not None:
                    snapshots.append((current_ts, current_cmds))
                current_ts = datetime.fromisoformat(m.group(1))
                current_cmds = []
                continue

            if current_ts is None:
                continue
            if not line.strip():
                continue

            cmd_match = CMD_RE.match(line)
            if not cmd_match:
                continue
            cmd = cmd_match.group(1).strip()
            if cmd:
                current_cmds.append(cmd)

    if current_ts is not None:
        snapshots.append((current_ts, current_cmds))

    return snapshots


def build_intervals(snapshots):
    active = {}
    intervals = defaultdict(list)
    last_ts = None

    for ts, cmds in snapshots:
        last_ts = ts
        seen = set(cmds)

        # end intervals for commands no longer present
        for cmd in list(active):
            if cmd not in seen:
                start_ts = active.pop(cmd)
                intervals[cmd].append((start_ts, ts))

        # start intervals for newly present commands
        for cmd in seen:
            if cmd not in active:
                active[cmd] = ts

    # close any commands still active at end of log
    for cmd, start_ts in active.items():
        intervals[cmd].append((start_ts, last_ts))

    return intervals


def is_meaningful_command(cmd):
    if re.match(r'^\[.*\](?: <defunct>)?$', cmd):
        return False
    if cmd.startswith('sh run_mirge3.sh'):
        return False
    if re.match(r'^/bin/sh -c\s+', cmd):
        return False
    if re.match(r'^/.*python .*miRge3\.0\b', cmd):
        return False
    if '--version' in cmd:
        return False
    return True


def format_duration(delta):
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def shell_quote(value):
    return shlex.quote(value)


def common_prefix(strings):
    if not strings:
        return ''
    prefix = strings[0]
    for s in strings[1:]:
        max_len = min(len(prefix), len(s))
        i = 0
        while i < max_len and prefix[i] == s[i]:
            i += 1
        prefix = prefix[:i]
        if not prefix:
            break
    return prefix


def common_suffix(strings):
    if not strings:
        return ''
    suffix = strings[0]
    for s in strings[1:]:
        max_len = min(len(suffix), len(s))
        i = 0
        while i < max_len and suffix[-1 - i] == s[-1 - i]:
            i += 1
        suffix = suffix[-i:] if i else ''
        if not suffix:
            break
    return suffix


def compute_template(values):
    if len(set(values)) == 1:
        return values[0], None
    prefix = common_prefix(values)
    suffix = common_suffix([v[len(prefix):] for v in values])
    if len(prefix) + len(suffix) >= min(len(v) for v in values):
        return None, None
    var_values = [v[len(prefix):len(v) - len(suffix) if len(suffix) else None] for v in values]
    if any(v == '' for v in var_values):
        return None, None
    if len(set(var_values)) == 1:
        return None, None
    return prefix + '${VAR}' + suffix, var_values


def derive_var_name(var_values, token_template):
    if all(re.match(r'^[A-Za-z0-9_.+-]+$', v) for v in var_values):
        if '/' not in token_template and '.' not in token_template:
            return 'ITEM'
        return 'SAMPLE'
    return 'VALUE'


def render_template_tokens(tokens, var_name):
    output = []
    for token in tokens:
        output.append(token.replace('${VAR}', f'${{{var_name}}}'))
    return ' '.join(output)


def cluster_commands(rows):
    # Collapse exact identical commands first
    command_map = defaultdict(list)
    for _, _, duration, cmd in rows:
        command_map[cmd].append(duration)

    unique_cmds = list(command_map.keys())
    token_map = {}
    for cmd in unique_cmds:
        try:
            token_map[cmd] = shlex.split(cmd)
        except ValueError:
            token_map[cmd] = cmd.split()

    clusters = []
    used = set()

    for cmd in unique_cmds:
        if cmd in used:
            continue
        base_tokens = token_map[cmd]
        cluster_cmds = [cmd]
        used.add(cmd)

        for other in unique_cmds:
            if other in used or other == cmd:
                continue
            other_tokens = token_map[other]
            if len(other_tokens) != len(base_tokens) or other_tokens[0] != base_tokens[0]:
                continue
            diff_positions = [i for i, (a, b) in enumerate(zip(base_tokens, other_tokens)) if a != b]
            if not diff_positions or len(diff_positions) > 2:
                continue

            values_by_pos = []
            templates = []
            for pos in diff_positions:
                values = [token_map[c][pos] for c in cluster_cmds] + [other_tokens[pos]]
                template, var_values = compute_template(values)
                if template is None:
                    break
                values_by_pos.append(tuple(var_values))
                templates.append(template)
            else:
                if len(values_by_pos) == 1 or all(values_by_pos[0] == values for values in values_by_pos[1:]):
                    cluster_cmds.append(other)
                    used.add(other)

        clusters.append(cluster_cmds)

    grouped = []
    for cluster_cmds in clusters:
        tokens = token_map[cluster_cmds[0]]
        diff_positions = [i for i in range(len(tokens))
                          if len({token_map[c][i] for c in cluster_cmds}) > 1]
        if not diff_positions:
            grouped.append((cluster_cmds, tokens, None, None))
            continue

        token_templates = list(tokens)
        var_values = None
        for pos in diff_positions:
            values = [token_map[c][pos] for c in cluster_cmds]
            template, values_list = compute_template(values)
            if template is None:
                token_templates = None
                break
            token_templates[pos] = template
            if var_values is None:
                var_values = values_list
            elif tuple(var_values) != tuple(values_list):
                token_templates = None
                break

        if token_templates is None:
            grouped.append((cluster_cmds, tokens, None, None))
            continue

        var_name = derive_var_name(var_values, token_templates[diff_positions[0]])
        grouped.append((cluster_cmds, token_templates, var_name, var_values))

    return grouped, command_map


def format_grouped_output(rows):
    grouped, command_map = cluster_commands(rows)
    out_lines = []

    for cluster_cmds, tokens, var_name, var_values in grouped:
        if var_name is not None and len(cluster_cmds) > 1:
            durations = [(var_values[i], command_map[cluster_cmds[i]][0]) for i in range(len(cluster_cmds))]
            out_lines.append(f'# group of {len(cluster_cmds)} similar commands')
            out_lines.append('# durations: ' + ' '.join(f'{v}={format_duration(d)}' for v, d in durations))
            array_name = var_name + 'S'
            quoted_values = ' '.join(shell_quote(v) for v, _ in durations)
            out_lines.append(f'{array_name}=({quoted_values})')
            out_lines.append(f'for {var_name} in "${{{array_name}[@]}}"; do')
            out_lines.append(f'  {render_template_tokens(tokens, var_name)}')
            out_lines.append('done')
            out_lines.append('')
        else:
            for cmd in cluster_cmds:
                duration = command_map[cmd][0]
                out_lines.append(f'# duration: {format_duration(duration)}')
                out_lines.append(cmd)
                out_lines.append('')
    return out_lines


def main():
    parser = argparse.ArgumentParser(description='提纯日志，输出优化后的命令脚本，类似 for 循环 + 变量替换。')
    parser.add_argument('logfile', help='输入日志文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径，默认 stdout')
    args = parser.parse_args()
    snapshots = parse_log(args.logfile)
    if not snapshots:
        raise SystemExit('未能解析任何日志快照，请确认日志文件格式是否符合')

    intervals = build_intervals(snapshots)
    rows = []
    for cmd, spans in intervals.items():
        if not is_meaningful_command(cmd):
            continue
        for start_ts, end_ts in spans:
            duration = end_ts - start_ts
            rows.append((start_ts, end_ts, duration, cmd))

    rows.sort(key=lambda x: x[0])
    out_lines = format_grouped_output(rows)

    output_text = '\n'.join(out_lines)
    if output_text and not output_text.endswith('\n'):
        output_text += '\n'
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fh:
            fh.write(output_text)
    else:
        try:
            print(output_text, end='')
        except BrokenPipeError:
            pass


if __name__ == '__main__':
    main()
