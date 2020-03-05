import json
from django.http import HttpResponse
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache


# get response from Aliyun api
def send_sms(telephone,params):
    client = AcsClient('LTAI4Fj5nqYvrdqzgcMX1ZRD', 'cKCQBQmkxmrkWglblt7PmnDc3ofK53', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', telephone)
    request.add_query_param('SignName', "漂流图书")
    request.add_query_param('TemplateCode', "SMS_179225017")

    request.add_query_param('TemplateParam', params)

    response = client.do_action(request)
    print(str(response, encoding = 'utf-8'))
    return response


def sms_state_handler(response):
    code = json.loads(response)['Code']
    if code != "OK":
        return {"code":0 ,"message":"验证码发送失败"}
    return {"code":1,"message":"success"}

