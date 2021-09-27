from flask import Flask, render_template, request, session, redirect
import requests
from chessdotcom import get_player_profile,get_player_stats,get_player_game_archives,get_player_games_by_month_pgn
import pprint
printer = pprint.PrettyPrinter()

def getPlayerDetails(username):
    data = get_player_stats(username).json['stats']
    categories = ['chess_rapid', 'chess_blitz', 'chess_bullet']
    for category in categories:
        print(f" CATEGORY: {category} ")
        print(f" CURRENT RATING: {data[category]['last']['rating']} ")
        print(f" PEAK RATING: {data[category]['best']['rating']} ")
        print(f" RECORD: {data[category]['record']} ")

def get_most_recent_game(username):
    data = get_player_game_archives(username).json['archives']
    url = data[-1]
    games = requests.get(url).json()
    game = games['games'][-1]
    # print(game)
    # print(url)
    pgn = game['pgn']
    print(pgn)
    return pgn

get_most_recent_game("dineshNG")

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def home():
    if request.method == "POST":
        username = request.form.get('username')
        pgn = get_most_recent_game(username)
        return render_template('board.html',pgn = pgn)
    return render_template('board.html')

app.run(debug=True)

