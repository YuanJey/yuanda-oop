import subprocess
import sys
from db.accounts import Database


def start_accounts():
    # 初始化数据库连接
    db = Database("accounts.db")

    # 获取所有 hx_account
    accounts = db.get_all_accounts()
    if not accounts:
        print("没有找到可用账户，请检查数据库。")
        return

    # 判断操作系统
    is_windows = sys.platform == 'win32'
    executable_path = "v7.exe" if is_windows else "./dist/sc9"

    for account in accounts:
        cmd = [
            executable_path,
            account.account,
            'Knight123.',
            "2025-06-20",  # 示例日期，可根据需要动态生成
            "--num100", "0",
            "--num200", "0",
            "--num500", "0",
            "--num1000", "0",
            "--num2000", "0"
        ]

        print(f"正在启动账户: {account.account}")
        try:
            # 在子进程中启动
            if is_windows:
                # Windows 下不加 ./，直接运行 exe
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                # Linux/macOS 下后台运行
                subprocess.Popen(cmd)
        except Exception as e:
            print(f"启动失败: {e}")


if __name__ == '__main__':
    start_accounts()
