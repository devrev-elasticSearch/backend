from spellchecker import SpellChecker
import re
import requests
from dotenv import load_dotenv
import os
load_dotenv()

apiKey = os.getenv("googleApiKey")

def translate(api_key: str, text: str, target_language: str) -> str:
    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    
    try:
        response = requests.post(url, json={"q": text, "target": target_language})
        response.raise_for_status()
        
        translated_text = response.json()["data"]["translations"][0]["translatedText"]
        return translated_text
    except Exception as error:
        print('Error translating text:', error)
        return text  # Return the original text in case of error


def translate_review_to_english(sentence):
    # Check if the sentence is in English (assuming sentences in English have fewer than 10% non-ASCII characters)
    if sum(1 for char in sentence if ord(char) > 127) / len(sentence) > 0.1:
        translated_sentence = translate(sentence)
        return translated_sentence
    return sentence

def has_spelling_mistakes(review, word_count):
    spell = SpellChecker()
    words = review.split()

    # Get misspelled words
    misspelled = spell.unknown(words)
    for word in words:
        if bool(re.search(r'(.)\1{3,}', word)):
            return True

    # Define a threshold for the number of spelling mistakes
    threshold = 0.3

    # Return True if there are lots of spelling mistakes
    return len(misspelled)/word_count > threshold


def spam_check(review):
    # review = translate_review_to_english(review)
    word_count = len(review.split())
    if word_count < 10:
        return None
    
    review = re.sub(r'[^a-zA-Z0-9\s]', '', review)
    if has_spelling_mistakes(review, word_count):
        return None

    return review