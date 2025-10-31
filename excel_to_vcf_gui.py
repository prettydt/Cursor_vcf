#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel转VCF工具 - GUI图形界面版
将Excel文件中的联系人信息转换为VCF格式，以便导入iOS通讯录
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path

# 导入转换函数
from excel_to_vcf import excel_to_vcf


class ExcelToVCFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel转VCF工具 - iOS通讯录导入助手")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以添加图标文件路径
            pass
        except:
            pass
        
        # 选择的文件路径
        self.excel_path = tk.StringVar()
        self.vcf_path = tk.StringVar()
        
        self.create_widgets()
        
        # 设置样式
        self.setup_style()
    
    def setup_style(self):
        """设置界面样式"""
        self.root.configure(bg='#f5f5f5')
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.root, bg='#f5f5f5')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="📱 Excel转VCF工具",
            font=("Arial", 20, "bold"),
            bg='#f5f5f5',
            fg='#333'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="快速将Excel联系人导入iPhone通讯录",
            font=("Arial", 11),
            bg='#f5f5f5',
            fg='#666'
        )
        subtitle_label.pack(pady=5)
        
        # Excel文件选择区域
        excel_frame = tk.Frame(self.root, bg='#f5f5f5')
        excel_frame.pack(pady=15, padx=30, fill='x')
        
        tk.Label(
            excel_frame,
            text="1. 选择Excel文件:",
            font=("Arial", 12, "bold"),
            bg='#f5f5f5',
            anchor='w'
        ).pack(anchor='w', pady=(0, 5))
        
        excel_select_frame = tk.Frame(excel_frame, bg='#f5f5f5')
        excel_select_frame.pack(fill='x')
        
        self.excel_entry = tk.Entry(
            excel_select_frame,
            textvariable=self.excel_path,
            font=("Arial", 10),
            state='readonly',
            bg='white',
            fg='#333'
        )
        self.excel_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        excel_btn = tk.Button(
            excel_select_frame,
            text="📁 选择文件",
            command=self.select_excel_file,
            font=("Arial", 10),
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        excel_btn.pack(side='right')
        
        # VCF输出路径区域
        vcf_frame = tk.Frame(self.root, bg='#f5f5f5')
        vcf_frame.pack(pady=15, padx=30, fill='x')
        
        tk.Label(
            vcf_frame,
            text="2. VCF输出位置 (可选，默认与Excel同目录):",
            font=("Arial", 12, "bold"),
            bg='#f5f5f5',
            anchor='w'
        ).pack(anchor='w', pady=(0, 5))
        
        vcf_select_frame = tk.Frame(vcf_frame, bg='#f5f5f5')
        vcf_select_frame.pack(fill='x')
        
        self.vcf_entry = tk.Entry(
            vcf_select_frame,
            textvariable=self.vcf_path,
            font=("Arial", 10),
            bg='white',
            fg='#333'
        )
        self.vcf_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        vcf_btn = tk.Button(
            vcf_select_frame,
            text="📁 选择位置",
            command=self.select_vcf_file,
            font=("Arial", 10),
            bg='#2196F3',
            fg='white',
            relief='flat',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        vcf_btn.pack(side='right')
        
        # 转换按钮
        convert_frame = tk.Frame(self.root, bg='#f5f5f5')
        convert_frame.pack(pady=30)
        
        self.convert_btn = tk.Button(
            convert_frame,
            text="🚀 开始转换",
            command=self.convert_file,
            font=("Arial", 14, "bold"),
            bg='#FF6B6B',
            fg='white',
            relief='flat',
            padx=40,
            pady=12,
            cursor='hand2',
            state='disabled'
        )
        self.convert_btn.pack()
        
        # 日志输出区域
        log_frame = tk.Frame(self.root, bg='#f5f5f5')
        log_frame.pack(pady=15, padx=30, fill='both', expand=True)
        
        tk.Label(
            log_frame,
            text="转换日志:",
            font=("Arial", 11, "bold"),
            bg='#f5f5f5',
            anchor='w'
        ).pack(anchor='w', pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Arial", 9),
            bg='white',
            fg='#333',
            wrap=tk.WORD
        )
        self.log_text.pack(fill='both', expand=True)
        
        # 绑定Excel路径变化事件
        self.excel_path.trace('w', self.on_excel_path_change)
    
    def on_excel_path_change(self, *args):
        """Excel文件选择后，启用转换按钮"""
        if self.excel_path.get():
            self.convert_btn.config(state='normal')
        else:
            self.convert_btn.config(state='disabled')
    
    def log(self, message):
        """添加日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def select_excel_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[
                ("Excel文件", "*.xlsx *.xls"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.excel_path.set(file_path)
            # 自动设置VCF输出路径
            if not self.vcf_path.get():
                vcf_path = os.path.splitext(file_path)[0] + ".vcf"
                self.vcf_path.set(vcf_path)
            self.log(f"✅ 已选择Excel文件: {os.path.basename(file_path)}")
    
    def select_vcf_file(self):
        """选择VCF输出位置"""
        file_path = filedialog.asksaveasfilename(
            title="保存VCF文件",
            defaultextension=".vcf",
            filetypes=[
                ("VCF文件", "*.vcf"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.vcf_path.set(file_path)
            self.log(f"✅ 已设置输出位置: {os.path.basename(file_path)}")
    
    def convert_file(self):
        """执行转换"""
        excel_file = self.excel_path.get()
        if not excel_file:
            messagebox.showerror("错误", "请先选择Excel文件！")
            return
        
        if not os.path.exists(excel_file):
            messagebox.showerror("错误", "Excel文件不存在！")
            return
        
        # 获取输出路径
        vcf_file = self.vcf_path.get().strip()
        if not vcf_file:
            vcf_file = None
        
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 禁用按钮
        self.convert_btn.config(state='disabled', text="转换中...")
        self.root.update()
        
        try:
            self.log("=" * 50)
            self.log("开始转换...")
            self.log(f"输入文件: {os.path.basename(excel_file)}")
            
            # 执行转换
            result_path = excel_to_vcf(excel_file, vcf_file if vcf_file else None)
            
            self.log("=" * 50)
            self.log("✅ 转换完成！")
            self.log(f"输出文件: {result_path}")
            
            # 显示成功对话框
            result = messagebox.askyesno(
                "转换成功",
                f"✅ VCF文件已成功生成！\n\n文件位置:\n{result_path}\n\n是否打开文件所在文件夹？"
            )
            
            if result:
                # 打开文件所在文件夹（macOS）
                if sys.platform == "darwin":
                    os.system(f'open "{os.path.dirname(result_path)}"')
                elif sys.platform == "win32":
                    os.system(f'explorer /select,"{result_path}"')
                else:
                    os.system(f'xdg-open "{os.path.dirname(result_path)}"')
            
        except Exception as e:
            self.log("=" * 50)
            self.log(f"❌ 转换失败: {str(e)}")
            messagebox.showerror("转换失败", f"转换过程中出现错误：\n\n{str(e)}")
        finally:
            # 恢复按钮
            self.convert_btn.config(state='normal', text="🚀 开始转换")


def main():
    """主函数"""
    root = tk.Tk()
    app = ExcelToVCFApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

