#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

# read secret key from file
with open('.secretkey') as file:
    app.secret_key = file.read().strip()

cache = {}

# default route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# route new_game
@app.route('/new-game', methods=['POST'])
def new_game():
    start = request.form['start']

    if not start or start.strip() == '':
        flash('Enter a title! :/', 'error')
        return redirect('/')
    else:
        session['article'] = start
        session['score'] = 0
        return redirect('/game')

# route game
@app.route('/game', methods=['GET'])
def game():
    if 'article' not in session.keys():
        return redirect('/')
    
    article = session['article']
    if not (article in cache.keys()):
        cache[article] = getPage(article)
    
    title, links = cache[article]
    session['possible_moves'] = links
    score = session['score']

    # Le first page requested doesn't exist
    if score == 0:
        if title == None or links == []:
            flash('The requested page doesn\'t exist or it doesn\'t contain any links :(', 'error')
            return redirect('/')
        elif title == 'Rome':
            flash('Nice try, you can\'t start with page Rome :/', 'error')
            return redirect('/')

    # we fall into a dead end
    if links == []:
        flash('You\'ve fallen on a page without any links, you have lost :(', 'error')
        return redirect('/')

    # we found the page Rome
    if title == 'Rome':
        flash(f'You made it to Rome!! Your score is {score} :)', 'success')
        return redirect('/')

    return render_template('game.html', title=title, links=enumerate(links), score=score)

# route move
@app.route('/move', methods=['POST'])
def move():
    # the score shouldn't change, otherwise we don't do anything
    if session['score'] == int(request.form['score']):
        destination = request.form['destination']
        # we make sure that the rquested page is a possible move
        if destination in session['possible_moves']:
            session['article'] = destination
            session['score'] += 1

    return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)

