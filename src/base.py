# -*-coding:utf-8 -*-

import pickle
from data import conf
import os


def log_path(dir):
    path = os.path.join(os.environ['APPDATA'], dir)
    return path


def chkdir(dir):
    path = log_path(dir)

    if os.path.isdir(path):
        return path
    else:
        os.mkdir(path)
        return path


def chkfile(filename):
    file_path = filename

    if (os.path.isfile(file_path)):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data

    else:
        with open(file_path, 'wb') as f:
            pickle.dump(conf.data, f, pickle.HIGHEST_PROTOCOL)
            return conf.data


def whirefile(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        return data


def whire_output(filename, data):
    '''
    將測試結果輸出到文本
    :param filename: 檔案名稱
    :param data: 測試完返回的字典
    :return:
    '''
    file_path = os.path.join(chkdir(conf.LOG_DIR), "%s.txt" % filename )

    f = open(file_path, 'a+')
    f.write('## 測驗結果\n')
    f.write('作答：%s\n' % data.get('fix_view'))
    f.write('測驗時間：%s\n' % data.get('min'))
    f.write('字數統計：%s\n' % data.get('max'))
    f.write('正確字數：%s\n' % data.get('ok'))
    f.write('錯誤字數：%s\n' % data.get('miss'))
    f.write('平均字數：%s\n' % data.get('avg'))
    f.write('\n')


def whire_output_html(filename, data):
    file_path = os.path.join(chkdir(conf.LOG_DIR), "%s.html" % filename)

    f = open(file_path, 'a+')
    f.write('<h2>測驗結果</h2>')
    f.write('<p>作答：%s</p>' % data.get('fix_view'))
    f.write('<p>測驗時間：%s分鐘 ' % data.get('min'))
    f.write('字數統計：%s ' % data.get('max'))
    f.write('正確字數：%s ' % data.get('ok'))
    f.write('錯誤字數：%s ' % data.get('miss'))
    f.write('平均字數：%s </p>' % data.get('avg'))


def create_output_html(filename, topic):
    file_path = os.path.join(chkdir(conf.LOG_DIR), "%s.html" % filename)

    f = open(file_path, 'w')

    f.write("<h1>%s</h1>" % filename)
    f.write('<p>題目：%s</p>' % topic)
    f.close()


def chk_wavs():
    # cwd = os.getcwd()
    for wav in conf.wavs:
        # print(wav)
        name = wav.get('key')
        if os.path.isfile(name):
            pass
        else:
            with open(name, 'wb') as f:
                f.write(wav.get('val'))

def chk_icons():
    # cwd = os.getcwd()
    for icon in conf.icons:
        # print(wav)
        name = icon.get('key')
        if os.path.isfile(name):
            pass
        else:
            with open(name, 'wb') as f:
                f.write(icon.get('val'))
