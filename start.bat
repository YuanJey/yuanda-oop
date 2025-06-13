@echo off
chcp 65001 >nul
set "CONFIG_FILE=accounts.txt"
if not exist "%CONFIG_FILE%" (
    echo 配置文件 %CONFIG_FILE% 不存在！
    exit /b 1
)
echo 正在启动账户任务...
for /f "usebackq tokens=*" %%a in ("%CONFIG_FILE%") do (
    echo 正在处理: %%a

    echo %%a | findstr "^#" >nul && continue
    for /f "tokens=1-6" %%A in ("%%a") do (
        set account=%%A
        set password=%%B
        set num100=%%C
        set num200=%%D
        set num500=%%E
        set num1000=%%F
        set num2000=%%G
        echo 启动账户: %%A
        start "" "dist\sc.exe" %%A %%B --num100 %%C --num200 %%D --num500 %%E --num1000 %%F --num2000 %%G

        timeout /t 1 >nul
    )
)
echo.
echo 所有程序已启动
echo.

exit /b 0
