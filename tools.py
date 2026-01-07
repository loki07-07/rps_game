# Available moves in the game
AVAILABLE_GAME_MOVES = ["rock", "paper", "scissors", "bomb"]

def initialize_player_name(player_name_input: str, current_game_state: dict) -> dict:
    current_game_state["player_name"] = player_name_input.strip().title()
    return current_game_state


def validate_player_move(selected_move: str, current_game_state: dict, current_player: str) -> dict:
    if selected_move not in AVAILABLE_GAME_MOVES:
        return {"valid": False, "reason": "Invalid move"}

    if selected_move == "bomb":
        if current_player == "user" and current_game_state["user_used_bomb"]:
            return {"valid": False, "reason": "User bomb already used"}
        if current_player == "bot" and current_game_state["bot_used_bomb"]:
            return {"valid": False, "reason": "Bot bomb already used"}

    return {"valid": True}


def determine_round_winner(human_player_move: str, computer_player_move: str) -> str:
    if human_player_move == computer_player_move:
        return "draw"

    if human_player_move == "bomb":
        return "user"
    if computer_player_move == "bomb":
        return "bot"

    winning_move_combinations = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    return "user" if winning_move_combinations[human_player_move] == computer_player_move else "bot"


def update_game_state_after_round(current_game_state: dict, round_winner: str, human_player_move: str, computer_player_move: str) -> dict:
    if human_player_move == "bomb":
        current_game_state["user_used_bomb"] = True
    if computer_player_move == "bomb":
        current_game_state["bot_used_bomb"] = True

    if round_winner == "user":
        current_game_state["user_score"] += 1
    elif round_winner == "bot":
        current_game_state["bot_score"] += 1

    current_game_state["round"] += 1
    if current_game_state["round"] > 3:
        current_game_state["game_over"] = True

    return current_game_state
