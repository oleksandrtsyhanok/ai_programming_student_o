def minimax(env, player):
    winner = env.check_winner()
    if winner == "X":
        return -1, None
    elif winner == "O":
        return 1, None
    elif winner == "draw":
        return 0, None

    best_move = None

    if player == "O":
        best_score = -float("inf")
        for action in env.available_actions():
            new_env = env.copy()
            new_env.make_move(action, "O")
            score, _ = minimax(new_env, "X")
            if score > best_score:
                best_score = score
                best_move = action
    else:
        best_score = float("inf")
        for action in env.available_actions():
            new_env = env.copy()
            new_env.make_move(action, "X")
            score, _ = minimax(new_env, "O")
            if score < best_score:
                best_score = score
                best_move = action

    return best_score, best_move