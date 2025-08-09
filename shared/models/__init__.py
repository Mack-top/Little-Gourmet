# 共享数据模型模块初始化文件

# 导入所有数据模型
from .decoration_model import DecorationModel
from .dynamic_pricing_model import DynamicPriceModel
from .event_model import RandomEventModel
from .game_name_model import GameNameModel
from .ingredient_model import IngredientModel
from .market_model import MarketModel
from .player_model import PlayerModel
from .recipe_model import RecipeModel

# 定义公开接口
__all__ = [
    "DecorationModel",
    "DynamicPriceModel",
    "RandomEventModel",
    "GameNameModel",
    "IngredientModel",
    "MarketModel",
    "PlayerModel",
    "RecipeModel"
]