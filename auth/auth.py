import requests

class Auth:
    def __init__(self,key):
        self.key = key

    def check(self):
        """通过网络请求验证MAC地址"""
        url = 'https://test-1312265679.cos.ap-chengdu.myqcloud.com/config_check.json'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                json_data = response.json()
                checks_list = json_data.get('checks', [])
                if self.key in checks_list:
                    return True
            print('网络请求失败或未找到匹配的机器信息')
            return False
        except requests.RequestException as e:
            print('请求错误:', e)
            return False