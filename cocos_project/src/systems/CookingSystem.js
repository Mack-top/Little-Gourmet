// CookingSystem.js - 烹饪系统

var CookingSystem = cc.Class.extend({
    ctor: function() {
        this.currentRecipe = null;
        this.currentStep = 0;
        this.isCooking = false;
    },

    // 开始制作配方
    startCooking: function(recipeId) {
        var recipe = dataManager.getRecipeById(recipeId);
        if (!recipe) {
            cc.log("配方未找到: " + recipeId);
            return false;
        }

        // 检查玩家是否解锁了这个配方
        if (!playerManager.isRecipeUnlocked(recipeId)) {
            cc.log("配方未解锁: " + recipe.name);
            return false;
        }

        // 检查玩家是否有足够的食材
        for (var i = 0; i < recipe.ingredients.length; i++) {
            var ingredient = recipe.ingredients[i];
            if (!playerManager.hasEnoughItems(ingredient.item_id, ingredient.quantity)) {
                var item = dataManager.getIngredientById(ingredient.item_id);
                cc.log("食材不足: 需要 " + ingredient.quantity + " 个 " + (item ? item.name : "未知食材"));
                return false;
            }
        }

        // 消耗食材
        for (var i = 0; i < recipe.ingredients.length; i++) {
            var ingredient = recipe.ingredients[i];
            playerManager.removeItemFromInventory(ingredient.item_id, ingredient.quantity);
        }

        // 设置当前配方
        this.currentRecipe = recipe;
        this.currentStep = 0;
        this.isCooking = true;

        cc.log("开始制作: " + recipe.name);
        return true;
    },

    // 获取当前步骤
    getCurrentStep: function() {
        if (!this.isCooking || !this.currentRecipe) {
            return null;
        }
        return {
            step: this.currentStep + 1,
            totalSteps: this.currentRecipe.steps.length,
            instruction: this.currentRecipe.steps[this.currentStep]
        };
    },

    // 下一步
    nextStep: function() {
        if (!this.isCooking || !this.currentRecipe) {
            return false;
        }

        this.currentStep++;

        if (this.currentStep >= this.currentRecipe.steps.length) {
            // 制作完成
            this.finishCooking();
            return false;
        }

        return true;
    },

    // 完成制作
    finishCooking: function() {
        if (!this.isCooking || !this.currentRecipe) {
            return false;
        }

        // 给玩家增加经验和金币
        playerManager.addExperience(this.currentRecipe.difficulty * 10);
        playerManager.addGold(this.currentRecipe.base_price);

        cc.log("制作完成: " + this.currentRecipe.name);
        cc.log("获得经验: " + (this.currentRecipe.difficulty * 10));
        cc.log("获得金币: " + this.currentRecipe.base_price);

        // 重置状态
        this.currentRecipe = null;
        this.currentStep = 0;
        this.isCooking = false;

        return true;
    },

    // 取消制作
    cancelCooking: function() {
        if (!this.isCooking) {
            return false;
        }

        // 这里可以添加返还部分食材的逻辑
        cc.log("制作已取消");

        // 重置状态
        this.currentRecipe = null;
        this.currentStep = 0;
        this.isCooking = false;

        return true;
    },

    // 检查是否正在制作中
    isInCooking: function() {
        return this.isCooking;
    }
});

// 导出单例实例
var cookingSystem = new CookingSystem();