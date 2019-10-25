import spacy as spacy_en
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import os

model = spacy_en.load('en_core_web_md')

def clean_my_text(song):

    """ It filters punctuation, numbers, stop word
    and returns lemmatized words"""

    doc = model(song)
    clean_text = ''

    for word in doc:

        if (word.is_stop == False)  and (word.pos_ != 'PUNCT') and  (word.pos_ != 'NUM'):

            word = word.lemma_
            clean_text += word + ' '

    return clean_text

def keep_english_for_spacy_nn(df):
    """This function takes the DataFrame for songs
        and keep songs with english as main language
        for english version of spacy neural network for word processing"""

    #Keep only english for spacy NN English preprocessing words
    #Network for other languages like french, spanish, portuguese are also available
    df = df.loc[df['Main Language'] == 'en',:]
    #Drop the translation column not use for lyrics in english
    df.drop(['English Translation Lyrics'],axis =1,inplace = True)

    return df

def apply_spacy_nn_to_DataFrame(df):
    """Apply reduction of words using clean_my_text Function
    to the lyrics column"""

    df['Text Lyrics'] = df['Text Lyrics'].apply(clean_my_text)

    return df

def save_transform_to_disk(cv, tf, folder_save):

    countvectorfile = os.path.join(folder_save, 'countvector.sav')
    pickle.dump(cv, open(countvectorfile, 'wb'))

    Tfidfile = os.path.join(folder_save, 'Tfidfile.sav')
    pickle.dump(tf, open(Tfidfile, 'wb'))

    return

def prepare_training(df_read, folder_save):
    """This function takes the database of artists as input
    and the folder where to save transform operations on data
    and return X and y for training"""

    #Songs in english for spacy nn (disable if multilanguage)
    df_prep = keep_english_for_spacy_nn(df_read)
    #Apply spacy nn to reduce dimension of text
    df_prep = apply_spacy_nn_to_DataFrame(df_prep)
    #Count vecorizer of words
    cv = CountVectorizer()
    corpus_vec = cv.fit_transform(df_prep['Text Lyrics'])
    #Tfidf Transform
    tf = TfidfTransformer()
    transform_vec = tf.fit_transform(corpus_vec)
    #Save transform to disk to reuse for predictions
    save_transform_to_disk(cv, tf, folder_save)
    #todense() to remove sparse formatting
    df_word_vec = pd.DataFrame(transform_vec.todense(), columns=cv.get_feature_names())
    y = df_prep['Name']
    X = df_word_vec

    return X,y
