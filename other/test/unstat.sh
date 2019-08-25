bash <(echo -e "hezuo\nshangye"|xargs -i echo -e "echo \\>== {} \\<==; grep -vf <(cat {}/*|awk '{print \$1\",\"\$4}'|sort|uniq) {}.txt")
