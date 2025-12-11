"""
ETF专属AI分析师团队
"""

from deepseek_client import DeepSeekClient
from typing import Dict, Any
import time
import re
import json


class ETFAnalysisAgents:
    """ETF分析AI智能体集合"""
    
    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.deepseek_client = DeepSeekClient(model=model)
    
    def etf_technical_analyst(self, etf_info: Dict, etf_data: Any, indicators: Dict) -> Dict[str, Any]:
        """ETF技术分析师：走势、指标、交易信号"""
        print("🔍 ETF技术分析师正在分析中...")
        time.sleep(1)
        
        prompt = f"""
你是一名资深的ETF技术分析师。请基于以下ETF数据进行专业的技术面分析：

ETF基本信息：
- ETF代码：{etf_info.get('symbol', 'N/A')}
- ETF名称：{etf_info.get('name', 'N/A')}
- 当前价格：{etf_info.get('current_price', 'N/A')}
- 涨跌幅：{etf_info.get('change_percent', 'N/A')}%
- 跟踪指数：{etf_info.get('tracking_index', 'N/A')}

最新技术指标：
- 收盘价：{indicators.get('price', 'N/A')}
- MA5：{indicators.get('ma5', 'N/A')}
- MA10：{indicators.get('ma10', 'N/A')}
- MA20：{indicators.get('ma20', 'N/A')}
- MA60：{indicators.get('ma60', 'N/A')}
- RSI：{indicators.get('rsi', 'N/A')}
- MACD：{indicators.get('macd', 'N/A')}
- MACD信号线：{indicators.get('macd_signal', 'N/A')}
- 布林带上轨：{indicators.get('bb_upper', 'N/A')}
- 布林带下轨：{indicators.get('bb_lower', 'N/A')}
- K值：{indicators.get('k_value', 'N/A')}
- D值：{indicators.get('d_value', 'N/A')}
- 量比：{indicators.get('volume_ratio', 'N/A')}

请从以下角度进行分析：
1. 趋势分析（均线系统、价格走势）
2. 超买超卖分析（RSI、KDJ）
3. 动量分析（MACD）
4. 支撑阻力分析（布林带）
5. 成交量分析
6. 短期、中期、长期技术判断
7. 关键技术位分析
8. ETF特有的技术特征（相对个股波动更平稳）

请给出专业、详细的技术分析报告，包含风险提示。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的ETF技术分析师，具有深厚的技术分析功底，了解ETF的技术特点。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=3000)
        
        return {
            "agent_name": "ETF技术分析师",
            "agent_role": "负责ETF技术指标分析、图表形态识别、趋势判断",
            "analysis": analysis,
            "focus_areas": ["技术指标", "趋势分析", "支撑阻力", "交易信号"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def etf_allocation_analyst(self, etf_info: Dict, holdings_data: Dict, sector_data: Dict) -> Dict[str, Any]:
        """ETF配置分析师：持仓结构、行业配置、风险分散"""
        print("📊 ETF配置分析师正在分析中...")
        time.sleep(1)
        
        # 格式化持仓和行业数据
        from etf_data import ETFDataFetcher
        fetcher = ETFDataFetcher()
        
        holdings_text = fetcher.format_etf_holdings_for_ai(holdings_data)
        sector_text = fetcher.format_etf_sector_for_ai(sector_data)
        
        prompt = f"""
你是一名资深的ETF配置分析师。请基于以下ETF的持仓结构和行业配置进行专业分析：

ETF基本信息：
- ETF代码：{etf_info.get('symbol', 'N/A')}
- ETF名称：{etf_info.get('name', 'N/A')}
- 跟踪指数：{etf_info.get('tracking_index', 'N/A')}
- 基金规模：{etf_info.get('fund_size', 'N/A')}

{holdings_text}

{sector_text}

请从以下角度进行深入分析：

1. **持仓结构分析**
   - 十大持仓股票的质量评估
   - 持仓集中度分析（是否过于集中）
   - 重仓股的行业分布和特点
   - 持仓股票的成长性和稳定性

2. **行业配置分析**
   - 行业配置的合理性评估
   - 行业集中度和分散度
   - 配置行业的景气度和前景
   - 行业配置与市场热点的匹配度

3. **风险分散评估**
   - 持仓的分散化程度
   - 行业分散对风险的对冲效果
   - 单一持仓风险评估
   - 行业集中风险评估

