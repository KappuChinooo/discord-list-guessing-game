import asyncio 
from game.game import GameSession

class ChannelStateManager:
    def __init__(self):
        self.active_games = {}
        self._lock = asyncio.Lock()

    async def start_game(self, channel_id, mode, fav_num, hated_num):
        async with self._lock:
            if channel_id in self.active_games:
                raise ValueError("Channel already has an active game.")
            game = GameSession(mode, fav_num, hated_num)
            self.active_games[channel_id] = game
            return game
        
    async def end_game(self, channel_id):
        async with self._lock:
            if channel_id in self.active_games:
                del self.active_games[channel_id]

    def get_game(self, channel_id):
        return self.active_games.get(channel_id)