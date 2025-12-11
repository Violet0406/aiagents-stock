"""
ETF基金数据获取模块
使用akshare数据源
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


class ETFDataFetcher:
    """ETF数据获取类"""
    
    def __init__(self):
        pass
    
    def _is_etf_code(self, symbol):
        """
        判断是否为ETF代码
        沪深ETF通常是6位数字
        沪市：51xxxx, 56xxxx
        深市：15xxxx, 16xxxx
        """
        if not isinstance(symbol, str):
            symbol = str(symbol)
        
        # 移除可能的空格
        symbol = symbol.strip()
        
        # 判断是否为6位数字
        if symbol.isdigit() and len(symbol) == 6:
            # 判断是否以51, 56, 15, 16开头
            return symbol.startswith(('51', '56', '15', '16'))
        
        return False
    
    def get_etf_info(self, symbol):
        """
        获取ETF基本信息
        
        Returns:
            dict: ETF基本信息
        """
        if not self._is_etf_code(symbol):
            return {
                'error': f'代码 {symbol} 不是有效的ETF代码',
                'data_success': False
            }
        
        try:
            etf_info = {
                'symbol': symbol,
                'name': '未知',
                'current_price': 'N/A',
                'change_percent': 'N/A',
                'volume': 'N/A',
                'amount': 'N/A',
                'fund_size': 'N/A',
                'tracking_index': 'N/A',
                'management_fee': 'N/A',
                'custodian_fee': 'N/A',
                'premium_rate': 'N/A',
                'data_success': True
            }
            
            # 1. 获取ETF实时行情
            try:
                etf_spot_df = ak.fund_etf_spot_em()
                if etf_spot_df is not None and not etf_spot_df.empty:
                    etf_row = etf_spot_df[etf_spot_df['代码'] == symbol]
                    if not etf_row.empty:
                        row = etf_row.iloc[0]
                        etf_info['name'] = row.get('名称', '未知')
                        etf_info['current_price'] = row.get('最新价', 'N/A')
                        etf_info['change_percent'] = row.get('涨跌幅', 'N/A')
                        etf_info['volume'] = row.get('成交量', 'N/A')
                        etf_info['amount'] = row.get('成交额', 'N/A')
                        print(f"✅ 成功获取ETF {symbol} 实时行情")
            except Exception as e:
                print(f"⚠️ 获取ETF实时行情失败: {e}")
            
            # 2. 获取ETF基金信息（规模、费率等）
            try:
                fund_info_df = ak.fund_etf_fund_info_em(fund=symbol, indicator="基金信息")
                if fund_info_df is not None and not fund_info_df.empty:
                    for _, row in fund_info_df.iterrows():
                        item = row.get('item', '')
                        value = row.get('value', 'N/A')
                        
                        if '基金规模' in item or '资产规模' in item:
                            etf_info['fund_size'] = value
                        elif '跟踪指数' in item or '标的指数' in item:
                            etf_info['tracking_index'] = value
                        elif '管理费率' in item:
                            etf_info['management_fee'] = value
                        elif '托管费率' in item:
                            etf_info['custodian_fee'] = value
                    
                    print(f"✅ 成功获取ETF {symbol} 基金信息")
            except Exception as e:
                print(f"⚠️ 获取ETF基金信息失败: {e}")
            
            # 3. 计算溢价率
            try:
                # 获取ETF净值数据
                fund_daily_df = ak.fund_etf_fund_daily_em(fund=symbol)
                if fund_daily_df is not None and not fund_daily_df.empty:
                    latest_data = fund_daily_df.iloc[-1]
                    unit_nav = latest_data.get('单位净值', None)
                    
                    if unit_nav is not None and etf_info['current_price'] != 'N/A':
                        try:
                            current_price = float(etf_info['current_price'])
                            unit_nav = float(unit_nav)
                            
                            # 溢价率 = (市价 - 净值) / 净值 * 100
                            premium_rate = ((current_price - unit_nav) / unit_nav) * 100
                            etf_info['premium_rate'] = f"{premium_rate:.2f}%"
                            print(f"✅ 计算溢价率: {etf_info['premium_rate']}")
                        except (ValueError, TypeError, ZeroDivisionError):
                            pass
            except Exception as e:
                print(f"⚠️ 计算溢价率失败: {e}")
            
            return etf_info
            
        except Exception as e:
            return {
                'error': f'获取ETF信息失败: {str(e)}',
                'data_success': False
            }
    
    def get_etf_hist_data(self, symbol, period="1y"):
        """
        获取ETF历史行情数据
        
        Args:
            symbol: ETF代码
            period: 时间周期 (1y, 6mo, 3mo, 1mo)
            
        Returns:
            DataFrame: 历史行情数据
        """
        if not self._is_etf_code(symbol):
            return {'error': f'代码 {symbol} 不是有效的ETF代码'}
        
        try:
            # 计算日期范围
            end_date = datetime.now().strftime('%Y%m%d')
            if period == "1y":
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            elif period == "6mo":
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
            elif period == "3mo":
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
            elif period == "1mo":
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            else:
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
            # 获取ETF历史数据
            df = ak.fund_etf_hist_em(
                symbol=symbol,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="qfq"
            )
            
            if df is not None and not df.empty:
                # 标准化列名
                df = df.rename(columns={
                    '日期': 'Date',
                    '开盘': 'Open',
                    '收盘': 'Close',
                    '最高': 'High',
                    '最低': 'Low',
                    '成交量': 'Volume',
                    '成交额': 'Amount'
                })
                
                # 设置日期索引
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                
                print(f"✅ 成功获取ETF {symbol} 历史数据，共 {len(df)} 条记录")
                return df
            else:
                return {'error': '无法获取ETF历史数据'}
                
        except Exception as e:
            return {'error': f'获取ETF历史数据失败: {str(e)}'}
    
    def get_etf_holdings(self, symbol, top_n=10):
        """
        获取ETF持仓结构（十大持仓股票）
        
        Args:
            symbol: ETF代码
            top_n: 返回前N大持仓，默认10
            
        Returns:
            dict: 持仓数据
        """
        if not self._is_etf_code(symbol):
            return {
                'error': f'代码 {symbol} 不是有效的ETF代码',
                'data_success': False
            }
        
        try:
            holdings_data = {
                'symbol': symbol,
                'holdings': [],
                'data_success': False
            }
            
            # 获取ETF持仓数据
            try:
                holdings_df = ak.fund_etf_fund_info_em(fund=symbol, indicator="持仓信息")
                
                if holdings_df is not None and not holdings_df.empty:
                    # 限制返回数量
                    holdings_df = holdings_df.head(top_n)
                    
                    # 转换为字典列表
                    holdings_list = []
                    for _, row in holdings_df.iterrows():
                        holding = {
                            'stock_code': row.get('股票代码', 'N/A'),
                            'stock_name': row.get('股票名称', 'N/A'),
                            'holding_ratio': row.get('持仓占比', 'N/A'),
                            'holding_shares': row.get('持仓股数', 'N/A'),
                            'market_value': row.get('持仓市值', 'N/A')
                        }
                        holdings_list.append(holding)
                    
                    holdings_data['holdings'] = holdings_list
                    holdings_data['data_success'] = True
                    holdings_data['count'] = len(holdings_list)
                    
                    print(f"✅ 成功获取ETF {symbol} 的 {len(holdings_list)} 个持仓")
                else:
                    holdings_data['error'] = '未获取到持仓数据'
                    
            except Exception as e:
                print(f"⚠️ 获取ETF持仓失败: {e}")
                holdings_data['error'] = str(e)
            
            return holdings_data
            
        except Exception as e:
            return {
                'error': f'获取ETF持仓失败: {str(e)}',
                'data_success': False
            }
    
    def get_etf_sector_allocation(self, symbol):
        """
        获取ETF行业配置分布
        
        Args:
            symbol: ETF代码
            
        Returns:
            dict: 行业配置数据
        """
        if not self._is_etf_code(symbol):
            return {
                'error': f'代码 {symbol} 不是有效的ETF代码',
                'data_success': False
            }
        
        try:
            sector_data = {
                'symbol': symbol,
                'sectors': [],
                'data_success': False
            }
            
            # 获取ETF行业配置
            try:
                sector_df = ak.fund_etf_fund_info_em(fund=symbol, indicator="行业配置")
                
                if sector_df is not None and not sector_df.empty:
                    # 转换为字典列表
                    sectors_list = []
                    for _, row in sector_df.iterrows():
                        sector = {
                            'sector_name': row.get('行业类别', row.get('行业', 'N/A')),
                            'allocation_ratio': row.get('占比', row.get('配置比例', 'N/A')),
                            'market_value': row.get('市值', 'N/A')
                        }
                        sectors_list.append(sector)
                    
                    sector_data['sectors'] = sectors_list
                    sector_data['data_success'] = True
                    sector_data['count'] = len(sectors_list)
                    
                    print(f"✅ 成功获取ETF {symbol} 的 {len(sectors_list)} 个行业配置")
                else:
                    sector_data['error'] = '未获取到行业配置数据'
                    
            except Exception as e:
                print(f"⚠️ 获取ETF行业配置失败: {e}")
                sector_data['error'] = str(e)
            
            return sector_data
            
        except Exception as e:
            return {
                'error': f'获取ETF行业配置失败: {str(e)}',
                'data_success': False
            }
    
    def format_etf_info_for_ai(self, etf_info):
        """格式化ETF基本信息供AI分析使用"""
        if not etf_info.get('data_success'):
            return "未能获取ETF基本信息"
        
        text = f"""
