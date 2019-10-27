import spacy as spacy_en
import pandas as pd
import pickle
import os

model = spacy_en.load('en_core_web_md')


def clean_my_new_text(song):
    """ It filters punctuation, numbers, stop word
    and returns lemmatized words"""

    doc = model(song)
    clean_text = ''

    for word in doc:

        if (word.is_stop == False) and (word.pos_ != 'PUNCT') and (word.pos_ != 'NUM'):
            word = word.lemma_
            clean_text += word + ' '

    return clean_text


def predict_from_text(new_text, folder_save):
    """This function takes a new text as input and predict the singer
    from the database classes. It loads the transforms and the weights from disk"""
    print(folder_save)

    # Load transform and weights from training phase
    countvectorfile = os.path.join(folder_save, 'countvector.sav')
    cv = pickle.load(open(countvectorfile, 'rb'))

    Tfidfile = os.path.join(folder_save, 'Tfidfile.sav')
    tf = pickle.load(open(Tfidfile, 'rb'))

    bayesfile = os.path.join(folder_save, 'bayes_weights.sav')
    clf_bayes = pickle.load(open(bayesfile, 'rb'))

    logisticfile = os.path.join(folder_save, 'logistic_weights.sav')
    clf_logistic = pickle.load(open(logisticfile, 'rb'))

    # Apply on new text
    Text_clean = clean_my_new_text(new_text)
    new_corpus_vec = cv.transform([Text_clean])
    new_transform_vec = tf.transform(new_corpus_vec)
    X_test = new_transform_vec.todense()

    # Print the results
    print(
        f'According to Logreg, this poetry was song by {clf_logistic.predict(X_test)[0].upper()}')

    print("The probabilities are : \n")
    print(f'{clf_logistic.classes_} \n')
    print(f'{clf_logistic.predict_proba(X_test)} \n')

    print(
        f'According to Bayes, this poetry was song by {clf_bayes.predict(X_test)[0].upper()}')

    print("The probabilities are : \n")
    print(f'{clf_bayes.classes_} \n')
    print(f'{clf_bayes.predict_proba(X_test)} \n')

    return
