# -*-coding:utf-8 -*-

import wx
from wx.adv import Sound
import datetime
from src.base import chkfile, whire_output_html

from wx.stc import StyledTextCtrl


class TestDialog(wx.Dialog):
    '''
    測驗功能 Dialog
    '''

    def __init__(self, parent, min, report=True, finish=False):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title="", size=(600, 550), style=wx.CAPTION)

        self.data = chkfile('data.pkl')
        self.topic = self.data.get('topic')

        self.finish = finish
        # self.sound = Sound(self.data.get('wav_path'))
        # self.msg = self.data.get('msg')
        self.Title = '測驗%s分鐘' % (str(int(min)))
        self.min = min
        self.report = report

        self.initUI()
        self.bind_evt()
        self.createTimer()

    def initUI(self):
        wx.StaticText(self, label="剩餘時間", pos=(60, 10), size=(-1, -1)).SetFont(
            wx.Font(16, 75, 90, 90, False, "MingLiU"))

        self.Label_CD = wx.StaticText(self, label="{}:00".format(self.min), pos=(160, 10), size=(-1, -1))
        self.Label_CD.SetFont(wx.Font(16, 75, 90, 90, False, "MingLiU"))

        self.Label_Max = wx.StaticText(self, label="字數：", pos=(280, 5), size=(-1, -1))
        self.Label_Max.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_MaxString = wx.StaticText(self, label='', pos=(330, 5), size=(-1, -1))
        self.Label_MaxString.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_OK = wx.StaticText(self, label="正確：", pos=(380, 5), size=(-1, -1))
        self.Label_OK.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_OkString = wx.StaticText(self, label="", pos=(430, 5), size=(-1, -1))
        self.Label_OkString.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_Miss = wx.StaticText(self, label="錯誤：", pos=(280, 25), size=(-1, -1))
        self.Label_Miss.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_MissString = wx.StaticText(self, label="", pos=(330, 25), size=(-1, -1))
        self.Label_MissString.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_Avg = wx.StaticText(self, label="平均：", pos=(380, 25), size=(-1, -1))
        self.Label_Avg.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.Label_AvgString = wx.StaticText(self, label="", pos=(430, 25), size=(-1, -1))
        self.Label_AvgString.SetFont(wx.Font(12, 75, 90, 90, False, "MingLiU"))

        self.m_staticText1 = wx.TextCtrl(self, wx.ID_ANY, value=self.topic,
                                         pos=(20, 50), size=(550, 200), style=0 | wx.TE_MULTILINE)
        self.m_staticText1.SetFont(wx.Font(16, 75, 90, 90, False, "MingLiU"))
        self.m_staticText1.SetBackgroundColour("White")
        self.m_staticText1.Enable(False)

        self.m_staticText2 = wx.TextCtrl(self, wx.ID_ANY, value="",
                                         pos=(20, 270), size=(550, 200), style=0 | wx.TE_MULTILINE)
        self.m_staticText2.SetFont(wx.Font(16, 75, 90, 90, False, "MingLiU"))

        # self.m_staticText2.SetMaxLength(self.m_staticText1.LastPosition) # 取消控制字數

        self.CDtime = self.Label_CD.GetLabel()
        self.min, s = self.CDtime.split(":")
        self.CDendtime = datetime.datetime.now() + datetime.timedelta(hours=int(0), minutes=int(self.min),
                                                                      seconds=int(s))

    def bind_evt(self):
        self.m_staticText2.Bind(wx.EVT_TEXT, self.text_evt)
        self.m_staticText2.Bind(wx.EVT_LEFT_DOWN, self.text_evt)
        self.m_staticText2.Bind(wx.EVT_KEY_DOWN, self.text_evt)

    def text_evt(self, event):
        # print("Text_evt")
        # print('1 當前行數', self.m_staticText1.GetScrollRange(0))  # 當前行數
        # print('2 當前行數', self.m_staticText2.GetScrollRange(0))  # 當前行數
        # print('1 當前卷軸數', self.m_staticText1.GetScrollPos(0))  # 卷軸數
        # print('2 當前卷軸數', self.m_staticText2.GetScrollPos(0))  # 卷軸數

        if self.m_staticText2.GetScrollPos(0) == self.m_staticText1.GetScrollPos(0):
            pass
        elif self.m_staticText2.GetScrollPos(0) > self.m_staticText1.GetScrollPos(0):

            self.loop = self.m_staticText2.GetScrollPos(0) - self.m_staticText1.GetScrollPos(0)
            for i in range(self.loop):
                self.m_staticText1.ScrollLines(1)
        elif self.m_staticText1.GetScrollPos(0) > self.m_staticText2.GetScrollPos(0):
            self.loop = self.m_staticText1.GetScrollPos(0) - self.m_staticText2.GetScrollPos(0)
            for i in range(self.loop):
                self.m_staticText1.ScrollLines(-1)
        else:
            # 滾回最上頁
            self.m_staticText1.ScrollLines(-self.m_staticText1.GetScrollRange(0))
            self.line = 0

        event.Skip()

    def OnStop(self, event):
        '''
        時間到

        :param event:
        :return:
        '''
        print("OnStop")
        self.timeCD.Stop()
        self.Label_CD.SetLabel('00：00')

        # 驗證測試結果
        data = self.marktopic()

        self.Label_MaxString.SetLabel(data.get('max'))
        self.Label_OkString.SetLabel(data.get('ok'))
        self.Label_MissString.SetLabel(data.get('miss'))
        self.Label_AvgString.SetLabel(data.get('avg'))

        if self.report:
            whire_output_html(self.filename, data)
            sound = Sound(self.data['wav_path']['test'])
            msg_data = self.data['msg']['test']
        else:
            sound = Sound(self.data['wav_path']['exercise'])
            msg_data = self.data['msg']['exercise']

        sound.Play()

        # 結束彈窗

        if self.finish:
            msg_data = {
                'title': '測驗結束',
                'msg': '測驗結束'
            }

            dig = MsgDialog(self, msg_data,center=True)
        else:
            dig = MsgDialog(self, msg_data)

        dig.ShowModal()
        dig.Destroy()
        self.EndModal(wx.ID_OK)

    def marktopic(self):
        '''
        驗證測驗結果
        :return:
        '''

        topic_line = self.cut(self.topic)
        user_val = self.m_staticText2.GetValue()
        user_line = user_val.replace("\n", "")

        # user_line = self.cut(self.m_staticText2.GetValue().strip())

        ok = 0
        miss = 0
        fix = []
        for x, y in zip(user_line, topic_line):
            if x == y:
                ok += 1
                fix.append(x)
            else:
                miss += 1
                fix.append('<span style="color:red">%s</span>' % x)

        data = {
            'topic': self.topic,
            'max': str(ok + miss),
            'ok': str(ok),
            'miss': str(miss),
            'avg': str((ok + miss) / int(self.min)),
            'fix_view': "".join(fix),
            'min': str(self.min)
        }

        return data

    def cut(self, string):
        newlist = []
        for numer in range(len(string)):
            newlist.append(string[numer])
        return newlist

    def createTimer(self):

        # timeCD 倒計時功能
        self.timeCD = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._OnCD, self.timeCD)
        self.timeCD.Start(1000)

    def _OnCD(self, event):

        '''
        CountDown
        :param event:
        :return:
        '''

        diff = self.CDendtime - datetime.datetime.now()

        if diff.total_seconds() <= 0:
            self.Label_CD.SetLabel(self.CDtime)
            min, s = self.CDtime.split(":")
            self.CDendtime = self.CDendtime + datetime.timedelta(hours=int(0), minutes=int(min), seconds=int(s))
            self.OnStop(event)

            # if self.ChkBox_CDAlart.Value: self.OnAboutDig(event)
        else:
            # print('diff', diff)

            hms_text = str(diff).split('.')[0]
            ms = hms_text.split(':')[-2:]
            self.Label_CD.SetLabel(":".join(ms))


