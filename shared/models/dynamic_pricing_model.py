# 共享动态价格数据模型
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

class DynamicPriceModel:
    """动态价格数据模型"""
    
    def __init__(self, item_id: int, base_price: float, item_name: str = ""):
        self.item_id = item_id
        self.item_name = item_name
        self.base_price = base_price  # 基础价格
        self.current_price = base_price  # 当前价格
        self.price_history: List[Dict[str, Any]] = []  # 价格历史记录
        self.supply = 100  # 供应量 (0-100)
        self.demand = 50   # 需求量 (0-100)
        self.last_update: datetime = datetime.now()  # 上次更新时间
        self.price_factors = {
            "supply_factor": 1.0,     # 供应因素
            "demand_factor": 1.0,     # 需求因素
            "seasonal_factor": 1.0,   # 季节因素
            "event_factor": 1.0,      # 事件因素
            "time_factor": 1.0        # 时间因素
        }
        
    def to_dict(self) -> Dict[str, Any]:
        """将动态价格对象转换为字典"""
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "base_price": self.base_price,
            "current_price": self.current_price,
            "price_history": self.price_history,
            "supply": self.supply,
            "demand": self.demand,
            "last_update": self.last_update.isoformat(),
            "price_factors": self.price_factors
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DynamicPriceModel':
        """从字典创建动态价格对象"""
        price_model = cls(
            data["item_id"],
            data["base_price"],
            data.get("item_name", "")
        )
        price_model.current_price = data.get("current_price", data["base_price"])
        price_model.price_history = data.get("price_history", [])
        price_model.supply = data.get("supply", 100)
        price_model.demand = data.get("demand", 50)
        
        # 解析上次更新时间
        last_update_str = data.get("last_update")
        if last_update_str:
            price_model.last_update = datetime.fromisoformat(last_update_str)
            
        price_model.price_factors = data.get("price_factors", {
            "supply_factor": 1.0,
            "demand_factor": 1.0,
            "seasonal_factor": 1.0,
            "event_factor": 1.0,
            "time_factor": 1.0
        })
        return price_model
        
    def update_supply(self, new_supply: int):
        """更新供应量"""
        self.supply = max(0, min(100, new_supply))  # 限制在0-100范围内
        self._update_supply_factor()
        
    def update_demand(self, new_demand: int):
        """更新需求量"""
        self.demand = max(0, min(100, new_demand))  # 限制在0-100范围内
        self._update_demand_factor()
        
    def _update_supply_factor(self):
        """根据供应量更新供应因素"""
        # 供应越多，价格越低；供应越少，价格越高
        # 供应量50为基准，低于50价格上涨，高于50价格下降
        if self.supply > 50:
            # 供应充足，价格下降，最低到基础价格的50%
            self.price_factors["supply_factor"] = 0.5 + (self.supply / 100) * 0.5
        else:
            # 供应不足，价格上涨，最高到基础价格的200%
            self.price_factors["supply_factor"] = 2.0 - (self.supply / 50) * 1.0
            
    def _update_demand_factor(self):
        """根据需求量更新需求因素"""
        # 需求越多，价格越高；需求越少，价格越低
        # 需求量50为基准，低于50价格下降，高于50价格上涨
        if self.demand > 50:
            # 需求旺盛，价格上涨，最高到基础价格的200%
            self.price_factors["demand_factor"] = 1.0 + ((self.demand - 50) / 50) * 1.0
        else:
            # 需求疲软，价格下降，最低到基础价格的50%
            self.price_factors["demand_factor"] = 0.5 + (self.demand / 50) * 0.5
            
    def apply_seasonal_factor(self, season: str):
        """应用季节因素"""
        seasonal_multipliers = {
            "spring": 1.0,   # 春季
            "summer": 1.1,   # 夏季 (冷饮需求增加)
            "autumn": 0.9,   # 秋季 (丰收季节)
            "winter": 1.2    # 冬季 (热饮需求增加)
        }
        self.price_factors["seasonal_factor"] = seasonal_multipliers.get(season, 1.0)
        
    def apply_event_factor(self, event_type: str):
        """应用事件因素"""
        event_multipliers = {
            "festival": 1.5,      # 节日 (需求大增)
            "sale": 0.7,          # 大促 (价格下降)
            "shortage": 2.0,      # 短缺 (价格飞涨)
            "normal": 1.0         # 正常
        }
        self.price_factors["event_factor"] = event_multipliers.get(event_type, 1.0)
        
    def apply_time_factor(self, hour: int):
        """应用时间因素"""
        # 假设商店在8:00-22:00营业
        if 8 <= hour <= 11:  # 上午 (刚开门，价格较低)
            self.price_factors["time_factor"] = 0.9
        elif 12 <= hour <= 14:  # 午餐时间 (需求高峰)
            self.price_factors["time_factor"] = 1.2
        elif 18 <= hour <= 20:  # 晚餐时间 (需求高峰)
            self.price_factors["time_factor"] = 1.3
        elif 21 <= hour <= 22:  # 晚上 (即将关门，可能降价清仓)
            self.price_factors["time_factor"] = 0.8
        else:
            self.price_factors["time_factor"] = 1.0
            
    def calculate_current_price(self) -> float:
        """计算当前价格"""
        # 综合所有因素计算价格
        multiplier = 1.0
        for factor in self.price_factors.values():
            multiplier *= factor
            
        new_price = self.base_price * multiplier
        
        # 限制价格波动范围，最低不低于基础价格的30%，最高不高于基础价格的300%
        new_price = max(self.base_price * 0.3, min(self.base_price * 3.0, new_price))
        
        # 记录价格历史
        self.price_history.append({
            "timestamp": datetime.now().isoformat(),
            "price": new_price,
            "factors": self.price_factors.copy()
        })
        
        # 只保留最近10条记录
        if len(self.price_history) > 10:
            self.price_history = self.price_history[-10:]
            
        self.current_price = new_price
        self.last_update = datetime.now()
        return self.current_price
        
    def get_price_trend(self) -> str:
        """获取价格趋势"""
        if len(self.price_history) < 2:
            return "stable"
            
        current_price = self.price_history[-1]["price"]
        previous_price = self.price_history[-2]["price"]
        
        if current_price > previous_price * 1.05:
            return "rising"
        elif current_price < previous_price * 0.95:
            return "falling"
        else:
            return "stable"
            
    def reset_to_base(self):
        """重置为基准价格"""
        self.current_price = self.base_price
        self.price_factors = {
            "supply_factor": 1.0,
            "demand_factor": 1.0,
            "seasonal_factor": 1.0,
            "event_factor": 1.0,
            "time_factor": 1.0
        }
        self.last_update = datetime.now()


