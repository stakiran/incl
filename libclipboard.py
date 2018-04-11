# encoding: utf-8

import ctypes
import win32clipboard
import win32con
import win32api

class Clipboard:
    @staticmethod
    def get():
        """ @retval A string from the clipboard.
        @retval 空文字列 取得に失敗 or 何も入ってない
        @exception pywintypes.error: (1418, 'GetClipboardData', 'スレッドはクリップボードを開いていません。' """
        if not(Clipboard._open()):
            return ""

        if not(Clipboard._is_available()):
            return ""

        ret = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        Clipboard._close()

        return ret

    @staticmethod
    def set(s):
        """ @param A string you want to set the clipboard.
        @retval True 成功
        @retval False 失敗 """
        if not(isinstance(s, str)):
            return False

        if not(Clipboard._open()):
            return False
        win32clipboard.EmptyClipboard()

        ret = True
        try:
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, s)
        except:
            ret = False

        Clipboard._close()
        return ret

    @staticmethod
    def set_ansi(rawstring, mode=win32con.CF_TEXT):
        """ @todo 2017/12/11 17:55:09 まだ試してない。bytestring だから動かんかも？
        指定文字列を指定モードでクリップボードに格納する.
        ANSI(ascii or sjis)の場合はこちらを使う.
        @retval True 成功
        @retval False 失敗 """
        if not(isinstance(rawstring, bytes)):
            return False

        # グローバルヒープ領域を確保.
        # クリップボードにセットするAPIはグローバルヒープを介さないといけない.
        hMem = ctypes.windll.kernel32.GlobalAlloc(
            win32con.GMEM_MOVEABLE,
            len(rawstring)+1
        )
        if hMem==0:
            return False
        # 確保した領域をロック.
        pMemBlock = ctypes.windll.kernel32.GlobalLock(hMem)
        if pMemBlock==0:
            return False
        # 確保した領域にコピーするデータを書き込む.
        pBuffer = ctypes.windll.kernel32.lstrcpy(
            ctypes.c_char_p(pMemBlock),
            rawstring
        )
        if pBuffer==0:
            ctypes.windll.kernel32.GlobalUnlock(hMem)
            return False
        ctypes.windll.kernel32.GlobalUnlock(hMem)

        # クリップボードを開く.
        if not(Clipboard._open()):
            return False
        # クリップボードに残っているデータを消す.
        # これをしないと上手くコピーされないことがある.
        win32clipboard.EmptyClipboard()

        # 確保した領域に書き込んだ内容をクリップボードに書き込む.
        ret = True
        try:
            win32clipboard.SetClipboardData(mode, hMem)
        except:
            ret = False

        Clipboard._close()
        return ret

    @staticmethod
    def _open():
        """ クリップボードを開く and 既に開いているかどうかを返す.
        @retval True オープン成功
        @retval False オープン失敗(既に他アプリで開かれている) """
        try:
            win32clipboard.OpenClipboard()
        except win32api.error:
            return False
        return True

    @staticmethod
    def _close():
        # 開いてない時に実行するとしくじるので吸収.
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        return

    @staticmethod
    def _is_available():
        ret = win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT)
        if(ret!=0):
            return True
        Clipboard._close()
        return False

def precise_clipget():
    """ たまにしくじるのを時間差で吸収した版. """
    from time import sleep
    import pywintypes

    c = 0
    cb = ''
    while True:
        try:
            cb = Clipboard.get()
            return cb
        except pywintypes.error:
            pass
        c += 1
        if c>100:
            raise RuntimeError('Clipboard.get() is failing...')
        sleep(0.05)

