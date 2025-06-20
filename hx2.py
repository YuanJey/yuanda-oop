from selenium.webdriver.support.wait import WebDriverWait
import requests

from db.accounts import Database
from order.order import Order
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from verification.verification import Verification
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
MAX_WORKERS = 6
transfer="https://hx.yuanda.biz/Home/User/tomall"

class Transfer:
    def __init__(self, driver,password):
        self.driver = driver
        self.password=password
        self.url="https://hx.yuanda.biz/Home/User/tomall"

    def transfer(self,account,money):
        self.driver.get(self.url)
        # 等待元素出现（最多等待10秒）
        account_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'account'))
        )
        account_input.clear()
        account_input.send_keys(account)
        money_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'money'))
        )
        money_input.clear()
        money_input.send_keys(str(money))

        passwd_input = WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.ID, 'passwd'))
        )
        passwd_input.clear()
        passwd_input.send_keys(str(money))
        wait = WebDriverWait(self.driver, 60)
        confirm_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="apply-footer-btn " and text()="确认转账"]'))
        )
        confirm_button.click()

    def transfer2(self, account, money):
        url = "https://hx.yuanda.biz/Home/User/tomall_apply"

        # 构造表单数据
        data = {
            'money': str(money),
            'account': account,
            'passwd': self.password
        }
        cookies = self.driver.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        try:
            response = requests.post(url, data=data,cookies=cookie_dict)
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None

    def get_available_transfer_money(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 60)
        # 定位到包含可转账金额的 span
        available_money_element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="可转账金额："]/following-sibling::span[1]'))
        )
        money_text = available_money_element.text.strip()
        try:
            return float(money_text)
        except ValueError:
            print(f"无法解析可转账金额: {money_text}")
            return 0.0


def read_balance_file(file_path):
    balance_map = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                continue  # 跳过空行
            parts = line.strip().split('\t')  # 使用制表符分割
            if len(parts) >= 2:
                key = parts[0]
                value = float(parts[1])
                balance_map[key] = value

    return balance_map

if __name__ == '__main__':
    date = input("请输入核销的订单日期(例如:2025-06-18)：")
    try:
        # 验证日期格式是否正确
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        previous_day_str = parsed_date.strftime("%Y-%m-%d")  # 标准化为统一格式
    except ValueError:
        print(f"日期格式错误: {date}，请使用 YYYY-MM-DD 格式。")
        exit(1)
    driver = webdriver.Chrome()
    driver.get("https://hx.yuanda.biz")
    input("请在浏览器中完成登陆操作后，按Enter继续...")
    order=Order()
    order_files=order.get_order_files(date)
    verification=Verification(driver)
    verification.set_cookie()
    while True:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:  # 线程池统一管理
            for order_file in order_files:
                jd_orders_map=order.get_orders_from_file(order_file)
                for jd_account, jd_password in jd_orders_map.items():
                    verification.run_verification_for_pair(jd_account, jd_password)
        verification.save_success_summary()
        Db=Database("accounts.db")
        accounts=Db.get_all_accounts()
        # password = input("输入密码开始配资:")
        hx_account=Db.get_hx_account()
        if hx_account.account:
            transfer = Transfer(driver, hx_account.password)
            for account in accounts:
                all_money = transfer.get_available_transfer_money()
                if all_money > (30000 - account.balance):
                    transfer.transfer2(account, 30000 - account.balance)
                    all_money1 = transfer.get_available_transfer_money()
                    if all_money1 ==all_money-(30000 - account.balance):
                        print('转账到',account.account, '成功，转账金额：', 30000 - account.balance)
                        Db.insert_account(account.account, 30000, 1)
                    else:
                        print(f"账户 {account} 可转账金额 {all_money1} 小于配置金额 {30000 - account.balance}，请手动充值。")
                else:
                    print(f"账户 {account} 可转账金额 {all_money} 小于配置金额 {30000 - account.balance}，请手动充值。")
        cont = input("是否再次核销（输入1继续，其他任意键退出）：")
        if cont == '1':
            continue
        else:
            print("退出程序")
            break


# if __name__ == '__main__':
#     balance_map = read_balance_file('2025-06-17_购买前余额_balance.txt')
#     print(balance_map)