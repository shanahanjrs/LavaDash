from nltk.classify import NaiveBayesClassifier, rte_classify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle

test_set = [
    ('hey call me so we can figure out where to eat', 'ham'),
    ('Youve won a free pair of tickets to the game! Reply to this text to claim', 'spam'),
    ('how you been', 'ham'),
    ('file your taxes today for free just go to freetaxfile.com', 'spam')
]

STOP_WORDS = set(stopwords.words('english'))
sms_spam_coll = []

"""
test_ham = 'Hey dude heres my phone num 561-911-4567'
print(f'Original sentence:\n{test_ham}')

tokenized_ham = word_tokenize(test_ham)
print(f'Tokenized sentence:\n{tokenized_ham}')

filtered_ham = [w for w in tokenized_ham if w not in STOP_WORDS]
print(f'Tokenized sentence with stopwords removed:\n{filtered_ham}')
"""

with open('training/datasets/SMSSpamCollection', 'r') as f:
    for l in f.readlines():
        if l.startswith('ham'):
            sms_spam_coll.append((l[4:], 'ham'))
        if l.startswith('spam'):
            sms_spam_coll.append((l[4:], 'spam'))

training_set = sms_spam_coll[:3000]
testing_set = sms_spam_coll[3000:]
classifier = NaiveBayesClassifier.train(training_set)
print(rte_classify.accuracy(classifier, training_set))
print(rte_classify.accuracy(classifier, testing_set))



#print(f'sms spam collection:\n{sms_spam_coll[:10]}')

