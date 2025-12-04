# Excel转VCF工具

将Excel文件中的联系人信息转换为VCF格式，以便导入iOS通讯录。

## 🌐 在线使用（推荐）

**无需安装，直接使用**：[https://prettydt.github.io/Cursor_vcf/](https://prettydt.github.io/Cursor_vcf/)

- ✅ 完全在线，无需下载
- ✅ 支持所有现代浏览器
- ✅ 手机、平板、电脑都可用
- ✅ 完全免费

## 功能特点

- 支持将Excel文件转换为标准VCF（vCard）格式
- 自动识别常见的中英文列名
- 支持多个联系人批量转换
- 生成的VCF文件可直接导入iOS通讯录
- 响应式设计，完美适配各种设备
- 支持PWA，可安装到桌面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方式一：图形界面（推荐）

最简单的方式，双击启动即可：

```bash
# macOS/Linux
./启动工具.sh
# 或
python3 excel_to_vcf_gui.py

# Windows
python excel_to_vcf_gui.py
```

GUI界面特点：
- 🖱️ 点击选择文件，无需输入命令
- 📊 实时显示转换日志
- ✅ 转换成功后可直接打开文件位置
- 🎨 简洁美观的用户界面

### 方式二：命令行

适合熟悉命令行的用户：

```bash
python excel_to_vcf.py <Excel文件路径> [输出VCF文件路径]
```

#### 示例

```bash
# 使用默认输出文件名（与Excel同名，扩展名为.vcf）
python excel_to_vcf.py contacts.xlsx

# 指定输出文件名
python excel_to_vcf.py contacts.xlsx output.vcf
```

## Excel文件格式要求

Excel文件应包含以下列（支持中英文列名）：

### 支持的列名

| 字段 | 支持的列名 |
|------|-----------|
| **姓名** | 姓名、name、名字、Name、联系人、Full Name |
| **电话** | 电话、phone、Phone、电话号、Tel |
| **手机** | 手机、mobile、Mobile、手机号、移动电话 |
| **邮箱** | 邮箱、email、Email、邮件、电子邮箱 |
| **公司** | 公司、company、Company、单位、工作单位 |
| **职位** | 职位、title、Title、职务、职称 |
| **地址** | 地址、address、Address、住址 |
| **备注** | 备注、note、Note、说明、注释 |

### Excel示例

| 姓名 | 手机 | 邮箱 | 公司 | 职位 |
|------|------|------|------|------|
| 张三 | 13800138000 | zhang@example.com | ABC公司 | 经理 |
| 李四 | 13900139000 | li@example.com | XYZ公司 | 主管 |

## 导入iOS通讯录

1. 将生成的VCF文件发送到你的iPhone（可通过邮件、AirDrop、iCloud等）
2. 在iPhone上打开VCF文件
3. 选择"添加到通讯录"
4. 完成导入

### 通过邮件导入

1. 将VCF文件作为附件发送到你的邮箱
2. 在iPhone上打开邮件附件
3. 点击VCF文件，选择"添加到通讯录"

### 通过iCloud导入

1. 访问 [iCloud.com](https://www.icloud.com)
2. 登录后选择"通讯录"
3. 点击左下角的设置图标（齿轮）
4. 选择"导入vCard"
5. 上传VCF文件即可

## 打包成可执行文件

如果想分享给别人使用，可以打包成独立的可执行文件：

### 使用PyInstaller打包

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包GUI版本（推荐）
./build_app.sh

# 或手动打包
pyinstaller --onefile --windowed --name "Excel转VCF工具" excel_to_vcf_gui.py
```

打包后的可执行文件在 `dist` 目录下，可以直接分享给其他人使用。

详细打包说明请查看 `打包说明.md`

## 📚 完整文档

### 🚀 部署和推广
- **[部署指南.md](部署指南.md)** - 5分钟快速部署到网络（GitHub Pages、Vercel等）
- **[平台部署与变现指南.md](平台部署与变现指南.md)** - 托管、收费、分成完整方案
- **[推广营销指南.md](推广营销指南.md)** - 从0到10万+访问量的推广策略
- **[项目优化总结.md](项目优化总结.md)** - 查看所有优化内容和快速开始指南

### 🎨 设计和开发
- **[生成图标指南.md](生成图标指南.md)** - PWA图标生成教程
- **[小红书分享文案.md](小红书分享文案.md)** - 社交媒体分享文案模板
- **[快速开始.md](快速开始.md)** - 3分钟快速上手
- **[打包说明.md](打包说明.md)** - 打包成可执行文件

### 💡 核心问题解决方案

你是否遇到这些问题？

1. **❓ 用户如何发现我的网页？**
   - 👉 查看 [推广营销指南.md](推广营销指南.md)
   - 提供小红书、知乎、B站等7大推广渠道
   - 包含爆款标题公式、SEO优化、推广时间表

2. **❓ 如何适配不同设备？**
   - 👉 已完成！查看 [项目优化总结.md](项目优化总结.md)
   - 支持手机、平板、桌面所有设备
   - 包含深色模式、触摸优化、PWA支持

3. **❓ 哪些平台可以托管、收费和分成？**
   - 👉 查看 [平台部署与变现指南.md](平台部署与变现指南.md)
   - 4种免费托管平台（Vercel、Netlify等）
   - 3种变现方案（Gumroad、Lemonsqueezy、爱发电）

## 小红书分享

如果要在小红书等平台分享这个工具，可以参考 `小红书分享文案.md` 文件，里面提供了：
- 📝 多个版本的分享文案模板
- 🖼️ 图片建议
- 🏷️ 标签推荐
- 📅 发布时间建议

## 注意事项

- Excel文件必须至少包含姓名列（或第一列作为姓名）
- 空行和无效数据会自动跳过
- VCF文件使用UTF-8编码，确保中文字符正确显示
- 如果Excel有多个工作表，默认使用第一个工作表
- GUI版本需要tkinter支持（macOS和Linux通常自带，Windows可能需要安装）
