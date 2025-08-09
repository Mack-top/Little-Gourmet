# 服务端商店服务
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import random
from shared.models.dynamic_pricing_model import dynamic_pricing_manager

class ShopService:
    """商店服务类"""
    
    def __init__(self):
        self.shop_inventory: Dict[int, Dict[str, Any]] = {}  # 商店库存
        self.sales_history: List[Dict[str, Any]] = []  # 销售历史
        self.daily_sales: Dict[int, int] = {}  # 每日销售统计 {item_id: quantity}
        self.last_reset_date: datetime = datetime.now()  # 上次重置日期
        self._load_initial_items()
        
    def _load_initial_items(self):
        """加载初始商品数据"""
        try:
            config_path = os.path.join("assets", "config", "shop_items.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    items = json.load(f)
                    self.initialize_shop_inventory(items)
        except Exception as e:
            print(f"加载商店商品数据失败: {e}")
            
    def initialize_shop_inventory(self, items: List[Dict[str, Any]]):
        """初始化商店库存"""
        for item in items:
            item_id = item["id"]
            self.shop_inventory[item_id] = {
                "id": item_id,
                "name": item["name"],
                "base_price": item["base_price"],
                "stock": item.get("stock", 100),
                "category": item.get("category", "general"),
                "description": item.get("description", "")
            }
            
            # 添加到动态定价系统
            dynamic_pricing_manager.add_item(
                item_id, 
                item["base_price"], 
                item["name"]
            )
            
    def get_shop_items(self) -> List[Dict[str, Any]]:
        """获取商店商品列表"""
        items = []
        current_prices = dynamic_pricing_manager.get_all_prices()
        
        for item_id, item_info in self.shop_inventory.items():
            current_price = current_prices.get(item_id, item_info["base_price"])
            price_model = dynamic_pricing_manager.get_price_model(item_id)
            
            item_data = item_info.copy()
            item_data["current_price"] = current_price
            item_data["price_trend"] = price_model.get_price_trend() if price_model else "stable"
            items.append(item_data)
            
        return items
        
    def get_item_info(self, item_id: int) -> Optional[Dict[str, Any]]:
        """获取商品详细信息"""
        if item_id not in self.shop_inventory:
            return None
            
        item_info = self.shop_inventory[item_id].copy()
        current_price = dynamic_pricing_manager.get_item_price(item_id)
        price_model = dynamic_pricing_manager.get_price_model(item_id)
        
        item_info["current_price"] = current_price or item_info["base_price"]
        item_info["price_trend"] = price_model.get_price_trend() if price_model else "stable"
        
        # 添加价格历史信息
        if price_model:
            item_info["price_history"] = price_model.price_history
            
        return item_info
        
    def purchase_item(self, player_id: str, item_id: int, quantity: int) -> Dict[str, Any]:
        """购买商品"""
        if item_id not in self.shop_inventory:
            return {
                "success": False,
                "message": "商品不存在"
            }
            
        item_info = self.shop_inventory[item_id]
        current_price = dynamic_pricing_manager.get_item_price(item_id)
        
        if current_price is None:
            current_price = item_info["base_price"]
            
        total_cost = current_price * quantity
        
        # 检查库存
        if item_info["stock"] < quantity:
            return {
                "success": False,
                "message": f"库存不足，仅剩{item_info['stock']}个"
            }
            
        # 这里应该检查玩家的金币数量，但暂时跳过
            
        # 更新库存
        self.shop_inventory[item_id]["stock"] -= quantity
        
        # 更新销售记录
        self._record_sale(player_id, item_id, quantity, total_cost)
        
        # 更新需求量（购买会增加需求）
        dynamic_pricing_manager.update_item_demand(
            item_id, 
            min(100, dynamic_pricing_manager.get_price_model(item_id).demand + quantity)
        )
        
        return {
            "success": True,
            "message": f"成功购买{quantity}个{item_info['name']}",
            "item_id": item_id,
            "quantity": quantity,
            "total_cost": total_cost,
            "unit_price": current_price
        }
        
    def sell_item(self, player_id: str, item_id: int, quantity: int) -> Dict[str, Any]:
        """出售商品给商店"""
        if item_id not in self.shop_inventory:
            return {
                "success": False,
                "message": "商品不被商店收购"
            }
            
        item_info = self.shop_inventory[item_id]
        current_price = dynamic_pricing_manager.get_item_price(item_id)
        
        if current_price is None:
            current_price = item_info["base_price"]
            
        # 商店收购价格为销售价格的70%
        purchase_price = current_price * 0.7
        total_value = purchase_price * quantity
        
        # 更新库存（商店收购增加库存）
        self.shop_inventory[item_id]["stock"] += quantity
        
        # 更新销售记录
        self._record_sale(player_id, item_id, -quantity, -total_value)  # 负数表示商店收购
        
        # 更新供应量（商店收购会增加供应）
        dynamic_pricing_manager.update_item_supply(
            item_id, 
            min(100, dynamic_pricing_manager.get_price_model(item_id).supply + quantity)
        )
        
        return {
            "success": True,
            "message": f"成功出售{quantity}个{item_info['name']}给商店",
            "item_id": item_id,
            "quantity": quantity,
            "total_value": total_value,
            "unit_price": purchase_price
        }
        
    def _record_sale(self, player_id: str, item_id: int, quantity: int, amount: float):
        """记录销售"""
        sale_record = {
            "player_id": player_id,
            "item_id": item_id,
            "quantity": quantity,  # 正数表示购买，负数表示出售
            "amount": amount,      # 正数表示支出，负数表示收入
            "timestamp": datetime.now().isoformat()
        }
        self.sales_history.append(sale_record)
        
        # 更新每日销售统计
        if item_id not in self.daily_sales:
            self.daily_sales[item_id] = 0
        self.daily_sales[item_id] += quantity
        
        # 只保留最近100条销售记录
        if len(self.sales_history) > 100:
            self.sales_history = self.sales_history[-100:]
            
    def restock_items(self):
        """补货商品"""
        for item_id, item_info in self.shop_inventory.items():
            # 恢复部分库存
            restock_amount = max(0, 50 - item_info["stock"]) // 2
            self.shop_inventory[item_id]["stock"] += restock_amount
            
            # 更新供应量
            supply = min(100, dynamic_pricing_manager.get_price_model(item_id).supply + restock_amount)
            dynamic_pricing_manager.update_item_supply(item_id, supply)
            
    def apply_daily_reset(self):
        """每日重置"""
        current_date = datetime.now()
        
        # 检查是否需要重置（新的一天）
        if current_date.date() != self.last_reset_date.date():
            # 重置每日销售统计
            self.daily_sales.clear()
            
            # 补货
            self.restock_items()
            
            # 更新上次重置日期
            self.last_reset_date = current_date
            
            return True
        return False
        
    def apply_event_effect(self, event_type: str):
        """应用事件效果"""
        dynamic_pricing_manager.apply_global_event(event_type)
        
    def update_season(self, season: str):
        """更新季节"""
        dynamic_pricing_manager.update_season(season)
        
    def update_time(self, hour: int):
        """更新时间因素"""
        dynamic_pricing_manager.update_time(hour)
        
    def simulate_market_activity(self):
        """模拟市场活动"""
        # 模拟市场波动
        dynamic_pricing_manager.simulate_market_fluctuations()
        
        # 随机事件影响
        events = ["normal", "festival", "sale", "shortage"]
        if random.random() < 0.1:  # 10%概率触发事件
            event = random.choice(events)
            self.apply_event_effect(event)
            
    def get_price_history(self, item_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """获取商品价格历史"""
        price_model = dynamic_pricing_manager.get_price_model(item_id)
        if price_model:
            return price_model.price_history[-limit:]
        return []
        
    def get_popular_items(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取热门商品（按销售量排序）"""
        # 按销售量排序
        sorted_items = sorted(
            self.daily_sales.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        popular_items = []
        for item_id, sales_count in sorted_items[:limit]:
            if item_id in self.shop_inventory:
                item_info = self.shop_inventory[item_id].copy()
                current_price = dynamic_pricing_manager.get_item_price(item_id)
                item_info["current_price"] = current_price or item_info["base_price"]
                item_info["sales_count"] = sales_count
                popular_items.append(item_info)
                
        return popular_items

# 创建全局商店服务实例
shop_service = ShopService()