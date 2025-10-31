#!/bin/bash
# Excel转VCF工具 - 自动打包脚本

echo "🚀 开始打包Excel转VCF工具..."

# 检查PyInstaller是否安装
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 正在安装PyInstaller..."
    pip3 install pyinstaller
fi

# 清理之前的构建
echo "🧹 清理旧的构建文件..."
rm -rf build dist __pycache__ *.spec

# 打包GUI版本
echo "📱 正在打包GUI版本..."
pyinstaller --onefile \
    --windowed \
    --name "Excel转VCF工具" \
    --add-data "README.md:." \
    --hidden-import=pandas \
    --hidden-import=openpyxl \
    excel_to_vcf_gui.py

# 打包命令行版本
echo "⌨️  正在打包命令行版本..."
pyinstaller --onefile \
    --name "excel_to_vcf" \
    --hidden-import=pandas \
    --hidden-import=openpyxl \
    excel_to_vcf.py

echo ""
echo "✅ 打包完成！"
echo "📁 GUI版本: dist/Excel转VCF工具"
echo "📁 命令行版本: dist/excel_to_vcf"
echo ""
echo "💡 提示：可以将这些文件分享给其他用户使用"

