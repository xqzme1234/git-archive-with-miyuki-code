#xqzme release v1.0.6
import random
import json
import nltk
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from telebot import types
from telebot import TeleBot
from sklearn.model_selection import train_test_split

TOKEN = '#####'

botik = TeleBot(TOKEN)


with open('BOT_CONFIG.json', encoding='utf-8') as f:
	BOT_CONFIG = json.load(f)

def classify_intent(replica):
	for intent in BOT_CONFIG['intents'].keys():
		for example in BOT_CONFIG['intents'][intent]['examples']:
			s1 = clean(replica)
			s2 = clean(example)
			if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
				return intent
	return 'intent not found :('

def get_answer_by_intent(intent):
	if intent in BOT_CONFIG['intents']:
		responses = BOT_CONFIG['intents'][intent]['responses']
		return random.choice(responses)


def clean(text):
	clean_text = ''
	for char in text.lower():
		if char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstvuwxyz -1234567890+-':
			clean_text = clean_text + char
	return clean_text

def generate_answer(replica):
	return get_intent_by_model(replica)

def get_stub():
	try:
		failure_phrases = BOT_CONFIG['failure_phrases']
		return random.choice(failure_phrases)
	except:
		failure_phrases = 'извините, я не умею на такое отвечать'
		return failure_phrases


def get_intent_by_model(text):
	pred = clf.predict(vectorizer.transform([text]))
	n = BOT_CONFIG['intents'][pred[0]]['responses']
	ansik = random.choice(n)
	return ansik

def get_intent(text):
	for intent in BOT_CONFIG['intents'].keys():
		for example in BOT_CONFIG['intents'][intent]['examples']:
			s1 = clean(text)
			s2 = clean(example)
			if nltk.edit_distance(s1, s2) / max(len(s1), len(s2)) < 0.4:
				return intent
	return 'intent not found :('

texts = []
intent_names = []

for intent, intent_data in BOT_CONFIG['intents'].items():
	for example in intent_data['examples']:
		texts.append(example)
		intent_names.append(intent)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

#print(len(vectorizer.get_feature_names_out())) 

#print(X.toarray())
vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
X2 = vectorizer2.fit_transform(texts)
vectorizer2.get_feature_names_out()
#print(X2.toarray())

clf = LogisticRegression().fit(X, intent_names)



n = 10
scores = []
for i in range(n):	
	X_train, X_test, y_train, y_test = train_test_split(X, intent_names, test_size=0.33)
	clf = LogisticRegression().fit(X_train, y_train)
	clf.fit(X_train, y_train)

	score = clf.score(X_test, y_test)
	scores.append(score)

print('.',sum(scores)/len(scores))
def bot(replica):
	intent = classify_intent(replica)

	if intent:
		answer = get_answer_by_intent(intent)
		if answer:	
			return answer
	answer = generate_answer(replica)
	if answer:
		return answer

	answer = get_stub()
	return answer


@botik.message_handler(commands=['start'])
def welcome(message):
	sti = open('welcome.webp', 'rb')
	botik.send_sticker(message.chat.id, sti)


	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('рандомное число🎲')
	item2 = types.KeyboardButton('ку')

	markup.add(item1, item2)

	botik.send_message(message.chat.id, 'добро пожаловать пользовать!)\nЯ - Miyuki!')

@botik.message_handler(content_types=['text'])
def kik(message):
	botik.send_message(message.chat.id, bot(str(message.text)))

botik.polling(none_stop=True)