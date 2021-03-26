python3  ../../compare3.py  A  B  C

mkdir -p select_color/
zcat compare3.py.gz >select_color/compare3.py
cd select_color/; python3 compare3.py ../A  ../B ../C ; cd -; pngtable2html.py <(ls select_color/*png|xargs -n 4|tr " " "\t") view.html; cd -
