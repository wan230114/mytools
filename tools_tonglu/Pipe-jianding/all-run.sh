# @Author: ChenJun
# @Date:   2019-02-28 19:08:52
# @Last Modified by:   JUN
# @Last Modified time: 2019-02-28 19:10:27

# 简介：将01.list.txt,list,gene,getPipe.sh 四个文件(夹)放置于脚本当前目录
# nohup本脚本run.sh即可完成一键构树与出图

##############==> 记得修改 <==#################
prjname="test"
##############==> 记得修改 <==#################

#1) 创建运行目录 
path=`pwd`
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/Pipe-jianding/Pipe-v2.py  input.list  gene

#2) 运行
cd run-workdir
sh runAllstart.sh
cat wuzhong.list |xargs -i /ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/02.change_pep.py {}
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tonglu/xiufu/xiufu.py . wuzhong.list
cd $path

#3) 进入可视化目录进行可视化输出
mkdir ALL_view
cd ALL_view/
ln -s $path/run-workdir $path/ALL_view/$prjname
ln -s $path/list $path/ALL_view/list
ln -s $path/gene $path/ALL_view/gene
echo "grep \> <(cat gene/*)|sed 's#^>##'"|bash >gene.list
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getAllsvg-itol.py $prjname gene.list
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgcut.py out_svg/ -f png
sort -k1 -k2 -k3 -k6 -k7n result.txt -o result.txt
sort -k1 -k2 -k3 -k6 -k7n result_all.txt -o result_all.txt

#4) 给基因标注染色体
python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/getChr2svg.py $prjname


#5) 获取各种html查看
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/py-gethtml2table-png.py
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/py-gethtml2table-svg.py

/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/py-gethtml2table-svg-chr.py
/ifs/TJPROJ3/Plant/chenjun/software/python3.5/bin/python3 /ifs/TJPROJ3/Plant/chenjun/mytools/tools_tree/imgdirView.py out_svg chr.svg

tar -czvf out_svg.tar.gz *.html *.html.xls result.txt result_all.txt out_svg/ -h
