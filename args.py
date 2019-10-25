import argparse

parser = argparse.ArgumentParser(description='Lyris scraping, training and prediction')

parser.add_argument('--weights_folder', default='./weights', type=str)

parser.add_argument('--data_folder', default='.', type=str)

parser.add_argument('--name_file_to_read', default='Database_songs.csv', type=str)

parser.add_argument('--name_file_to_save', default='Database_songs.csv', type=str)

parser.add_argument('--nb_artist', default=5, type=int)

parser.add_argument('--list_artist', default=['Coldplay','Rihanna','Eminem','Akon','Metronomy'], type=list)

parser.add_argument('--mode',default='prediction', type=str, choices=['scraping', 'training', 'prediction'])
