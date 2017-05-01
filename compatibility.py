from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/alexa_friend")

def get_headlines():
    user_pass_dict = {'user': 'swolexaskill',
                      'passwd': '@lexaLifts',
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
    welcome_message = 'Hello, how can I help you?'
    return question(welcome_message)

#@ask.intent("AnswerIntent", convert={'answerString': 'string'})
#def answer(answerString):
 #   msg = 'Charlie blows Licorice'
  #  if 'best friend' in answerString:
   #    msg = "I'm sorry, I don't think we're compatible. Amazon is sending a return box.\
     #                       Please pack everything I came with and return ship the box with the included return label."
    #else:
     #  msg = "Please never talk to me again"
    #return statement(msg)

@ask.intent("YesIntent")
def share_headlines():
    headline_msg = "I'm sorry, I don't think we're compatible. Amazon is sending a return box. Please pack everything I came with and ship the box using the included return label."

    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Why did you ask me to run then?... bye'
    return statement(bye_text)
    
if __name__ == '__main__':
    app.run(debug=True)

