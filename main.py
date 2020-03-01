if __name__ == '__main__':
    # the implementation of how to make history_to_infosets is domain-specific
    c = LeducCFR(history_to_infosets, Players.P1, Players.P2, False)

    for t in range(1, N_ITERATIONS + 1):
        print("iter: " + str(t))
        for infoset in history_to_infosets.values():
            if not infoset.is_terminal():
                infoset.action_to_sigma[t + 1] = deepcopy(infoset.action_to_sigma.get(t))
        for player_id in Players:
            # the implementation of getRealState() is domain-specific
            real_state = getRealState()
            c.cfr(real_state, [], player_id, 1, 1, t)
        for infoset in history_to_infosets.values():
            if not infoset.is_terminal():
                del infoset.action_to_sigma[t]

    if PRINT_STRATEGY:
        print("\n\n\nSTRATEGY\n")
        for infoset in history_to_infosets.values():
            if infoset.is_terminal() or infoset.is_chance():
                continue
            strategy = infoset.action_to_strategy
            print(str(infoset.player_id) + " " + str(infoset.id))
            norm = 0
            for a, p in strategy.items():
                norm += p
            if norm == 0:
                continue
            for a, p in strategy.items():
                print("A: " + str(a) + " --> " + str(p / norm))