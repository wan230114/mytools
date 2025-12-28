#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#############################################
# @ Author: Chen Jun
# @ Author Email: 1170101471@qq.com
# @ Created Date: 2022-11-05, 15:51:46
# @ Modified By: Chen Jun
# @ Last Modified: 2025-11-02, 13:15:22
#############################################

"""
跨平台目录大小计算器
无需依赖系统du命令，精确模拟du -bs行为

用法:
    python get_dir_size.py [选项] <目录路径>...

选项:
    -h, --help      显示帮助信息
    -H, --human     以人类可读格式显示大小
    -f, --follow    跟随符号链接

示例:
    python get_dir_size.py /path/to/dir
    python get_dir_size.py -H /path/to/dir1 /path/to/dir2
"""

import os
import sys
import argparse
from typing import Set, Tuple


def calculate_size(
    path: str,
    follow_symlinks: bool = False,
    visited_inodes: Set[Tuple[int, int]] = None
) -> int:
    """
    精确模拟du -bs命令行为计算路径大小
    完全基于os.walk，确保与du -bs行为一致
    
    Args:
        path: 要计算大小的路径
        follow_symlinks: 是否跟随符号链接
        visited_inodes: 已访问的inode集合，用于硬链接检测
        
    Returns:
        int: 路径大小（字节）
    """
    if visited_inodes is None:
        visited_inodes = set()
    
    # 首先检查路径是否存在
    if not os.path.exists(path):
        return 0
    
    # 检查是否为符号链接
    if os.path.islink(path):
        if follow_symlinks:
            # 跟随符号链接
            try:
                real_path = os.path.realpath(path)
                return calculate_size(real_path, follow_symlinks, visited_inodes)
            except OSError:
                return 0
        else:
            # 不跟随符号链接，返回0
            return 0
    
    # 检查是否为文件
    if os.path.isfile(path):
        try:
            stat_info = os.stat(path)
            
            # 硬链接处理
            if stat_info.st_nlink > 1:
                inode_key = (stat_info.st_dev, stat_info.st_ino)
                if inode_key in visited_inodes:
                    return 0
                visited_inodes.add(inode_key)
            
            return stat_info.st_size
        except (OSError, PermissionError):
            return 0
    
    # 检查是否为目录
    if os.path.isdir(path):
        total_size = 0
        
        # 使用os.walk遍历目录，设置followlinks参数
        try:
            for root, dirs, files in os.walk(path, followlinks=follow_symlinks):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    # 跳过符号链接
                    if not follow_symlinks and os.path.islink(file_path):
                        continue
                    
                    try:
                        # 计算文件大小
                        stat_info = os.stat(file_path)
                        
                        # 硬链接处理
                        if stat_info.st_nlink > 1:
                            inode_key = (stat_info.st_dev, stat_info.st_ino)
                            if inode_key in visited_inodes:
                                continue
                            visited_inodes.add(inode_key)
                        
                        total_size += stat_info.st_size
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        
        return total_size
    
    return 0


def human_readable_size(size_bytes: int) -> str:
    """
    将字节大小转换为人类可读格式
    
    Args:
        size_bytes: 字节大小
        
    Returns:
        str: 人类可读的大小
    """
    if size_bytes == 0:
        return "0 B"
    
    size_units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(size_units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{size_bytes} {size_units[unit_index]}"
    else:
        return f"{size:.2f} {size_units[unit_index]}"


def get_du_equivalent(
    path: str,
    follow_symlinks: bool = False,
    visited_inodes: Set[Tuple[int, int]] = None
) -> int:
    """
    获取路径的du命令等效大小
    
    Args:
        path: 要计算大小的路径
        follow_symlinks: 是否跟随符号链接
        visited_inodes: 已访问的inode集合，用于硬链接检测
        
    Returns:
        int: 路径大小（字节）
    """
    if visited_inodes is None:
        visited_inodes = set()
    return calculate_size(
        path, 
        follow_symlinks=follow_symlinks,
        visited_inodes=visited_inodes
    )


def main():
    """
    主函数，解析命令行参数并执行目录大小计算
    """
    parser = argparse.ArgumentParser(description="跨平台目录大小计算器")
    parser.add_argument(
        "paths", 
        metavar="<路径>", 
        nargs="+",
        help="要计算大小的目录或文件路径"
    )
    parser.add_argument(
        "-H", 
        "--human", 
        action="store_true",
        help="以人类可读格式显示大小"
    )
    parser.add_argument(
        "-f", 
        "--follow", 
        action="store_true",
        help="跟随符号链接"
    )
    args = parser.parse_args()
    
    # 创建一个共享的inode集合，用于正确检测多个路径之间的硬链接关系
    shared_visited_inodes = set()
    
    # 存储所有路径的大小信息，用于排序和汇总
    results = []
    
    for path in args.paths:
        try:
            size = get_du_equivalent(
                path,
                follow_symlinks=args.follow,
                visited_inodes=shared_visited_inodes
            )
            results.append((size, path))
        except Exception as e:
            print(f"错误: {path}: {str(e)}", file=sys.stderr)
    
    # 按大小排序结果
    results.sort(key=lambda x: x[0])
    
    # 输出排序后的结果
    for size, path in results:
        if args.human:
            print(f"{human_readable_size(size)}	{path}")
        else:
            print(f"{size}	{path}")
    
    # 计算并输出总大小
    total_size = sum(size for size, _ in results)
    print("-----------")
    if args.human:
        print(human_readable_size(total_size))
    else:
        print(total_size)


if __name__ == '__main__':
    main()
