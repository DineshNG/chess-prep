from flask import Flask, render_template, request, session, redirect, flash
import chess.engine
import os
import sys
import stat
from user import *


"""
App config section
"""

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
        return render_template('player.html', pgn=pgn, categories=categories, player_profile=player_profile,
                               player_stats=player_stats)
    else:
        flash("Username not found", "warning")
        return redirect('/')

@app.route('/player/<string:username>/games',methods=['GET','POST'])
def games(username):
    if request.method == "POST":
        pgn=""
        daymonth = request.form.get('daymonth')
        year = daymonth[0:4]
        month = daymonth[5:]
        gamelist = gamesbyMonth(username,year,month)
        gamelist.reverse()
        return render_template('games.html', pgn=pgn, gamelist = gamelist,username=username)



@app.route('/tactics')
def tactics():
    return render_template('tactics.html')

@app.route('/leaderboards')
def leaderboards():
    return render_template('leaderboards.html')

@app.route('/analyze',methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        pgn = request.form.get('analyze')
        return render_template('analyze.html',pgn=pgn)
    else:
        return render_template('analyze.html')

@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/make_move', methods = ['POST'])
def make_move():
    if sys.platform == "linux":
        os.chmod("./sf14", stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        engine = chess.engine.SimpleEngine.popen_uci("./sf14")
    else:
        engine = chess.engine.SimpleEngine.popen_uci("./sf14.exe")
    fen = request.form.get('data')
    board = chess.Board(fen)
    info = engine.play(board,chess.engine.Limit(time=1.0))
    board.push(info.move)
    return board.fen()

if __name__ == '__main__':
    app.run(debug=True,threaded = True)
