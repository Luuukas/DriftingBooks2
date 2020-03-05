from User.sendsms import send_sms, sms_state_handler

import json
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.core.cache import cache

from User.models import User

# 全局变量及共用的函数
responseTable = ["success",
                 "无法根据uid找到相关信息",
                 "密码错误",
                 "验证码错误"]

def constructHttpResponse(errorNum):
    resCode = 1 if errorNum == 0 else 0
    resMsg = responseTable[errorNum]
    response = {'code': resCode, "message": resMsg}
    return HttpResponse(json.dumps(response, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


################################################################
#   以下为业务逻辑
################################################################

# 接收前端发来的uid(get请求)，向该用户名绑定的手机号发送短信验证码
def sendSms2BindedPhone(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    # uid是否需要转换为int?
    # get binded phonenumber from uid
    if not user:
        ret = "\"code\":0,\"message\":\"无法获取该用户绑定的手机号\""
        return HttpResponse(json.dumps(ret, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

    phonenumber = user.phonenumber
    code = get_random_string(length=4, allowed_chars="0123456789")
    params = "{\"code\":\"" + code + "\"}"
    sms_result = sms_state_handler(send_sms(phonenumber,params))

    if sms_result["code"] == 1:
        cache.set(phonenumber, code, timeout=600)
    return HttpResponse(json.dumps(sms_result, ensure_ascii=False),
                        content_type="application/json,charset=utf-8")


# 接收uid、原密码、新密码与验证码
# input:
# (json)
# {
#   uid:XXX
#   oldpassword:XXX
#   newpassword:XXX
#   code:XXX
# }
def changePassword(request):
    if request.method == "POST":
        errorNum = 0
        result = json.loads(request.body)
        oldpassword = result["oldpassword"]
        newpassword = result["newpassword"]
        code = result["code"]
        username = request.session.get("username")
        user = User.objects.get(username=username)

        # check if old password correct
        if not user:
            errorNum = 1
        if oldpassword!=user.password:
            errorNum = 2
        if errorNum==0 and code != cache.get(user.phonenumber):
            errorNum = 3

        # update password in database
        if errorNum == 0:
            user.password = newpassword
            user.save()
        # according to errorNum
        # return 'Response' to front-end
        return constructHttpResponse(errorNum)


# input:
# {
#   uid:XXXX
#   password:XXXX
#   newphonenumber:XXXX
#   code:XXXX
# }
def changePhonenumber(request):
    if request.method == "POST":
        errorNum = 0
        result = json.loads(request.body)
        password = result["password"]
        newphonenumber = result["newphonenumber"]
        code = result["code"]
        username = request.session.get("username")
        user = User.objects.get(username=username)
        # check password
        if not user:
            errorNum = 1
        if password!=user.password:
            errorNum = 2
        if errorNum==0 and code != cache.get(user.phonenumber):
            errorNum = 3

        # update phonenumber in database
        if errorNum == 0:
            user.phonenumber = newphonenumber
            user.save()
        return constructHttpResponse(errorNum)




