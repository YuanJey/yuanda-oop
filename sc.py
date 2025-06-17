import argparse

from selenium.webdriver.chrome.options import Options
from datetime import datetime

from auth.auth import Auth
from buy.buy import Buy
from transfer.transfer import Transfer
from user.user import User
from selenium import webdriver
import time

if __name__ == '__main__':
    auth=Auth('19162856317')
    if auth.check():
        print('验证通过')
        parser = argparse.ArgumentParser(description='账户信息')
        parser.add_argument('account', type=str, help='账户')
        parser.add_argument('password', type=str, help='密码')
        parser.add_argument('date', type=str, help='订单日期')
        parser.add_argument('--num100', type=int, default=0, help='100元数量')
        parser.add_argument('--num200', type=int, default=0, help='200元数量')
        parser.add_argument('--num500', type=int, default=0, help='500元数量')
        parser.add_argument('--num1000', type=int, default=0, help='1000元数量')
        parser.add_argument('--num2000', type=int, default=0, help='2000元数量')
        args = parser.parse_args()
        num100 = args.num100
        num200 = args.num200
        num500 = args.num500
        num1000 = args.num1000
        num2000 = args.num2000
        account = args.account
        password = args.password
        date = args.date
        try:
            # 验证日期格式是否正确
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
            previous_day_str = parsed_date.strftime("%Y-%m-%d")  # 标准化为统一格式
        except ValueError:
            print(f"日期格式错误: {date}，请使用 YYYY-MM-DD 格式。")
            exit(1)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 开启无头模式
        driver=webdriver.Chrome(chrome_options)
        user=User(driver,account,password)
        if user.login():
            print(account,' 登录成功')
            user.download_order(date)
            user.save_balance_to_file("购买前余额")
            buy=Buy(driver, num100, num200, num500, num1000, num2000)
            balance = user.get_balance()
            if balance>0:
                transfer=Transfer(driver, "nuoshou780", "Knight123.")
                transfer.transfer(balance,  user.get_cookie())
            while True:
                balance = user.get_balance()
                if buy.check_balance(balance):
                    print("余额大于等于配置金额,即将开始执行。")
                    break
                else:
                    print("余额小于配置金额，等待充值...")
                    time.sleep(20)
            buy.start()
            user.save_balance_to_file("购买后余额")
            driver.quit()
    else:
        print('验证失败')

# if __name__ == '__main__':
#     max_attempts = 1
#     attempt = 0
#
#     while attempt < max_attempts:
#         driver = None
#         try:
#             auth = Auth('19162856317')
#             if not auth.check():
#                 print("认证失败，退出")
#                 break
#
#             parser = argparse.ArgumentParser(description='账户信息')
#             parser.add_argument('account', type=str, help='账户')
#             parser.add_argument('password', type=str, help='密码')
#             parser.add_argument('--num100', type=int, default=0, help='100元数量')
#             parser.add_argument('--num200', type=int, default=0, help='200元数量')
#             parser.add_argument('--num500', type=int, default=0, help='500元数量')
#             parser.add_argument('--num1000', type=int, default=0, help='1000元数量')
#             parser.add_argument('--num2000', type=int, default=0, help='2000元数量')
#             args = parser.parse_args()
#             num100 = args.num100
#             num200 = args.num200
#             num500 = args.num500
#             num1000 = args.num1000
#             num2000 = args.num2000
#             account = args.account
#             password = args.password
#
#             chrome_options = Options()
#             # chrome_options.add_argument("--headless")  # 开启无头模式
#             driver = webdriver.Chrome(chrome_options)
#
#             user = User(driver, account, password)
#             if not user.login():
#                 print("登录失败，准备重试...")
#                 attempt += 1
#                 driver.quit()
#                 continue
#
#             print('登录成功')
#             user.download_order()
#             user.save_balance_to_file("购买前余额")
#
#             buy = Buy(driver, num100, num200, num500, num1000, num2000)
#             balance = user.get_balance()
#             if balance > 0:
#                 transfer = Transfer(driver, "nuoshou780", "Knight123.")
#                 transfer.transfer(balance, user.get_cookie())
#
#             while True:
#                 balance = user.get_balance()
#                 if buy.check_balance(balance):
#                     print("余额大于等于配置金额,即将开始执行。")
#                     break
#                 else:
#                     print("余额小于配置金额，等待充值...")
#                     time.sleep(20)
#
#             buy.start()
#             user.save_balance_to_file("购买后余额")
#             driver.quit()
#             break  # 成功执行完流程，退出循环
#
#         except Exception as e:
#             print(f"发生异常: {e}，准备重试...")
#             attempt += 1
#             if driver:
#                 driver.quit()
#         finally:
#             if attempt >= max_attempts:
#                 print("已达到最大重试次数，任务失败")
