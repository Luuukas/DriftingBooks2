import rsa

text = 'Welcome to RSA'
# 生成密钥对
pubkey, prikey = rsa.newkeys(1024)
# 加密：使用公钥
result = rsa.encrypt(text.encode(), pubkey)
print('加密后的数据：',result)
# 解密：使用私钥
print('解密后的数据：',rsa.decrypt(result, prikey))