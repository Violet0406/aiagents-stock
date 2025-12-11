"""
行业深度分析数据获取模块
使用akshare数据源
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


class IndustryAnalysisDataFetcher:
    """行业数据获取类"""
    
    def __init__(self):
        pass
    
    def _normalize_industry_name(self, industry_name):
        """
        规范化行业名称，支持模糊匹配
        
        Args:
            industry_name: 用户输入的行业名称
            
        Returns:
            str: 规范化的行业名称，如果找不到则返回None
        """
        try:
            # 获取所有行业列表
            industry_list_df = ak.stock_board_industry_name_em()
            
            if industry_list_df is None or industry_list_df.empty:
                return None
            
            # 精确匹配
            exact_match = industry_list_df[industry_list_df['板块名称'] == industry_name]
            if not exact_match.empty:
                return industry_name
            
            # 模糊匹配（包含关系）
            fuzzy_match = industry_list_df[industry_list_df['板块名称'].str.contains(industry_name, na=False)]
            if not fuzzy_match.empty:
                matched_name = fuzzy_match.iloc[0]['板块名称']
                print(f"✅ 模糊匹配成功：'{industry_name}' → '{matched_name}'")
                return matched_name
            
            return None
            
        except Exception as e:
            print(f"⚠️ 规范化行业名称失败: {e}")
            return None
    
    def get_industry_quotes(self, industry_name):
        """
        获取指定行业的板块行情
        
        Args:
            industry_name: 行业名称
            
        Returns:
            dict: 行业行情数据
        """
        # 规范化行业名称
        normalized_name = self._normalize_industry_name(industry_name)
        if not normalized_name:
            return {
                'error': f'未找到行业 "{industry_name}"，请检查行业名称是否正确',
                'data_success': False
            }
        
        try:
            industry_data = {
                'industry_name': normalized_name,
                'original_name': industry_name,
                'latest_price': 'N/A',
                'change_percent': 'N/A',
                'change_amount': 'N/A',
                'volume': 'N/A',
                'amount': 'N/A',
                'amplitude': 'N/A',
                'leading_stocks': [],
                'data_success': False
            }
            
            # 获取行业板块行情
            try:
                industry_spot_df = ak.stock_board_industry_name_em()
                
                if industry_spot_df is not None and not industry_spot_df.empty:
                    industry_row = industry_spot_df[industry_spot_df['板块名称'] == normalized_name]
                    
                    if not industry_row.empty:
                        row = industry_row.iloc[0]
                        industry_data['latest_price'] = row.get('最新价', 'N/A')
                        industry_data['change_percent'] = row.get('涨跌幅', 'N/A')
                        industry_data['change_amount'] = row.get('涨跌额', 'N/A')
                        industry_data['volume'] = row.get('成交量', 'N/A')
                        industry_data['amount'] = row.get('成交额', 'N/A')
                        industry_data['amplitude'] = row.get('振幅', 'N/A')
                        industry_data['leading_stock'] = row.get('领涨股票', 'N/A')
                        industry_data['leading_change'] = row.get('领涨股票涨跌幅', 'N/A')
                        industry_data['data_success'] = True
                        
                        print(f"✅ 成功获取行业 '{normalized_name}' 的行情数据")
            except Exception as e:
                print(f"⚠️ 获取行业行情失败: {e}")
                industry_data['error'] = str(e)
            
            return industry_data
            
        except Exception as e:
            return {
                'error': f'获取行业行情失败: {str(e)}',
                'data_success': False
            }
    
    def get_industry_constituents(self, industry_name):
        """
        获取行业内所有成分股列表
        
        Args:
            industry_name: 行业名称
            
        Returns:
            dict: 成分股数据
        """
        # 规范化行业名称
        normalized_name = self._normalize_industry_name(industry_name)
        if not normalized_name:
            return {
                'error': f'未找到行业 "{industry_name}"',
                'data_success': False
            }
        
        try:
            constituents_data = {
                'industry_name': normalized_name,
                'constituents': [],
                'count': 0,
                'data_success': False
            }
            
            # 获取行业成分股
            try:
                constituents_df = ak.stock_board_industry_cons_em(symbol=normalized_name)
                
                if constituents_df is not None and not constituents_df.empty:
                    # 转换为字典列表
                    constituents_list = []
                    for _, row in constituents_df.iterrows():
                        stock = {
                            'code': row.get('代码', 'N/A'),
                            'name': row.get('名称', 'N/A'),
                            'price': row.get('最新价', 'N/A'),
                            'change_percent': row.get('涨跌幅', 'N/A'),
                            'change_amount': row.get('涨跌额', 'N/A'),
                            'volume': row.get('成交量', 'N/A'),
                            'amount': row.get('成交额', 'N/A'),
                            'amplitude': row.get('振幅', 'N/A'),
                            'turnover_rate': row.get('换手率', 'N/A'),
                            'pe_ratio': row.get('市盈率', 'N/A'),
                            'market_cap': row.get('总市值', 'N/A')
                        }
                        constituents_list.append(stock)
                    
                    constituents_data['constituents'] = constituents_list
                    constituents_data['count'] = len(constituents_list)
                    constituents_data['data_success'] = True
                    
                    print(f"✅ 成功获取行业 '{normalized_name}' 的 {len(constituents_list)} 只成分股")
            except Exception as e:
                print(f"⚠️ 获取行业成分股失败: {e}")
                constituents_data['error'] = str(e)
            
            return constituents_data
            
        except Exception as e:
            return {
                'error': f'获取行业成分股失败: {str(e)}',
                'data_success': False
            }
    
    def get_industry_capital_flow(self, industry_name):
        """
        获取行业资金流向数据
        
        Args:
            industry_name: 行业名称
            
        Returns:
            dict: 资金流向数据
        """
        # 规范化行业名称
        normalized_name = self._normalize_industry_name(industry_name)
        if not normalized_name:
            return {
                'error': f'未找到行业 "{industry_name}"',
                'data_success': False
            }
        
        try:
            capital_data = {
                'industry_name': normalized_name,
                'main_net_inflow': 'N/A',
                'main_net_inflow_ratio': 'N/A',
                'super_large_net_inflow': 'N/A',
                'large_net_inflow': 'N/A',
                'medium_net_inflow': 'N/A',
                'small_net_inflow': 'N/A',
                'data_success': False
            }
            
            # 获取行业资金流向
            try:
                # 使用板块资金流接口
                capital_df = ak.stock_board_industry_name_em()
                
                if capital_df is not None and not capital_df.empty:
                    industry_row = capital_df[capital_df['板块名称'] == normalized_name]
                    
                    if not industry_row.empty:
                        row = industry_row.iloc[0]
                        
                        # 从行情数据中提取资金相关信息（如果有）
                        # 注意：akshare的行业接口可能不包含详细资金流向
                        # 这里主要获取成交额作为资金活跃度参考
                        capital_data['amount'] = row.get('成交额', 'N/A')
                        capital_data['data_success'] = True
                        
                        print(f"✅ 获取行业 '{normalized_name}' 的资金数据")
            except Exception as e:
                print(f"⚠️ 获取行业资金流向失败: {e}")
                capital_data['error'] = str(e)
            
            return capital_data
            
        except Exception as e:
            return {
                'error': f'获取行业资金流向失败: {str(e)}',
                'data_success': False
            }
    
    def get_industry_valuation(self, constituents_data):
        """
        计算行业估值水平（平均市盈率、市净率）
        
        Args:
            constituents_data: 成分股数据
            
        Returns:
            dict: 估值数据
        """
        if not constituents_data.get('data_success'):
            return {
                'error': '无成分股数据',
                'data_success': False
            }
        
        try:
            valuation_data = {
                'industry_name': constituents_data.get('industry_name'),
                'avg_pe': 'N/A',
                'median_pe': 'N/A',
                'avg_pb': 'N/A',
                'median_pb': 'N/A',
                'avg_market_cap': 'N/A',
                'data_success': False
            }
            
            constituents = constituents_data.get('constituents', [])
            if not constituents:
                return valuation_data
            
            # 提取市盈率数据
            pe_values = []
            pb_values = []
            market_cap_values = []
            
            for stock in constituents:
                # 市盈率
                pe = stock.get('pe_ratio', 'N/A')
                if pe != 'N/A' and pe is not None:
                    try:
                        pe_float = float(pe)
                        if 0 < pe_float < 1000:  # 过滤异常值
                            pe_values.append(pe_float)
                    except (ValueError, TypeError):
                        pass
                
                # 市值
                market_cap = stock.get('market_cap', 'N/A')
                if market_cap != 'N/A' and market_cap is not None:
                    try:
                        market_cap_values.append(float(market_cap))
                    except (ValueError, TypeError):
                        pass
            
            # 计算平均值和中位数
            if pe_values:
                valuation_data['avg_pe'] = round(np.mean(pe_values), 2)
                valuation_data['median_pe'] = round(np.median(pe_values), 2)
            
            if market_cap_values:
                valuation_data['avg_market_cap'] = round(np.mean(market_cap_values), 2)
            
            valuation_data['data_success'] = True
            print(f"✅ 计算行业估值：平均市盈率 {valuation_data['avg_pe']}")
            
            return valuation_data
            
        except Exception as e:
            return {
                'error': f'计算行业估值失败: {str(e)}',
                'data_success': False
            }
    
    def get_industry_leading_stocks(self, constituents_data, top_n=10):
        """
        筛选行业龙头股票（市值排名Top N）
        
        Args:
            constituents_data: 成分股数据
            top_n: 返回前N只龙头股
            
        Returns:
            dict: 龙头股数据
        """
        if not constituents_data.get('data_success'):
            return {
                'error': '无成分股数据',
                'data_success': False
            }
        
        try:
            leading_data = {
                'industry_name': constituents_data.get('industry_name'),
                'leading_stocks': [],
                'count': 0,
                'data_success': False
            }
            
            constituents = constituents_data.get('constituents', [])
            if not constituents:
                return leading_data
            
            # 按市值排序
            sorted_stocks = []
            for stock in constituents:
                market_cap = stock.get('market_cap', 0)
                if market_cap != 'N/A' and market_cap is not None:
                    try:
                        stock['market_cap_float'] = float(market_cap)
                        sorted_stocks.append(stock)
                    except (ValueError, TypeError):
                        pass
            
            # 按市值降序排序
            sorted_stocks.sort(key=lambda x: x.get('market_cap_float', 0), reverse=True)
            
            # 取前N只
            leading_stocks = sorted_stocks[:top_n]
            
            # 移除临时字段
            for stock in leading_stocks:
                if 'market_cap_float' in stock:
                    del stock['market_cap_float']
            
            leading_data['leading_stocks'] = leading_stocks
            leading_data['count'] = len(leading_stocks)
            leading_data['data_success'] = True
            
            print(f"✅ 筛选出 {len(leading_stocks)} 只龙头股")
            
            return leading_data
            
        except Exception as e:
            return {
                'error': f'筛选龙头股失败: {str(e)}',
                'data_success': False
            }
    
    def format_industry_quotes_for_ai(self, industry_data):
        """格式化行业行情供AI分析使用"""
        if not industry_data.get('data_success'):
            return "未能获取行业行情数据"
        
        text = f"""
