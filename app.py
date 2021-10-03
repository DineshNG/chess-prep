from flask import Flask, render_template, request, session, redirect, flash
import requests
from chessdotcom import get_player_profile, get_player_stats, get_player_game_archives, get_player_games_by_month_pgn
import pprint

printer = pprint.PrettyPrinter()


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


app = Flask(__name__)
app.secret_key = 'this_is_my_key_of_secrets'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        username = request.form.get('username')
        return redirect('/player/' + username)
    return render_template('index.html')


@app.route('/player/<string:username>', methods=['GET', 'POST'])
def player(username):
    if isValid(username):
        pgn = latestGame(username)
        player_profile = playerProfile(username)
        categories, player_stats = playerStats(username)
        return render_template('board.html', pgn=pgn, categories=categories, player_profile=player_profile,
                               player_stats=player_stats)
    else:
        flash("Username not found", "warning")
        return redirect('/')


@app.route('/tactics')
def tactics():
    return render_template('tactics.html')


if __name__ == '__main__':
    app.run(debug=True)
