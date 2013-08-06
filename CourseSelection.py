#-*- coding: UTF-8 -*-

import httplib
import urllib
import getpass
import time
import re
from HTMLParser import HTMLParser

import OCR


host = "xk.fudan.edu.cn"
studentId = raw_input("studentId: ")
password = getpass.getpass("password: ")
#password = raw_input("password: ")
lessons = raw_input('lessons(separate by spaces): ').split()
headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Origin": "http://xk.fudan.edu.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://xk.fudan.edu.cn/xk/",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
}


def login():
    conn = httplib.HTTPConnection(host)

    # get captcha
    conn.request("GET", "/xk")
    res = conn.getresponse()
    res.read()

    conn.request("GET", "/xk/image.do")
    res = conn.getresponse()
    if res.getheader("Set-Cookie") is not None:
        headers["Cookie"] = res.getheader("Set-Cookie").split(";")[0]
    with open("captcha.jpg", "wb") as F:
        F.write(res.read())

    # OCR
    OCRHdl = OCR.CaptchaHandler()
    rand = OCRHdl.captcha_from_image("captcha.jpg")

    # POST form
    data = urllib.urlencode({"studentId": studentId,
                             "password": password,
                             "rand": rand,
                             "Submit2": r"提交"})
    try:
        time.sleep(0.2)
        conn.request("POST", "/xk/loginServlet", data, headers)
        res = conn.getresponse()
        F = open("out.html", "w")
        F.write(res.read())
        F.close()
    except Exception as e:
        print "Exception"
        return False
    conn.close()

    return res.reason == "Found"


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self._token = None
        self._lesson = None
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "input" and ("name", "token") in attrs:
            for attr in attrs:
                if attr[0] == "value":
                    self._token = attr[1]

    def handle_data(self, data):
        if data.strip() == self._lesson:
            self._lesson = "FOUND"

    def get_token(self):
        return self._token

    def set_lesson(self, lesson):
        self._lesson = lesson

    def has_lesson(self):
        return self._lesson == "FOUND"


def chooseLesson(lesson):
    conn = httplib.HTTPConnection(host)

    # get captcha
    conn.request("GET", "/xk/input.jsp", None, headers)
    res = conn.getresponse()
    parser = MyHTMLParser()
    parser.feed(res.read())
    token = parser.get_token()
    if token is None:
        print "have bugs in my programme"
        return False

    conn.request("GET", "/xk/image.do?token={}".format(token), None, headers)
    res = conn.getresponse()
    if res.getheader("Set-Cookie") is not None:
        headers["Cookie"] = res.getheader("Set-Cookie").split(";")[0]
    with open("captcha.jpg", "wb") as F:
        F.write(res.read())

    # OCR
    OCRHdl = OCR.CaptchaHandler()
    rand = OCRHdl.captcha_from_image("captcha.jpg")

    # POST
    data = urllib.urlencode({"token": token,
                             "selectionId": lesson,
                             "xklb": "ss",
                             "rand": rand})
    try:
        time.sleep(3)
        conn.request("POST", "/xk/doSelectServlet", data, headers)
        res = conn.getresponse()
        F = open("out.html", "w")
        F.write(res.read())
        F.close()
        print u"返回结果写在out.html中，请查看"
    except Exception as e:
        print u"请求失败"
        return False

    # check if lesson is selected
    conn.request("GET", "/xk/courseTableServlet", None, headers)
    res = conn.getresponse()
    parser.set_lesson(lesson)
    parser.feed(res.read())
    conn.close()

    return parser.has_lesson()


if __name__ == "__main__":
    cnt = 0
    while True:
        cnt += 1
        print
        print u"第{}次尝试：".format(cnt)
        if login():
            print u"登录成功"
            break
        print u"登录失败，将自动重新登录（可能是学号/密码输入错误）"

    cnt = 0
    while lessons:
        cnt += 1
        print
        print u"第{}次尝试：".format(cnt)
        for lesson in lessons:
            print u"now trying", lesson
            if chooseLesson(lesson):
                print lesson + u" 选课成功"
                lessons.remove(lesson)
                break
            else:
                print lesson + u" 选课失败"