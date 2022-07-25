#!/usr/bin/python3


import urllib.request
import re
from twilio.rest import Client

request_url_licang = urllib.request.urlopen("https://air-quality.com/place/china/licang/bf0516a5?lang=en&standard=aqi_us")
request_url_shilaoren = urllib.request.urlopen("https://air-quality.com/place//d5067b0b?lang=en&standard=aqi_us")
request_url_shinan = urllib.request.urlopen('https://air-quality.com/place//774671d4?lang=en&standard=aqi_us')

licang = request_url_licang.read().decode('utf-8')
shilaoren = request_url_shilaoren.read().decode('utf-8')
shinan = request_url_shinan.read().decode('utf-8')


def value(x):
    value_str_list = re.findall(r': AQI \(US\) (.*?) ',x)
    value_int_list = list(map(int, value_str_list))
    value_int = value_int_list[0]
    return value_int

print(value(licang))
print(value(shilaoren))
print(value(shinan))

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

def sendSMS(code):
    credentials = AccessKeyCredential('your-access-key-id', 'your-access-key-secret')
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    client = AcsClient(region_id='cn-qingdao', credential=credentials)

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('PhoneNumbers', "your phone number")
    request.add_query_param('SignName', "test")
    request.add_query_param('TemplateCode', code)

    response = client.do_action(request)
    # python2:  print(response) 
    print(str(response, encoding = 'utf-8'))

if value(licang) <= 50 and value(shilaoren) <= 50 and value(shinan) <= 50:
    code_green = 'SMS_229481740'    
    sendSMS(code_green)
elif value(licang) > 50 and value(shilaoren) <= 50 and value(shinan) <= 50:
    code_blue = 'SMS_229466772'
    sendSMS(code_blue)
elif value(licang) > 50 and value(shilaoren) <= 50 and value(shinan) > 50:
    code_shilaoren = 'SMS_229471773'
    sendSMS(code_shilaoren)
elif value(licang) > 50 and value(shilaoren) > 50 and value(shinan) <= 50:
    code_shinan = 'SMS_229481748'
    sendSMS(code_shinan)
elif value(licang) >= 100:
    code_grey = 'SMS_229466781'
    sendSMS(code_grey)