class DynamicPricingManager:
    """动态价格管理器"""
    
    def __init__(self):
        self.price_models: Dict[int, DynamicPriceModel] = {}
        self.global_factors = {
            "inflation_rate": 1.0,    # 通胀率
            "market_stability": 1.0,  # 市场稳定性
            "season": "spring"        # 当前季节
        }
        
    def add_item(self, item_id: int, base_price: float, item_name: str = "") -> DynamicPriceModel:
        """添加商品到动态定价系统"""
        if item_id not in self.price_models:
            price_model = DynamicPriceModel(item_id, base_price, item_name)
            self.price_models[item_id] = price_model
            return price_model
        return self.price_models[item_id]
        
    def get_item_price(self, item_id: int) -> Optional[float]:
        """获取商品当前价格"""
        if item_id in self.price_models:
            return self.price_models[item_id].calculate_current_price()
        return None
        
    def update_item_supply(self, item_id: int, supply: int):
        """更新商品供应量"""
        if item_id in self.price_models:
            self.price_models[item_id].update_supply(supply)
            
    def update_item_demand(self, item_id: int, demand: int):
        """更新商品需求量"""
        if item_id in self.price_models:
            self.price_models[item_id].update_demand(demand)
            
    def apply_global_event(self, event_type: str):
        """应用全局事件"""
        for price_model in self.price_models.values():
            price_model.apply_event_factor(event_type)
            
    def update_season(self, season: str):
        """更新季节"""
        self.global_factors["season"] = season
        for price_model in self.price_models.values():
            price_model.apply_seasonal_factor(season)
            
    def update_time(self, hour: int):
        """更新时间因素"""
        for price_model in self.price_models.values():
            price_model.apply_time_factor(hour)
            
    def get_all_prices(self) -> Dict[int, float]:
        """获取所有商品的当前价格"""
        prices = {}
        for item_id, price_model in self.price_models.items():
            prices[item_id] = price_model.calculate_current_price()
        return prices
        
    def get_price_model(self, item_id: int) -> Optional[DynamicPriceModel]:
        """获取价格模型"""
        return self.price_models.get(item_id)
        
    def simulate_market_fluctuations(self):
        """模拟市场波动"""
        for price_model in self.price_models.values():
            # 随机小幅波动供应和需求
            supply_change = random.randint(-5, 5)
            demand_change = random.randint(-5, 5)
            
            price_model.update_supply(max(0, min(100, price_model.supply + supply_change)))
            price_model.update_demand(max(0, min(100, price_model.demand + demand_change)))

# 创建全局动态价格管理器实例
dynamic_pricing_manager = DynamicPricingManager()