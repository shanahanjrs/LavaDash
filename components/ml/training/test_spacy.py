#!/usr/bin/env python3

import pandas as pd
import os
import random
import spacy
from spacy.util import minibatch, compounding


def evaluate(tokenizer, textcat, texts, cats):
    docs = (tokenizer(text) for text in texts)
    tp = 0.0  # True positives
    fp = 1e-8  # False positives
    fn = 1e-8  # False negatives
    tn = 0.0  # True negatives
    for i, doc in enumerate(textcat.pipe(docs)):
        gold = cats[i]
        for label, score in doc.cats.items():
            if label not in gold:
                continue
            if label == "NEGATIVE":
                continue
            if score >= 0.5 and gold[label] >= 0.5:
                tp += 1.0
            elif score >= 0.5 and gold[label] < 0.5:
                fp += 1.0
            elif score < 0.5 and gold[label] < 0.5:
                tn += 1
            elif score < 0.5 and gold[label] >= 0.5:
                fn += 1
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    if (precision + recall) == 0:
        f_score = 0.0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"textcat_p": precision, "textcat_r": recall, "textcat_f": f_score}


model_file = 'datasets/SMSSpamCollection_spaCy_model'
n_iter = 5
spam_data = pd.read_csv('datasets/SMSSpamCollection', sep='\t', names=['label', 'message'])
print(spam_data.head(10))
# print(spam_data.describe())

training_set = spam_data[:3000]
testing_set = spam_data[3000:]

# Pull or Create a model
# NOTE: For now just create a new one
# if os.path.exists(model_file):
#     model = spacy.load(model_file)
# else:
#     model = spacy.blank("en")
model = spacy.blank("en")

# add the text classifier to the pipeline if it doesn't exist
# model.create_pipe works for built-ins that are registered with spaCy
if "textcat" not in model.pipe_names:
    textcat = model.create_pipe(
        "textcat", config={"exclusive_classes": True, "architecture": "simple_cnn"}
    )
    model.add_pipe(textcat, last=True)
# otherwise, get it, so we can add labels to it
else:
    textcat = model.get_pipe("textcat")

textcat.add_label('ham')
textcat.add_label('spam')

# get names of other pipes to disable them during training
pipe_exceptions = ["textcat", "trf_wordpiecer", "trf_tok2vec"]
other_pipes = [pipe for pipe in model.pipe_names if pipe not in pipe_exceptions]

with model.disable_pipes(*other_pipes):  # only train textcat
    optimizer = model.begin_training()
    print("Training the model...")
    print("{:^5}\t{:^5}\t{:^5}\t{:^5}".format("LOSS", "P", "R", "F"))
    batch_sizes = compounding(4.0, 32.0, 1.001)
    for i in range(n_iter):
        losses = {}
        # batch up the examples using spaCy's minibatch
        # random.shuffle(training_set)
        batches = minibatch(training_set, size=batch_sizes)
        for batch in batches:
            print(batch, flush=True)
            texts, annotations = zip(*batch)
            model.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
        with textcat.model.use_params(optimizer.averages):
            # evaluate on the dev data split off in load_data()
            # scores = evaluate(model.tokenizer, textcat, dev_texts, dev_cats)
            scores = evaluate(model.tokenizer, textcat, testing_set['message'], testing_set['label'])
        print(
            "{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}".format(  # print a simple table
                losses["textcat"],
                scores["textcat_p"],
                scores["textcat_r"],
                scores["textcat_f"],
            )
        )

# test the trained model
test_text = "Reply now to win a free iPhone 12!"
doc = model(test_text)
print(test_text, doc.cats)

# NOTE: Dont save the models for now
# if output_dir is not None:
#     with model.use_params(optimizer.averages):
#         model.to_disk(output_dir)
#     print("Saved model to", output_dir)
#
#     # test the saved model
#     print("Loading from", output_dir)
#     nlp2 = spacy.load(output_dir)
#     doc2 = nlp2(test_text)
#     print(test_text, doc2.cats)



