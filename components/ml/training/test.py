import spacy

def is_spam(n):
    if n.cats['spam'] > 0.5:
        return 'SPAM'
    return 'HAM'

spam_text = 'Reply to this text message for free tickets to the game!'
ham_text = 'Hey bro what you up to'


nlp = spacy.load('trained_model_2.spacy')
# Start up spacy and get some shit loaded
#nlp = spacy.load('trained_model.spacy')
doc = nlp(spam_text)
print('Spam text: {}'.format(spam_text))
print(doc.cats)
print(is_spam(doc))
doc2 = nlp(ham_text)
print('Ham text: {}'.format(ham_text))
print(doc2.cats)
print(is_spam(doc2))

