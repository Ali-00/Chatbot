from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as s
import threading
import wikipedia
from playsound import playsound

engine = pp.init()

voices = engine.getProperty('voices')
print(voices)

engine.setProperty('voice', voices[1].id)

def speak(word):
    engine.say(word)
    engine.runAndWait()

bot = ChatBot(
    "My Bot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response':'0',
            'maximum_similarity_threshold': 0.90
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'play music',
            # 'output_text': '1',
            'response':'1',
            'maximum_similarity_threshold': 0.98
        }
    ]
)

convo = [
    'hello',
    'hi there !',
    'hi,How can i help you',
    'what is your name?',
    'My name is Bot, i am created by ali',
    'how are you?',
    'I am doing great these days',
    'Good',
    'thank you',
    'Welcome',
    'In which language you talk?',
    'I mostly talk in English.',
    'In which city you live ?',
    'I live in peshawar'
]

trainer = ListTrainer(bot)

# now training the bot with the help of trainer

trainer.train(convo)

# answer = bot.get_response('What is your name?')
# print(answer)

# print("Talk to bot")
# while True:
#     query = input()
#     if query == 'exit':
#         break
#     answer = bot.get_response(query)
#     print("bot : ",answer)

main = Tk()

main.geometry("500x650")

main.title("My Chat bot")

img = PhotoImage(file="bot.png")

photoL = Label(main, image=img)

photoL.pack(pady=5)

def takeQuery():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print("your bot is listening try to speak")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("Not recognized")

def ask_from_bot():
    query = textF.get()
    answer_from_bot = bot.get_response(query)
    if(str(answer_from_bot) != '0'):
        
        msgs.insert(END, "you : " + query + '\n')
        msgs.insert(END, "bot : " + str(answer_from_bot) + '\n')
        speak(answer_from_bot)
        textF.delete(0, END)
        msgs.yview(END)
    elif(str(answer_from_bot) == '1'):
        answer_from_bot = playsound('The_Break_Up_MashUp_Full_Video_Song_2014__DJ_Chetas.mp3')
        
    else:
        answer_from_bot = wikipedia.summary(query, sentences=4)
        msgs.insert(END, "you : " + query + '\n')
        msgs.insert(END, "bot : " + str(answer_from_bot) + '\n')
        speak(answer_from_bot)
        textF.delete(0, END)
        msgs.yview(END)


frame = Frame(main)

# sc = Scrollbar(frame,orient='vertical')
# msgs = Listbox(frame, width=80, height=20)
#
# sc.pack(side=RIGHT, fill=Y)
# msgs.pack(side=LEFT, fill=BOTH, pady=10)
sc=Scrollbar(frame)
sc.pack(side=RIGHT, fill=Y)

msgs=Text(frame, wrap=WORD, width=80, height=20)
msgs.pack(expand=1, fill=BOTH)

msgs.configure(yscrollcommand=sc.set)
sc.configure(command=msgs.yview)

frame.pack()

# creating text field

textF = Entry(main, font=("Verdana", 20))
textF.pack(fill=X, pady=10)

btn = Button(main, text="Ask from bot", font=("Verdana", 20), command=ask_from_bot)
btn.pack()

def enter_function(event):
    btn.invoke()

main.bind('<Return>', enter_function)

def repeatL():
    while True:
        takeQuery()

t = threading.Thread(target=repeatL)

t.start()

main.mainloop()
