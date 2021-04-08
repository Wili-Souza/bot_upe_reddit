import praw
import os
from config import username, password, client_id, client_secret
from service import get_qa, get_ids, get_commands, save_as_replied
from time import sleep
from best_answers import qa
from random import randint
from datetime import datetime

bot_comment = "\n\n*Não me leve a sério, sou só um unibot*"

def bot_login():
    print("Logging in")
    r = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "Unibode comment responder bot v0.1")
    print("Logged in")
    return r

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

def run_bot(r):
    print("Getting fresh and clean data...")
    qa_data = get_qa_data()
    commands = get_commands()
    already_replied = get_ids()

    print("Obtaining new comments...")
    for comment in r.subreddit('UpeCaruaru').comments(limit=25):
        if comment.id in already_replied or comment.author == r.user.me():
            continue

        for command in commands:
            if command["value"] in comment.body:
                # emergency_user = comment.author
                comment.reply(command["comment"])
                save_as_replied(comment.id)

        #identificando pergunta
        for i in range(0, len(qa_data['q'])): # cada conjunto de perguntas
            for question in qa_data['q'][i]: # cada pergunta
                if question in comment.body.lower() and\
                    is_a_question(comment.body, question):

                    # comentando
                    if len(qa_data['a']) > 1:
                        ranIdx = randint(0, len(qa_data['a'][i])-1)
                        comment.reply("{} {}".format(qa_data['a'][i][ranIdx], bot_comment))
                    elif len(qa_data['a']) > 0:
                        comment.reply("{} {}".format(qa_data['a'][i][0], bot_comment))
                    else:
                        comment.reply("Buguei :/", bot_comment)

                    save_as_replied(comment.id)

def get_qa_data():
    qa = get_qa()
    qa_data = {
        'q': [],
        'a': [],
    }
    for item in qa:
        qa_data['q'].append(item['q'])
        qa_data['a'].append(item['a'])
    return qa_data

# --- executing
r = bot_login()
while True:
    run_bot(r)
