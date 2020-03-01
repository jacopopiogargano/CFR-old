class CFR(metaclass=ABCMeta):
    def __init__(self, infoset_map, player_id_1, player_id_2, is_Random_Sampling):
        self.history_to_infosets = infoset_map
        self.player_id_1 = player_id_1
        self.player_id_2 = player_id_2
        self.is_Random_Sampling = is_Random_Sampling

    def cfr(self, real_state: list, history: list, player_id, prob_1: float, prob_2: float, t: int):
        """

        @param real_state: contains the private information of player1, player2
        @param history: the history reached
        @param player_id: the id of the player that CFR is running for
        @param prob_1: the probability of player 1 reaching the information set associated to the history
        @param prob_2: the probability of player 2 reaching the information set associated to the history
        @param t: the number of CFR iteration
        @return: the expected value for the information set
        """

        infoset = self.get_infoset(history, real_state)
        
        if self.is_player_1(history):
            assert infoset.state.get_current_player_id() == self.player_id_1
        else:
            assert infoset.state.get_current_player_id() == self.player_id_2

        if self.is_terminal(infoset):
            return infoset.get_utility_for_player(player_id)

        if self.is_chance(infoset):
            return self.handle_chance_infoset(real_state, history, player_id, prob_1, prob_2, t, infoset)

        exp_value = 0
        value = infoset.action_to_value
        sigma = infoset.action_to_sigma
        actions = infoset.get_actions()

        for a in actions:
            history_new = deepcopy(history)
            history_new.append(a)
            if self.is_player_1(history):
                value[a] = self.cfr(real_state, history_new, player_id,
                                    (sigma.get(t)).get(a) * prob_1, prob_2, t)
            else:
                value[a] = self.cfr(real_state, history_new, player_id, prob_1,
                                    (sigma.get(t)).get(a) * prob_2, t)
            exp_value += sigma[t][a] * value[a]
        
        if infoset.player_id == player_id:
            infoset.expected_value = exp_value

        # update strategy
        if infoset.get_current_player() == player_id:
            prob_player = prob_1 if self.is_player_1(history) else prob_2
            prob_opponent = prob_2 if self.is_player_1(history) else prob_1
            regret = infoset.action_to_regret
            strategy = infoset.action_to_strategy

            for a in actions:
                regret[a] += prob_opponent * (value.get(a) - exp_value)
                strategy[a] += prob_player * (sigma.get(t)).get(a)
            regret_sum = sum(max(x, 0) for x in regret.values())
            infoset.regret = max(regret.values())

            uniform_prob = 1 / len(actions)
            for a in actions:
                if regret_sum > 0:
                    (sigma.get(t + 1))[a] = max(regret[a], 0) / regret_sum
                else:
                    (sigma.get(t + 1))[a] = uniform_prob

        return exp_valu
e
    @abstractmethod
    def is_player_1(self, history):
        """
        @param history:
        @return: True if player 1 is the next one playing
        """
        pass

    def get_infoset(self, history, real_state):
        if self.is_player_1(history):
            private_info = real_state[0]
            key = [private_info]
            key.extend(history)
        else:
            assert len(history) > 0
            private_info = real_state[1]
            key = [history[0], private_info]
            if len(history) > 1:
                key.extend(history[1:])
        return self.history_to_infosets.get(tuple(key), None)

    def is_terminal(self, infoset: InformationSet):
        return infoset.is_terminal()

    def is_chance(self, infoset: InformationSet):
        return infoset.is_chance()

    @abstractmethod
    def handle_chance_infoset(self, real_state, history, player_id, prob_1, prob_2, t, infoset):
        pass