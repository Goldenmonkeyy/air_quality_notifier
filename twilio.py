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


#value1 = re.findall(r': AQI \(US\) (.*?) ',html_licang)
#value2 = re.findall(r': AQI \(US\) (.*?) ',html_shilaoren)
#value3 = re.findall(r': AQI \(US\) (.*?) ',html_shinan)

#htmls=  [html_licang, html_shilaoren, html_shinan]

#values = [value1, value2, value3]
def value(x):
    value_str_list = re.findall(r': AQI \(US\) (.*?) ',x)
    value_int_list = list(map(int, value_str_list))
    value_int = value_int_list[0]
    return value_int

print(value(licang))
print(value(shilaoren))
print(value(shinan))
#value1 = list(map(int, value1))
#value1 = value1[0]
#print(value1)

def sendSMS(x):
    account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth_token = 'xxxxxxxxxxxxxxxxxxxxxx'
    client = Client(account_sid, auth_token)
    numbers_to_message = ['+86xxxxxxxxxxxxxxx']

    for num in numbers_to_message:
        message = client.messages.create(
            body = x,
            from_ = '+1386284xxxx',
            to = num
        )
    print(message.sid)

if value(licang) <= 50 and value(shilaoren) <= 50 and value(shinan) <= 50:
    body1 = 'Green day, outdoor sports'    
    sendSMS(body1)
elif value(licang) > 50 and value(shilaoren) <= 50 and value(shinan) <= 50:
    body2 = 'Blue day, go to seaside'
    sendSMS(body2)
elif value(licang) > 50 and value(shilaoren) <= 50 and value(shinan) > 50:
    body3 = 'Blue day, shilaoren'
    sendSMS(body3)
elif value(licang) > 50 and value(shilaoren) > 50 and value(shinan) <= 50:
    body4 = 'Blue day,zhanqiao'
    sendSMS(body4)
elif value(licang) >= 50:
    body5 = 'mask is must'
    sendSMS(body5)
