# Lyrics_classifier
---
>
>
## Introduction

Web scraping, is data scraping used for extracting data from websites using its HTML structure.
In this project, I used BeautifulSoup python package in order to automatically extract all lyrics from artists
at [https://metrolyrics.com](https://metrolyrics.com), to then build an artist's classifier to predict the
artist on new text. The program works in three modes: The scraping mode, the training mode and the prediction mode
which are described in the next sections

## Requirements

```
- spacy 2.2.1
- sklearn 0.21.3
- pandas 0.23.4
- langdetect 1.0.7
- googletrans 2.4.0
- beautifulsoup 4.6.5

```

## Scraping web data

In scraping mode, the program will automatically gather the data from the web for the artists defined,
using beautifulsoup package. Then, it will create a database containing the title of the songs, the name
of the artist, the url to the lyrics, the text of the lyrics, its length (number of letter), its
main language (label obtained from the text using langtetect package). An additional column contain its
translation in english using googletrans package. The program can easily adapted to translate the lyrics to
other language (see the notebook Example_googletrans, to see a simple example how to translate a portuguese
text to english, spanish or french).

Then it will be saved to disk as a csv file.

Below, an example how the database should look like:

<img src="Data_base_ex.png" alt="Example of artist's database" title="Example"  />


## Training

In training mode, the program will read a database from the disk, and then it will preprocessed
the words to return features and label. The preprocessing consists mainly in:

1)  Apply neural net from spacy package to filter punctuation, numbers, stop word
    and return lemmatized words. In this program i used the english version of spacy, but it
    can easily be adapted by loading instead another language version of spacy model.

2)  Apply a count vecorizer of words for all lyrics in the database followed by a TFIDF
    (frequency–inverse document frequency) transform to the words. The TFIDF transform used
    is from the sklearn package.

3)  It will save the transform to the disk (to be used later on prediction mode)


Then features and label will be used to train a naive bayes classifier (multinomial), and a
logistic regression classifier. Both with slight regularization. Both model's weights will be saved to disk
to be used in prediction mode.


## Prediction

In prediction mode, the program will ask for new text to predict between the artists. It will load
the weights of transforms and model, and will deliver its predictions (for both Bayes and logistic
regression models). Below, a demo example where the program ask for new text to predict between
Coldplay, Rihanna, Eminem, Akon and Metronomy. It correctly predicted this text being from Coldplay.

<img src="demo_lyrics_prediction_zoom_quick.gif" alt="Demo prediction mode" title="Demo prediction mode" align="right" />

---


## How to use

To use the program, you can launch from the terminal: `python main.py`
and it will run with the default options (prediction mode on new text from Coldplay, Rihanna, Eminem,
Akon or Metronomy). The default options can be modified as followed:

```
python main.py OPTIONS

Possible OPTIONS (with default setting) are defined below:

* Mode of the program:

--mode: default='prediction', type=str, choices=['scraping', 'training', 'prediction']

* Folder where to save weights of models (for training mode):

--weights_folder: default='./weights', type=str

* Folder where to save data base or to read database:

--data_folder: default='.', type=str

* Name of the file to read as database (for training mode):

--name_file_to_read: default='Database_songs.csv', type=str

* Name of the file to save to disk as database (for scraping mode):

--name_file_to_save: default='Database_songs.csv', type=str

* Number of artists considered:

--nb_artist: default=5, type=int

* List of artists considered:

--list_artist: default=['Coldplay','Rihanna','Eminem','Akon','Metronomy'], type=list

```

Here are some example to use with a different database as the one included in this repository.

Let's suppose you want to create a database for only rihanna and eminem, you would have to type
on the terminal:

` python main.py --mode='scraping' --nb_artist=2 --list_artist="Eminem,Rihanna" --name_file_to_save="Data_test.csv"`

Now, if you want to train the models on this new database and save them to disk to a new folder,
you would have to type on the terminal:

` python main.py --mode="training" --name_file_to_read="Data_test.csv" --weights_folder="weights_test"`

Now if you want to predict on new text, you will have to type:

` python main.py --mode="prediction" --list_artist="eminem,rihanna" --weights_folder="./weights_test"`


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
