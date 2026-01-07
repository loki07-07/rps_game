def create_initial_game_state(): 
    return {
    "player_name": None,
    "round": 1,
    "user_score": 0,
    "bot_score": 0,
    "user_used_bomb": False,
    "bot_used_bomb": False,
    "game_over": False
}

default_game_state = create_initial_game_state()