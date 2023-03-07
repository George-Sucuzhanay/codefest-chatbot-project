from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests
import json
import webbrowser

chatbot = ChatBot('MovieBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english.movies')

api_key = '4f62dc31b603b2fe2f73e09cddbfe121'
search_url = 'https://api.themoviedb.org/3/search/movie'
image_base_url = 'https://image.tmdb.org/t/p/w500/'

print("Hi, I'm MovieBot! What would you like to know?")

while True:
    user_input = input("You: ")
    
    if 'give me ' in user_input.lower() and ' movie recommendations' in user_input.lower():
        genre = user_input.lower().split('give me ')[1].split(' movie recommendations')[0]
        
        params = {'api_key': api_key, 'query': genre, 'page': 1}
        response = requests.get(search_url, params=params)
        data = json.loads(response.text)

        for result in data['results'][:5]:
            title = result['title']
            overview = result['overview']
            release_date = result['release_date']
            poster_path = result['poster_path']
            poster_url = image_base_url + poster_path if poster_path else ''
            print(f"{title} ({release_date})\n")
            print("MovieBot: Do you want to know more about this movie?")

            while True:
                user_input = input("You: ")
                
                if 'yes' in user_input.lower():
                    print(f"Overview: {overview}\n")
                    if poster_url:
                        print(f"Poster: {poster_url}\n")
                        print("MovieBot: Here's a link to the poster:")
                        webbrowser.open(poster_url)
                    print("MovieBot: Do you need any other recommendations?")
                    break
                
                elif 'no' in user_input.lower():
                    break
                
                else:
                    print("MovieBot: I'm sorry, I didn't understand. Please answer with yes or no.")
        
    else:
        bot_response = chatbot.get_response(user_input)
        print("MovieBot:", bot_response)
        print("MovieBot: Do you need any other help?")
        
    # End the conversation if the user says "bye"
    if 'bye' in user_input.lower():
        print("MovieBot: Goodbye!")
        break
