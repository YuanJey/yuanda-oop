from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class  Buy:
    def __init__(self, driver,num100, num200, num500, num1000, num2000):
        self.driver = driver
        self.num100 = num100
        self.num200 = num200
        self.num500 = num500
        self.num1000 = num1000
        self.num2000 = num2000
        self.amount=  num100*100+num200*200+num500*500+num1000*1000+num2000*2000
        self.m_100 = 'https://sc.yuanda.biz/pg/234.html'
        self.m_200 = 'https://sc.yuanda.biz/pg/235.html'
        self.m_500 = 'https://sc.yuanda.biz/pg/237.html'
        self.m_1000 = 'https://sc.yuanda.biz/pg/240.html'
        self.m_2000 = 'https://sc.yuanda.biz/pg/241.html'
        pass

    def check_balance(self,balance):
        if balance >= self.amount:
            print(f"余额: {balance} 配置金额为: {self.amount}, 可以开始购买。")
            return True
        else:
            print(f"余额: {balance} 配置金额为: {self.amount}, 不足，请充值。")
            return False
    def start(self):
        for i in range(self.num100):
            self.handle(100)
        for i in range(self.num200):
            self.handle(200)
        for i in range(self.num500):
            self.handle(500)
        for i in range(self.num1000):
            self.handle(1000)
        for i in range(self.num2000):
            self.handle(2000)
    def handle(self,number):
        url= None
        if  number == 100:
            url = self.m_100
        elif number == 200:
            url = self.m_200
        elif number == 500:
            url = self.m_500
        elif number == 1000:
            url = self.m_1000
        elif number == 2000:
            url = self.m_2000
        try:
            self.driver.get(url)
            buy_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.cart-buy > a.buy-btn'))
            )
            # 使用JavaScript点击
            self.driver.execute_script("arguments[0].click();", buy_button)

            # 找“找人代付”并点击
            pay_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.ID, 'alipay'))
            )
            self.driver.execute_script("arguments[0].click();", pay_button)

            # 点击结算按钮
            submit_btn = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.ID, 'jiesuan'))
            )
            # 使用JavaScript点击
            self.driver.execute_script("arguments[0].click();", submit_btn)

            success_message = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'zhengwen'))
            )
            message_text = success_message.text
            print("成功信息：", message_text,number, "面额购买成功+1")
        except Exception as e:
            print(f"操作失败：{e}", "金额:", number)