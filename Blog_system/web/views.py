import redis
import smtplib
import numpy as np
from email.mime.text import MIMEText
from email.header import Header
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from Blog.settings import EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT, subject


# Create your views here.

class Login(APIView):
    def post(self, request):
        data = request.data.get('data')
        email,pwd,verify = data.split("&")
        email = email.split("=")[1]
        pwd = pwd.split("=")[1]
        verify = verify.split("=")[1]
        return Response(data="登录成功")


class GetCode(APIView):
    def get(self, request):
        email = request.GET.get('email')
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        code = "".join(str(i) for i in np.random.randint(0, 9, 4))
        html_content = """<div><p>您好,您的验证码为:%s</p></div>""" % code

        message = MIMEText(html_content, 'html', 'utf-8')
        message['From'] = Header(EMAIL_FROM, 'utf-8')
        message['To'] = Header(email, 'utf-8')
        message['message'] = Header(subject, 'utf-8')
        message['Subject'] = Header(subject, 'utf-8')

        try:
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, [email], message.as_string())
            server.quit()
            r.set(email+"_code",code)
        except Exception:
            return Response(data="邮件发送失败")
        return Response(data="邮件发送成功")