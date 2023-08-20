
'''

Class to adapt draft recommendations to league settings and other criteria

'''


class League:

    def __init__(
            self,
            draft_position,
            n_teams
    ):
        self.n_teams = n_teams
        self.draft_position = draft_position
