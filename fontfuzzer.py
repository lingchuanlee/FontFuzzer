#-------------------------------------------------------------------------------
# Name	     : TrueType Font Fuzzer ver 0.1
# Purpose	 : Fuzz the ttf font file - attacking Windows Kernel
#
# Author	: Lee Ling Chuan (a.k.a lclee_vx) & Chan Lee Yee (a.k.a lychan25)
#
# Created:     22/05/2012
#
# Licence:
#Copyright (c) 2011, Lee Ling Chuan & Chan Lee Yee
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification,
#are permitted provided that the following conditions are met:

#Redistributions of source code must retain the above copyright notice, this list
#of conditions and the following disclaimer.
#Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation and/or
#other materials provided with the distribution.
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import sys
import os
import win32api
import win32gui
import struct
import time
from ctypes import *
from fontTools import ttLib
from win32con import *

FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1
FR_PRIVATE=0x10

class mainWindow():
    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst=windll.kernel32.GetModuleHandleW(None)

    def CreateWindow(self):
        reg=self.RegisterClass()
        hwnd=self.BuildWindow(reg)
        return hwnd

    def RegisterClass(self):
        #className="fuzzer"
        WndProc={
            WM_DESTROY: self.OnDestroy}
        wc=win32gui.WNDCLASS()
        wc.hInstance=self.hinst
        wc.hbrBackground=COLOR_BTNFACE+1
        wc.hCursor=win32gui.LoadCursor(0, IDC_ARROW)
        wc.hIcon=win32gui.LoadIcon(0, IDI_APPLICATION)
        wc.lpszClassName="font fuzzer"
        wc.lpfnWndProc=WndProc
        reg=win32gui.RegisterClass(wc)
        return reg
    def BuildWindow(self, reg):
        hwnd=windll.user32.CreateWindowExW(
            WS_EX_TOPMOST|WS_EX_NOACTIVATE,
            reg,
            "font fuzzer",
            WS_POPUP,
            0,
            600,
            1000,
            200,
            0,
            0,
            self.hinst,
            0)
        windll.user32.ShowWindow(hwnd, SW_SHOW)
        windll.user32.UpdateWindow(hwnd)
        return hwnd
    def OnDestroy(self, hwnd, message, wparam, lparam):
        win32gui.PostQuitMessage(0)
        return True

def shortName(font):
    name = ""
    family = ""

    for record in font['name'].names:
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            if '\000' in record.string:
                name = unicode(record.string, 'utf-16-be').encode('utf-8')
            else:
                name = record.string
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            if '\000' in record.string:
                family = unicode(record.string, 'utf-16-be').encode('utf-8')
            else:
                family = record.string
        if name and family:
            break
    return name, family

if __name__ == '__main__':
    if(len(sys.argv[1:])<1):
        print "Usage: ", sys.argv[0], "Target(Font File)"
        sys.exit()

    else:
        fileFont=sys.argv[1]
        try:
            tt=ttLib.TTFont(fileFont)

        except:
            print "Font File Corrupted"

        else:
            fontName=shortName(tt)[1]
            lf=win32gui.LOGFONT()
            htr=windll.gdi32.AddFontResourceExA(fileFont, FR_PRIVATE, None)
            w=mainWindow()
            hwnd=w.CreateWindow()
            hdc=windll.user32.GetDC(hwnd)
            for fontsize in range (0, 1000, 100):
                lf.lfHeight=fontsize
                lf.lfFaceName=fontName
                #lf.lfFaceName=fontPath
                lf.lfWidth=0
                lf.lfEscapement=0
                lf.lfOrientation=0
                lf.lfWeight=FW_NORMAL
                lf.lfItalic=False
                lf.lfUnderline=False
                lf.lfStrikeOut=False
                lf.lfCharSet=DEFAULT_CHARSET
                lf.lfOutPrecision=OUT_DEFAULT_PRECIS
                lf.lfClipPrecision=CLIP_DEFAULT_PRECIS
                lf.lfPitchAndFamily=DEFAULT_PITCH|FF_DONTCARE

                hFont=win32gui.CreateFontIndirect(lf)
                oldFt=win32gui.SelectObject(hdc, hFont)
                print lf.lfFaceName
                print lf.lfHeight

                z=[chr(58),chr(41),chr(58),chr(41),chr(58),chr(41)]

                array_types=c_wchar*6
                var1=array_types()

                for y in range(0, 6, 1):
                    var1[y]=z[y]

                    ETO_GLYPH_INDEX=16
                    windll.gdi32.ExtTextOutW(
                        hdc,
                        5,
                        5,
                        ETO_GLYPH_INDEX,
                        None,
                        var1,
                        len(var1),
                        None)

                    windll.gdi32.DeleteObject(win32gui.SelectObject(hdc, oldFt))
                    windll.gdi32.GdiFlush()
                    windll.gdi32.RemoveFontResourceExW(fileFont, FR_PRIVATE, None)
            time.sleep(1)
            windll.user32.ReleaseDC(hwnd, hdc)
            windll.user32.DestroyWindow(hwnd)
