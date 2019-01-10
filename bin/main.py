# -*-coding:utf-8 -*-

import wx
from src.frame import MyFrame1
from src import base


if __name__ == '__main__':
    base.chk_wavs()
    base.chk_icons()

    app = wx.App()
    frame = MyFrame1().Show()
    app.MainLoop()
