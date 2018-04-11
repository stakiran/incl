# -*- coding: utf-8 -*-

import os
import threading
import sys

import libclipboard
import libdialog
import libexec
import libfile
import libisearch
import libkeyboard
from libkeyboard import KEYCODE
import libwindow
import versioninfo

CAPTION       = versioninfo.name
DESCRIPTION   = versioninfo.description

SYSCMD_DIR    = '@dir'
SYSCMD_EDIT   = '@edit'
SYSCMD_QUIT   = '@quit'

def on_text(new_stirng):
    pass

def on_enter(idx, value):
    if len(value)==0:
        return

    do_command(value)
    sys.exit(0)

def search_func(strlist, queries_by_str):
    """ lower and AND-searching. """
    queries = queries_by_str.split(' ')

    if len(queries)==0:
        return strlist

    firstq = queries[0]
    if len(firstq)==0:
        return strlist
    if firstq[0]==' ':
        return strlist

    ret = []
    for original_line in strlist:
        line = original_line.lower()

        is_matched = True
        for query in queries:
            if line.find(query)==-1:
                is_matched = False
                break
        if is_matched:
            ret.append(original_line)

    return ret

def execute(cmdline):
    # 普通に起動すると Tkinter GUI 側がブロッキングしてしまうため,
    # start コマンドを用いてノンブロッキングに実行する.
    commandline = 'start "" "%s"' % cmdline
    libexec.execute(commandline)

def copytext(s):
    # !(QUERIES-FOR-SERACH)!(COPYEE-TEXT)
    _, queries, copyee = s.split('!', 2)

    libclipboard.Clipboard.set(copyee)

def do_command(v):
    if v==SYSCMD_DIR:
        execute(SELF_DIR)
        return

    if v==SYSCMD_EDIT:
        execute(args.input)
        return

    if v==SYSCMD_QUIT:
        ope = libkeyboard.Operator()
        ope.keydown(KEYCODE.ALT)
        ope.press(KEYCODE.F4)
        ope.keyup(KEYCODE.ALT)
        return

    if len(v)>=2 and v[0]=='!':
        copytext(v)
        return

    commandline = v
    if v.find(',')!=-1:
        commandline = v.split(',')[0]

    execute(commandline)

def lines_mabiki(lines):
    return [l for l in lines if len(l)!=0 and l[0]!=';']

def center_pos(wx, wy):
    dx, dy = libwindow.get_dispsize()
    return (dx/2)-(wx/2), (dy/2)-(wy/2)

def abort(msg):
    raise RuntimeError('[Error!] {}'.format(msg))

def dialog_error(msg):
    title = '{} - Error!'.format(CAPTION)
    libdialog.ok(msg, title)

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=DESCRIPTION,
    )

    parser.add_argument('-i', '--input', default=None,
        help='A datafile path.')

    parser.add_argument('-x', '--windowx', default=640, type=int,
        help='Window X size.')
    parser.add_argument('-y', '--windowy', default=320, type=int,
        help='Window Y size.')

    parsed_args = parser.parse_args()
    return parsed_args

# [cx_freeze]
# エラーが起きるとダイアログでスタックトレースが表示されるが,
# これには以下問題がある.
# - 長文な上に専門的なので利用者が面食らう
# - ビルド環境の Python パスが見えてしまう
# これを隠蔽するため例外を吸収した上で, ダイアログで出すようにする.
try:
    args = parse_arguments()

    if args.input == None:
        abort('-i option required.')
    if not(libfile.is_file(args.input)):
        abort('The datafile "{}" is invalid'.format(args.input))
    lines = libfile.file2list(args.input)

    # [cx_freeze]
    # os.path.abspath(os.path.dirname(__file__)) がお手軽だが
    # __file__ は実行ファイルでは未定義になってしまうので使わない.
    SELF_FULLPATH = os.path.abspath(sys.argv[0])
    SELF_DIR      = os.path.dirname(SELF_FULLPATH)

    wx, wy = args.windowx, args.windowy
    px, py = center_pos(wx, wy)
    isrh = libisearch.ISearcher()
    isrh.set_caption(CAPTION) \
        .set_window_rect(px, py, wx, wy) \
        .set_on_text(on_text) \
        .set_on_enter(on_enter) \
        .set_search_func(search_func) \
        .set_lines(lines_mabiki(lines))
    isrh.go()
except Exception as e:
    dialog_error(e)
    sys.exit(1)
