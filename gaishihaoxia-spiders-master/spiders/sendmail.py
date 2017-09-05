#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart


#message = {"df": "i know that "}
#messages = str(message)
#urlnums = 208
my_sender = '******@sina.cn'
my_user = '*******@pingan.com.cn'


def fa_mail(message, urlnums):
    ret = True
    try:
        messages = str(message)
        htmlmessage = '<html><h1>总共扫描了%s个链接;其中错误的URL为：%s</h1></html>'%(urlnums, messages)

        #msg=MIMEText(htmlmessage, 'html', 'utf-8')
        msg=MIMEMultipart()
        
        msg.attach(MIMEText(htmlmessage, 'html', 'utf-8'))
        
        att1 = MIMEText(open("all_urls.txt", 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="all_urls.txt"'
        msg.attach(att1)
        
        msg['From'] = formataddr(["监控脚本", my_sender])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["监控人", my_user])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "URL监控结果" #邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.sina.com", 25)  #发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "****")    #括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, my_user.split(","), msg.as_string())   #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()   #这句是关闭连接的意思
    except Exception as e:   #如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
        print(e)
    return ret

    if ret:
        print('ok')
    else:
        print("fail")

if __name__ == "__main__":
    fa_mail()
