from flask import Flask
from flask_ask import Ask, statement, question, session
import json, os
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

redUsr = os.environ['RED_USR']
redPas = os.environ['RED_PAS']

def get_headlines():
    user_pass_dict = {'user': redUsr,
                      'passwd': redPas,
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: Sentdex'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/news/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    print data
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles  

@app.route('/')
def homepage():
    return "hi there."

@ask.launch
def start_skill():
    welcome_message = 'Hello, would you like the news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Why did you ask me to run then?... bye'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)

