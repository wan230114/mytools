#!/bin/bash

# crontab -e
# * * * * * /work/soft/moni_docer/moni_docer.sh /work/soft/moni_docer/logs
# * * * * * sleep 30; /work/soft/moni_docer/moni_docer.sh /work/soft/moni_docer/logs

# 一次性获取所有运行中容器的统计信息，跳过标题行
cd /work/soft/moni_docer/
container_ids=$(docker ps | grep -vf black_kw.txt | tail -n +2 | awk '{print $1}' | xargs)

logdir=$1
# 检查是否有容器数据
if [[ -n "$container_ids" ]]; then
    mkdir -p $logdir
    docker_stats=$(docker stats --no-stream --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $container_ids | tail -n +2 )
    # 获取当前时间戳
    timestamp=$(date '+%F %T')
    
    # 逐行处理每个容器的统计信息
    while IFS= read -r line; do
        # 检查数据是否有效
        if [[ $line != *"N/A"* ]]; then
            # 提取容器ID (使用更可靠的方法)
            container_id=$(echo "$line" | awk '{print $1}')
            name=$(echo "$line" | awk '{print $2}')


            # 确保容器ID不为空
            if [[ -n "$container_id" ]]; then
                # 使用显式的容器ID并保存退出状态
                container_cmd=$(docker inspect --format '{{.Path}} {{.Args}}' "$container_id" 2>/dev/null)
                container_runs_cmd=$(docker exec "$container_id" ps -eo cmd | sed 1d | grep -v "ps -eo cmd" | xargs -I {} echo -en "{};  ")
                exit_status=$?
                
                # 检查docker inspect命令是否成功执行
                if [[ $exit_status -eq 0 && -n "$container_cmd" ]]; then
                    # 将命令添加到输出行的末尾并写入日志
                    echo -e "$timestamp\t$line\t\"$container_cmd\"\t\"$container_runs_cmd\"" >>$logdir/docker_stats_${container_id}_${name}.log
                else
                    # 如果获取命令失败，记录具体的容器ID和错误
                    echo -e "$timestamp\t$line\t[ERROR: Failed to get command for container $container_id]" >>$logdir/docker_stats_${container_id}_${name}.log
                fi
            fi
        fi
    done <<< "$docker_stats"
fi
