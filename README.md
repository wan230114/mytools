# mytools

## 1. 简介

- 方便不同平台代码转移
- 环境变量同步
- 环境中同步常用工具

## 2. 使用方法
```bash
# step01: git clone
cd your_path/
git clone https://gitee.com/wan230114/mytools.git

# step02: 初始化配置
cd mytools/       # 进入clone目录
. init_bashrc.sh  # 加载保存环境变量
# 或调用bash：`bash init_bashrc.sh`
# 或调用sh：`sh init_bashrc.sh`
```

注：

(1) 若运行初始化失败，可手动在编辑 `~/.bashrc`中追加：
```bash
# >>> bashrc >>>
source /home/chenjun/mytools/bashrc_my.sh
mymail="1170101471@qq.com"  # 设置自己的邮箱，用于pysend和qjk等需要邮箱的命令
source /home/chenjun/mytools/bashrc_Tools.sh
```

(2) 随后将bashrc文件夹文件复制到用户主目录下：
```bash
cp -ir $(ls ./bashrc/.* -d | sed 1,2d) ~/
```

一些特殊工具，需要的环境创建: [./env_create.md](./env_create.md)

## 3. 功能简介
### 3.1 适用系统
centos、ubuntu、macOS

### 3.2 命令常用工具：

| 命令    | 功能简介                                            |
|---------|-----------------------------------------------------|
| **文件及路径状态获取**| |
| `r`       | 返回多个指定文件当前文件夹的绝对真实路径                |
| `f`       | 返回多个指定文件当前文件夹的绝对路径                |
| `asum`    | 求某一列的所有数字之和(封装awk, 性能不错)           |
| `getsize` | 从stdin或指定文件读入将某列数值转换为计算机存储单位 |
| **文本处理** | |
| `mdc`     | 对markdown文档的标题进行升级或者降级操作            |
| `cah`     | 打印格式化后的sh文件                                |
| `cag`     | 打印gbk编码的文件                                   |
| `ca`      | 打印带色彩的普通文本                                |
| `rep`     | 批量替换文件指定列的关键词                          |
| **进程管理** | |
| `ks`      | 批量杀一组父子进程                                  |
| `p`    | ps xjf           | 显示父子进程的进程树               |
| **网页应用** | |
| `view`    | 查找指定目录下所有图片(png/svg/pdf)，生成网页版报告 |
| **网络应用** | |
| `pysend`  | 快捷发送邮件                                        |
| `pywget`  | python版wget，可以代理转发                          |
| `IP`      | 返回当前计算机所在环境的公网IPv4                    |
| ...     | ...                                                 |


---
### 3.3. 系统命令的改造
| 命令 | 原始命令         | 功能                               |
|------|------------------|------------------------------------|
| `h`    | history \        | less -S|显示命令历史记录           |
| `l`    | ls -lh           | 存储换算，列表显示                 |
| `ll`   | ls -lhrt         | 存储换算，列表显示，按时间逆序排序 |
| `lll`  | ls -l            | 仅列表显示(存储显示字节数)         |
| `e`    | less -S          | 不换行查看文件                     |
| `ee`   | less -SN         | 不换行查看文件并显示行号           |
| `eee`  | less             | 默认参数查看文件                   |
| `vb`   | vim ~/.bashrc    | 快速编辑环境变量                   |
| `vbs`  | source ~/.bashrc | 快速重新导入环境变量               |
| `cr`   | crontab -e       | 快速打开开机设置                   |
| `vb1`  | vim ${tools_path}/bashrc_my.sh     | 编辑常用快捷键列表 |
| `vb2`  | vim ${tools_path}/bashrc_Tools.sh  | 编辑常用的高级命令列表 | 
| `vbb`  | vim ${tools_path}/Note.sh          | 一些杂烩笔记汇总 |
| ...  | ...              | ...                                |


---
### 3.4 SGE集群快捷键及功能命令：
| 命令 | 功能                                                 |
|------|------------------------------------------------------|
| `dfa`  | 快速查看指定磁盘空间                                 |
| `qs`   | 快速查看投递job任务                                  |
| `q`    | 查看个人在集群投递的任务                             |
| `vs`   | 快速查看集群使用统计情况                             |
| `pp`   | 查看占用资源最多的进程                               |
| `qd`   | 指定关键词批量杀任务                                 |
| `qgjd` | 指定关键词批量改节点:"小/大/所有"节点                |
| `qjg`  | 解挂                                                 |
| `qjk`  | 任务监控                                             |
| `pjk`  | 进程监控                                             |
| `oss`  | oss集群互传工具                                      |
| `md5`  | 本地计算当前目录md5和checksize                       |
| `md5q` | 自动投递集群计算当前目录md5和checksize, 用法: `md5q` |
| `sjms` | sjm流程提取工具                                      |
| ...  | ...                                                  |

### 3.5 其他

shell主题配置、shell命令历史记录格式化、vim定义F5粘贴模式及主题、screen主题配置...

---

如有任何问题，敬请联系：

-- ChenJun 1170101471@qq.com
