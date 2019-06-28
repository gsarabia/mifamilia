from flask import Flask, render_template
from flask_ask import Ask, statement, question
import datetime
import logging

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def launch():
    welcome_text = render_template('welcome_text')
    return question(welcome_text)


@ask.intent('BirthdayIntent')
def birthday(firstname):
    if firstname is None:
        #no name was given
        ask_name_text = render_template('ask_name', detalle='el cumple')
        return question(ask_name_text)
        
    today = datetime.datetime.now()
    current_year = today.year

    name = firstname.lower()

    if name == 'violeta':
        next_bd = datetime.datetime(current_year, 8, 25)
    elif name == 'zuri':
        next_bd = datetime.datetime(current_year, 10, 31)
    elif name == 'evan':
        next_bd = datetime.datetime(current_year, 7, 28)
    elif name == 'gil':
        next_bd = datetime.datetime(current_year, 6, 12)
    else:
        next_bd = datetime.datetime.now()

    if today < next_bd:
        days =  next_bd - today
    else:
        days = datetime.datetime(current_year + 1, next_bd.month, next_bd.day) - today 


    days_left = days.days

    if days_left > 0:
        response_text = render_template('info_birthday', days=days_left, firstname=firstname)
    else:
        response_text = render_template('birthday', days=days_left, firstname=firstname)
    
    return statement(response_text).simple_card('Cumple', response_text)

if __name__ == '__main__':
    app.run(debug=True)
