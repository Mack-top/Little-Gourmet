# 创建模拟经营系统
import godot
from datetime import datetime, timedelta

class BusinessManager(godot.Node):
    """模拟经营系统管理器"""
    
    # 餐厅等级配置
    RESTAURANT_LEVELS = [
        {"level": 1, "name": "小摊位", "capacity": 10, "upgrade_cost": 0, "revenue_multiplier": 1.0},
        {"level": 2, "name": "小餐厅", "capacity": 25, "upgrade_cost": 1000, "revenue_multiplier": 1.2},
        {"level": 3, "name": "中餐厅", "capacity": 50, "upgrade_cost": 3000, "revenue_multiplier": 1.5},
        {"level": 4, "name": "大餐厅", "capacity": 100, "upgrade_cost": 8000, "revenue_multiplier": 2.0},
        {"level": 5, "name": "连锁餐厅", "capacity": 200, "upgrade_cost": 20000, "revenue_multiplier": 2.5},
        {"level": 6, "name": "美食广场", "capacity": 500, "upgrade_cost": 50000, "revenue_multiplier": 3.0},
        {"level": 7, "name": "餐饮集团", "capacity": 1000, "upgrade_cost": 100000, "revenue_multiplier": 4.0},
        {"level": 8, "name": "国际连锁", "capacity": 5000, "upgrade_cost": 500000, "revenue_multiplier": 5.0}
    ]
    
    def __init__(self):
        super().__init__()
        self.restaurant_level = 1  # 餐厅等级
        self.reputation = 50  # 声誉值 0-100
        self.customer_satisfaction = 50  # 顾客满意度 0-100
        self.daily_revenue = 0  # 日收入
        self.total_revenue = 0  # 总收入
        self.staff_count = 1  # 员工数量
        self.upgrade_progress = 0  # 升级进度 0-100
        self.last_update_time = datetime.now()  # 上次更新时间
        self.daily_customer_count = 0  # 日顾客数
        self.total_customer_count = 0  # 总顾客数
        
    def to_dict(self):
        """序列化经营数据"""
        return {
            "restaurant_level": self.restaurant_level,
            "reputation": self.reputation,
            "customer_satisfaction": self.customer_satisfaction,
            "daily_revenue": self.daily_revenue,
            "total_revenue": self.total_revenue,
            "staff_count": self.staff_count,
            "upgrade_progress": self.upgrade_progress,
            "last_update_time": self.last_update_time.isoformat(),
            "daily_customer_count": self.daily_customer_count,
            "total_customer_count": self.total_customer_count
        }
        
    @staticmethod
    def from_dict(data):
        """从字典恢复经营数据"""
        business_manager = BusinessManager()
        business_manager.restaurant_level = data.get("restaurant_level", 1)
        business_manager.reputation = data.get("reputation", 50)
        business_manager.customer_satisfaction = data.get("customer_satisfaction", 50)
        business_manager.daily_revenue = data.get("daily_revenue", 0)
        business_manager.total_revenue = data.get("total_revenue", 0)
        business_manager.staff_count = data.get("staff_count", 1)
        business_manager.upgrade_progress = data.get("upgrade_progress", 0)
        
        if "last_update_time" in data:
            business_manager.last_update_time = datetime.fromisoformat(data["last_update_time"])
            
        business_manager.daily_customer_count = data.get("daily_customer_count", 0)
        business_manager.total_customer_count = data.get("total_customer_count", 0)
        return business_manager
        
    def get_current_restaurant_info(self):
        """获取当前餐厅信息"""
        level_info = self.RESTAURANT_LEVELS[self.restaurant_level - 1]
        return {
            "level": self.restaurant_level,
            "name": level_info["name"],
            "capacity": level_info["capacity"],
            "revenue_multiplier": level_info["revenue_multiplier"],
            "current_customers": self.daily_customer_count
        }
        
    def serve_customers(self, customer_count, dish_quality=50):
        """服务顾客"""
        # 获取当前餐厅信息
        restaurant_info = self.get_current_restaurant_info()
        max_capacity = restaurant_info["capacity"]
        
        # 实际服务的顾客数不能超过餐厅容量
        actual_served = min(customer_count, max_capacity - self.daily_customer_count)
        if actual_served <= 0:
            return 0, "餐厅已满，无法接待更多顾客"
            
        # 增加顾客数
        self.daily_customer_count += actual_served
        self.total_customer_count += actual_served
        
        # 根据菜肴质量和顾客满意度计算收入
        quality_factor = dish_quality / 100.0  # 质量系数 0.0-1.0
        satisfaction_factor = self.customer_satisfaction / 100.0  # 满意度系数
        reputation_factor = self.reputation / 100.0  # 声誉系数
        
        # 基础收入
        base_revenue = actual_served * 10  # 每个顾客基础消费10金币
        
        # 计算总收入（考虑各种系数）
        total_revenue = (base_revenue * 
                        quality_factor * 
                        satisfaction_factor * 
                        reputation_factor * 
                        restaurant_info["revenue_multiplier"])
        
        # 更新收入统计
        self.daily_revenue += total_revenue
        self.total_revenue += total_revenue
        
        # 根据服务质量调整声誉和满意度
        if dish_quality >= 80:
            self.reputation = min(100, self.reputation + 0.5)
            self.customer_satisfaction = min(100, self.customer_satisfaction + 0.3)
        elif dish_quality >= 60:
            self.reputation = min(100, self.reputation + 0.2)
            self.customer_satisfaction = min(100, self.customer_satisfaction + 0.1)
        elif dish_quality >= 40:
            self.reputation = max(0, self.reputation - 0.1)
            self.customer_satisfaction = max(0, self.customer_satisfaction - 0.2)
        else:
            self.reputation = max(0, self.reputation - 0.3)
            self.customer_satisfaction = max(0, self.customer_satisfaction - 0.5)
            
        return total_revenue, f"成功服务 {actual_served} 位顾客，获得收入 {total_revenue:.2f} 金币"
        
    def hire_staff(self):
        """雇佣员工"""
        hire_cost = self.staff_count * 200  # 雇佣成本随员工数量增加
        if self.total_revenue >= hire_cost:
            self.staff_count += 1
            self.total_revenue -= hire_cost
            return True, f"成功雇佣一名员工，当前员工数: {self.staff_count}"
        else:
            return False, f"金币不足，需要 {hire_cost} 金币"
            
    def can_upgrade_restaurant(self):
        """检查是否可以升级餐厅"""
        if self.restaurant_level >= len(self.RESTAURANT_LEVELS):
            return False, "已达到最高等级"
            
        next_level_info = self.RESTAURANT_LEVELS[self.restaurant_level]
        upgrade_cost = next_level_info["upgrade_cost"]
        
        if self.total_revenue >= upgrade_cost:
            return True, f"升级到 {next_level_info['name']} 需要 {upgrade_cost} 金币"
        else:
            return False, f"金币不足，需要 {upgrade_cost} 金币"
            
    def start_upgrade(self):
        """开始升级餐厅"""
        can_upgrade, message = self.can_upgrade_restaurant()
        if not can_upgrade:
            return False, message
            
        next_level_info = self.RESTAURANT_LEVELS[self.restaurant_level]
        upgrade_cost = next_level_info["upgrade_cost"]
        
        # 扣除升级费用
        self.total_revenue -= upgrade_cost
        self.upgrade_progress = 0
        
        return True, f"开始升级到 {next_level_info['name']}，升级费用: {upgrade_cost} 金币"
        
    def update_upgrade_progress(self, delta_time_minutes):
        """更新升级进度"""
        if self.upgrade_progress < 100:
            # 升级速度与员工数量相关
            progress_rate = 0.1 * self.staff_count
            self.upgrade_progress = min(100, self.upgrade_progress + progress_rate * delta_time_minutes)
            
            if self.upgrade_progress >= 100:
                # 升级完成
                self.restaurant_level += 1
                self.upgrade_progress = 0
                new_level_info = self.RESTAURANT_LEVELS[self.restaurant_level - 1]
                return True, f"餐厅升级完成！现在是 {new_level_info['name']}"
                
        return False, f"升级进度: {self.upgrade_progress:.1f}%"
        
    def get_upgrade_progress(self):
        """获取升级进度"""
        return self.upgrade_progress
        
    def reset_daily_stats(self):
        """重置日统计数据"""
        self.daily_revenue = 0
        self.daily_customer_count = 0
        self.last_update_time = datetime.now()
        
    def update_with_time_delta(self, current_time):
        """根据时间差更新经营状态"""
        # 计算时间差（分钟）
        time_diff = (current_time - self.last_update_time).total_seconds() / 60
        
        # 如果超过一天，重置日统计数据
        if time_diff >= 1440:  # 1440分钟 = 24小时
            self.reset_daily_stats()
            
        # 更新升级进度
        if self.upgrade_progress > 0:
            upgrade_complete, message = self.update_upgrade_progress(time_diff)
            if upgrade_complete:
                godot.print(message)
                
        self.last_update_time = current_time
        
    def get_business_report(self):
        """获取经营报告"""
        restaurant_info = self.get_current_restaurant_info()
        
        return {
            "restaurant_level": self.restaurant_level,
            "restaurant_name": restaurant_info["name"],
            "reputation": self.reputation,
            "customer_satisfaction": self.customer_satisfaction,
            "daily_revenue": self.daily_revenue,
            "total_revenue": self.total_revenue,
            "staff_count": self.staff_count,
            "daily_customer_count": self.daily_customer_count,
            "total_customer_count": self.total_customer_count,
            "upgrade_progress": self.upgrade_progress,
            "capacity": restaurant_info["capacity"],
            "current_occupancy": f"{self.daily_customer_count}/{restaurant_info['capacity']}"
        }