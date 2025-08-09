// Game Scene for Little Gourmet Game

var GameScene = cc.Scene.extend({
    onEnter: function () {
        this._super();
        
        var size = cc.winSize;
        
        // Add background
        var background = new cc.LayerColor(cc.color(255, 255, 200, 255)); // Light yellow background
        this.addChild(background);
        
        // Add title
        var gameLabel = new cc.LabelTTF("Little Gourmet Game", "Arial", 28);
        gameLabel.setPosition(size.width / 2, size.height - 50);
        gameLabel.setColor(cc.color(0, 0, 0));
        this.addChild(gameLabel);
        
        // Add back button
        var backButton = new cc.MenuItemFont("Back to Menu", this.onBackToMenu, this);
        backButton.setFontSize(20);
        backButton.setPosition(100, size.height - 30);
        
        var menu = new cc.Menu(backButton);
        menu.setPosition(0, 0);
        this.addChild(menu);
        
        // Add cooking area
        this.createCookingArea();
    },
    
    createCookingArea: function() {
        var size = cc.winSize;
        
        // Add a simple cooking pot representation
        var pot = new cc.DrawNode();
        pot.drawCircle(cc.p(0, 0), 50, cc.color(100, 100, 100, 255), 10, false);
        pot.setPosition(size.width / 2, size.height / 2);
        this.addChild(pot);
        
        var potLabel = new cc.LabelTTF("Cooking Pot", "Arial", 16);
        potLabel.setPosition(size.width / 2, size.height / 2 - 80);
        potLabel.setColor(cc.color(0, 0, 0));
        this.addChild(potLabel);
    },
    
    onBackToMenu: function () {
        // Transition back to main menu
        cc.director.runScene(new MainMenuScene());
    }
});