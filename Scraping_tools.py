import requests
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
from langdetect import detect


def create_table_artist_link_lyrics(artist):
    """This function receives an artist name as input and return
    a dataframe containing the name of the artist, title of the song
    and link for the song"""

    # Path to the first page of artist's songs
    path = f'https://www.metrolyrics.com/{artist}-lyrics.html'
    artist_request = requests.get(path)

    if (artist_request.status_code != 200):

        print("It seems this artist does not exist on www.metrolyrics.com,\n"
              "Try again with a valid artist name in https://www.metrolyrics.com/artistname-lyrics.html")

    else:

        soup_artist = soup(artist_request.text, 'html.parser')
        Title = []
        Link = []
        # Check the number of songs in the first page to know if we need to check next pages
        Nb_first_page = len(soup_artist.find_all(
            class_="songs-table compact")[0].find_all('a'))

        for link in soup_artist.find_all(class_="songs-table compact")[0].find_all('a'):

            Title.append(link.get('title')), Link.append(link.get('href'))

        # If < 75 it means we only have one page for this artist
        if Nb_first_page < 75:

            # Remove artist name from title
            pattern = f"(?i){artist}\s(.+)\s+lyrics"
            Title = [re.findall(pattern, text)[0] for text in Title]
            df_artist = pd.DataFrame({'Title': Title, 'Link Lyrics': Link})
            df_artist['Name'] = f'{artist}'
            # df_artist.to_csv(f'{artist}_link.csv')

        # If >= 75 songs, it needs to scrap more pages
        else:

            for link in soup_artist.find_all(class_="pages")[0].find_all('a'):

                path_next_page = link.get('href')
                artist_request_nextpage = requests.get(path_next_page)
                soup_artist_next = soup(
                    artist_request_nextpage.text, 'html.parser')

                for link in soup_artist_next.find_all(class_="songs-table compact")[0].find_all('a'):

                    Title.append(link.get('title')), Link.append(
                        link.get('href'))
            # Remove artist name from title
            pattern = f"(?i){artist}\s(.+)\s+lyrics"
            Title = [re.findall(pattern, text)[0] for text in Title]
            # Create pandas dataframe to save to disk
            df_artist = pd.DataFrame({'Title': Title, 'Link Lyrics': Link})
            # Add a column with artist's name
            df_artist['Name'] = f'{artist}'
            # df_artist.to_csv(f'{artist}_link.csv')

    return df_artist


def get_lyrics(url_lyrics):
    """Function that take the url of a Lyric
    and return the text of the lyric as a string"""

    lyrics_request = requests.get(url_lyrics)
    print(lyrics_request.status_code)
    if (lyrics_request.status_code != 200):

        print('It seems the link  is not available, It will be removed from database')

        lyrics = None

    elif (lyrics_request.url != url_lyrics):

        print(f'It seems the link {url_lyrics} is being redirected, It will be removed from database')

        lyrics = None

    # If the link exists we can scrap the text
    else:
        artist_lyrics = soup(lyrics_request.text, 'html.parser')

        lyrics = []

        print('url_lyrics')

        for each in artist_lyrics.find_all(id="lyrics-body-text")[0].find_all('p'):

            print(len(each))
            print(each.get_text())
            # Obtain only the text of the lyrics from html page
            lyrics.append(each.get_text())
        # Join the text into one and clean the return line symbols \n
        lyrics = '. '.join(lyrics)
        lyrics = lyrics.split('\n')
        lyrics = " ".join(lyrics)

    return lyrics


def add_text_Lyrics_column(data_artist):

    Nb_songs = data_artist.shape[0]
    Text_lyrics = []

    for i in range(Nb_songs):
        print(f'Song number {i}')
        Text_lyrics.append(get_lyrics(data_artist['Link Lyrics'].iloc[i]))

    data_artist['Text Lyrics'] = Text_lyrics

    return data_artist