ETF基本信息：
- ETF名称：{etf_info.get('name', 'N/A')}
- ETF代码：{etf_info.get('symbol', 'N/A')}
- 当前价格：{etf_info.get('current_price', 'N/A')} 元
- 涨跌幅：{etf_info.get('change_percent', 'N/A')}%
- 成交量：{etf_info.get('volume', 'N/A')}
- 成交额：{etf_info.get('amount', 'N/A')}
- 基金规模：{etf_info.get('fund_size', 'N/A')}
- 跟踪指数：{etf_info.get('tracking_index', 'N/A')}
- 管理费率：{etf_info.get('management_fee', 'N/A')}
- 托管费率：{etf_info.get('custodian_fee', 'N/A')}
- 溢价率：{etf_info.get('premium_rate', 'N/A')}
"""
        return text.strip()
    
    def format_etf_holdings_for_ai(self, holdings_data):
        """格式化ETF持仓信息供AI分析使用"""
        if not holdings_data.get('data_success'):
            return "未能获取ETF持仓信息"
        
        holdings_list = holdings_data.get('holdings', [])
        if not holdings_list:
            return "无持仓数据"
        
        text = f"ETF十大持仓股票（共{len(holdings_list)}只）：\n"
        for i, holding in enumerate(holdings_list, 1):
            text += f"\n{i}. {holding.get('stock_name', 'N/A')} ({holding.get('stock_code', 'N/A')})\n"
            text += f"   - 持仓占比：{holding.get('holding_ratio', 'N/A')}\n"
            text += f"   - 持仓股数：{holding.get('holding_shares', 'N/A')}\n"
            text += f"   - 持仓市值：{holding.get('market_value', 'N/A')}\n"
        
        return text.strip()
    
    def format_etf_sector_for_ai(self, sector_data):
        """格式化ETF行业配置供AI分析使用"""
        if not sector_data.get('data_success'):
            return "未能获取ETF行业配置信息"
        
        sectors_list = sector_data.get('sectors', [])
        if not sectors_list:
            return "无行业配置数据"
        
        text = f"ETF行业配置（共{len(sectors_list)}个行业）：\n"
        for i, sector in enumerate(sectors_list, 1):
            text += f"\n{i}. {sector.get('sector_name', 'N/A')}\n"
            text += f"   - 配置比例：{sector.get('allocation_ratio', 'N/A')}\n"
            if sector.get('market_value') != 'N/A':
                text += f"   - 配置市值：{sector.get('market_value', 'N/A')}\n"
        
        return text.strip()
