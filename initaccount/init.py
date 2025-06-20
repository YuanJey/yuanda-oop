from db.accounts import Database

if __name__ == '__main__':
    db = Database("accounts.db")
    hx_account = input("请输入核销账号：")
    hx_password = input("请输入核销密码：")
    db.insert_hx_account(hx_account, hx_password)