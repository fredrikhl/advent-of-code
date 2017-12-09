" Advent of Code 2016
" Day 2: Bathroom Security
"
" http://adventofcode.com/2016/day/2
"
" Part 1

" next = keypad[direction][current - 1]
" current   '1', '2', '3', '4', '5', '6', '7', '8', '9'
let s:keypad = {
    \ 'U': ['1', '2', '3', '1', '2', '3', '4', '5', '6'],
    \ 'D': ['4', '5', '6', '7', '8', '9', '7', '8', '9'],
    \ 'L': ['1', '1', '2', '4', '4', '5', '7', '7', '8'],
    \ 'R': ['2', '3', '3', '5', '6', '6', '8', '9', '9'],
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

command! -nargs=1 Keypad call s:keycode('<args>')
