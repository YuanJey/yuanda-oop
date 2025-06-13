#!/bin/bash

# 配置文件路径
CONFIG_FILE="accounts.txt"

# 启动每个账户
if [[ -f "$CONFIG_FILE" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
        # 忽略注释和空行
        [[ "$line" =~ ^#.* || -z "$line" ]] && continue

        # 解析每一行
        read -r account password num100 num200 num500 num1000 num2000 <<< "$line"

        # 启动脚本
        ./dist/sc "$account" "$password" \
            --num100 "$num100" \
            --num200 "$num200" \
            --num500 "$num500" \
            --num1000 "$num1000" \
            --num2000 "$num2000" &

        echo "已启动账户: $account"
    done < "$CONFIG_FILE"
else
    echo "配置文件 $CONFIG_FILE 不存在！"
    exit 1
fi

echo "所有程序已启动"
wait
