《基因鉴定流程说明书》


简介：用于鉴定给定基因在目标物种中的基因，并输出鉴定的基因结果


输入：待鉴定的基因pep，目标物种的fa,gff,cds,pep
输出：挑选的基因信息结果及可视化构树结果 (具体:./ALL_view/out_svg.tar.gz)


亮点：
    交互：创建Pipe时检查输入的所有参数，以交互模式确认；
    批量：批量同时鉴定多个物种的某一类基因；
    标注颜色：对挑选结果直接于集群构树，并标注参考基因为红色，目标基因为绿色；
    汇总信息：给出挑选出的基因和总的构树的基因详细信息；
    网页可视化：最后所有构树图片直接生成png和svg网页版查看；
    标注染色体：进化树中给基因标注出染色体，汇总网页版；
    可直接搜索：SVG网页版中可以直接搜索某个基因在网页中迅速定位(非图片)；


使用方法：
1) 准备：
    1. 运行准备: <创建文件input.list, 和文件夹gene> 或 <只需要复制getPipe.sh于项目运行目录>
       (可以只需要复制 shell_getPipe.sh ，运行过程中会复制模式文件input.list到当前文件夹，并创建gene文件夹，此时再手动去配置修改输入文件)
    2. 文件说明:
       input.list    需要鉴定的基因的物种的：物种名,fasta,gff,cds,pep
       gene          需要鉴定的参考基因，如某个家族的基因

2) 运行方法：
    直接 sh getPipe.sh 运行按照提示一步一步执行即可

3) 注意事项：
    如何手动调参？
    1. 若要细致调参可以在 “sh getPipe.sh” 的最后一步不投递。
    2. 然后进入run-workdir, 批量调参, 如：
       cat wuzhong.list |xargs -i echo "sed -i 's#-overlap 0.2#-overlap 0.5#g' {}/run.sh; sed -i 's#-Soverlap 0.2#-Soverlap 0.5#g' {}/run.sh "
       即可输出替换的命令，
       若确认无误，末尾直接加上sh即可执行。
       cat wuzhong.list |xargs -i echo "sed -i 's#-overlap 0.2#-overlap 0.5#g' {}/run.sh; sed -i 's#-Soverlap 0.2#-Soverlap 0.5#g' {}/run.sh "|sh

    3. 最后回到项目运行主目录手动投递：
       nohup sh all-run.sh &
       或 加入运行完邮箱提醒的投递：
       nohup sh all-run.sh && python /ifs/TJPROJ3/Plant/chenjun/mytools/sendmail.py 1234567890@qq.com -c "构树完成啦" &

