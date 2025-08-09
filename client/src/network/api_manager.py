# 客户端API管理器
import os
import json
import asyncio
from typing import Dict, Any, Optional, List

class APIManager:
    def __init__(self):
        # 确保保存目录存在
        self.save_dir = "saves/"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_game(self, slot_name, data):
        # 保存游戏进度
        try:
            file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False

    def load_game(self, slot_name):
        # 加载游戏进度
        try:
            file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return None

    def get_player_data(self, player_id):
        # 获取玩家数据
        try:
            file_path = os.path.join(self.save_dir, f"player_{player_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"获取玩家数据失败: {e}")
            return None

    def update_player_data(self, player_id, data):
        # 更新玩家数据
        try:
            file_path = os.path.join(self.save_dir, f"player_{player_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"更新玩家数据失败: {e}")
            return False
            
    def delete_save_slot(self, slot_name):
        # 删除存档
        try:
            file_path = os.path.join(self.save_dir, f"{slot_name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"删除存档失败: {e}")
            return False
            
    def list_save_slots(self):
        # 列出所有存档
        try:
            save_files = []
            if os.path.exists(self.save_dir):
                for file in os.listdir(self.save_dir):
                    if file.endswith('.json') and not file.startswith('player_'):
                        save_files.append(file[:-5])  # 移除.json后缀
            return save_files
        except Exception as e:
            print(f"列出存档失败: {e}")
            return []
            
    def save_exists(self, slot_name):
        # 检查存档是否存在
        file_path = os.path.join(self.save_dir, f"{slot_name}.json")
        return os.path.exists(file_path)
        
    # 新增RESTful API接口方法
    async def rest_get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        RESTful GET请求
        :param endpoint: API端点
        :param params: 请求参数
        :return: 响应数据
        """
        # 这里应该实现实际的HTTP GET请求
        # 暂时模拟返回数据
        return await self._simulate_api_response("GET", endpoint, params)
        
    async def rest_post(self, endpoint: str, data: Dict) -> Dict:
        """
        RESTful POST请求
        :param endpoint: API端点
        :param data: 请求数据
        :return: 响应数据
        """
        # 这里应该实现实际的HTTP POST请求
        # 暂时模拟返回数据
        return await self._simulate_api_response("POST", endpoint, data)
        
    async def rest_put(self, endpoint: str, data: Dict) -> Dict:
        """
        RESTful PUT请求
        :param endpoint: API端点
        :param data: 请求数据
        :return: 响应数据
        """
        # 这里应该实现实际的HTTP PUT请求
        # 暂时模拟返回数据
        return await self._simulate_api_response("PUT", endpoint, data)
        
    async def rest_delete(self, endpoint: str) -> Dict:
        """
        RESTful DELETE请求
        :param endpoint: API端点
        :return: 响应数据
        """
        # 这里应该实现实际的HTTP DELETE请求
        # 暂时模拟返回数据
        return await self._simulate_api_response("DELETE", endpoint, None)
        
    async def _simulate_api_response(self, method: str, endpoint: str, data: Any) -> Dict:
        """
        模拟API响应
        :param method: HTTP方法
        :param endpoint: 端点
        :param data: 数据
        :return: 模拟响应
        """
        # 模拟网络延迟
        await asyncio.sleep(0.1)
        
        # 根据端点返回不同的模拟数据
        response_data = {
            "method": method,
            "endpoint": endpoint,
            "timestamp": str(datetime.now()),
            "data": data or {},
            "status": "success"
        }
        
        return response_data