行业行情数据：
- 行业名称：{industry_data.get('industry_name', 'N/A')}
- 最新指数：{industry_data.get('latest_price', 'N/A')}
- 涨跌幅：{industry_data.get('change_percent', 'N/A')}%
- 涨跌额：{industry_data.get('change_amount', 'N/A')}
- 成交量：{industry_data.get('volume', 'N/A')}
- 成交额：{industry_data.get('amount', 'N/A')}
- 振幅：{industry_data.get('amplitude', 'N/A')}%
- 领涨股票：{industry_data.get('leading_stock', 'N/A')} (涨跌幅: {industry_data.get('leading_change', 'N/A')}%)
"""
        return text.strip()
    
    def format_industry_constituents_for_ai(self, constituents_data, top_n=20):
        """格式化成分股数据供AI分析使用"""
        if not constituents_data.get('data_success'):
            return "未能获取成分股数据"
        
        constituents = constituents_data.get('constituents', [])
        total_count = len(constituents)
        display_count = min(top_n, total_count)
        
        text = f"行业成分股（共{total_count}只，显示前{display_count}只）：\n"
        
        for i, stock in enumerate(constituents[:display_count], 1):
            text += f"\n{i}. {stock.get('name', 'N/A')} ({stock.get('code', 'N/A')})\n"
            text += f"   价格: {stock.get('price', 'N/A')} | "
            text += f"涨跌幅: {stock.get('change_percent', 'N/A')}% | "
            text += f"市值: {stock.get('market_cap', 'N/A')}\n"
        
        return text.strip()
    
    def format_leading_stocks_for_ai(self, leading_data):
        """格式化龙头股数据供AI分析使用"""
        if not leading_data.get('data_success'):
            return "未能获取龙头股数据"
        
        leading_stocks = leading_data.get('leading_stocks', [])
        if not leading_stocks:
            return "无龙头股数据"
        
        text = f"行业龙头股票（按市值排名Top {len(leading_stocks)}）：\n"
        
        for i, stock in enumerate(leading_stocks, 1):
            text += f"\n{i}. {stock.get('name', 'N/A')} ({stock.get('code', 'N/A')})\n"
            text += f"   市值: {stock.get('market_cap', 'N/A')} 元\n"
            text += f"   最新价: {stock.get('price', 'N/A')} 元\n"
            text += f"   涨跌幅: {stock.get('change_percent', 'N/A')}%\n"
            text += f"   换手率: {stock.get('turnover_rate', 'N/A')}%\n"
            text += f"   市盈率: {stock.get('pe_ratio', 'N/A')}\n"
        
        return text.strip()
