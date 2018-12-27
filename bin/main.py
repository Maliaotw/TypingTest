# -*-coding:utf-8 -*-

import wx
from src.frame import MyFrame1
from src import base

base.chk_wavs()


if __name__ == '__main__':

    app = wx.App()
    frame = MyFrame1().Show()
    app.MainLoop()
