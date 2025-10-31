#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel转VCF工具
将Excel文件中的联系人信息转换为VCF格式，以便导入iOS通讯录
"""

import pandas as pd
import sys
import os
from pathlib import Path


def excel_to_vcf(excel_path, vcf_path=None, sheet_name=0):
    """
    将Excel文件转换为VCF格式
    
    参数:
        excel_path: Excel文件路径
        vcf_path: 输出VCF文件路径（如果为None，则使用Excel文件名）
        sheet_name: Excel工作表名称或索引（默认为0，即第一个工作表）
    
    返回:
        生成的VCF文件路径
    """
    # 检查Excel文件是否存在
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel文件不存在: {excel_path}")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        raise Exception(f"读取Excel文件失败: {str(e)}")
    
    if df.empty:
        raise ValueError("Excel文件为空")
    
    # 如果没有指定输出路径，使用Excel文件名
    if vcf_path is None:
        excel_name = Path(excel_path).stem
        vcf_path = os.path.join(os.path.dirname(excel_path), f"{excel_name}.vcf")
    
    # 列名映射（支持中文和英文列名）
    column_mapping = {
        'name': ['姓名', 'name', '名字', 'Name', 'NAME', '联系人', '名字', 'Full Name'],
        'phone': ['电话', 'phone', '手机', 'Phone', 'PHONE', '电话号', '手机号', '移动电话', 'Tel', 'TEL'],
        'mobile': ['手机', 'mobile', 'Mobile', 'MOBILE', '手机号', '移动电话', '手机号码'],
        'email': ['邮箱', 'email', 'Email', 'EMAIL', '邮件', '电子邮箱', 'Mail'],
        'company': ['公司', 'company', 'Company', 'COMPANY', '单位', '工作单位'],
        'title': ['职位', 'title', 'Title', 'TITLE', '职务', '职称'],
        'address': ['地址', 'address', 'Address', 'ADDRESS', '住址'],
        'note': ['备注', 'note', 'Note', 'NOTE', '说明', '注释']
    }
    
    # 查找对应的列
    def find_column(df, possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    name_col = find_column(df, column_mapping['name'])
    phone_col = find_column(df, column_mapping['phone'])
    mobile_col = find_column(df, column_mapping['mobile'])
    email_col = find_column(df, column_mapping['email'])
    company_col = find_column(df, column_mapping['company'])
    title_col = find_column(df, column_mapping['title'])
    address_col = find_column(df, column_mapping['address'])
    note_col = find_column(df, column_mapping['note'])
    
    # 如果找不到姓名列，使用第一列
    if name_col is None:
        if len(df.columns) > 0:
            name_col = df.columns[0]
            print(f"警告: 未找到姓名列，使用第一列 '{name_col}' 作为姓名")
        else:
            raise ValueError("Excel文件中没有找到有效的姓名列")
    
    # 生成VCF内容
    vcf_lines = []
    
    for index, row in df.iterrows():
        # 获取姓名
        name = str(row[name_col]).strip() if pd.notna(row[name_col]) else ""
        if not name or name.lower() in ['nan', 'none', '']:
            continue
        
        # 开始一个VCard
        vcf_lines.append("BEGIN:VCARD")
        vcf_lines.append("VERSION:3.0")
        
        # 处理姓名（N字段：姓;名;;;）
        name_parts = name.split()
        if len(name_parts) >= 2:
            last_name = name_parts[0]
            first_name = " ".join(name_parts[1:])
            vcf_lines.append(f"N:{last_name};{first_name};;;")
        else:
            vcf_lines.append(f"N:;{name};;;")
        
        # FN字段（全名）
        vcf_lines.append(f"FN:{name}")
        
        # 电话号码
        phone_used = False
        if phone_col and pd.notna(row[phone_col]):
            phone = str(row[phone_col]).strip()
            if phone and phone.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"TEL;TYPE=WORK,VOICE:{phone}")
                phone_used = True
        
        if mobile_col and pd.notna(row[mobile_col]) and not phone_used:
            mobile = str(row[mobile_col]).strip()
            if mobile and mobile.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"TEL;TYPE=CELL:{mobile}")
        
        # 邮箱
        if email_col and pd.notna(row[email_col]):
            email = str(row[email_col]).strip()
            if email and email.lower() not in ['nan', 'none', ''] and '@' in email:
                vcf_lines.append(f"EMAIL;TYPE=INTERNET:{email}")
        
        # 公司
        if company_col and pd.notna(row[company_col]):
            company = str(row[company_col]).strip()
            if company and company.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"ORG:{company}")
        
        # 职位
        if title_col and pd.notna(row[title_col]):
            title = str(row[title_col]).strip()
            if title and title.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"TITLE:{title}")
        
        # 地址
        if address_col and pd.notna(row[address_col]):
            address = str(row[address_col]).strip()
            if address and address.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"ADR;TYPE=HOME:;;{address};;;;")
        
        # 备注
        if note_col and pd.notna(row[note_col]):
            note = str(row[note_col]).strip()
            if note and note.lower() not in ['nan', 'none', '']:
                vcf_lines.append(f"NOTE:{note}")
        
        # 结束VCard
        vcf_lines.append("END:VCARD")
        vcf_lines.append("")  # 空行分隔
    
    # 写入VCF文件
    try:
        with open(vcf_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(vcf_lines))
        print(f"✅ 成功生成VCF文件: {vcf_path}")
        print(f"   共转换 {len([line for line in vcf_lines if line == 'BEGIN:VCARD'])} 个联系人")
        return vcf_path
    except Exception as e:
        raise Exception(f"写入VCF文件失败: {str(e)}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python excel_to_vcf.py <Excel文件路径> [输出VCF文件路径]")
        print("\n示例:")
        print("  python excel_to_vcf.py contacts.xlsx")
        print("  python excel_to_vcf.py contacts.xlsx output.vcf")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    vcf_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        excel_to_vcf(excel_path, vcf_path)
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

