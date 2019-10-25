import pandas as pd
from langdetect import detect
from googletrans import Translator
from Scraping_tools import create_table_artist_link_lyrics
from Scraping_tools import add_text_Lyrics_column
import os


def get_language(x):
    """Main language in a text"""

    return detect(x)

def get_len(x):
    """len of string"""

    return len(x)

def clean_table_add_language(df):
    """Function to remove links without lyrics
       and add a column with the main language
       of the database"""

    # Remove songs without Lyrics on the html page
    df.dropna(inplace=True)

    # Add a column with string length
    df['Length']=df['Text Lyrics'].apply(get_len)

    # Remove lyrics with less than 50 letters
    indexnames = df[df['Length'] < 50].index
    df.drop(indexnames,inplace = True)

    # Detect main language of each song and label into a new column
    df['Main Language'] = df['Text Lyrics'].apply(get_language)

    return df

def translate_to_english(text_in):
    """This function will convert a string
    in english"""

    trans = Translator()
    translation = trans.translate(text_in)
    text_english = translation.text

    return text_english

def update_dataframe_to_english(df):
    """This function will convert the lyrics
    text not in english oto english"""

    df['English Translation Lyrics'] = ''

    mask = (df['Main Language'] != 'en')

    df.loc[mask,'English Translation Lyrics'] = df.loc[mask,'Text Lyrics'].apply(translate_to_english)

    return df

def create_database_save_to_disk(artist, data_folder):
    """This function takes the artist's name as input,
        create a database of its songs and lyrics and
        save it to disk"""

    #Create table with all songs title and url to lyrics
    df_artist = create_table_artist_link_lyrics(artist)

    #Add a column with clean lyrics for each song
    df_artist = add_text_Lyrics_column(df_artist)
    print(f'Done converting to text for {artist}')

    #Clean the table and add language label for each song
    df_artist = clean_table_add_language(df_artist)
    print(f'Done clean table for {artist}')

    #Update non english songs (comment if not relevant )
    df_artist = update_dataframe_to_english(df_artist)
    print(f'Done translating for {artist}')

    #Save to disk
    path_artist = os.path.join(data_folder,f'{artist}_songs.csv')
    df_artist.to_csv(path_artist,index=False)
    print(f'Done save to disk for {artist}')

    return

def merge_databases_into_one(list_artist, data_folder, file_name_to_save):
    """This function takes a list of artist as input,
        merge all the songs into one database and
        save it to disk"""

    df_merge = pd.DataFrame()

    for artist_name in list_artist:
        path_artist = os.path.join(data_folder,f'{artist_name}_songs.csv')
        df_read = pd.read_csv(path_artist)
        df_merge = pd.concat([df_merge, df_read])

    all_artist = ''
    for artist in list_artist :
        all_artist += artist + ' '
    #Save to disk
    df_merge.to_csv(f'{os.path.join(data_folder,file_name_to_save)}',index=False)
    print(f'Done save to disk for {all_artist}')

    return
