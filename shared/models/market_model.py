# 共享市场数据模型
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

class MarketModel:
    """共享市场数据模型"""
    
    def __init__(self, market_id: str, name: str):
        self.market_id = market_id
        self.name = name
        self.items = {}  # 商品列表 {item_id: item_data}
        self.price_history = {}  # 价格历史 {item_id: [history_records]}
        self.last_update = datetime.now()
        self.trends = {}  # 市场趋势 {category: trend_value}
        
    def add_item(self, item_id: int, item_name: str, base_price: float, 
                 category: str = "", stock: int = 100):
        """
        添加商品到市场
        :param item_id: 商品ID
        :param item_name: 商品名称
        :param base_price: 基础价格
        :param category: 商品类别
        :param stock: 库存数量
        """
        self.items[item_id] = {
            "item_id": item_id,
            "name": item_name,
            "base_price": base_price,
            "category": category,
            "current_price": base_price,
            "stock": stock,
            "supply": 100,  # 供应量 (0-100)
            "demand": 50,   # 需求量 (0-100)
            "price_factors": {
                "supply_factor": 1.0,
                "demand_factor": 1.0,
                "seasonal_factor": 1.0,
                "event_factor": 1.0,
                "time_factor": 1.0
            }
        }
        
    def update_price(self, item_id: int, supply: Optional[int] = None, 
                     demand: Optional[int] = None):
        """
        更新商品价格
        :param item_id: 商品ID
        :param supply: 供应量 (0-100)
        :param demand: 需求量 (0-100)
        """
        if item_id not in self.items:
            return
            
        item = self.items[item_id]
        
        # 更新供应和需求
        if supply is not None:
            item["supply"] = max(0, min(100, supply))
        if demand is not None:
            item["demand"] = max(0, min(100, demand))
            
        # 计算价格因子
        # 供应因子：供应越少价格越高
        item["price_factors"]["supply_factor"] = 1.0 + (50 - item["supply"]) / 100.0
        
        # 需求因子：需求越高价格越高
        item["price_factors"]["demand_factor"] = 1.0 + (item["demand"] - 50) / 100.0
        
        # 计算当前价格
        factor = (item["price_factors"]["supply_factor"] * 
                 item["price_factors"]["demand_factor"] *
                 item["price_factors"]["seasonal_factor"] * 
                 item["price_factors"]["event_factor"] * 
                 item["price_factors"]["time_factor"])
                 
        # 限制价格波动范围（最大单日波动±20%）
        factor = max(0.8, min(1.2, factor))
        
        new_price = item["base_price"] * factor
        item["current_price"] = round(new_price, 2)
        
        # 记录价格历史
        if item_id not in self.price_history:
            self.price_history[item_id] = []
            
        self.price_history[item_id].append({
            "timestamp": datetime.now().isoformat(),
            "price": item["current_price"],
            "supply": item["supply"],
            "demand": item["demand"],
            "factors": item["price_factors"].copy()
        })
        
        # 保持价格历史记录在合理范围内（最多100条记录）
        if len(self.price_history[item_id]) > 100:
            self.price_history[item_id] = self.price_history[item_id][-100:]
            
        self.last_update = datetime.now()
        
    def get_item_price(self, item_id: int) -> Optional[float]:
        """
        获取商品当前价格
        :param item_id: 商品ID
        :return: 当前价格
        """
        if item_id not in self.items:
            return None
        return self.items[item_id]["current_price"]
        
    def get_item_info(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        获取商品完整信息
        :param item_id: 商品ID
        :return: 商品信息
        """
        return self.items.get(item_id)
        
    def get_all_items(self) -> Dict[int, Dict[str, Any]]:
        """
        获取所有商品信息
        :return: 所有商品信息
        """
        return self.items.copy()
        
    def update_trend(self, category: str, trend_value: float):
        """
        更新市场趋势
        :param category: 商品类别
        :param trend_value: 趋势值 (-1.0 到 1.0)
        """
        self.trends[category] = max(-1.0, min(1.0, trend_value))
        
    def apply_seasonal_factor(self, season: str):
        """
        应用季节性因子
        :param season: 季节
        """
        seasonal_factors = {
            "spring": {"蔬菜": 0.9, "水果": 0.8, "海鲜": 1.1},
            "summer": {"蔬菜": 0.8, "水果": 0.7, "冷饮": 0.6},
            "autumn": {"蔬菜": 0.9, "水果": 0.9, "干货": 0.8},
            "winter": {"蔬菜": 1.2, "水果": 1.1, "热饮": 0.8}
        }
        
        factors = seasonal_factors.get(season, {})
        for item_id, item in self.items.items():
            category = item["category"]
            if category in factors:
                item["price_factors"]["seasonal_factor"] = factors[category]
                self.update_price(item_id)  # 更新价格
                
    def apply_event_factor(self, event_name: str, multiplier: float):
        """
        应用事件因子
        :param event_name: 事件名称
        :param multiplier: 乘数因子
        """
        for item in self.items.values():
            item["price_factors"]["event_factor"] = multiplier
            # 这里应该根据具体事件影响特定商品，简化处理影响所有商品
            
        # 更新所有商品价格
        for item_id in self.items.keys():
            self.update_price(item_id)
            
    def to_dict(self) -> Dict[str, Any]:
        """将市场对象转换为字典"""
        return {
            "market_id": self.market_id,
            "name": self.name,
            "items": self.items,
            "price_history": self.price_history,
            "last_update": self.last_update.isoformat(),
            "trends": self.trends
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MarketModel':
        """从字典创建市场对象"""
        market = cls(data["market_id"], data["name"])
        market.items = data.get("items", {})
        market.price_history = data.get("price_history", {})
        market.trends = data.get("trends", {})
        
        last_update_str = data.get("last_update")
        if last_update_str:
            market.last_update = datetime.fromisoformat(last_update_str)
            
        return market