# 
cat /home/oms/20* /TJPROJ1/lims/XJ/20*|sed '/^$/d' >xiajiALL.list
# 过滤第24列为1908, 1919, 1920
#awk -F"\t" 'NR==FNR{a[$1]=$0}NR>FNR{if($24 in a) print $0}' groups xiajiWENKU.list >xiajiWENKU.list.filter
