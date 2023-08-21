
import sys
import os

REPO_NAME = 'draft-assistant'
CWD = str(os.getcwd())
REPO_DIR = CWD[:CWD.find(REPO_NAME)+len(REPO_NAME)]
sys.path.insert(0,REPO_DIR)

import json
import pandas as pd
import numpy as np

from src.stats.offense import *

'''

Class to adapt draft recommendations to league settings and other criteria

'''


class League:

    def __init__(
            self,
            draft_position,
            n_teams,
            end_week = 18
    ):
        self.n_teams = n_teams
        self.draft_position = draft_position
        self.end_week = end_week

        # Load rosters config
        self.roster_settings = json.load(open(f'{REPO_DIR}/src/config/rosters.json'))
        self.scoring_settings = json.load(open(f'{REPO_DIR}/src/config/scoring.json'))

    def offense_fantasy_stats(self, pbp_data):
        # Offense
        POS = ['QB','WR','RB','TE']
        pbp_data = pbp_data[pbp_data['week'] <= self.end_week]
        pass_data = get_passing_stats_by_week(pbp_data)
        pass_data['fp'] = pass_data.apply(lambda x: \
            x['interception'] * self.scoring_settings['offense']['INT'] + \
            x['pass_touchdown'] * self.scoring_settings['offense']['PTD'] + \
            x['passing_yards'] * self.scoring_settings['offense']['PY']
            , axis = 1)

        rush_data = get_rushing_stats_by_week(pbp_data)
        rush_data['fp'] = rush_data.apply(lambda x: \
            x['rush_touchdown'] * self.scoring_settings['offense']['RTD'] + \
            x['rushing_yards'] * self.scoring_settings['offense']['RY']
            , axis = 1)

        rec_data = get_receiving_stats_by_week(pbp_data)
        rec_data['fp'] = rec_data.apply(lambda x: \
            x['receptions'] * self.scoring_settings['offense']['REC'] + \
            x['receiving_touchdown'] * self.scoring_settings['offense']['RETD'] + \
            x['receiving_yards'] * self.scoring_settings['offense']['REY']
            , axis = 1)

        fum_data = get_fumble_stats_by_week(pbp_data)
        fum_data['fp'] = fum_data.apply(lambda x: \
            x['fumbles'] * self.scoring_settings['offense']['FUML'], axis = 1)

        join_cols = [
            'season',
            'week',
            'posteam',
            'player_id'
        ]

        f_dfs = [pass_data, rush_data, rec_data]
        dfs = [df[join_cols] for df in f_dfs]
        base = pd.concat(dfs).drop_duplicates()
        for df in f_dfs:
            base = base.merge(df, how = 'left', on = join_cols)

        fp_cols = [c for c in base.columns if c.find('fp') > -1]
        base['FP'] = base.apply(lambda x:
            np.nansum([x[c] for c in fp_cols]), axis = 1)
        base = base[join_cols + ['FP']]

        return base.sort_values(['season','week','posteam','player_id'])