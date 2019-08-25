# 保留最后两次扫盘结果，sed '$d'实现不打印末尾行
ls */scan/01.scan_results/01.scan_shell_out/|grep :|tr -d :|sed '$d'|sed '$d'
