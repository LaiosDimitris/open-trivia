import requests
import random
import html

def get_question():
    categories = {
        "General Knowledge": 9,
        "Movies": 11,
        "Video Games": 15,
        "Science and Nature": 17,
        "Science and Computers": 18,
        "Mythology": 20,
        "Geography": 22,
        "History": 23,
        "Anime and Manga": 31
    }

    category = random.choice(list(categories.keys()))
    difficulty = random.choice(['easy', 'medium', 'hard'])

    url = f'https://opentdb.com/api.php?amount=1&category={categories[category]}&difficulty={difficulty}&type=multiple'

    response = requests.get(url).json()['results'][0]

    answers = [
        html.unescape(response['incorrect_answers'][0]),
        html.unescape(response['incorrect_answers'][1]),
        html.unescape(response['incorrect_answers'][2]),
        html.unescape(response['correct_answer'])
    ]

    random.shuffle(answers)

    return {
        "category": category.replace('and', '&'),
        "category_image": fr"..\data\images\{category.replace('&', 'and')}.png",
        "difficulty": response['difficulty'],
        "question": html.unescape(response['question']),
        "correct_answer": html.unescape(response['correct_answer']),
        "answers": answers
    }
    