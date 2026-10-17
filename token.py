# -*- coding: utf-8 -*-
"""
中国联通 短信验证码换取 Token 提取器
原理：利用官方 App 获取的通用短信验证码，走 radomLogin.htm 换取 token_online
"""
import os
import sys
import time
import random
import base64
from datetime import datetime
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

# 联通官方登录公钥
LOGIN_PUB_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDc+CZK9bBA9IU+gZUOc6FUGu7yO9WpTNB0PzmgFBh96Mg1WrovD1oqZ+eIF4LjvxKXGOdI79JRdve9NPhQo07+uqGQgE4imwNnRx7PFtCRryiIEcUoavuNtuRVoBAm6qdB0SrctgaqGfLgKvZHOnwTjyNqjBUxzMeQlEC2czEMSwIDAQAB
-----END PUBLIC KEY-----"""

def rsa_encrypt(val):
    random_str = ''.join(str(random.randint(0, 9)) for _ in range(6))
    text = str(val) + random_str
    cipher_rsa = PKCS1_v1_5.new(RSA.import_key(LOGIN_PUB_KEY.encode()))
    return base64.b64encode(cipher_rsa.encrypt(text.encode('utf-8'))).decode('utf-8')

def main():
    print("=" * 50)
    print("      中国联通短信验证码换取 Token 工具")
    print("=" * 50)
    
    mobile = input("1. 请输入11位联通手机号: ").strip()
    if len(mobile) != 11 or not mobile.isdigit():
        print("[-] 手机号格式不正确")
        return

    print("\n【关键步骤】")
    print("请打开手机上的【中国联通官方 App】，在登录页面输入你的手机号，点击【获取验证码】。")
    sms_code = input("2. 请输入手机收到的 6 位短信验证码: ").strip()
    if not sms_code:
        print("[-] 验证码不能为空")
        return

    print("\n正在向联通接口提交验证码换取凭据...")

    session = requests.Session()
    headers = {
        'User-Agent': 'ChinaUnicom4.x/12.0.1 (com.chinaunicom.mobilebusiness; build:120001; iOS 19.2.0) Alamofire/5.9.1 unicom{version:iphone_c@12.0100}'
    }

    # 1. 调用 radomLogin.htm (短信验证码登录接口)
    login_url = 'https://m.client.10010.com/mobileService/radomLogin.htm'
    data = {
        'version': 'iphone_c@12.0100',
        'mobile': rsa_encrypt(mobile),
        'password': rsa_encrypt(sms_code),
        'reqtime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'deviceModel': 'iPhone17,2',
    }

    try:
        res = session.post(login_url, data=data, headers=headers, timeout=15)
        res_json = res.json()
    except Exception as e:
        print(f"[-] 请求异常: {e}")
        return

    code = str(res_json.get('code', ''))
    token_online = res_json.get('token_online')
    app_id = res_json.get('appId', '')

    if code not in ('0', '0000') or not token_online:
        print(f"[-] 换取 Token 失败: [{code}] {res_json.get('dsc') or res_json.get('msg') or res_json}")
        return

    print("[+] 验证码校验成功！已取得 token_online")

    # 2. 校验会话在线有效性并激活 (onLine.htm)
    print("正在激活在线会话...")
    online_url = 'https://m.client.10010.com/mobileService/onLine.htm'
    online_data = {
        'isFirstInstall': '1',
        'netWay': 'Wifi',
        'version': 'android@11.0000',
        'token_online': token_online,
        'provinceChanel': 'general',
        'deviceModel': 'ALN-AL10',
        'step': 'dingshi',
        'androidId': '291a7deb1d716b5a',
        'reqtime': int(time.time() * 1000)
    }
    if app_id:
        online_data['appId'] = app_id

    try:
        on_res = session.post(online_url, data=online_data, headers={'User-Agent': 'Dalvik/2.1.0'}, timeout=15).json()
        if str(on_res.get('code')) in ('0', '0000'):
            app_id = on_res.get('appId') or app_id
            print("[+] 在线会话已激活！")
        else:
            print(f"[!] 会话激活返回: {on_res.get('dsc') or on_res.get('msg')}，但 Token 已取得")
    except Exception:
        pass

    # 3. 输出配置条目
    final_cookie = f"{token_online}#{app_id}#{mobile}" if app_id else f"{token_online}#{mobile}"
    
    print("\n" + "=" * 50)
    print("🎉 获取成功！请复制以下内容到青龙面板：")
    print(f"变量名: chinaUnicomCookie")
    print(f"变量值: {final_cookie}")
    print("=" * 50)

if __name__ == '__main__':
    main()
