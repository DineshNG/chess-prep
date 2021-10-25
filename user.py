from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives, get_player_games_by_month
import requests

def playerProfile(username):
    """
    (['avatar', 'player_id', '@id', 'url', 'username', 'followers', 'country', 'last_online', 'joined',
    'status', 'is_streamer'])
    """

    response = get_player_profile(username)
    player = response.json['player']
    return player

def playerStats(username):
    """
    {'last': {'rating': 1640, 'date': 1633184482, 'rd': 45},
     'best': {'rating': 1649,
    'date': 1632726714,
    'game': 'https://www.chess.com/game/live/26922645557'},
    'record': {'win': 660, 'loss': 530, 'draw': 67}}
    """
    data = get_player_stats(username).json['stats']
    allcats = data.keys()
    mylist = ['chess_rapid', 'chess_blitz', 'chess_bullet']
    categories = []
    for cat in allcats:
        if cat in mylist:
            categories.append(cat)
    return categories, data

def latestGame(username):
    data = get_player_game_archives(username).json['archives']
    url = data[-1]
    games = requests.get(url).json()
    game = games['games'][-1]
    pgn = game['pgn']
    return pgn

def isValid(username):
    try:
        response = get_player_profile(username)
        return True
    except:
        return False

def gamesbyMonth(username, year, month):
    gamelist = []
    try:
        res = get_player_games_by_month(username, year, month)
        data = res.json['games']
        if (len(data) > 0):
            for game in data:
                game_dict = {}
                game_dict['pgn'] = game['pgn']
                game_dict['time'] = game['time_class']
                game_dict['white'] = game['white']['username']
                game_dict['black'] = game['black']['username']
                game_dict['url'] = game['url']
                gamelist.append(game_dict)
        return gamelist
    except:
        return gamelist
