from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
import json

# create chatbot instance
bot = ChatBot('MovieBot')

# create a trainer
trainer = ListTrainer(bot)

# train the chatbot on some sample data
trainer.train([
    "Hello",
    "Hi there!",
    "What's your name?",
    "My name is MovieBot. How can I help you today?",
    "Can you recommend a movie for me?",
    "Can you give me a movie recommendation?",
    "Sure, what kind of movie are you in the mood for?"
])

# function to get movie recommendation from API
def get_movie_recommendation(genre):
    url = 'http://www.omdbapi.com/'
    api_key = '4d5aedd0'
    params = {'apikey': api_key, 's': genre, 'type': 'movie', 'r': 'json'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('Response') == 'True' and data.get('Search'):
            movie = data['Search'][0]
            return f"I recommend you watch {movie['Title']} ({movie['Year']})!"
    return "Sorry, I couldn't find any movies for that genre."

# function to get response from chatbot
def get_bot_response(user_input):
    response = bot.get_response(user_input)
    if 'movie' in response.text.lower():
        genre = input("What genre are you in the mood for? ")
        return get_movie_recommendation(genre)
    return response.text

# run the chatbot
while True:
    user_input = input("You: ")
  
    if user_input.lower() == 'bye':
        print("MovieBot: Goodbye!")
        break
    bot_response = get_bot_response(user_input)
    print("MovieBot:", bot_response)