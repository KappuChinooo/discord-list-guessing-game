class Entry:
    def __init__(self, name):
        self.name: int | str = name
        self.owners: dict[int, bool] = {} # {player_id: favorited}
        self.revealed: bool = False
        self.guesses: dict[int, (int, bool)] = {} # {player_id: (owner_guess, favorited_guess)}
        self.scored: bool = False


class Player:
    def __init__(self, id, name = None):
        self.id: int = id
        self.name: str = name
        self.score: int  = 0