// Recipe Book Scene for Little Gourmet Game

var RecipeBookScene = cc.Scene.extend({
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        
        // 添加背景
        var background = new cc.LayerColor(cc.color(245, 245, 220, 255)); // 米色背景
        this.addChild(background);
        
        // 添加标题
        var titleLabel = new cc.LabelTTF("食谱手册", "Arial", 36);
        titleLabel.setPosition(size.width / 2, size.height - 50);
        titleLabel.setColor(cc.color(100, 70, 20));
        this.addChild(titleLabel);
        
        // 添加返回按钮
        var backButton = new cc.MenuItemFont("返回", this.onBack, this);
        backButton.setFontSize(20);
        backButton.setPosition(100, size.height - 30);
        
        var menu = new cc.Menu(backButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
        
        // 显示食谱列表
        this.showRecipeList(size);
    },
    
    // 显示食谱列表
    showRecipeList: function(size) {
        var recipes = dataManager.getAllRecipes();
        var yPos = size.height - 150;
        var menuItems = [];
        
        for (var i = 0; i < recipes.length; i++) {
            var recipe = recipes[i];
            var isUnlocked = playerManager.isRecipeUnlocked(recipe.id);
            
            // 食谱名称（根据是否解锁显示不同颜色）
            var recipeLabel = new cc.LabelTTF(
                recipe.name + (isUnlocked ? "" : "（未解锁）"), 
                "Arial", 
                20
            );
            recipeLabel.setAnchorPoint(0, 0.5);
            recipeLabel.setPosition(50, yPos);
            recipeLabel.setColor(isUnlocked ? cc.color(0, 0, 0) : cc.color(150, 150, 150));
            this.addChild(recipeLabel);
            
            // 如果已解锁，添加查看详情按钮
            if (isUnlocked) {
                var detailButton = new cc.MenuItemFont(
                    "详情", 
                    this.showRecipeDetail.bind(this, recipe.id), 
                    this
                );
                detailButton.setFontSize(18);
                detailButton.setPosition(size.width - 100, yPos);
                menuItems.push(detailButton);
            }
            
            yPos -= 50;
            
            // 如果位置太低，停止添加更多项目
            if (yPos < 100) {
                break;
            }
        }
        
        if (menuItems.length > 0) {
            var menu = new cc.Menu(menuItems);
            menu.setPosition(0, 0);
            this.addChild(menu);
        }
    },
    
    // 显示食谱详情
    showRecipeDetail: function(recipeId) {
        cc.director.runScene(new RecipeDetailScene(recipeId));
    },
    
    // 返回按钮回调
    onBack: function() {
        cc.director.runScene(new MainMenuScene());
    }
});