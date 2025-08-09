# 日记系统管理器
import godot
import json
import os
from datetime import datetime

class DiaryManager(godot.Node):
    def __init__(self):
        super().__init__()
        self.diary_entries = {}  # 日记条目
        self.mood_tracker = {}   # 心情追踪
        
        # 心情类型
        self.mood_types = {
            "happy": {"name": "开心", "icon": "😊", "color": "#FFD700"},
            "excited": {"name": "兴奋", "icon": "😄", "color": "#FF6347"},
            "calm": {"name": "平静", "icon": "😌", "color": "#87CEEB"},
            "tired": {"name": "疲惫", "icon": "😴", "color": "#708090"},
            "sad": {"name": "难过", "icon": "😢", "color": "#4682B4"}
        }
        
    def add_diary_entry(self, player_id, title, content, mood=None):
        """添加日记条目"""
        if player_id not in self.diary_entries:
            self.diary_entries[player_id] = []
            
        entry = {
            "id": len(self.diary_entries[player_id]) + 1,
            "title": title,
            "content": content,
            "mood": mood,
            "timestamp": datetime.now().isoformat(),
            "tags": self._extract_tags(content)
        }
        
        self.diary_entries[player_id].append(entry)
        
        # 记录心情
        if mood:
            self._track_mood(player_id, mood)
            
        godot.print(f"玩家 {player_id} 添加了日记: {title}")
        
        return entry
        
    def _extract_tags(self, content):
        """从内容中提取标签"""
        tags = []
        # 简单的标签提取，实际可以更复杂
        if "美容" in content or "护肤" in content:
            tags.append("美容")
        if "菜谱" in content or "烹饪" in content:
            tags.append("烹饪")
        if "朋友" in content or "社交" in content:
            tags.append("社交")
        if "装饰" in content or "布置" in content:
            tags.append("装饰")
        return tags
        
    def _track_mood(self, player_id, mood):
        """追踪心情"""
        if player_id not in self.mood_tracker:
            self.mood_tracker[player_id] = []
            
        self.mood_tracker[player_id].append({
            "mood": mood,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_diary_entries(self, player_id):
        """获取日记条目"""
        return self.diary_entries.get(player_id, [])
        
    def get_diary_entry(self, player_id, entry_id):
        """获取特定日记条目"""
        entries = self.get_diary_entries(player_id)
        for entry in entries:
            if entry["id"] == entry_id:
                return entry
        return None
        
    def get_mood_statistics(self, player_id):
        """获取心情统计"""
        if player_id not in self.mood_tracker:
            return {}
            
        mood_stats = {}
        for record in self.mood_tracker[player_id]:
            mood = record["mood"]
            mood_stats[mood] = mood_stats.get(mood, 0) + 1
            
        return mood_stats
        
    def get_favorite_mood(self, player_id):
        """获取最喜欢的心情"""
        mood_stats = self.get_mood_statistics(player_id)
        if mood_stats:
            return max(mood_stats, key=mood_stats.get)
        return None
        
    def get_mood_trend(self, player_id, days=7):
        """获取心情趋势"""
        if player_id not in self.mood_tracker:
            return []
            
        # 筛选最近几天的记录
        recent_records = []
        cutoff_date = datetime.now().date() - timedelta(days=days)
        
        for record in self.mood_tracker[player_id]:
            record_date = datetime.fromisoformat(record["timestamp"]).date()
            if record_date >= cutoff_date:
                recent_records.append(record)
                
        # 按日期分组
        trend = {}
        for record in recent_records:
            date = datetime.fromisoformat(record["timestamp"]).date()
            mood = record["mood"]
            if date not in trend:
                trend[date] = []
            trend[date].append(mood)
            
        return trend
        
    def get_diary_insights(self, player_id):
        """获取日记洞察"""
        entries = self.get_diary_entries(player_id)
        if not entries:
            return "还没有日记条目"
            
        insights = []
        
        # 统计信息
        total_entries = len(entries)
        insights.append(f"总共记录了 {total_entries} 篇日记")
        
        # 标签统计
        tag_count = {}
        for entry in entries:
            for tag in entry["tags"]:
                tag_count[tag] = tag_count.get(tag, 0) + 1
                
        if tag_count:
            favorite_tag = max(tag_count, key=tag_count.get)
            insights.append(f"最常记录的内容是: {favorite_tag}")
            
        # 心情洞察
        favorite_mood = self.get_favorite_mood(player_id)
        if favorite_mood and favorite_mood in self.mood_types:
            mood_info = self.mood_types[favorite_mood]
            insights.append(f"你最常感到: {mood_info['name']} {mood_info['icon']}")
            
        return "\n".join(insights)
        
    def search_diary(self, player_id, keyword):
        """搜索日记"""
        entries = self.get_diary_entries(player_id)
        results = []
        
        for entry in entries:
            if keyword.lower() in entry["title"].lower() or \
               keyword.lower() in entry["content"].lower():
                results.append(entry)
                
        return results
        
    def get_monthly_summary(self, player_id, year, month):
        """获取月度总结"""
        entries = self.get_diary_entries(player_id)
        month_entries = []
        
        for entry in entries:
            entry_date = datetime.fromisoformat(entry["timestamp"])
            if entry_date.year == year and entry_date.month == month:
                month_entries.append(entry)
                
        if not month_entries:
            return "本月没有日记条目"
            
        summary = f"{year}年{month}月总结:\n"
        summary += f"共记录 {len(month_entries)} 篇日记\n\n"
        
        # 心情统计
        mood_stats = {}
        for entry in month_entries:
            if entry["mood"]:
                mood = entry["mood"]
                mood_stats[mood] = mood_stats.get(mood, 0) + 1
                
        if mood_stats:
            summary += "本月心情分布:\n"
            for mood, count in mood_stats.items():
                if mood in self.mood_types:
                    mood_info = self.mood_types[mood]
                    summary += f"  {mood_info['icon']} {mood_info['name']}: {count}次\n"
                    
        return summary