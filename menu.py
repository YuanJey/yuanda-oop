from db.accounts import Database


database = Database("accounts.db")
def init_account():
    hx_account = input("请输入核销账号：")
    hx_password = input("请输入核销密码：")
    database.insert_hx_account(hx_account, hx_password)
if __name__ == '__main__':
    while True:
        print("===============================================")
        # 提示用户选择操作
        choice = input("1.获取账号信息\n"
                       "2.重新设置核销账号\n"
                       "3.获取已经转账的账号\n"
                       "4.获取还未转账的账号\n"
                       "5.设置授权码\n"
                       "其他任意键退出...\n")
        if choice == "1":  # 用户按下回车键
            account = database.get_hx_account()
            print("当前核销账号信息：", account.account, account.password)
            continue
        if choice == "2":
            init_account()
            continue
        if choice == "3":
            accounts=database.get_account_by_transfed(1)
            for account in accounts:
                print("账号：", account.account, "余额：", account.balance, "是否已转账：", account.transfed)
            continue
        if choice == "4":
            accounts = database.get_account_by_transfed(0)
            for account in accounts:
                print("账号：", account.account, "余额：", account.balance, "是否已转账：", account.transfed)
            continue
        if choice == "5":
            key = input("请输入授权码：")
            database.insert_key(key)
            print("授权码已设置。")
            continue
        else:
            print("程序已退出。")
            break
