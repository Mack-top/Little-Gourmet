// Recipe Detail Scene for Little Gourmet Game

var RecipeDetailScene = cc.Scene.extend({
    ctor: function(recipeId) {
        this._super();
        this.recipeId = recipeId;
    },
    
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        var recipe = dataManager.getRecipeById(this.recipeId);
        
        if (!recipe) {
            // 如果食谱不存在，返回食谱手册
            cc.director.runScene(new RecipeBookScene());
            return;
        }
        
        // 添加背景
        var background = new cc.LayerColor(cc.color(255, 250, 240, 255)); // 浅橙色背景
        this.addChild(background);
        
        // 添加标题
        var titleLabel = new cc.LabelTTF(recipe.name, "Arial", 32);
        titleLabel.setPosition(size.width / 2, size.height - 60);
        titleLabel.setColor(cc.color(200, 100, 50));
        this.addChild(titleLabel);
        
        // 添加描述
        var descLabel = new cc.LabelTTF(recipe.description, "Arial", 18);
        descLabel.setPosition(size.width / 2, size.height - 100);
        descLabel.setColor(cc.color(80, 80, 80));
        this.addChild(descLabel);
        
        // 添加难度和时间信息
        var infoLabel = new cc.LabelTTF(
            "难度: " + recipe.difficulty + "    时间: " + recipe.time_required + "分钟", 
            "Arial", 
            18
        );
        infoLabel.setPosition(size.width / 2, size.height - 140);
        infoLabel.setColor(cc.color(0, 0, 0));
        this.addChild(infoLabel);
        
        // 添加所需食材标题
        var ingredientsTitle = new cc.LabelTTF("所需食材:", "Arial", 22);
        ingredientsTitle.setPosition(100, size.height - 190);
        ingredientsTitle.setAnchorPoint(0, 0.5);
        ingredientsTitle.setColor(cc.color(0, 0, 0));
        this.addChild(ingredientsTitle);
        
        // 添加食材列表
        var yPos = size.height - 230;
        for (var i = 0; i < recipe.ingredients.length; i++) {
            var ingredientInfo = recipe.ingredients[i];
            var ingredient = dataManager.getIngredientById(ingredientInfo.item_id);
            var ingredientName = ingredient ? ingredient.name : "未知食材";
            
            var ingredientLabel = new cc.LabelTTF(
                ingredientName + " x " + ingredientInfo.quantity,
                "Arial",
                18
            );
            ingredientLabel.setPosition(120, yPos);
            ingredientLabel.setAnchorPoint(0, 0.5);
            ingredientLabel.setColor(cc.color(0, 0, 0));
            this.addChild(ingredientLabel);
            
            yPos -= 30;
        }
        
        // 添加制作步骤标题
        var stepsTitle = new cc.LabelTTF("制作步骤:", "Arial", 22);
        stepsTitle.setPosition(100, yPos - 30);
        stepsTitle.setAnchorPoint(0, 0.5);
        stepsTitle.setColor(cc.color(0, 0, 0));
        this.addChild(stepsTitle);
        
        // 添加步骤列表
        yPos -= 70;
        for (var i = 0; i < recipe.steps.length; i++) {
            var stepLabel = new cc.LabelTTF(
                (i + 1) + ". " + recipe.steps[i],
                "Arial",
                18
            );
            stepLabel.setPosition(120, yPos);
            stepLabel.setAnchorPoint(0, 0.5);
            stepLabel.setColor(cc.color(0, 0, 0));
            this.addChild(stepLabel);
            
            yPos -= 30;
        }
        
        // 添加返回按钮
        var backButton = new cc.MenuItemFont("返回", this.onBack, this);
        backButton.setFontSize(20);
        backButton.setPosition(100, size.height - 30);
        
        // 添加制作按钮（如果玩家已解锁该食谱）
        var menuItems = [backButton];
        if (playerManager.isRecipeUnlocked(this.recipeId)) {
            var cookButton = new cc.MenuItemFont("开始制作", this.onStartCooking, this);
            cookButton.setFontSize(24);
            cookButton.setPosition(size.width - 150, 100);
            menuItems.push(cookButton);
        }
        
        var menu = new cc.Menu(menuItems);
        menu.setPosition(0, 0);
        this.addChild(menu);
    },
    
    // 返回按钮回调
    onBack: function() {
        cc.director.runScene(new RecipeBookScene());
    },
    
    // 开始制作按钮回调
    onStartCooking: function() {
        cc.director.runScene(new KitchenScene());
        // 延迟一下再开始制作，让场景切换完成
        this.scheduleOnce(function() {
            cookingSystem.startCooking(this.recipeId);
        }, 0.1);
    }
});