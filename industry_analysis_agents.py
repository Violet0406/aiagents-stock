"""
行业专属AI分析师团队
"""

from deepseek_client import DeepSeekClient
from typing import Dict, Any, List
import time
import re
import json


class IndustryAnalysisAgents:
    """行业分析AI智能体集合"""
    
    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.deepseek_client = DeepSeekClient(model=model)
    
    def industry_trend_analyst(self, industry_data: Dict, constituents_data: Dict, valuation_data: Dict) -> Dict[str, Any]:
        """行业趋势分析师：行业走势、周期判断、未来展望"""
        print("📊 行业趋势分析师正在分析中...")
        time.sleep(1)
        
        # 格式化数据
        from industry_analysis_data import IndustryAnalysisDataFetcher
        fetcher = IndustryAnalysisDataFetcher()
        
        industry_text = fetcher.format_industry_quotes_for_ai(industry_data)
        constituents_text = fetcher.format_industry_constituents_for_ai(constituents_data, top_n=10)
        
        prompt = f"""
你是一名资深的行业趋势分析师。请基于以下行业数据进行专业的趋势分析：

{industry_text}

行业估值数据：
- 平均市盈率：{valuation_data.get('avg_pe', 'N/A')}
- 中位数市盈率：{valuation_data.get('median_pe', 'N/A')}
- 平均市值：{valuation_data.get('avg_market_cap', 'N/A')} 元

{constituents_text}

请从以下角度进行深入分析：

1. **行业整体走势分析**
   - 行业指数涨跌幅评估
   - 成交活跃度分析
   - 与大盘对比（相对强弱）
   - 短期、中期、长期趋势判断

2. **行业周期判断** ⭐ 重点
   - 行业当前所处周期阶段（萌芽期/成长期/成熟期/衰退期）
   - 周期性特征分析
   - 景气度评估
   - 拐点识别（上升/下降）

3. **行业估值水平**
   - 当前估值合理性（平均市盈率分析）
   - 历史估值对比（如可推断）
   - 估值中枢判断
   - 是否存在高估/低估

4. **成分股表现分析**
   - 领涨股和领跌股特征
   - 板块内部分化程度
   - 龙头股表现
   - 个股活跃度

5. **行业政策环境**
   - 相关政策支持或限制
   - 政策对行业的影响
   - 未来政策预期

6. **行业竞争格局**
   - 竞争激烈程度
   - 市场集中度
   - 龙头优势分析

7. **未来展望** ⭐ 核心
   - 行业发展前景
   - 增长驱动因素
   - 潜在风险和机遇
   - 1-3年发展预判

8. **投资价值判断**
   - 行业投资价值评估
   - 投资时机判断
   - 趋势面的建议

请给出专业、深入的行业趋势分析报告。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的行业趋势分析师，擅长行业周期判断和趋势预测。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "行业趋势分析师",
            "agent_role": "负责行业走势、周期判断、未来展望",
            "analysis": analysis,
            "focus_areas": ["行业走势", "周期判断", "景气度", "未来展望"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def industry_capital_analyst(self, industry_data: Dict, capital_data: Dict, constituents_data: Dict) -> Dict[str, Any]:
        """行业资金分析师：资金流向、主力动向、市场关注度"""
        print("💰 行业资金分析师正在分析中...")
        time.sleep(1)
        
        # 格式化数据
        from industry_analysis_data import IndustryAnalysisDataFetcher
        fetcher = IndustryAnalysisDataFetcher()
        
        industry_text = fetcher.format_industry_quotes_for_ai(industry_data)
        
        # 分析成分股的资金活跃度
        constituents = constituents_data.get('constituents', [])[:20]  # 取前20只
        top_volume_stocks = sorted(constituents, 
                                   key=lambda x: float(x.get('amount', 0)) if x.get('amount') not in ['N/A', None] else 0, 
                                   reverse=True)[:10]
        
        volume_text = "成交额最大的10只股票：\n"
        for i, stock in enumerate(top_volume_stocks, 1):
            volume_text += f"{i}. {stock.get('name')} - 成交额: {stock.get('amount')}, 涨跌幅: {stock.get('change_percent')}%\n"
        
        prompt = f"""
你是一名资深的行业资金分析师。请基于以下行业数据进行专业的资金分析：

{industry_text}

{volume_text}

行业资金数据：
- 成交额：{capital_data.get('amount', industry_data.get('amount', 'N/A'))}

请从以下角度进行深入分析：

