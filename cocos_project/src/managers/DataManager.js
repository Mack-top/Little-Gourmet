// DataManager.js - 游戏数据管理器

var DataManager = cc.Class.extend({
    ctor: function() {
        this.ingredients = [];
        this.recipes = [];
        this.achievements = [];
        this.loadAllData();
    },

    // 加载所有游戏数据
    loadAllData: function() {
        // 在实际项目中，这些数据应该从JSON文件加载
        // 这里为了演示，我们使用简化版本的数据
        this.loadIngredients();
        this.loadRecipes();
        this.loadAchievements();
    },

    // 加载食材数据
    loadIngredients: function() {
        // 模拟从 ingredients.json 加载数据
        this.ingredients = [
            {
                "id": 101,
                "name": "草莓",
                "category": "水果",
                "freshness_duration": 24,
                "base_price": 10,
                "season": "spring"
            },
            {
                "id": 201,
                "name": "面粉",
                "category": "谷物",
                "freshness_duration": 72,
                "base_price": 5,
                "season": "all"
            },
            {
                "id": 301,
                "name": "鸡蛋",
                "category": "蛋类",
                "freshness_duration": 48,
                "base_price": 8,
                "season": "all"
            },
            {
                "id": 401,
                "name": "牛奶",
                "category": "乳制品",
                "freshness_duration": 72,
                "base_price": 12,
                "season": "all"
            },
            {
                "id": 501,
                "name": "黄油",
                "category": "乳制品",
                "freshness_duration": 96,
                "base_price": 15,
                "season": "all"
            }
        ];
    },

    // 加载配方数据
    loadRecipes: function() {
        // 模拟从 recipes.json 加载数据
        this.recipes = [
            {
                "id": 1,
                "name": "草莓蛋糕",
                "category": "烘焙",
                "description": "美味的草莓蛋糕，口感松软香甜",
                "ingredients": [
                    {"item_id": 101, "quantity": 3}, // 草莓 x3
                    {"item_id": 201, "quantity": 2}, // 面粉 x2
                    {"item_id": 301, "quantity": 1}, // 鸡蛋 x1
                    {"item_id": 401, "quantity": 1}  // 牛奶 x1
                ],
                "steps": [
                    "将面粉和鸡蛋混合搅拌",
                    "加入切碎的草莓",
                    "倒入模具并放入烤箱烘烤",
                    "装饰表面"
                ],
                "difficulty": 3,
                "time_required": 60,
                "base_price": 50
            },
            {
                "id": 2,
                "name": "煎蛋卷",
                "category": "简单料理",
                "description": "简单美味的煎蛋卷",
                "ingredients": [
                    {"item_id": 301, "quantity": 2} // 鸡蛋 x2
                ],
                "steps": [
                    "打散鸡蛋",
                    "在平底锅中加热",
                    "翻面继续煎制",
                    "装盘即可"
                ],
                "difficulty": 1,
                "time_required": 10,
                "base_price": 20
            }
        ];
    },

    // 加载成就数据
    loadAchievements: function() {
        // 模拟从 achievements.json 加载数据
        this.achievements = [
            {
                "id": 1,
                "name": "初学者厨师",
                "description": "完成你的第一个食谱",
                "condition": "cook_recipe_count >= 1"
            },
            {
                "id": 2,
                "name": "烘焙大师",
                "description": "完成5个烘焙类食谱",
                "condition": "cook_recipe_category_baking >= 5"
            }
        ];
    },

    // 根据ID获取食材
    getIngredientById: function(id) {
        return this.ingredients.find(ingredient => ingredient.id === id);
    },

    // 根据ID获取配方
    getRecipeById: function(id) {
        return this.recipes.find(recipe => recipe.id === id);
    },

    // 根据名称获取配方
    getRecipeByName: function(name) {
        return this.recipes.find(recipe => recipe.name === name);
    },

    // 获取所有食材
    getAllIngredients: function() {
        return this.ingredients;
    },

    // 获取所有配方
    getAllRecipes: function() {
        return this.recipes;
    },

    // 获取特定类别的配方
    getRecipesByCategory: function(category) {
        return this.recipes.filter(recipe => recipe.category === category);
    }
});

// 导出单例实例
var dataManager = new DataManager();