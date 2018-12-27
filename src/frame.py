# -*-coding:utf-8 -*-

import wx
import time
import random
from data import conf
from src.base import chkfile, whirefile, create_output_html, log_path
from src.mydialog import TestDialog, MsgDialog,TopicDialog
import os


class MyFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="測試打字", pos=wx.DefaultPosition, size=wx.Size(300, 200),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour('White')

        # --- Default
        # 沒有的話就新增
        self.data = chkfile('data.pkl')
        self.startdate = time.strftime("%Y%m%d%H%M")

        # self.topic = random.choice(conf.data.get('topic'))
        self.topic = self.data.get('topic')

        # --- 創建報告
        create_output_html(self.startdate, self.topic)

        # print(self.startdate)

        self.menuUI()

        # --- 标题 小區塊

        self.Label_Name1 = wx.StaticText(
            self, wx.ID_ANY, "測試打字小程序", (45, 5), wx.Size(-1, -1), 0
        )
        self.Label_Name1.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        # --- 功能 btn

        #  Exercise Test_btn
        #  Exercise Test_btn
        self.btn_Start = wx.Button(self, wx.ID_ANY, "開始", (100, 60), wx.Size(60, -1), 0)
        self.btn_Exercise = wx.Button(self, wx.ID_ANY, "練習", (77, 60), wx.Size(60, -1), 0)
        self.btn_Exercise.Hide()
        self.btn_Test = wx.Button(self, wx.ID_ANY, "測驗", (147, 60), wx.Size(60, -1), 0)
        self.btn_Test.Hide()

        # self.createTimer()
        self.bindEvent()
        self.bindMenuEvent()

    def menuUI(self):

        self.m_menubar = wx.MenuBar(0)

        # Menu1
        self.Menu1 = wx.Menu()
        self.menuSetting = wx.MenuItem(self.Menu1, 11, "鬧鈴聲音")
        self.Menu1.AppendItem(self.menuSetting)
        self.menuItem1 = wx.MenuItem(self.Menu1, 12, "提醒內容")
        self.Menu1.AppendItem(self.menuItem1)
        self.m_menubar.Append(self.Menu1, "設定")

        # Menu2
        self.Menu2 = wx.Menu()
        self.menuOpen = wx.MenuItem(self.Menu2, 21, "打開")
        self.Menu2.AppendItem(self.menuOpen)
        self.m_menubar.Append(self.Menu2, "顯示")

        # Menu 3
        self.Menu3 = wx.Menu()
        self.menuTopic = wx.MenuItem(self.Menu3, 31, '修改題目')
        self.Menu3.AppendItem(self.menuTopic)
        self.m_menubar.Append(self.Menu3, '題目')

        self.SetMenuBar(self.m_menubar)

    def bindMenuEvent(self):
        self.Bind(wx.EVT_MENU, self.OnBeepSetting, id=11)
        self.Bind(wx.EVT_MENU, self.OnMsgSetting, id=12)

        self.Bind(wx.EVT_MENU, self.OnOpenSetting, id=21)

        self.Bind(wx.EVT_MENU, self.OnTopicSetting, id=31)

    def bindEvent(self):
        self.btn_Start.Bind(wx.EVT_BUTTON, self.OnStart)
        self.btn_Exercise.Bind(wx.EVT_BUTTON, self.OnExercise)
        self.btn_Test.Bind(wx.EVT_BUTTON, self.OnTest)

    def OnStart(self, event):
        self.OnExercise(event)
        self.OnTest(event)

    def OnTopicSetting(self,event):
        '''
        修改 題目
        :param event:
        :return:
        '''
        dig = wx.PasswordEntryDialog(self, '')
        dig.Title = "輸入密碼"

        if dig.ShowModal() == wx.ID_OK:
            if dig.Value == '123456':
                dig = TopicDialog(self)
                if dig.ShowModal() == wx.ID_EDIT:
                    self.data['topic'] = dig.m_TextCtrl1.GetValue()
                    whirefile("data.pkl", self.data)

        dig.Destroy()


    def OnOpenSetting(self, event):
        '''
        打開 紀錄資料夾
        :param event:
        :return:
        '''

        print('OnOpenSetting')
        dig = wx.PasswordEntryDialog(self, '')
        dig.Title = "輸入密碼"

        if dig.ShowModal() == wx.ID_OK:
            if dig.Value == '123456':
                os.system("explorer %s" % log_path(conf.LOG_DIR))
        dig.Destroy()

    def OnBeepSetting(self, event):
        '''
        設置聲音檔案路徑
        :param event:
        :return:
        '''

        dlg = wx.FileDialog(self, "聲音檔案路徑", defaultFile=self.data.get('wav_path'), wildcard="Wav files (*.wav)|*.wav")

        if dlg.ShowModal() == wx.ID_OK:
            self.data['wav_path'] = dlg.Path
            whirefile("data.pkl", self.data)

        dlg.Destroy()

    def OnMsgSetting(self, event):
        '''
        設定鬧鈴提醒內容
        :param event:
        :return:
        '''
        dlg = wx.TextEntryDialog(self, '設定鬧鈴提醒內容', "設定")
        dlg.SetValue(self.data['msg'])

        if dlg.ShowModal() == wx.ID_OK:
            self.data['msg'] = dlg.GetValue()
            whirefile("data.pkl", self.data)

        dlg.Destroy()

    def OnExercise(self, event):
        print("Exercise 测验10分钟")

        dialog = TestDialog(self,min='10',report=False)

        dialog.startdate = self.startdate

        # dialog.ShowModal()
        if dialog.ShowModal() == wx.ID_OK:
            dialog.Destroy()

    def OnTest(self, event):
        print("Exercise 测验2分钟")

        # dialog = TestDialog(self, wav_path=self.data.get('wav_path'), msg=self.data.get('msg'), min='2')

        for i in range(3):
            dig = TestDialog(self, min='2')
            dig.startdate = self.startdate

            if dig.ShowModal() == wx.ID_OK:
                dig.Destroy()

    def createTimer(self):
        pass
