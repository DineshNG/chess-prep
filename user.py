from chessdotcom import (
    get_player_profile,
    get_player_stats,
    get_player_game_archives,
    get_player_games_by_month,
)
import requests


def playerProfile(username):
    """
    (['avatar', 'player_id', '@id', 'url', 'username', 'followers', 'country', 'last_online', 'joined',
    'status', 'is_streamer'])
    """

    response = get_player_profile(username)
    player = response.json["player"]
    return player


def playerStats(username):
    """
    {'last': {'rating': 1640, 'date': 1633184482, 'rd': 45},
     'best': {'rating': 1649,
    'date': 1632726714,
    'game': 'https://www.chess.com/game/live/26922645557'},
    'record': {'win': 660, 'loss': 530, 'draw': 67}}
    """
    data = get_player_stats(username).json["stats"]
    allcats = data.keys()
    mylist = ["chess_rapid", "chess_blitz", "chess_bullet"]
    categories = []
    for cat in allcats:
        if cat in mylist:
            categories.append(cat)
    return categories, data


def latestGame(username):
    data = get_player_game_archives(username).json["archives"]
    url = data[-1]
    games = requests.get(url).json()
    game = games["games"][-1]
    pgn = game["pgn"]
    return pgn


def isValid(username):
    try:
        response = get_player_profile(username)
        return True
    except:
        return False


def gamesbyMonth(username, year, month):
    """
    dict_keys(
        ['url','pgn','time_control','end_time','rated','tcn','uuid','initial_setup','fen','time_class','rules','white','black'])
    """
    BLITZ_ICON = "/static/img/blitz_icon.png"
    RAPID_ICON = "/static/img/rapid_icon.png"
    BULLET_ICON = "/static/img/bullet_icon.png"
    gamelist = []
    try:
        res = get_player_games_by_month(username, year, month)
        data = res.json["games"]
        if len(data) > 0:
            for game in data:
                icon_path = ""
                game_dict = {}
                result = "draw"
                game_dict["pgn"] = game["pgn"]
                game_dict["time"] = game["time_class"]
                if game["time_class"].casefold() == "rapid":
                    icon_path = RAPID_ICON
                elif game["time_class"].casefold() == "blitz":
                    icon_path = BLITZ_ICON
                elif game["time_class"].casefold() == "bullet":
                    icon_path = BULLET_ICON
                game_dict["icon"] = icon_path
                game_dict["white"] = game["white"]["username"]
                game_dict["black"] = game["black"]["username"]
                game_dict["url"] = game["url"]
                black_result = game["black"]["result"]
                white_result = game["white"]["result"]
                if game_dict["white"].casefold() == username.casefold():
                    if white_result == "win":
                        result = "win"
                    elif black_result == "win":
                        result = "lost"
                if game_dict["black"].casefold() == username.casefold():
                    if black_result == "win":
                        result = "win"
                    elif white_result == "win":
                        result = "lost"
                if result == "win":
                    result_color = "#30a153cf"
                if result == "lost":
                    result_color = "#ff3333"
                if result == "draw":
                    result_color = "#a5a5a5"
                game_dict["result_color"] = result_color
                gamelist.append(game_dict)
        return gamelist
    except:
        return gamelist