class MsgDialog(wx.Dialog):
    '''
    消息框 MsgDialog
    '''

    def __init__(self, parent, msg_data, center=False):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title="", size=(350, 115), style=wx.CAPTION | wx.CLOSE_BOX)

        self.SetTitle(msg_data.get('title'))

        self.msg = msg_data.get('msg')

        if center:
            self.msg_pos = (135, 25)
        else:
            self.msg_pos = (40,25)

        self.initUI()

    def initUI(self):
        self.Label_1 = wx.StaticText(self, label=self.msg, pos=self.msg_pos, size=(-1, -1))
        self.Label_1.SetFont(wx.Font(12, 75, 90, 90, False, "SimSun"))

        self.Label_2 = wx.StaticText(self, label=self.msg, pos=self.msg_pos, size=(-1, -1))
        self.Label_2.SetFont(wx.Font(12, 75, 90, 90, False, "SimSun"))
        self.Label_2.Hide()


class TopicDialog(wx.Dialog):
    '''
    修改題目 Dig
    '''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title="修改題目", size=(550, 550), style=wx.CAPTION | wx.CLOSE_BOX)

        self.data = chkfile('data.pkl')

        self.initUI()

    def initUI(self):
        m_StaticText1 = wx.StaticText(self, label='題目', pos=(20, 20), size=(-1, -1), style=0)
        m_StaticText1.SetFont(wx.Font(16, 75, 90, 90, False, "MingLiU"))

        self.m_TextCtrl1 = wx.TextCtrl(self, value=self.data.get('topic'), pos=(20, 60), size=(500, 350),
                                       style=wx.TE_MULTILINE)

        btn_EDIT = wx.Button(self, wx.ID_ANY, "修改", (200, 420), wx.Size(100, 60), 0)

        btn_EDIT.Bind(wx.EVT_BUTTON, self.OnStart)

    def OnStart(self, event):
        self.EndModal(wx.ID_EDIT)

