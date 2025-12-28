#!/bin/bash

# 创建临时文件存储标题和数据
temp_file=$(mktemp)

# 写入标题行
echo -e "IMAGE ID\tREPOSITORY:TAG\tSIZE\tCREATED\t创建真实日期" > "$temp_file"

# 追加Docker镜像信息
docker images --format "{{.ID}}\t{{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}\t{{.CreatedAt}}" >> "$temp_file"

# 使用column命令格式化输出
column -t -s $'\t' "$temp_file"

# 清理临时文件
rm -f "$temp_file"