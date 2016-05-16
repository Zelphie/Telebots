"""
This is a detailed example using almost every command of the API
"""

import telebot
from telebot import types
import time
import random

TOKEN = '239988627:AAF_hGPeXGJ0nIwU1Trng9iHctlWiS0C2IE'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

questions = ["Is Kynaston awesome?", "Isn't telegram cool?", "What loses its head in the morning and gets it back at night?",
            "What can you catch but not throw?", "Give me food, and I will live. Give me water, and I will die. What am I?",
            "What is the center of gravity?", "I'm many people's favorite place, even though many don't remember their stay. You'll love to come but hate to leave, if you get cold use my sleeves. What am I?",
            "What's orange and sounds like a parrot?", "What is so delicate that even mentioning it breaks it?", "You use a knife to slice my head and weep beside me when I am dead. What am I?",
            "What has a single eye but cannot see?", "I'm light as a feather, yet the strongest man can't hold me for more than 5 minutes. What am I?",
            "Without fingers, I point, without arms, I strike, without feet, I run. What am I?", "I am an instrument that you can hear, but you can not touch or see me. What am I?",
            "I have a name that's not mine, and no one cares about me in their prime. People cry at my sight, and lie by me all day and night. What am I?",
            "What building has the most stories?", "I am a small room, but no life lives inside. No matter what weather looms, very cold my residents reside. What am I?",
            "A mirror for the famous, but informative to all. I'll show you the world, but it may be a bit small.", 
            "I am the beginning of the end, the end of every place. I am the beginning of eternity, the end of time and space. What am I?",
            "There is an ancient invention still used in some parts of the world today that allows people to see through walls. What is it?", "Different lights make me strange. For each one my size will change. What am I?",
            "I cannot hear or see, but sense light and sounds there may be. Sometimes i end up on the hook, or even deep inside a book. What am I?"
            ]

answers = ["yes", "yes", "pillow", "cold", "fire", "v", "bed", "carrot", "silence", "onion", "needle", "breath", "clock", "voice", "tombstone", "library",
            "refrigerator", "television", "e", "window", "pupil", "worm"

]

commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Gives you information about the available commands',
              'play' : '''Starts a game of "What am I?" ''',
              #'setQuestion' : 'Allows you to set a question',
              #'viewQuestions' : 'Allows you to view all questions',
              #'sendLongText': 'A test using the \'send_chat_action\' command',
              #'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
}


r = random.randint(0, len(questions)-1)

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('A', 'B', 'C','D')

hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print "New user detected, who hasn't used \"/start\" yet"
        return 0

def generate_rand():
    global r
    r = random.randint(0, len(questions)-1)

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener




# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, m.chat.first_name + ", I already know you, no need for me to scan you again!")




# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page





# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


# user can view questions
@bot.message_handler(commands=['viewQuestions'])
def view_questions(m):
    cid = m.chat.id
    bot.send_message(cid, "Questions are: " + str(questions))


# user can upload questions with answers (multi-stage command)
@bot.message_handler(commands=['setQuestion'])
def command_setQuestion(m):
    cid = m.chat.id
    bot.send_message(cid, "Please type the question.")
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# add question to list
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def get_question(m):
    cid = m.chat.id
    text = m.text
    questions.append(text)

    if '?' in text:  
        bot.send_message(cid, "Now tell me the answer.")
        userStep[cid] = 2
    else:
        bot.send_message(cid, "Your question needs to some work. Try ending with a question mark!")

# add answer to list
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 2)
def get_answer(m):
    cid = m.chat.id
    text = m.text
    answers.append(text)

    bot.send_message(cid, "Great! I've recorded the question.")


# user can start the trivia
@bot.message_handler(commands=['play'])
def play_trivia(m):
    cid = m.chat.id
    bot.send_message(cid, "Welcome to a new game of trivia, " + m.chat.first_name + "!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Type start when you are ready!")

@bot.message_handler(func=lambda message: message.text.lower() == 'start')
def give_question(m):
    cid = m.chat.id
    generate_rand()
    bot.send_message(cid, "Question: " + str(questions[r]))
    userStep[cid] = 4

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 4)
def check_ans(m):
    cid = m.chat.id
    text = m.text.lower()

    if text == str(answers[r]):
        bot.send_message(cid, "Correct! Next question.")
        bot.send_chat_action(cid, 'typing')
        give_question(m)
    else:
        bot.send_message(cid, "Wrong! Try again.")

# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['getImage'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Which do you prefer?", reply_markup=imageSelect)  # show the keyboard
    userStep[cid] = 4  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 5)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text

    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'upload_photo')

    if text == "A":  # send the appropriate image based on the reply to the "/getImage" command
        bot.send_photo(cid, open('rooster.jpg', 'rb'),
                       reply_markup=hideBoard)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
    elif text == "B":
        bot.send_photo(cid, open('kitten.jpg', 'rb'), reply_markup=hideBoard)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Don't type bullsh*t, if I give you a predefined keyboard!")
        bot.send_message(cid, "Please try again")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Hi there! Wanna have a go at some riddles? Type /play to start a game!")





# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()
