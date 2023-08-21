
BASE_COLS = [
        'season',
        'week',
        'posteam'
        ]

def get_passing_stats_by_week(pbp_data):
    # Need yards, td, interceptions
    id_cols = ['passer_player_id']
    cols = BASE_COLS + id_cols + [
        'interception',
        'pass_touchdown',
        'passing_yards',
    ]
    mask = (~pbp_data['passing_yards'].isna())
    gb_cols = BASE_COLS + id_cols
    res = pbp_data[cols][mask].groupby(gb_cols).sum().reset_index()
    res.rename(columns = {
                id_cols[0]:'player_id'
    }, inplace = True)
    return res

def get_rushing_stats_by_week(pbp_data):
    # Need yards, td
    id_cols = ['rusher_player_id']
    cols = BASE_COLS + id_cols + [
        'rushing_yards',
        'rush_touchdown'
    ]
    mask = (~pbp_data['rushing_yards'].isna())
    gb_cols = BASE_COLS + id_cols
    res = pbp_data[cols][mask].groupby(gb_cols).sum().reset_index()
    res.rename(columns = {
                id_cols[0]:'player_id'
    }, inplace = True)
    return res

def get_receiving_stats_by_week(pbp_data):
    # Need yards, rec, td
    id_cols = ['receiver_player_id']
    cols = BASE_COLS + id_cols + [
        'receiving_yards',
        'pass_touchdown',
        'receiver'
    ]
    mask = (~pbp_data['receiving_yards'].isna())
    pbp_data['receiver'] = 1
    gb_cols = BASE_COLS + id_cols
    res = pbp_data[cols][mask].groupby(gb_cols).sum().reset_index()
    res.rename(columns = {
        id_cols[0]:'player_id',
        'receiver':'receptions',
        'pass_touchdown':'receiving_touchdown'}, inplace = True)
    return res

def get_fumble_stats_by_week(pbp_data):
    id_cols = ['fumbled_1_player_id']
    cols = BASE_COLS + id_cols + [
        'desc'
    ]
    gb_cols = BASE_COLS + id_cols
    pbp_data['desc'] = 1
    mask = ~pbp_data['fumbled_1_player_id'].isna()
    res = pbp_data[cols][mask].groupby(gb_cols).sum().reset_index()
    res.rename(columns = {
        'desc':'fumbles',
        id_cols[0]:'player_id'
    }, inplace = True)
    return res
