// PlayerManager.js - 玩家管理器

var PlayerManager = cc.Class.extend({
    ctor: function() {
        this.inventory = []; // 玩家库存
        this.recipesUnlocked = []; // 已解锁的配方
        this.achievementsUnlocked = []; // 已解锁的成就
        this.level = 1; // 玩家等级
        this.experience = 0; // 玩家经验
        this.gold = 100; // 玩家金币
        this.initializePlayer();
    },

    // 初始化玩家
    initializePlayer: function() {
        // 默认解锁一些基础配方
        this.recipesUnlocked.push(2); // 默认解锁煎蛋卷
        
        // 给玩家一些初始食材
        this.addItemToInventory(201, 5); // 面粉 x5
        this.addItemToInventory(301, 5); // 鸡蛋 x5
        this.addItemToInventory(401, 3); // 牛奶 x3
    },

    // 向库存中添加物品
    addItemToInventory: function(itemId, quantity) {
        var item = this.inventory.find(i => i.id === itemId);
        if (item) {
            item.quantity += quantity;
        } else {
            this.inventory.push({
                id: itemId,
                quantity: quantity
            });
        }
    },

    // 从库存中移除物品
    removeItemFromInventory: function(itemId, quantity) {
        var itemIndex = this.inventory.findIndex(i => i.id === itemId);
        if (itemIndex !== -1) {
            var item = this.inventory[itemIndex];
            if (item.quantity >= quantity) {
                item.quantity -= quantity;
                if (item.quantity === 0) {
                    // 如果数量为0，从库存中移除
                    this.inventory.splice(itemIndex, 1);
                }
                return true;
            }
        }
        return false; // 库存不足
    },

    // 检查是否有足够的物品
    hasEnoughItems: function(itemId, quantity) {
        var item = this.inventory.find(i => i.id === itemId);
        return item && item.quantity >= quantity;
    },

    // 获取库存中的物品数量
    getItemCount: function(itemId) {
        var item = this.inventory.find(i => i.id === itemId);
        return item ? item.quantity : 0;
    },

    // 获取玩家库存
    getInventory: function() {
        return this.inventory;
    },

    // 解锁配方
    unlockRecipe: function(recipeId) {
        if (!this.isRecipeUnlocked(recipeId)) {
            this.recipesUnlocked.push(recipeId);
            return true;
        }
        return false;
    },

    // 检查配方是否已解锁
    isRecipeUnlocked: function(recipeId) {
        return this.recipesUnlocked.includes(recipeId);
    },

    // 获取已解锁的配方
    getUnlockedRecipes: function() {
        return this.recipesUnlocked;
    },

    // 增加经验值
    addExperience: function(exp) {
        this.experience += exp;
        // 检查是否升级
        this.checkLevelUp();
    },

    // 检查升级
    checkLevelUp: function() {
        var expNeeded = this.level * 100; // 简单的升级公式
        if (this.experience >= expNeeded) {
            this.level++;
            this.experience -= expNeeded;
            // 可以在这里添加升级奖励
        }
    },

    // 增加金币
    addGold: function(amount) {
        this.gold += amount;
    },

    // 减少金币
    removeGold: function(amount) {
        if (this.gold >= amount) {
            this.gold -= amount;
            return true;
        }
        return false; // 金币不足
    },

    // 获取玩家信息
    getPlayerInfo: function() {
        return {
            level: this.level,
            experience: this.experience,
            gold: this.gold,
            inventoryCount: this.inventory.length,
            unlockedRecipesCount: this.recipesUnlocked.length
        };
    }
});

// 导出单例实例
var playerManager = new PlayerManager();