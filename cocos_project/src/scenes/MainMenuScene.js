// Main Menu Scene for Little Gourmet Game

var MainMenuScene = cc.Scene.extend({
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        
        // 添加背景
        var background = new cc.LayerColor(cc.color(255, 240, 240, 255)); // 浅粉色背景
        this.addChild(background);
        
        // 添加标题
        var titleLabel = new cc.LabelTTF("Little Gourmet", "Arial", 48);
        titleLabel.setPosition(size.width / 2, size.height - 100);
        titleLabel.setColor(cc.color(200, 50, 50)); // 深红色文字
        this.addChild(titleLabel);
        
        // 添加玩家信息面板
        this.createPlayerInfoPanel(size);
        
        // 添加按钮
        var startButton = new cc.MenuItemFont("开始游戏", this.onStartGame, this);
        startButton.setFontSize(28);
        startButton.setPosition(size.width / 2, size.height / 2 + 50);
        
        var recipeButton = new cc.MenuItemFont("食谱手册", this.onRecipeBook, this);
        recipeButton.setFontSize(28);
        recipeButton.setPosition(size.width / 2, size.height / 2 - 20);
        
        var inventoryButton = new cc.MenuItemFont("背包", this.onInventory, this);
        inventoryButton.setFontSize(28);
        inventoryButton.setPosition(size.width / 2, size.height / 2 - 90);
        
        var quitButton = new cc.MenuItemFont("退出游戏", this.onQuit, this);
        quitButton.setFontSize(28);
        quitButton.setPosition(size.width / 2, size.height / 2 - 160);
        
        var menu = new cc.Menu(startButton, recipeButton, inventoryButton, quitButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
    },
    
    // 创建玩家信息面板
    createPlayerInfoPanel: function(size) {
        var playerInfo = playerManager.getPlayerInfo();
        
        // 创建一个半透明背景
        var infoBg = new cc.LayerColor(cc.color(255, 255, 255, 180), 300, 100);
        infoBg.setPosition(20, size.height - 130);
        this.addChild(infoBg);
        
        // 添加玩家信息文本
        var levelLabel = new cc.LabelTTF("等级: " + playerInfo.level, "Arial", 20);
        levelLabel.setAnchorPoint(0, 1);
        levelLabel.setPosition(30, size.height - 30);
        levelLabel.setColor(cc.color(0, 0, 0));
        this.addChild(levelLabel);
        
        var expLabel = new cc.LabelTTF("经验: " + playerInfo.experience, "Arial", 20);
        expLabel.setAnchorPoint(0, 1);
        expLabel.setPosition(30, size.height - 60);
        expLabel.setColor(cc.color(0, 0, 0));
        this.addChild(expLabel);
        
        var goldLabel = new cc.LabelTTF("金币: " + playerInfo.gold, "Arial", 20);
        goldLabel.setAnchorPoint(0, 1);
        goldLabel.setPosition(30, size.height - 90);
        goldLabel.setColor(cc.color(0, 0, 0));
        this.addChild(goldLabel);
    },
    
    // 开始游戏按钮回调
    onStartGame: function () {
        // 进入厨房场景
        cc.director.runScene(new KitchenScene());
    },
    
    // 食谱手册按钮回调
    onRecipeBook: function () {
        // 进入食谱手册场景
        cc.director.runScene(new RecipeBookScene());
    },
    
    // 背包按钮回调
    onInventory: function () {
        // 进入背包场景
        cc.director.runScene(new InventoryScene());
    },
    
    // 退出游戏按钮回调
    onQuit: function () {
        cc.log("退出游戏");
        // 在浏览器中无法真正退出，这里只是演示
    }
});