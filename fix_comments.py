// 修复Python注释问题
// 使用井号代替双斜杠作为注释符号

// 示例修复：
// models/recipe_model.py
SAMPLE_RECIPES = [
    {
        "id": 1,
        "name": "草莓蛋糕",
        "ingredients": [
            {"item_id": 101, "quantity": 3},  # 草莓
            {"item_id": 201, "quantity": 2},  # 面粉
            {"item_id": 301, "quantity": 1}   # 鸡蛋
        ],
        "steps": [
            "将面粉和鸡蛋混合搅拌",
            "加入切碎的草莓",
            "倒入模具并放入烤箱烘烤",
            "装饰表面"
        ],
        "unlock_conditions": {"type": "level", "value": 3}
    },
    {
        "id": 2,
        "name": "寿司拼盘",
        "ingredients": [
            {"item_id": 401, "quantity": 4},  # 米饭
            {"item_id": 501, "quantity": 6},  # 生鱼片
            {"item_id": 601, "quantity": 1}   # 海苔
        ],
        "steps": [
            "准备醋饭",
            "切制新鲜食材",
            "在海苔上铺米饭",
            "摆放生鱼片并卷起",
            "切成小段"
        ],
        "unlock_conditions": {"type": "story_progress", "value": 5}
    }
]