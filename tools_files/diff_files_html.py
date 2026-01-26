#!/usr/bin/env python3
"""
文件差异对比HTML生成工具 - 宽度优化版
用法: python generate_diff_html.py file1 file2 [输出文件]
"""

import difflib
import sys
import os
import argparse
from datetime import datetime

def read_file_lines(filepath):
    """读取文件内容，返回行列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except UnicodeDecodeError:
        # 如果utf-8失败，尝试其他编码
        with open(filepath, 'r', encoding='gbk') as f:
            return f.readlines()
    except Exception as e:
        print(f"错误: 无法读取文件 {filepath}")
        print(f"错误信息: {e}")
        sys.exit(1)

def generate_html_diff(file1, file2, output_file, title=None):
    """生成差异对比HTML文件"""
    
    # 读取文件内容
    print(f"正在读取文件: {file1}")
    lines1 = read_file_lines(file1)
    
    print(f"正在读取文件: {file2}")
    lines2 = read_file_lines(file2)
    
    # 设置默认标题
    if title is None:
        title = f"文件差异对比报告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # 提取文件名
    file1_name = os.path.basename(file1)
    file2_name = os.path.basename(file2)
    
    # 创建HtmlDiff对象
    differ = difflib.HtmlDiff(
        tabsize=4,  # 制表符宽度
        wrapcolumn=80,  # 自动换行列数
    )
    
    # 生成HTML内容
    print("正在生成差异对比报告...")
    html_content = differ.make_file(
        fromlines=lines1,
        tolines=lines2,
        fromdesc=f"原文件: {file1_name}",
        todesc=f"新文件: {file2_name}",
        context=True,  # 显示上下文
        numlines=3,  # 上下文行数
    )
    
    # 添加自定义CSS样式 - 优化宽度
    custom_css = """
    <style>
    * {
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        margin: 0;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        color: #333;
        overflow-x: hidden;  /* 防止水平滚动条 */
    }
    
    .container {
        max-width: 100vw;  /* 最大宽度为视口宽度 */
        margin: 0 auto;
    }
    
    .header {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .header h1 {
        margin: 0 0 15px 0;
        font-size: 1.5em;
        color: #2c3e50;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .file-info {
        display: flex;
        flex-direction: column;
        gap: 8px;
        font-size: 0.9em;
    }
    
    .file-path {
        background: #f8f9fa;
        padding: 8px 12px;
        border-radius: 4px;
        border-left: 4px solid #667eea;
        word-break: break-all;  /* 允许长路径换行 */
    }
    
    .file-path strong {
        color: #495057;
    }
    
    /* 差异表格容器 - 添加滚动条 */
    .table-container {
        background: white;
        border-radius: 8px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow-x: auto;  /* 水平滚动条 */
        max-width: 100%;    /* 最大宽度100% */
    }
    
    .diff_table {
        min-width: 100%;    /* 最小宽度100%，确保表格不压缩 */
        border-collapse: collapse;
        font-size: 0.9em;
        line-height: 1.4;
    }
    
    /* 设置表格列宽 */
    .diff_table th,
    .diff_table td {
        padding: 8px 12px;
        vertical-align: top;
        text-align: left;
        white-space: pre-wrap;  /* 保持空白，允许换行 */
        word-break: break-all;  /* 允许长单词换行 */
        max-width: 600px;       /* 限制每列最大宽度 */
    }
    
    /* 行号列固定宽度 */
    .diff_table th:nth-child(1),
    .diff_table th:nth-child(3),
    .diff_table td:nth-child(1),
    .diff_table td:nth-child(3) {
        width: 60px;  /* 固定行号列宽度 */
        min-width: 60px;
        max-width: 60px;
        text-align: right;
        background-color: #f8f9fa;
        color: #6c757d;
        border-right: 2px solid #dee2e6;
        white-space: nowrap;  /* 行号不换行 */
    }
    
    /* 内容列自适应宽度 */
    .diff_table th:nth-child(2),
    .diff_table th:nth-child(4),
    .diff_table td:nth-child(2),
    .diff_table td:nth-child(4) {
        min-width: 300px;  /* 最小宽度 */
        max-width: 600px;  /* 最大宽度，防止过长 */
    }
    
    .diff_header {
        background-color: #2c3e50;
        color: white;
        font-weight: bold;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .diff_next {
        background-color: #f8f9fa;
    }
    
    /* 差异高亮样式 */
    .diff_add {
        background-color: #d4edda;
    }
    
    .diff_chg {
        background-color: #fff3cd;
    }
    
    .diff_sub {
        background-color: #f8d7da;
    }
    
    /* 统计信息 */
    .summary {
        background: white;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .stat-box {
        text-align: center;
        padding: 15px;
        border-radius: 6px;
        background: #f8f9fa;
        transition: transform 0.2s;
    }
    
    .stat-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stat-box.added {
        border-left: 4px solid #28a745;
    }
    
    .stat-box.deleted {
        border-left: 4px solid #dc3545;
    }
    
    .stat-box.changed {
        border-left: 4px solid #ffc107;
    }
    
    .stat-value {
        font-size: 1.8em;
        font-weight: bold;
        margin: 5px 0;
    }
    
    .stat-label {
        font-size: 0.9em;
        color: #6c757d;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        body {
            padding: 10px;
        }
        
        .header h1 {
            font-size: 1.2em;
        }
        
        .file-info {
            font-size: 0.8em;
        }
        
        .diff_table th,
        .diff_table td {
            padding: 6px 8px;
            font-size: 0.85em;
        }
        
        .diff_table th:nth-child(1),
        .diff_table th:nth-child(3),
        .diff_table td:nth-child(1),
        .diff_table td:nth-child(3) {
            width: 50px;
            min-width: 50px;
            max-width: 50px;
        }
        
        .stats {
            grid-template-columns: 1fr;
        }
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        height: 8px;
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    </style>
    
    <script>
    // 添加一些交互功能
    document.addEventListener('DOMContentLoaded', function() {
        // 高亮切换功能
        const highlightButtons = document.querySelectorAll('.highlight-btn');
        highlightButtons.forEach(button => {
            button.addEventListener('click', function() {
                const type = this.dataset.type;
                const elements = document.querySelectorAll('.diff_' + type);
                elements.forEach(el => {
                    el.style.opacity = el.style.opacity === '0.3' ? '1' : '0.3';
                });
            });
        });
        
        // 搜索功能
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                const rows = document.querySelectorAll('.diff_table tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (searchTerm && text.includes(searchTerm)) {
                        row.style.backgroundColor = '#fff3cd';
                    } else {
                        row.style.backgroundColor = '';
                    }
                });
            });
        }
        
        // 复制文件路径功能
        const copyButtons = document.querySelectorAll('.copy-btn');
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const path = this.dataset.path;
                navigator.clipboard.writeText(path).then(() => {
                    alert('文件路径已复制到剪贴板: ' + path);
                });
            });
        });
    });
    </script>
    """
    
    # 插入自定义CSS
    html_content = html_content.replace('</head>', custom_css + '\n</head>')
    
    # 计算一些统计信息
    diff = difflib.SequenceMatcher(None, lines1, lines2)
    added_lines = 0
    deleted_lines = 0
    changed_lines = 0
    
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        if tag == 'insert':
            added_lines += (j2 - j1)
        elif tag == 'delete':
            deleted_lines += (i2 - i1)
        elif tag == 'replace':
            changed_lines += max((i2 - i1), (j2 - j1))
    
    # 添加头部信息和表格容器
    header = f"""
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="file-info">
                <div class="file-path">
                    <strong>原文件:</strong> {file1}
                </div>
                <div class="file-path">
                    <strong>新文件:</strong> {file2}
                </div>
                <div style="margin-top: 10px; font-size: 0.9em; color: #6c757d;">
                    <strong>生成时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                    <strong>原文件行数:</strong> {len(lines1)} | 
                    <strong>新文件行数:</strong> {len(lines2)}
                </div>
            </div>
            
            <div style="margin-top: 15px;">
                <input type="text" id="searchInput" placeholder="搜索差异内容..." 
                       style="padding: 8px 12px; width: 100%; max-width: 300px; 
                              border: 1px solid #ddd; border-radius: 4px; font-size: 0.9em;">
                <div style="margin-top: 10px; display: flex; gap: 10px;">
                    <button class="highlight-btn" data-type="add" 
                            style="background: #28a745; color: white; border: none; 
                                   padding: 6px 12px; border-radius: 4px; cursor: pointer; 
                                   font-size: 0.85em;">
                        切换新增高亮
                    </button>
                    <button class="highlight-btn" data-type="sub" 
                            style="background: #dc3545; color: white; border: none; 
                                   padding: 6px 12px; border-radius: 4px; cursor: pointer; 
                                   font-size: 0.85em;">
                        切换删除高亮
                    </button>
                    <button class="highlight-btn" data-type="chg" 
                            style="background: #ffc107; color: #333; border: none; 
                                   padding: 6px 12px; border-radius: 4px; cursor: pointer; 
                                   font-size: 0.85em;">
                        切换修改高亮
                    </button>
                </div>
            </div>
        </div>
        
        <div class="summary">
            <h3 style="margin-top: 0;">差异统计</h3>
            <div class="stats">
                <div class="stat-box added">
                    <div class="stat-label">新增行数</div>
                    <div class="stat-value">+{added_lines}</div>
                </div>
                <div class="stat-box deleted">
                    <div class="stat-label">删除行数</div>
                    <div class="stat-value">-{deleted_lines}</div>
                </div>
                <div class="stat-box changed">
                    <div class="stat-label">修改行数</div>
                    <div class="stat-value">~{changed_lines}</div>
                </div>
            </div>
        </div>
        
        <div class="table-container">
    """
    
    # 在HTML的body开始处添加头部
    html_content = html_content.replace('<body>', '<body>\n' + header)
    
    # 在表格后添加关闭标签
    html_content = html_content.replace('</table>', '</table>\n</div>\n</div>')
    
    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 差异报告已生成: {output_file}")
    print(f"📁 文件大小: {os.path.getsize(output_file)} 字节")
    print(f"🔍 可以在浏览器中打开查看: file://{os.path.abspath(output_file)}")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(
        description='生成两个文件的差异对比HTML报告 - 宽度优化版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s file1.txt file2.txt
  %(prog)s file1.txt file2.txt -o diff_report.html
  %(prog)s /path/to/old.md /path/to/new.md -o comparison.html
        """
    )
    
    parser.add_argument('file1', help='第一个文件（原文件）路径')
    parser.add_argument('file2', help='第二个文件（新文件）路径')
    parser.add_argument('-o', '--output', default='diff_report.html', 
                       help='输出HTML文件路径 (默认: diff_report.html)')
    parser.add_argument('-t', '--title', help='报告标题')
    parser.add_argument('-O', '--open', action='store_true',
                       help='生成后自动在浏览器中打开')
    parser.add_argument('--nowrap', action='store_true',
                       help='禁用自动换行（保持原始格式）')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    for filepath in [args.file1, args.file2]:
        if not os.path.exists(filepath):
            print(f"错误: 文件不存在 - {filepath}")
            sys.exit(1)
    
    # 生成差异报告
    output_path = generate_html_diff(args.file1, args.file2, args.output, args.title)
    
    # 如果指定了自动打开
    if args.open:
        import webbrowser
        try:
            webbrowser.open(f'file://{os.path.abspath(output_path)}')
            print("🌐 已在浏览器中打开报告")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")

if __name__ == '__main__':
    main()