#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求发现自动化脚本
自动从知乎、V2EX、Product Hunt等平台抓取需求数据
"""

import requests
import json
import csv
import time
from datetime import datetime
from urllib.parse import quote
import os

class DemandDiscoveryBot:
    """需求发现自动化机器人"""
    
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_zhihu(self, keyword, limit=20):
        """
        搜索知乎问题
        
        参数:
            keyword: 搜索关键词
            limit: 最多返回结果数
        
        返回:
            问题列表
        """
        print(f"🔍 正在搜索知乎: {keyword}")
        
        # 知乎搜索API (需要登录才能使用官方API，这里使用模拟方式)
        url = f"https://www.zhihu.com/api/v4/search_v3"
        params = {
            't': 'general',
            'q': keyword,
            'correction': 1,
            'offset': 0,
            'limit': limit
        }
        
        try:
            # 注意: 实际使用需要处理知乎的反爬虫机制
            # 建议使用selenium或者获取知乎API权限
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                questions = []
                
                for item in data.get('data', []):
                    if item.get('type') == 'search_result':
                        obj = item.get('object', {})
                        if obj.get('type') == 'question':
                            questions.append({
                                '平台': '知乎',
                                '标题': obj.get('title', ''),
                                '链接': f"https://www.zhihu.com/question/{obj.get('id', '')}",
                                '关键词': keyword,
                                '热度': obj.get('follower_count', 0),
                                '回答数': obj.get('answer_count', 0),
                                '发现时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                
                print(f"✅ 找到 {len(questions)} 个相关问题")
                return questions
            else:
                print(f"❌ 请求失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索出错: {str(e)}")
            return []
    
    def search_v2ex(self, keyword, limit=20):
        """
        搜索V2EX主题
        
        参数:
            keyword: 搜索关键词
            limit: 最多返回结果数
        
        返回:
            主题列表
        """
        print(f"🔍 正在搜索V2EX: {keyword}")
        
        # V2EX有公开API
        url = "https://www.v2ex.com/api/topics/hot.json"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                topics = []
                
                for item in data[:limit]:
                    # 简单的关键词过滤
                    if keyword.lower() in item.get('title', '').lower() or \
                       keyword.lower() in item.get('content', '').lower():
                        topics.append({
                            '平台': 'V2EX',
                            '标题': item.get('title', ''),
                            '链接': item.get('url', ''),
                            '关键词': keyword,
                            '热度': item.get('replies', 0),
                            '回答数': item.get('replies', 0),
                            '发现时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                
                print(f"✅ 找到 {len(topics)} 个相关主题")
                return topics
            else:
                print(f"❌ 请求失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索出错: {str(e)}")
            return []
    
    def search_producthunt(self, keyword, limit=20):
        """
        搜索Product Hunt产品
        
        参数:
            keyword: 搜索关键词
            limit: 最多返回结果数
        
        返回:
            产品列表
        """
        print(f"🔍 正在搜索Product Hunt: {keyword}")
        
        # Product Hunt需要API token
        # 这里提供基本框架，实际使用需要申请API key
        url = "https://api.producthunt.com/v2/api/graphql"
        
        # 注意: 需要在https://api.producthunt.com/v2/oauth/applications申请token
        headers = {
            'Authorization': 'Bearer YOUR_API_TOKEN_HERE',
            'Content-Type': 'application/json'
        }
        
        query = """
        query {
            posts(first: %d, postedAfter: "2024-01-01") {
                edges {
                    node {
                        name
                        tagline
                        url
                        votesCount
                        commentsCount
                    }
                }
            }
        }
        """ % limit
        
        try:
            # 实际使用需要有效的API token
            print("⚠️  Product Hunt需要API token，请参考文档配置")
            return []
            
        except Exception as e:
            print(f"❌ 搜索出错: {str(e)}")
            return []
    
    def search_google_trends(self, keyword):
        """
        获取Google Trends数据
        
        参数:
            keyword: 搜索关键词
        
        返回:
            趋势数据
        """
        print(f"🔍 正在查询Google Trends: {keyword}")
        
        # 使用pytrends库
        try:
            from pytrends.request import TrendReq
            
            pytrends = TrendReq(hl='zh-CN', tz=480)
            pytrends.build_payload([keyword], timeframe='today 3-m')
            
            # 获取兴趣度数据
            interest = pytrends.interest_over_time()
            
            if not interest.empty:
                avg_interest = interest[keyword].mean()
                print(f"✅ 平均搜索热度: {avg_interest:.1f}")
                return {
                    '关键词': keyword,
                    '平均热度': round(avg_interest, 1),
                    '最高热度': interest[keyword].max(),
                    '最低热度': interest[keyword].min()
                }
            else:
                print("❌ 未找到趋势数据")
                return None
                
        except ImportError:
            print("⚠️  需要安装pytrends: pip install pytrends")
            return None
        except Exception as e:
            print(f"❌ 查询出错: {str(e)}")
            return None
    
    def save_to_csv(self, filename='需求发现结果.csv'):
        """
        保存结果到CSV文件
        
        参数:
            filename: 文件名
        """
        if not self.results:
            print("⚠️  没有数据可保存")
            return
        
        print(f"💾 正在保存到 {filename}")
        
        # 确保所有记录有相同的键
        keys = set()
        for item in self.results:
            keys.update(item.keys())
        keys = sorted(keys)
        
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)
        
        print(f"✅ 已保存 {len(self.results)} 条记录")
    
    def save_to_excel(self, filename='需求发现结果.xlsx'):
        """
        保存结果到Excel文件
        
        参数:
            filename: 文件名
        """
        try:
            import pandas as pd
            
            if not self.results:
                print("⚠️  没有数据可保存")
                return
            
            print(f"💾 正在保存到 {filename}")
            
            df = pd.DataFrame(self.results)
            df.to_excel(filename, index=False, engine='openpyxl')
            
            print(f"✅ 已保存 {len(self.results)} 条记录")
            
        except ImportError:
            print("⚠️  需要安装pandas和openpyxl: pip install pandas openpyxl")
            print("💡 将使用CSV格式保存")
            self.save_to_csv(filename.replace('.xlsx', '.csv'))
        except Exception as e:
            print(f"❌ 保存出错: {str(e)}")
    
    def run_batch_search(self, keywords, platforms=['zhihu', 'v2ex']):
        """
        批量搜索多个关键词
        
        参数:
            keywords: 关键词列表
            platforms: 平台列表
        """
        print(f"🚀 开始批量搜索 {len(keywords)} 个关键词")
        print(f"📋 平台: {', '.join(platforms)}")
        print("="*50)
        
        for i, keyword in enumerate(keywords, 1):
            print(f"\n[{i}/{len(keywords)}] 搜索关键词: {keyword}")
            print("-"*50)
            
            if 'zhihu' in platforms:
                results = self.search_zhihu(keyword, limit=10)
                self.results.extend(results)
                time.sleep(2)  # 避免请求过快
            
            if 'v2ex' in platforms:
                results = self.search_v2ex(keyword, limit=10)
                self.results.extend(results)
                time.sleep(2)
            
            if 'producthunt' in platforms:
                results = self.search_producthunt(keyword, limit=10)
                self.results.extend(results)
                time.sleep(2)
        
        print("\n" + "="*50)
        print(f"✅ 搜索完成！共找到 {len(self.results)} 条需求")
        
        return self.results


def main():
    """主函数"""
    print("=" * 60)
    print("需求发现自动化脚本 v1.0")
    print("自动从多个平台搜索产品需求")
    print("=" * 60)
    print()
    
    # 创建机器人实例
    bot = DemandDiscoveryBot()
    
    # 定义搜索关键词（可以自定义）
    keywords = [
        "有什么好用的工具",
        "效率工具推荐",
        "在线工具",
        "免费工具",
        "开发工具",
        "设计工具",
        "数据处理工具",
        "文件转换工具"
    ]
    
    # 让用户选择搜索模式
    print("请选择搜索模式：")
    print("1. 快速模式（仅搜索V2EX，最快）")
    print("2. 标准模式（搜索知乎+V2EX，推荐）")
    print("3. 完整模式（搜索所有平台，需要API配置）")
    print()
    
    choice = input("请输入选择 (1/2/3，默认2): ").strip() or '2'
    
    if choice == '1':
        platforms = ['v2ex']
    elif choice == '3':
        platforms = ['zhihu', 'v2ex', 'producthunt']
    else:
        platforms = ['zhihu', 'v2ex']
    
    print()
    
    # 让用户选择是否自定义关键词
    custom = input("是否使用自定义关键词？(y/n，默认n): ").strip().lower()
    
    if custom == 'y':
        print("请输入关键词（多个关键词用逗号分隔）：")
        custom_keywords = input().strip()
        if custom_keywords:
            keywords = [k.strip() for k in custom_keywords.split(',')]
    
    print()
    print(f"将搜索以下关键词: {', '.join(keywords[:3])}{'...' if len(keywords) > 3 else ''}")
    print()
    
    # 开始搜索
    results = bot.run_batch_search(keywords, platforms=platforms)
    
    # 保存结果
    if results:
        print()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'需求发现结果_{timestamp}.xlsx'
        bot.save_to_excel(filename)
        
        print()
        print("=" * 60)
        print(f"🎉 完成！结果已保存到: {filename}")
        print(f"📊 共发现 {len(results)} 条需求")
        print()
        print("💡 下一步：")
        print("  1. 打开Excel文件查看结果")
        print("  2. 筛选高热度的需求（热度>50）")
        print("  3. 使用Google Trends验证搜索量")
        print("  4. 使用RICE模型评分")
        print("=" * 60)
    else:
        print()
        print("⚠️  未找到任何需求，建议：")
        print("  1. 检查网络连接")
        print("  2. 更换关键词重试")
        print("  3. 尝试快速模式（V2EX）")


if __name__ == '__main__':
    main()
