" Advent of Code 2016
" Day 2: Bathroom Security
"
" http://adventofcode.com/2016/day/2
"
" Part 2

" next = keypad[direction][current - 1]
" current   '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D'
let s:keypad = {
    \ 'U': ['1', '2', '1', '4', '5', '2', '3', '4', '9', '6', '7', '8', 'B'],
    \ 'D': ['3', '6', '7', '8', '5', 'A', 'B', 'C', '9', 'A', 'D', 'C', 'D'],
    \ 'L': ['1', '2', '2', '3', '5', '5', '6', '7', '8', 'A', 'A', 'B', 'D'],
    \ 'R': ['1', '3', '4', '4', '6', '7', '8', '9', '9', 'B', 'C', 'C', 'D'],
    \ }


function! s:keymove(direction, position)
    return s:keypad[a:direction][str2nr(a:position, 16) - 1]
endfunction


function! s:keycode(filename)
    let instructions = readfile(fnameescape(a:filename))
    let code = ''
    let position = '5'

    for keypress in instructions
        for movement in split(keypress, '\zs')
            let position = s:keymove(movement, position)
        endfor
        let code = code . position
    endfor
    echo code
endfunction

command! -complete=file -nargs=1 Keypad call s:keycode('<args>')
