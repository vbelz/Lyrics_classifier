from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import pickle
import os

def train_bayes(X,y,folder_save) :
    """This function train naive bayes, print the accuracy on the Database
       and save the weights to disk"""

    clf_bayes = MultinomialNB(alpha=0.01)
    clf_bayes.fit(X,y)

    print(f'This Bayes network, has an accuracy on this database of {clf_bayes.score(X,y)}')

    bayesfile = os.path.join(folder_save, 'bayes_weights.sav')
    pickle.dump(clf_bayes, open(bayesfile, 'wb'))

    print(f'Weights of this network have been save to disk at {folder_save}')

    return

def train_logistic(X,y,folder_save):
    """This function train logistic regression, print the accuracy on the Database
       and save the weights to disk"""

    clf_logistic = LogisticRegression(C=4.0, solver='lbfgs', multi_class='auto')
    clf_logistic.fit(X,y)

    print(f'This LogisticRegression network, has an accuracy on this database of {clf_logistic.score(X,y)}')

    logisticfile = os.path.join(folder_save, 'logistic_weights.sav')
    pickle.dump(clf_logistic, open(logisticfile, 'wb'))

    print(f'Weights of this network have been save to disk at {folder_save}')

    return
