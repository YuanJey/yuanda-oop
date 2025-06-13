import time

from selenium import webdriver

from user.user import User

if  __name__ == '__main__':
    account = "nuoshou780"
    password = "Yuan970901"
    driver = webdriver.Chrome()
    user = User(driver, account, password)
    start_time = time.time()
    if user.login():
        elapsed_time = time.time() - start_time
        print(f'登录耗时: {elapsed_time:.2f} 秒')
        print('登录成功')
    else:
        print('登录失败')