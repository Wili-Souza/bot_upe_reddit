import praw
import os
from config import username, password, client_id, client_secret
from time import sleep
from best_answers import qa
from random import randint
from win32com.client import Dispatch #pip install pywin32
from datetime import datetime

bot_comment = "\n\n*Não me leve a sério, sou só um unibot*"

def init_talk():
    speak = Dispatch("SAPI.SpVoice")
    return speak

def bot_login():
    print("Logging in")
    r = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "Unibode comment responder bot v0.1")
    print("Logged in")
    return r

def save_as_replied(id):
    already_replied.append(id)
    with open("comments_replied_to.txt", "a") as f:
        f.write(id + "\n")

def is_a_question(comment, question):
    if '?' not in comment:
        return False

    i1 = comment.lower().find(question)
    i2 = comment.find('?')
    if i2 == -1:
        return False
    
    if '.' not in comment[i1:i2] and\
        ',' not in comment[i1:i2]:
        return True

def run_bot(r, already_replied):
    print("Obtaining comments...")
    print(already_replied)
    for comment in r.subreddit('UpeCaruaru').comments(limit=25):
        if comment.id in already_replied: # or comment.author == r.user.me():
            continue

        if "!emergência!" in comment.body or "!emergencia!" in comment.body:
            emergency_user = comment.author
            emergency_date = datetime.now()
            save_as_replied(comment.id)
            talk.Speak(f"Situação de emergência detectada por {emergency_user}")
            comment.reply("Situação de emergência informada.")

        #identificando pergunta
        for i in range(0, len(qa_data['q'])): # cada conjunto de perguntas
            for question in qa_data['q'][i]: # cada pergunta
                if question in comment.body.lower() and\
                    is_a_question(comment.body, question) and\
                    comment.author != username:

                    # comentando
                    if isinstance(qa_data['a'][i], str):
                        comment.reply("{} {}".format(qa_data['a'][i], bot_comment))
                        talk.Speak("Encontrado")
                    elif isinstance(qa_data['a'][i], list):
                        ranIdx = randint(0, len(qa_data['a'][i])-1)
                        comment.reply("{} {}".format(qa_data['a'][i][ranIdx], bot_comment))
                        talk.Speak("Encontrado")

                    save_as_replied(comment.id)
        
    sleep(10)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        already_replied = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            already_replied = f.read()
            already_replied = already_replied.split("\n")
            already_replied = [x for x in already_replied if x is not None and x != "" ]

    return already_replied

def get_qa_data(qa):
    qa_data = {
        'q': [],
        'a': [],
    }
    for item in qa:
        qa_data['q'].append(item['q'])
        qa_data['a'].append(item['a'])
    return qa_data

qa_data = get_qa_data(qa)
talk = init_talk()

# executing
already_replied = get_saved_comments()
r = bot_login()
while True:
    run_bot(r, already_replied)