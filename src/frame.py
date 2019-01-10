# -*-coding:utf-8 -*-

import wx
import time
import random
from data import conf
from src.base import chkfile, whirefile, create_output_html, log_path
from src.mydialog import TestDialog, MsgDialog, TopicDialog
import os
import datetime


class MyFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="中文打字測驗", pos=wx.DefaultPosition, size=wx.Size(510, 300),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)



        # loc = wx.IconLocation(r'icon.ico', 0)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(r'icon.ico', wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)
        self.SetBackgroundColour((246, 222, 116))

        # self.Ba
        # --- Default
        # 沒有的話就新增
        self.data = chkfile('data.pkl')

        # self.topic = random.choice(conf.data.get('topic'))
        self.topic = self.data.get('topic')

        # print(self.startdate)

        self.menuUI()

        # --- 标题 小區塊

        self.Label_Name1 = wx.StaticText(
            self, wx.ID_ANY, "中文打字測驗", (170, 5), wx.Size(-1, -1), 0
        )

        self.Label_Name1.SetFont(wx.Font(14, 75, 90, wx.BOLD, False, "SimSun"))

        body_text = '練習時間: \n點擊下方【開始】視窗後，將開始計時進行5分鐘中文打字練習。 \n\n測驗時間: \n練習結束後，即進行兩次測驗，每次測驗時間2分鐘，\n取最高平均字數為測驗結果。 \n\n測驗說明: \n請注意若有漏字和多字，該行後續之所有字元將被視為錯字。'

        self.Label_Name2 = wx.StaticText(
            self, wx.ID_ANY, body_text, (30, 40), wx.Size(-1, -1), 0
        )

        self.Label_Name2.SetFont(wx.Font(12, 75, 90, 90, False, "SimSun"))
        # self.Label_Name2.Hide()

        #  wxFont( 14, wxFONTFAMILY_ROMAN, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD, false, wxT("PMingLiU") ) );

        # --- 功能 btn

        #  Exercise Test_btn
        #  Exercise Test_btn
        self.btn_Start = wx.Button(self, wx.ID_ANY, "開始", (200, 200), wx.Size(60, -1), 0)
        self.btn_Exercise = wx.Button(self, wx.ID_ANY, "練習", (77, 60), wx.Size(60, -1), 0)
        self.btn_Exercise.Hide()
        self.btn_Test = wx.Button(self, wx.ID_ANY, "測驗", (147, 60), wx.Size(60, -1), 0)
        self.btn_Test.Hide()

        # self.createTimer()
        self.bindEvent()
        self.bindMenuEvent()

    def menuUI(self):

        self.m_menubar = wx.MenuBar(0)
        # self.m_menubar.SetBackgroundColour((246, 222, 116))
        self.m_menubar.SetForegroundColour((246, 222, 116))
        self.m_menubar.SetBackgroundColour((246, 222, 116))

        # Menu1
        self.Menu1 = wx.Menu()


        # self.menuExercise_Msg = wx.MenuItem(self.Menu1, 11, "練習結束提醒")
        # self.Menu1.AppendItem(self.menuExercise_Msg)
        # self.menuTest_Msg = wx.MenuItem(self.Menu1, 12, "測驗結束提醒")
        # self.Menu1.AppendItem(self.menuTest_Msg)
        # self.m_menubar.Append(self.Menu1, "提醒")

        # Menu 2
        self.Menu2 = wx.Menu()
        self.menuExercise_Wav = wx.MenuItem(self.Menu2, 21, "練習結束音效")
        self.Menu2.AppendItem(self.menuExercise_Wav)
        self.menuTest_Wav = wx.MenuItem(self.Menu2, 22, "測驗結束內容")
        self.Menu2.AppendItem(self.menuTest_Wav)
        self.m_menubar.Append(self.Menu2, "音效")

        # Menu 3
        self.Menu3 = wx.Menu()
        self.menuOpen = wx.MenuItem(self.Menu3, 31, "打開")
        self.Menu3.AppendItem(self.menuOpen)
        self.m_menubar.Append(self.Menu3, "顯示")

        # Menu 4
        self.Menu4 = wx.Menu()
        self.menuTopic = wx.MenuItem(self.Menu4, 41, '修改題目')
        self.Menu4.AppendItem(self.menuTopic)
        self.m_menubar.Append(self.Menu4, '題目')

        self.SetMenuBar(self.m_menubar)

    def bindMenuEvent(self):

        # self.Bind(wx.EVT_MENU, self.OnExercise_Msg, id=11)
        # self.Bind(wx.EVT_MENU, self.OnTest_Msg, id=12)

        self.Bind(wx.EVT_MENU, self.OnExercise_Wav, id=21)
        self.Bind(wx.EVT_MENU, self.OnTest_Wav, id=22)

        self.Bind(wx.EVT_MENU, self.OnOpenSetting, id=31)

        self.Bind(wx.EVT_MENU, self.OnTopicSetting, id=41)

    def bindEvent(self):

        self.btn_Start.Bind(wx.EVT_BUTTON, self.OnStart)
        self.btn_Exercise.Bind(wx.EVT_BUTTON, self.OnExercise)
        self.btn_Test.Bind(wx.EVT_BUTTON, self.OnTest)

    def OnStart(self, event):
        '''
        開始
        :param event:
        :return:
        '''

        # 綁定姓名
        dlg = wx.TextEntryDialog(self, '輸入您的姓名', "輸入姓名")
        # dlg.SetValue()

        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
        dlg.Destroy()

        # --- 創建報告
        # self.startdate = time.strftime("%Y%m%d%H%M")

        date_now = datetime.datetime.now()

        date = '{Y}年{M}月{D}日 {h}時{m}分'.format(
            **{
                'Y': date_now.year,
                'M': date_now.month,
                'D': date_now.day,
                'h': date_now.hour,
                'm': date_now.minute
            }
        )

        self.filename = "%s %s" % (date, name)

        create_output_html(self.filename, self.topic)

        self.OnExercise(event)
        self.OnTest(event)

    def OnTopicSetting(self, event):
        '''
        修改 題目
        :param event:
        :return:
        '''
        dig = wx.PasswordEntryDialog(self, '')
        dig.Title = "輸入密碼"

        if dig.ShowModal() == wx.ID_OK:
            if dig.Value == conf.PASSWORD:
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
            if dig.Value == conf.PASSWORD:
                os.system("explorer %s" % log_path(conf.LOG_DIR))
        dig.Destroy()

    def OnExercise_Wav(self, event):
        '''
        設置聲音檔案路徑
        :param event:
        :return:
        '''

        dlg = wx.FileDialog(self, "聲音檔案路徑", defaultFile=self.data.get('wav_path').get('exercise'),
                            wildcard="Wav files (*.wav)|*.wav")

        if dlg.ShowModal() == wx.ID_OK:
            self.data['wav_path']['exercise'] = dlg.Path
            whirefile("data.pkl", self.data)

        dlg.Destroy()

    def OnTest_Wav(self, event):
        '''
        設置聲音檔案路徑
        :param event:
        :return:
        '''

        dlg = wx.FileDialog(self, "聲音檔案路徑", defaultFile=self.data.get('wav_path').get('test'),
                            wildcard="Wav files (*.wav)|*.wav")

        if dlg.ShowModal() == wx.ID_OK:
            self.data['wav_path']['test'] = dlg.Path
            whirefile("data.pkl", self.data)



        dlg.Destroy()

    def OnExercise_Msg(self, event):
        '''
        設定鬧鈴提醒內容
        :param event:
        :return:
        '''
        dlg = wx.TextEntryDialog(self, '設定鬧鈴提醒內容', "設定")
        dlg.SetValue(self.data.get('msg').get('exercise'))

        if dlg.ShowModal() == wx.ID_OK:
            self.data['msg']['exercise'] = dlg.GetValue()
            whirefile("data.pkl", self.data)

        dlg.Destroy()

    def OnTest_Msg(self, event):
        '''
        設定鬧鈴提醒內容
        :param event:
        :return:
        '''
        dlg = wx.TextEntryDialog(self, '設定鬧鈴提醒內容', "設定")
        dlg.SetValue(self.data.get('msg').get('test'))

        if dlg.ShowModal() == wx.ID_OK:
            self.data['msg']['test'] = dlg.GetValue()
            whirefile("data.pkl", self.data)

        dlg.Destroy()

    def OnExercise(self, event):
        print("Exercise 测验5分钟")

        dialog = TestDialog(self, min='5', report=False)

        dialog.filename = self.filename

        # dialog.ShowModal()
        if dialog.ShowModal() == wx.ID_OK:
            dialog.Destroy()

    def OnTest(self, event):
        print("Exercise 测验2分钟")

        # dialog = TestDialog(self, wav_path=self.data.get('wav_path'), msg=self.data.get('msg'), min='2')

        loop_num = 2

        finish_num = list(range(loop_num)).pop() + 1

        for i in range(loop_num):

            if i+1 == finish_num:
                # 最後一次
                dig = TestDialog(self, min='2', finish=True)
            else:
                dig = TestDialog(self, min='2')

            dig.filename = self.filename

            if dig.ShowModal() == wx.ID_OK:
                dig.Destroy()

    def createTimer(self):
        pass
