"set nu
syntax on
set shiftwidth=4
set softtabstop=4
set tabstop=4
"set expandtab
set noexpandtab
"set fdm=indent
set autoindent
set fileencodings=ucs-bom,utf-8,utf-16,gbk,big5,gb18030,gb2312,latin1
set encoding=utf-8
set cul

"用F5来切换粘贴模式，可以解决是否自动缩进
set pastetoggle=<F5>   


"set foldlevelstart=99

autocmd BufNewFile *.py,*.pl,*.c,*.cpp,*.r exec ":call SetTitle()"

func SetTitle()
call append(0, "\#################################################")
call append(1,"\#  File Name:".expand("%"))
call append(2,"\#  Author: chenjun")
call append(3,"\#  Mail: chenjun4663@novogene.com")
call append(4,"\#  Created Time: ".strftime("%c"))
call append(5,"\#################################################")
call append(6,"")
autocmd BufNewFile * normal G
endfunc

filetype plugin on
let g:pydiction_location = '~/.vim/tools/pydiction/complete-dict'
autocmd FileType python set omnifunc=pythoncomplete#Complete
