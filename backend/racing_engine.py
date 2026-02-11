"""Racing game rules: same as frontend engine (advanceSteps, roll)."""

TRACK_LENGTH = 22
INITIAL_CONDITION = 6


def advance_steps(mode: str, dice: int, condition: int) -> int:
    if mode == "normal":
        return 2 if dice % 2 == 0 else 1
    return min(dice, max(0, condition))


def has_won(position: int) -> bool:
    return position >= TRACK_LENGTH


def is_game_over(condition: int) -> bool:
    return condition <= 0


def roll(position: int, condition: int, mode: str, dice: int) -> dict:
    steps = advance_steps(mode, dice, condition)
    new_position = position + steps
    new_condition = condition - 1 if mode == "super" else condition
    won = has_won(new_position)
    game_over = not won and is_game_over(new_condition)
    return {
        "steps": steps,
        "newPosition": new_position,
        "newCondition": new_condition,
        "won": won,
        "gameOver": game_over,
    }
