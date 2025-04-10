---
title: Verilog Vim 配置
toc: true
comments: true
date: 2025-04-10 10:02:23
updated: 2025-04-10 11:44:50
categories: Vim
tags: [Vim， Verilog]
description: 数字IC设计开发Vim配置
---

# 格式化 Verilog 的信号声明

```vim
command! -range -nargs=0 Vdfmt call FormatVerilogSignalDeclaration()

function! FormatVerilogSignalDeclaration()
    " 获取 visual 选区
    let start_pos = getpos("'<")
    let end_pos = getpos("'>")

    " 获取选中的所有行
    let lines = getline(start_pos[1], end_pos[1])

    " 步骤1：将每一行行首的第一个 wire 或 reg 前面的空格替换为 3 个空格
    for i in range(len(lines))
        let line = lines[i]
        let new_line = substitute(line, '^\s*\(wire\|reg\)', '   \1', '')
        let lines[i] = new_line
    endfor

    " 步骤2：将每一行行首的第一个 input 或 output 或 inout 前面的空格替换为 3 个空格
    for i in range(len(lines))
        let line = lines[i]
        let new_line = substitute(line, '^\s*\(input\|output\|inout\)', '   \1', '')
        let lines[i] = new_line
    endfor

    " 步骤3：对齐 'wire' 或 'reg'
    for i in range(len(lines))
        let line = lines[i]
        let new_line1 = substitute(line, 'input\s\+wire', 'input  wire', '')
        let new_line2 = substitute(new_line1, 'output\s\+wire', 'output wire', '')
        let new_line3 = substitute(new_line2, 'output\s\+reg', 'output reg', '')
        let lines[i] = new_line3
    endfor

    " 步骤4：对齐 '['
    for i in range(len(lines))
        let line = lines[i]
        let new_line1 = substitute(line, 'wire\s\+\[', 'wire [', '')
        let new_line2 = substitute(new_line1, 'reg\s\+\[', 'reg  [', '')
        let lines[i] = new_line2
    endfor

    " 步骤5：删除 '[' 与 ']' 之间的空格
    for i in range(len(lines))
        let line = lines[i]
        let line = substitute(line, '\[\(\%(\]\@!.\)*\)\]', 
                    \ '\=printf("[%s]", substitute(submatch(1), " ", "", "g"))', 'g')
        let lines[i] = line
    endfor

    " 更新选区中的行
    call setline(start_pos[1], lines)

    " 步骤6：使用 :Tabularize 按照 wire 或 reg 之后的第一个单词对齐
    execute "normal! gv"
    execute ":'<,'>Tabularize /\\(wire\\|reg\\)\\s*\\(\\[.*\\]\\)\\?\\s*\\zs\\w\\+/"

    " 步骤7：使用 :Tabularize 对齐 ';' 或 ','
    execute "normal! gv"
    execute ":'<,'>Tabularize /\\(;\\|,\\)/"

endfunction
```

在 visual 模式下，选中需要格式化的信号声明，然后执行 `:Vdfmt` 命令即可。

