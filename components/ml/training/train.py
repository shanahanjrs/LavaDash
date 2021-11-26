import spacy
import random
import pandas as pd

spacy.prefer_gpu()

MODEL_NAME = 'sms_spam_collection_trained.model'
TRAINING_ITERATIONS = 10


def spam_ham_to_int(x):
    """
    1 == spam
    0 == ham
    """
    ret = {
        'cats': {'spam': 1 if x == 'spam' else 0}
    }
    return ret


# Start up a DF obj and get it formatted nicely
with open("datasets/SMSSpamCollection", encoding="utf8") as f:
    df = pd.read_csv(f, sep='\t', names=['label', 'message'])

df = df[['message', 'label']]
df['label'] = df['label'].apply(spam_ham_to_int)

# Create a correctly formatted obj for spacy
formatted_data = [
    (msg, lbl) for msg, lbl in df.itertuples(index=False)
]
training_data = formatted_data[:1000]
testing_data = formatted_data[3000:]

# Start up spacy and get some shit loaded
nlp = spacy.blank("en")
textcat = nlp.create_pipe('textcat')
textcat.add_label("spam")
nlp.add_pipe(textcat)

# Start the training
nlp.begin_training()
for itn in range(TRAINING_ITERATIONS):
    # Shuffle the training data
    random.shuffle(training_data)
    losses = {}

    # Batch the examples and iterate over them
    for batch in spacy.util.minibatch(training_data, size=2):
        texts = [text for text, entities in batch]
        annotations = [entities for text, entities in batch]

        # Update the model
        nlp.update(texts, annotations, losses=losses)
    print(f'Iteration #{itn+1} losses: {losses}')

# Save model
nlp.to_disk(MODEL_NAME)
