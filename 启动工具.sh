#!/bin/bash
# Excel转VCF工具 - 快速启动脚本

cd "$(dirname "$0")"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 正在安装依赖..."
    python3 -m pip install -r requirements.txt
fi

# 启动GUI版本
echo "🚀 启动Excel转VCF工具..."
python3 excel_to_vcf_gui.py

