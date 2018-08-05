# -*- coding: utf-8 -*-
import sys
import requests
import re
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from pprint import pprint
reload(sys)
sys.setdefaultencoding('utf-8')

def get_ticket_info():
    url_station='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9049'
    response = requests.get(url_station, verify=False)
    stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
    #pprint(dict(stations), indent=4)
    #print stations
    url_head = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-08-10&leftTicketDTO.from_station=HGH&leftTicketDTO.to_station=JNK&purpose_codes=ADULT'
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
    head = {'User-Agent': user_agent, 'Content-Type': 'application/json;charset=UTF-8', 'Cache-Control': 'max-age=0',
            'If-Modified-Since': bytes(0), 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest'}
    # data = {'scope': 0, 'username': 'admin', 'password': 'Admin@storage'}
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    r = requests.get(url_head, allow_redirects=True, verify=False, timeout=10)
    if r.status_code == 200:
        # station_dict = r.json()['data']['map']
        traindatas = r.json()['data']['result']
        for data in traindatas:
            trainInfo = {}
            # 解析网页内容，抓取余票信息
            trainRowItem = re.compile('\|([^\|]*)').findall(data)
            if trainRowItem[2] == "G282" and trainRowItem[-7] == "有":

                # 第三方 SMTP 服务
                mail_host = "smtp.163.com"  # 设置服务器
                mail_user = "hund567"  # 用户名
                mail_pass = "1990312peking"  # 口令

                sender = 'hund567@163.com'
                receivers = 'hund567@163.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

                message = MIMEText('G282有票了', 'plain', 'utf-8')
                message['From'] = Header("菜鸟教程", 'utf-8')
                message['To'] = Header("测试", 'utf-8')

                subject = 'G282有票了'
                message['Subject'] = Header(subject, 'utf-8')
                try:
                    smtpObj = smtplib.SMTP()
                    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
                    smtpObj.login(mail_user, mail_pass)
                    smtpObj.sendmail(sender, receivers, message.as_string())
                    print "邮件发送成功"
                except smtplib.SMTPException:
                    print "Error: 无法发送邮件"


if __name__ == '__main__':
    get_ticket_info()
