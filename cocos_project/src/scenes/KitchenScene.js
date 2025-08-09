// Kitchen Scene for Little Gourmet Game

var KitchenScene = cc.Scene.extend({
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        
        // 添加背景
        var background = new cc.LayerColor(cc.color(255, 250, 230, 255)); // 浅黄色背景
        this.addChild(background);
        
        // 添加标题
        var titleLabel = new cc.LabelTTF("厨房", "Arial", 36);
        titleLabel.setPosition(size.width / 2, size.height - 50);
        titleLabel.setColor(cc.color(150, 100, 50));
        this.addChild(titleLabel);
        
        // 添加返回按钮
        var backButton = new cc.MenuItemFont("返回主菜单", this.onBackToMenu, this);
        backButton.setFontSize(20);
        backButton.setPosition(100, size.height - 30);
        
        var menu = new cc.Menu(backButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
        
        // 创建烹饪界面
        this.createCookingInterface(size);
    },
    
    // 创建烹饪界面
    createCookingInterface: function(size) {
        // 如果正在制作中，显示制作界面
        if (cookingSystem.isInCooking()) {
            this.showCookingInProgress(size);
        } else {
            // 否则显示选择配方界面
            this.showRecipeSelection(size);
        }
    },
    
    // 显示制作进行中的界面
    showCookingInProgress: function(size) {
        var stepInfo = cookingSystem.getCurrentStep();
        if (!stepInfo) return;
        
        // 显示步骤信息
        var stepLabel = new cc.LabelTTF("步骤 " + stepInfo.step + "/" + stepInfo.totalSteps, "Arial", 24);
        stepLabel.setPosition(size.width / 2, size.height / 2 + 100);
        stepLabel.setColor(cc.color(0, 0, 0));
        this.addChild(stepLabel);
        
        // 显示制作说明
        var instructionLabel = new cc.LabelTTF(stepInfo.instruction, "Arial", 20);
        instructionLabel.setPosition(size.width / 2, size.height / 2 + 50);
        instructionLabel.setColor(cc.color(0, 0, 0));
        this.addChild(instructionLabel);
        
        // 下一步按钮
        var nextButton = new cc.MenuItemFont("下一步", this.onNextStep, this);
        nextButton.setFontSize(24);
        nextButton.setPosition(size.width / 2, size.height / 2 - 50);
        
        // 取消按钮
        var cancelButton = new cc.MenuItemFont("取消", this.onCancelCooking, this);
        cancelButton.setFontSize(24);
        cancelButton.setPosition(size.width / 2, size.height / 2 - 120);
        
        var menu = new cc.Menu(nextButton, cancelButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
    },
    
    // 显示配方选择界面
    showRecipeSelection: function(size) {
        // 显示提示文本
        var selectLabel = new cc.LabelTTF("选择要制作的食谱", "Arial", 28);
        selectLabel.setPosition(size.width / 2, size.height / 2 + 150);
        selectLabel.setColor(cc.color(0, 0, 0));
        this.addChild(selectLabel);
        
        // 获取已解锁的配方
        var unlockedRecipes = playerManager.getUnlockedRecipes();
        var yPos = size.height / 2 + 100;
        
        // 为每个已解锁的配方创建按钮
        var menuItems = [];
        for (var i = 0; i < unlockedRecipes.length; i++) {
            var recipeId = unlockedRecipes[i];
            var recipe = dataManager.getRecipeById(recipeId);
            if (recipe) {
                var recipeButton = new cc.MenuItemFont(
                    recipe.name, 
                    this.onStartCooking.bind(this, recipeId), 
                    this
                );
                recipeButton.setFontSize(20);
                recipeButton.setPosition(size.width / 2, yPos);
                menuItems.push(recipeButton);
                yPos -= 50;
            }
        }
        
        // 如果没有已解锁的配方，显示提示
        if (menuItems.length === 0) {
            var noRecipesLabel = new cc.LabelTTF("暂无已解锁的食谱", "Arial", 20);
            noRecipesLabel.setPosition(size.width / 2, size.height / 2);
            noRecipesLabel.setColor(cc.color(100, 100, 100));
            this.addChild(noRecipesLabel);
        }
        
        // 添加"更多食谱"按钮
        var moreRecipesButton = new cc.MenuItemFont("更多食谱", this.onMoreRecipes, this);
        moreRecipesButton.setFontSize(20);
        moreRecipesButton.setPosition(size.width / 2, yPos - 50);
        menuItems.push(moreRecipesButton);
        
        var menu = new cc.Menu(menuItems);
        menu.setPosition(0, 0);
        this.addChild(menu);
    },
    
    // 开始制作按钮回调
    onStartCooking: function(recipeId) {
        if (cookingSystem.startCooking(recipeId)) {
            // 重新加载场景以显示制作界面
            cc.director.runScene(new KitchenScene());
        }
    },
    
    // 下一步按钮回调
    onNextStep: function() {
        if (!cookingSystem.nextStep()) {
            // 制作完成，返回选择界面
            cc.director.runScene(new KitchenScene());
        } else {
            // 更新界面显示下一步
            cc.director.runScene(new KitchenScene());
        }
    },
    
    // 取消制作按钮回调
    onCancelCooking: function() {
        cookingSystem.cancelCooking();
        // 返回选择界面
        cc.director.runScene(new KitchenScene());
    },
    
    // 更多食谱按钮回调
    onMoreRecipes: function() {
        cc.director.runScene(new RecipeBookScene());
    },
    
    // 返回主菜单按钮回调
    onBackToMenu: function () {
        // 如果正在制作中，先取消制作
        if (cookingSystem.isInCooking()) {
            cookingSystem.cancelCooking();
        }
        cc.director.runScene(new MainMenuScene());
    }
});