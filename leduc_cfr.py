class LeducCFR(CFR):

    def is_player_1(self, history):
        action_count = 0
        for elem in history:
            if isinstance(elem, Actions):
                if elem != Actions.RANDOM:
                    action_count += 1
        if action_count % 2 == 0:  # if there is an even number of actions --> player 1
            return True
        else:
            return False

    def handle_chance_infoset(self, real_state, history, player_id, prob_1, prob_2, t, infoset: LeducInformationSet):
        exp_value = 0
        children = infoset.get_children(action=Actions.RANDOM)
        n_possibilities = len(children)
        assert n_possibilities != 0, "There are no children for a chance infoset"

        if self.is_Random_Sampling:
            child = children[randint(0, n_possibilities - 1)]
            public_card = child.state.public_card
            history_new = deepcopy(history)
            history_new.append(public_card)
            exp_value = self.cfr(real_state, history_new, player_id, prob_1, prob_2, t)
            infoset.expected_value = exp_value
            return exp_value
        else:
            for child in children:
                public_card = child.state.public_card
                history_new = deepcopy(history)
                history_new.append(public_card)
                exp_value += self.cfr(real_state, history_new, player_id, prob_1, prob_2, t)
            infoset.expected_value = exp_value / n_possibilities
            return exp_value / n_possibilities