4. **跟踪效果评估**
   - 持仓结构与跟踪指数的匹配度
   - 是否存在明显偏离
   - 跟踪误差的可能来源

5. **配置优势与劣势**
   - 配置方案的优点
   - 配置方案的不足
   - 与同类ETF的对比（如有）

6. **投资建议**
   - 基于配置结构的投资建议
   - 适合的投资者类型
   - 配置面的机会和风险

请给出专业、详细的配置分析报告。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的ETF配置分析师，擅长资产配置和风险管理。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "ETF配置分析师",
            "agent_role": "负责持仓结构、行业配置、风险分散分析",
            "analysis": analysis,
            "focus_areas": ["持仓结构", "行业配置", "风险分散", "资产配置"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def etf_valuation_analyst(self, etf_info: Dict, indicators: Dict) -> Dict[str, Any]:
        """ETF估值分析师：溢价率、流动性、跟踪误差"""
        print("💰 ETF估值分析师正在分析中...")
        time.sleep(1)
        
        prompt = f"""
你是一名资深的ETF估值分析师。请基于以下ETF数据进行专业的估值分析：

ETF基本信息：
- ETF代码：{etf_info.get('symbol', 'N/A')}
- ETF名称：{etf_info.get('name', 'N/A')}
- 当前价格：{etf_info.get('current_price', 'N/A')} 元
- 跟踪指数：{etf_info.get('tracking_index', 'N/A')}
- 溢价率：{etf_info.get('premium_rate', 'N/A')}
- 基金规模：{etf_info.get('fund_size', 'N/A')}
- 成交量：{etf_info.get('volume', 'N/A')}
- 成交额：{etf_info.get('amount', 'N/A')}
- 管理费率：{etf_info.get('management_fee', 'N/A')}
- 托管费率：{etf_info.get('custodian_fee', 'N/A')}

请从以下角度进行深入分析：

1. **溢价率分析** ⭐ 重点
   - 当前溢价率水平评估
   - 溢价/折价的原因分析
   - 溢价率的合理区间
   - 溢价率对投资的影响
   - 申购赎回套利机会

2. **流动性分析**
   - 成交量和成交额评估
   - 流动性充足性判断
   - 买卖价差分析（如有数据）
   - 大额交易的冲击成本
   - 流动性与基金规模的匹配

3. **费率分析**
   - 管理费率和托管费率水平
   - 与同类ETF的费率对比
   - 费率对长期收益的影响
   - 费率的合理性评估

4. **跟踪效果分析**
   - 跟踪误差评估（基于可得数据）
   - 跟踪偏离的可能原因
   - ETF与标的指数的拟合度
   - 跟踪效果的稳定性

5. **规模分析**
   - 基金规模的合理性
   - 规模对流动性的影响
   - 规模对管理效率的影响
   - 清盘风险评估

6. **综合估值判断**
   - ETF的估值水平（合理/高估/低估）
   - 性价比评估
   - 与直接购买成分股的对比
   - 投资价值判断

7. **投资建议**
   - 基于估值的操作建议
   - 最佳买入时机判断
   - 风险提示

请给出专业、详细的估值分析报告。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的ETF估值分析师，擅长ETF估值、流动性和跟踪效果分析。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "ETF估值分析师",
            "agent_role": "负责溢价率、流动性、跟踪误差分析",
            "analysis": analysis,
            "focus_areas": ["溢价率", "流动性", "跟踪误差", "费率分析", "估值判断"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def etf_investment_advisor(self, etf_info: Dict, agents_results: Dict) -> Dict[str, Any]:
        """ETF投资顾问：综合团队意见，给出投资建议"""
        print("🎯 ETF投资顾问正在制定建议...")
        time.sleep(1)
        
        # 收集各分析师报告
        technical_report = agents_results.get('technical', {}).get('analysis', '')
        allocation_report = agents_results.get('allocation', {}).get('analysis', '')
        valuation_report = agents_results.get('valuation', {}).get('analysis', '')
        
        prompt = f"""
你是一名资深的ETF投资顾问。请综合以下分析师的报告，给出最终的投资建议：

ETF基本信息：
- ETF代码：{etf_info.get('symbol', 'N/A')}
- ETF名称：{etf_info.get('name', 'N/A')}
- 当前价格：{etf_info.get('current_price', 'N/A')} 元
- 跟踪指数：{etf_info.get('tracking_index', 'N/A')}

【ETF技术分析师报告】
{technical_report}

【ETF配置分析师报告】
{allocation_report}

【ETF估值分析师报告】
{valuation_report}

请综合以上三位分析师的专业意见，从以下角度给出最终投资建议：

1. **综合评估**
   - 各分析师观点的一致性和分歧
   - 技术面、配置面、估值面的综合判断
   - ETF的整体投资价值评估

2. **投资评级**
   - 明确给出：买入/持有/卖出
   - 评级的主要依据
   - 信心度评估（1-10分）

3. **操作策略** ⭐ 核心
   - 具体的买入/卖出建议
   - 最佳进场时机和价位
   - 仓位配置建议（轻仓/中仓/重仓）
   - 持有周期建议

4. **关键位置**
   - 建议买入价格区间
   - 止盈价位建议
   - 止损价位建议

5. **适合人群**
   - 该ETF适合的投资者类型
   - 风险承受能力要求
   - 投资期限建议

6. **优势与风险**
   - 投资该ETF的主要优势
   - 需要关注的风险点
   - 与直接买股票的对比

7. **总结建议**
   - 一句话总结投资建议
   - 关键决策要点
   - 需要持续关注的事项

请给出明确、可执行的投资建议，避免模棱两可。
"""
        
        messages = [
            {"role": "system", "content": "你是一名资深的ETF投资顾问，擅长综合各方面信息给出明确的投资建议。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "ETF投资顾问",
            "agent_role": "综合团队意见，给出最终投资建议",
            "analysis": analysis,
            "focus_areas": ["综合评估", "投资评级", "操作策略", "风险收益"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def run_etf_analysis(self, etf_info: Dict, etf_data: Any, indicators: Dict, 
                         holdings_data: Dict, sector_data: Dict) -> Dict[str, Any]:
        """运行ETF分析流程"""
        print("🚀 启动ETF分析系统...")
        print("=" * 50)
        
        agents_results = {}
        
        # 1. ETF技术分析
        agents_results["technical"] = self.etf_technical_analyst(etf_info, etf_data, indicators)
        
        # 2. ETF配置分析
        agents_results["allocation"] = self.etf_allocation_analyst(etf_info, holdings_data, sector_data)
        
        # 3. ETF估值分析
        agents_results["valuation"] = self.etf_valuation_analyst(etf_info, indicators)
        
        # 4. ETF投资顾问
        agents_results["advisor"] = self.etf_investment_advisor(etf_info, agents_results)
        
        print("✅ ETF分析完成")
        print("=" * 50)
        
        return agents_results
    
    def make_etf_final_decision(self, agents_results: Dict, etf_info: Dict) -> Dict[str, Any]:
        """制定ETF最终投资决策"""
        print("📋 正在制定ETF最终投资决策...")
        time.sleep(1)
        
        # 收集所有分析师报告
        advisor_report = agents_results.get('advisor', {}).get('analysis', '')
        technical_report = agents_results.get('technical', {}).get('analysis', '')
        valuation_report = agents_results.get('valuation', {}).get('analysis', '')
        
        prompt = f"""
基于ETF分析师团队的综合分析，现在需要做出最终的投资决策。

ETF信息：
- ETF代码：{etf_info.get('symbol', 'N/A')}
- ETF名称：{etf_info.get('name', 'N/A')}
- 当前价格：{etf_info.get('current_price', 'N/A')} 元

投资顾问建议：
{advisor_report}

请给出最终投资决策，必须包含以下内容（以JSON格式输出）：

{{
    "rating": "买入/持有/卖出",
    "target_price": "目标价位（具体数字）",
    "operation_advice": "具体操作建议",
    "entry_range": "进场价位区间",
    "take_profit": "止盈价位",
    "stop_loss": "止损价位",
    "holding_period": "持有周期",
    "position_size": "仓位建议（轻仓/中等仓位/重仓）",
    "risk_warning": "风险提示",
    "confidence_level": "信心度(1-10分)"
}}
"""
        
        messages = [
            {"role": "system", "content": "你是一名专业的ETF投资决策专家，需要给出明确、可执行的投资建议。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.deepseek_client.call_api(messages, temperature=0.3, max_tokens=2000)
        
        try:
            # 尝试解析JSON响应
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                decision_json = json.loads(json_match.group())
                return decision_json
            else:
                return {"decision_text": response}
        except (json.JSONDecodeError, AttributeError):
            return {"decision_text": response}
