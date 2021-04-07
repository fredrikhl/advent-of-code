" Advent of Code 2016
" Day 2: Bathroom Security
"
" http://adventofcode.com/2016/day/2
"
" usage: vim -S keypad.vim -R input


let s:dec_moves = {
    \ 'U': ['1', '2', '3', '1', '2', '3', '4', '5', '6'],
    \ 'D': ['4', '5', '6', '7', '8', '9', '7', '8', '9'],
    \ 'L': ['1', '1', '2', '4', '4', '5', '7', '7', '8'],
    \ 'R': ['2', '3', '3', '5', '6', '6', '8', '9', '9'],
    \ }

let s:hex_moves = {
    \ 'U': ['1', '2', '1', '4', '5', '2', '3', '4', '9', '6', '7', '8', 'B'],
    \ 'D': ['3', '6', '7', '8', '5', 'A', 'B', 'C', '9', 'A', 'D', 'C', 'D'],
    \ 'L': ['1', '2', '2', '3', '5', '5', '6', '7', '8', 'A', 'A', 'B', 'D'],
    \ 'R': ['1', '3', '4', '4', '6', '7', '8', '9', '9', 'B', 'C', 'C', 'D'],
    \ }

let s:keypads = {'dec': s:dec_moves, 'hex': s:hex_moves}


function! s:keymove(moves, direction, position)
    return a:moves[a:direction][str2nr(a:position, 16) - 1]
endfunction


function! s:solve(moves, instructions)
    let code = ''
    let position = '5'

    for keypress in a:instructions
        for movement in split(keypress, '\zs')
            let position = s:keymove(a:moves, movement, position)
        endfor
        let code = code . position
    endfor
    return code
endfunction


" function! s:solvefile(keypad, filename)
"     let moves = s:keypads[a:keypad]
"     let instructions = readfile(fnameescape(a:filename))
"     echo s:solve(s:keypads[a:keypad], instructions)
" endfunction

" command! -complete=file -nargs=1 KeypadDecimal call s:solvefile('dec', '<args>')
" command! -complete=file -nargs=1 KeypadHexadecimal call s:solvefile('hex', '<args>')


function! s:solvebuf()
    let buffer = bufnr("")
    let lines = getline(1, '$')
    let solutons = [
        \ {'bufnr': buffer, 'module': 'keypad-dec', 'text': s:solve(s:keypads['dec'], lines)},
        \ {'bufnr': buffer, 'module': 'keypad-hex', 'text': s:solve(s:keypads['hex'], lines)},
        \ ]
    call setqflist(solutons)
    execute ':copen'
endfunction

command! KeypadSolve call s:solvebuf()
call s:solvebuf()
