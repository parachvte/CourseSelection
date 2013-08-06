# coding: UTF-8
import httplib
import urllib
#import getpass
import time

import OCR


host = "xk.fudan.edu.cn"
studentId = raw_input("studentID: ")
password = raw_input("password: ")
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

    conn.request("GET", "/xk")
    res = conn.getresponse()
    res.read()

    conn.request("GET", "/xk/image.do")
    res = conn.getresponse()
    if res.getheader("Set-Cookie") is not None:
        headers['Cookie'] = res.getheader("Set-Cookie").split(";")[0]
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
        print 'Exception'
        return False
    conn.close()
    result = res.reason == "Found"
    if result:
        OCRHdl.save_attribute_codes([i for i in rand])
    return result


if __name__ == "__main__":
    no = 0
    while True:
        no += 1
        if login():
            print 'Yes {}'.format(no)
        else:
            print 'No'
            no = 0