1. **行业资金流向分析**
   - 行业整体资金活跃度
   - 成交额水平评估
   - 资金流入/流出判断
   - 与历史水平对比（如可推断）

2. **主力资金动向** ⭐ 重点
   - 主力资金对该行业的态度
   - 大资金进场迹象识别
   - 机构关注度评估
   - 主力操作意图推断

3. **市场关注度分析**
   - 行业热度评估
   - 市场关注程度
   - 相对于其他行业的热度对比
   - 话题性和舆论关注

4. **个股资金分化**
   - 龙头股资金表现
   - 资金在板块内的分布
   - 强势股和弱势股的资金差异
   - 资金追逐的方向

5. **资金流向的持续性**
   - 资金流向是否可持续
   - 短期炒作还是长期配置
   - 资金流向的稳定性

6. **投资建议**
   - 基于资金面的操作建议
   - 资金流向的指示意义
   - 风险提示

请给出专业、详细的资金分析报告。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的行业资金分析师，擅长资金流向和主力行为研究。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=3500)
        
        return {
            "agent_name": "行业资金分析师",
            "agent_role": "负责资金流向、主力动向、市场关注度分析",
            "analysis": analysis,
            "focus_areas": ["资金流向", "主力动向", "市场关注度", "资金活跃度"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def industry_stock_picker(self, leading_data: Dict, constituents_data: Dict, industry_data: Dict) -> Dict[str, Any]:
        """行业个股精选师：龙头推荐、成长股挖掘、投资标的"""
        print("🎯 行业个股精选师正在分析中...")
        time.sleep(1)
        
        # 格式化数据
        from industry_analysis_data import IndustryAnalysisDataFetcher
        fetcher = IndustryAnalysisDataFetcher()
        
        leading_text = fetcher.format_leading_stocks_for_ai(leading_data)
        
        # 筛选涨幅较大的股票（潜力股）
        constituents = constituents_data.get('constituents', [])
        top_gainers = sorted([s for s in constituents if s.get('change_percent') not in ['N/A', None]], 
                            key=lambda x: float(x.get('change_percent', 0)), 
                            reverse=True)[:10]
        
        gainers_text = "当日涨幅前10的股票：\n"
        for i, stock in enumerate(top_gainers, 1):
            gainers_text += f"{i}. {stock.get('name')} ({stock.get('code')}) - "
            gainers_text += f"涨幅: {stock.get('change_percent')}%, 市值: {stock.get('market_cap')}\n"
        
        prompt = f"""
你是一名资深的行业个股精选师。请基于以下数据，精选优质投资标的：

行业：{industry_data.get('industry_name', 'N/A')}

{leading_text}

{gainers_text}

请从以下角度进行深入分析和精选：

1. **龙头股推荐** ⭐ 核心
   - 推荐3-5只行业龙头股
   - 每只股票的推荐理由（市值、地位、竞争力）
   - 龙头股的投资价值
   - 风险收益评估

2. **成长股挖掘**
   - 识别具有成长潜力的中小市值股票
   - 成长性分析（业绩增速、市场空间等）
   - 推荐2-3只潜力成长股
   - 成长股的风险提示

3. **价值股筛选**
   - 估值合理或低估的股票
   - 安全边际评估
   - 推荐1-2只价值股（如有）

4. **强势股分析**
   - 当前强势股特征
   - 强势原因分析
   - 追高风险评估

5. **投资组合建议** ⭐ 重点
   - 构建行业投资组合（龙头+成长+价值）
   - 仓位配置建议
   - 分散化策略

6. **个股风险提示**
   - 各推荐股票的主要风险
   - 需要规避的股票类型
   - 投资注意事项

7. **操作建议**
   - 买入时机建议
   - 持仓周期建议
   - 止盈止损策略

请给出专业、可操作的个股精选报告，明确推荐具体股票代码和名称。
"""
        
        messages = [
            {"role": "system", "content": "你是一名经验丰富的行业个股精选师，擅长挖掘优质投资标的。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "行业个股精选师",
            "agent_role": "负责龙头推荐、成长股挖掘、投资标的筛选",
            "analysis": analysis,
            "focus_areas": ["龙头推荐", "成长股挖掘", "价值股", "投资组合"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def industry_investment_strategist(self, industry_data: Dict, agents_results: Dict) -> Dict[str, Any]:
        """行业投资策略师：综合建议、配置比例、风险提示"""
        print("🎲 行业投资策略师正在制定策略...")
        time.sleep(1)
        
        # 收集各分析师报告
        trend_report = agents_results.get('trend', {}).get('analysis', '')
        capital_report = agents_results.get('capital', {}).get('analysis', '')
        stock_picker_report = agents_results.get('stock_picker', {}).get('analysis', '')
        
        prompt = f"""
你是一名资深的行业投资策略师。请综合以下分析师的报告，制定完整的投资策略：

行业：{industry_data.get('industry_name', 'N/A')}

【行业趋势分析师报告】
{trend_report}

【行业资金分析师报告】
{capital_report}

【行业个股精选师报告】
{stock_picker_report}

请综合以上分析，制定完整的行业投资策略：

1. **综合评估**
   - 各分析师观点的一致性和分歧
   - 趋势、资金、个股的综合判断
   - 行业整体投资价值评估

2. **投资评级** ⭐ 核心
   - 明确给出：买入/持有/卖出
   - 评级的主要依据
   - 信心度评估（1-10分）

3. **投资策略** ⭐ 重点
   - 具体的投资策略（激进/稳健/保守）
   - 配置时机建议
   - 持仓周期建议（短期/中期/长期）

4. **仓位配置建议**
   - 该行业在整体资产中的建议配置比例
   - 龙头股/成长股/价值股的配置比例
   - 仓位调整建议

5. **推荐股票组合**
   - 核心持仓（2-3只龙头）
   - 卫星持仓（2-3只成长股）
   - 具体的股票代码和名称

6. **风险控制** ⭐ 重要
   - 主要风险识别
   - 止损策略
   - 风险对冲建议
   - 需要关注的风险信号

7. **操作计划**
   - 分批建仓/一次性建仓
   - 买入价格区间建议
   - 加仓/减仓条件
   - 清仓信号

8. **后续跟踪要点**
   - 需要持续关注的指标
   - 决策调整的触发条件
   - 定期复盘建议

请给出明确、可执行的投资策略，避免模棱两可。
"""
        
        messages = [
            {"role": "system", "content": "你是一名资深的行业投资策略师，擅长制定完整的投资策略和风险控制方案。"},
            {"role": "user", "content": prompt}
        ]
        
        analysis = self.deepseek_client.call_api(messages, max_tokens=4000)
        
        return {
            "agent_name": "行业投资策略师",
            "agent_role": "综合建议、配置比例、风险提示",
            "analysis": analysis,
            "focus_areas": ["投资策略", "配置比例", "风险控制", "操作计划"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def run_industry_analysis(self, industry_data: Dict, constituents_data: Dict, 
                              capital_data: Dict, valuation_data: Dict, 
                              leading_data: Dict) -> Dict[str, Any]:
        """运行行业分析流程"""
        print("🚀 启动行业分析系统...")
        print("=" * 50)
        
        agents_results = {}
        
        # 1. 行业趋势分析
        agents_results["trend"] = self.industry_trend_analyst(industry_data, constituents_data, valuation_data)
        
        # 2. 行业资金分析
        agents_results["capital"] = self.industry_capital_analyst(industry_data, capital_data, constituents_data)
        
        # 3. 行业个股精选
        agents_results["stock_picker"] = self.industry_stock_picker(leading_data, constituents_data, industry_data)
        
        # 4. 行业投资策略
        agents_results["strategist"] = self.industry_investment_strategist(industry_data, agents_results)
        
        print("✅ 行业分析完成")
        print("=" * 50)
        
        return agents_results
    
    def make_industry_final_decision(self, agents_results: Dict, industry_data: Dict) -> Dict[str, Any]:
        """制定行业最终投资决策"""
        print("📋 正在制定行业最终投资决策...")
        time.sleep(1)
        
        # 收集投资策略师报告
        strategist_report = agents_results.get('strategist', {}).get('analysis', '')
        
        prompt = f"""
基于行业分析师团队的综合分析，现在需要做出最终的投资决策。

行业：{industry_data.get('industry_name', 'N/A')}

投资策略师建议：
{strategist_report}

请给出最终投资决策，必须包含以下内容（以JSON格式输出）：

{{
    "rating": "买入/持有/卖出",
    "recommended_stocks": ["股票代码1", "股票代码2", "股票代码3"],
    "allocation_ratio": "建议配置比例（如5%-10%）",
    "holding_period": "持有周期（短期/中期/长期）",
    "operation_advice": "具体操作建议",
    "risk_warning": "风险提示",
    "confidence_level": "信心度(1-10分)"
}}
"""
        
        messages = [
            {"role": "system", "content": "你是一名专业的行业投资决策专家，需要给出明确、可执行的投资建议。"},
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
