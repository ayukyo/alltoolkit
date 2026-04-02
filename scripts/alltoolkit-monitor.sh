#!/bin/bash
# AllToolkit GitHub Actions 自动监控脚本
# 用法：./alltoolkit-monitor.sh [run_id]

REPO="ayukyo/alltoolkit"
TOKEN="$GITHUB_TOKEN"
MAX_RETRIES=3

# 获取 GitHub Token
if [ -z "$TOKEN" ]; then
    TOKEN=$(grep GITHUB_TOKEN ~/.openclaw/secrets/tokens/.env 2>/dev/null | cut -d'=' -f2)
fi

if [ -z "$TOKEN" ]; then
    echo "❌ 未找到 GITHUB_TOKEN"
    exit 1
fi

# 获取最近的 workflow run
get_latest_run() {
    response=$(curl -s -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$REPO/actions/runs?per_page=1")
    
    run_id=$(echo $response | jq -r '.workflow_runs[0].id')
    status=$(echo $response | jq -r '.workflow_runs[0].status')
    conclusion=$(echo $response | jq -r '.workflow_runs[0].conclusion')
    html_url=$(echo $response | jq -r '.workflow_runs[0].html_url')
    
    echo "$run_id|$status|$conclusion|$html_url"
}

# 下载并分析日志
analyze_failure() {
    local run_id=$1
    echo "🔍 下载构建日志..."
    
    cd /tmp
    curl -sL -H "Authorization: token $TOKEN" \
        "https://api.github.com/repos/$REPO/actions/runs/$run_id/logs" \
        -o logs.zip
    
    if [ ! -f logs.zip ]; then
        echo "❌ 无法下载日志"
        return 1
    fi
    
    unzip -o logs.zip > /dev/null 2>&1
    
    echo "📊 分析错误..."
    find . -name "*.txt" -exec grep -l "error:\|FAILED\|Error" {} \; | head -5 | while read log; do
        echo "=== $log ==="
        grep -A3 "error:\|FAILED\|Error" "$log" | head -20
    done
}

# 主监控流程
echo "🔍 开始监控 AllToolkit GitHub Actions 构建..."

# 如果指定了 run_id，使用指定的；否则获取最新的
if [ -n "$1" ]; then
    run_id=$1
else
    echo "⏳ 等待 2 分钟让构建启动..."
    sleep 120
    
    run_info=$(get_latest_run)
    run_id=$(echo $run_info | cut -d'|' -f1)
fi

echo "📋 Run ID: $run_id"

retry=0
while [ $retry -lt $MAX_RETRIES ]; do
    run_info=$(get_latest_run)
    status=$(echo $run_info | cut -d'|' -f2)
    conclusion=$(echo $run_info | cut -d'|' -f3)
    html_url=$(echo $run_info | cut -d'|' -f4)
    
    echo "📊 检查构建状态：status=$status, conclusion=$conclusion"
    
    if [ "$status" = "completed" ]; then
        if [ "$conclusion" = "success" ]; then
            echo "✅ 构建成功！"
            echo "🔗 $html_url"
            exit 0
        elif [ "$conclusion" = "failure" ]; then
            echo "❌ 构建失败 (第 $((retry+1)) 次)"
            echo "🔗 $html_url"
            
            # 分析失败原因
            analyze_failure $run_id
            
            # 根据错误类型决定修复策略
            echo "🔧 尝试自动修复..."
            
            # 这里可以根据具体错误类型调用不同的修复脚本
            # 目前先通知用户手动修复
            echo "⚠️ 需要人工介入修复"
            echo ""
            echo "请查看构建日志：$html_url"
            
            retry=$((retry + 1))
            if [ $retry -lt $MAX_RETRIES ]; then
                echo "⏳ 等待 5 分钟后重试..."
                sleep 300
            fi
        else
            echo "⚠️ 构建状态：$conclusion"
            exit 1
        fi
    else
        echo "⏳ 构建还在运行中..."
        sleep 60
    fi
done

echo "⚠️ 连续 $MAX_RETRIES 次失败，需要人工介入"
echo "🔗 查看构建：$html_url"
exit 1
