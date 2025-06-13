import requests

class Transfer:
    def __init__(self,driver,to_account,password):
        self.driver = driver
        self.to_account = to_account
        self.password = password
        self.url="https://sc.yuanda.biz/jingdian/user/transfer.html"



    def  transfer(self,money,  cookie):
        try:
            data = {
                'money': money,
                'to_account': self.to_account,
                'paytype': '5',  # 假设5代表转账
                'login_password': self.password
            }
            response = requests.post(self.url, data=data,cookies=cookie, timeout=10)
            if response.status_code == 200:
                print("转账成功 金额",  money,  "收款账号", self.to_account,)
            else:
                print("转账失败")
        except requests.RequestException as e:
            print("请求失败:", e)