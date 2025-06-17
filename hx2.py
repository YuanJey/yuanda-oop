from order.order import Order
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor

from verification.verification import Verification
MAX_WORKERS = 6
if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("https://hx.yuanda.biz")
    input("请在浏览器中完成登陆操作后，按Enter继续...")
    order=Order()
    order_files=order.get_order_files()
    verification=Verification(driver)
    verification.set_cookie()
    while True:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:  # 线程池统一管理
            for order_file in order_files:
                jd_orders_map=order.get_orders_from_file(order_file)
                for jd_account, jd_password in jd_orders_map.items():
                    verification.run_verification_for_pair(jd_account, jd_password)
        verification.save_success_summary()
        cont = input("是否再次核销（输入1继续，其他任意键退出）：")
        if cont == '1':
            continue
        else:
            print("退出程序")
            break