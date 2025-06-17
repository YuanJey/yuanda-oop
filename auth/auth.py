import base64
from datetime import datetime, timedelta
import requests

class Auth:
    def __init__(self):
        pass

    def get_key(self,file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            key = ''
            for line in file:
                line = line.strip()
                if not line:
                    continue  # 跳过空行
                key = line
        return key

    def base64_encode(self, key):
        """将字符串进行 Base64 编码"""
        encoded_bytes = base64.b64encode(key.encode("utf-8"))
        return encoded_bytes.decode("utf-8")
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

    def check2(self):
        current_date = datetime.now()
        # 计算前一天的日期
        # 格式化输出为字符串（格式为YYYY-MM-DD）
        previous_day_str = current_date.strftime("%Y-%m-%d")
        try:
            if self.base64_encode(previous_day_str) == self.get_key('key.txt'):
                return True
            print('请联系管理员获取授权')
            return False
        except requests.RequestException as e:
            print('请联系管理员获取授权')
            return False