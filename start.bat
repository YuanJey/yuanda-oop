@echo off
setlocal enabledelayedexpansion

set CONFIG_FILE=accounts.txt

if not exist "%CONFIG_FILE%" (
    echo 配置文件 %CONFIG_FILE% 不存在！
    exit /b 1
)

echo 正在启动账户...

for /f "tokens=*" %%a in (%CONFIG_FILE%) do (
    set "line=%%a"

    echo.!line! | findstr "^#">nul && continue
    if "!line!" == "" continue

    for /f "tokens=1-8" %%b in ("!line!") do (
        set account=%%b
        set password=%%c
        set date=%%d
        set num100=%%e
        set num200=%%f
        set num500=%%g
        set num1000=%%h
        set num2000=%%i

        :: 启动 v7.exe，并传入所有参数
        start "" "./v7.exe" "!account!" "!password!" "!date!" ^
            --num100 !num100! ^
            --num200 !num200! ^
            --num500 !num500! ^
            --num1000 !num1000! ^
            --num2000 !num2000!

        echo 已启动账户: !account!
    )
)

echo 所有程序已启动
endlocal