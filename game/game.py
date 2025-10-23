from models import Entry, Player
import asyncio
import random 
import config

class GameSession:
    def __init__(self, mode, fav_num, hated_num):
        self.mode = mode
        self.fav_num = fav_num
        self.hated_num = hated_num


        self.players: dict[int, Player] = {}
        self.list_owners: set[int] = ()
        self.entries: list[Entry] = []
        self._lock = asyncio.Lock()
        self.current_entry = None

    async def submit_entry(self, player_id, entry_name, category):
        if self.current_entry: 
            return
        async with self._lock:
            self.list_owners.add(player_id)
            existing = next((e for e in self.entries if e.name.strip().lower() == entry_name.strip().lower()), None)
            if existing:
                existing.owners[player_id] = category
            else:
                new_entry = Entry(entry_name)
                new_entry.owners[player_id] = category
                self.entries.append(new_entry)

    async def add_guess(self, player_id, owner_guess, favorited_guess):
        if self.current_entry is None:
            return
        player = self.players.setdefault(player_id, Player(player_id))
        async with self._lock:
            self.current_entry.guesses[player.id] = (owner_guess, favorited_guess)

    async def next_entry(self):
        unrevealed_entries = [entry for entry in self.entries if not entry.revealed]
        
        if not unrevealed_entries:
            return None
        
        async with self._lock():
            self.current_entry = random.choice(unrevealed_entries)
            self.current_entry.revealed = True
        
        return self.current_entry
    
    async def calculate_score(self, entry: Entry):
        OWNER_CORRECT_POINTS = config.OWNER_CORRECT_POINTS
        BOTH_CORRECT_POINTS = config.BOTH_CORRECT_POINTS

        if entry.scored:
            return
        
        score_log = {}

        async with self._lock:
            for player_id, (owner_guess, category_guess) in entry.guesses.items():
                if player_id in entry.owners and not config.can_score_on_own_list:
                    continue
                points_awarded = 0
                if owner_guess not in entry.owners:
                    score_log[player_id] = None
                    continue
                points_awarded += OWNER_CORRECT_POINTS
                if entry.owners[owner_guess] == category_guess:
                    points_awarded += BOTH_CORRECT_POINTS
                score_log[player_id] = points_awarded
                self.players[player_id].score += points_awarded
            entry.scored = True

    def get_scores(self):
        players_list = list(self.players.values())
        players_list.sort(key=lambda p: p.score, reverse=True)
        return players_list
    
    def is_game_over(self):
        return all(entry.scored for entry in self.entries)