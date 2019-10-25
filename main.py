from make_data_base import create_database_save_to_disk, merge_databases_into_one
from prepare_for_training import prepare_training
import pandas as pd
from training import train_bayes, train_logistic
from prediction import predict_from_text
from args import parser
import os


if __name__ == '__main__':

    args = parser.parse_args()

    folder_save = args.weights_folder
    nb_artist = args.nb_artist
    artist = args.list_artist
    mode = args.mode
    data_folder = args.data_folder
    file_name_to_save = args.name_file_to_save
    file_name_to_read = args.name_file_to_read

    # Initialize all modes to zero
    scraping_mode = False
    training_mode = False
    prediction_mode = False

    # Update the mode the user is asking
    if mode == 'prediction':
        prediction_mode = True
    elif mode == 'training':
        training_mode = True
    elif mode == 'scraping':
        scraping_mode = True

    if scraping_mode:
        #Example: python main.py --mode='scraping' --nb_artist=2 --list_artist="Eminem,Rihanna" --name_file_to_save="Data_test.csv"
        # Transform the letters from command line into list of artists

        if artist != parser.get_default('list_artist'):
            merge_list = ''
            for item in artist:
                merge_list += item

            new_list = merge_list.split(',')
            artist = new_list

        if (nb_artist == len(artist)):

            artist = [x.lower() for x in artist]

            sentence_to_ask = f'You are going to scrape for {nb_artist} artists with names: '
            names = ''
            names = ', '.join(artist)
            sentence_to_ask += names + '  '

            print(sentence_to_ask)


            for artist_name in artist:

                print(artist_name)

                create_database_save_to_disk(artist_name, data_folder)

            merge_databases_into_one(artist, data_folder, file_name_to_save)
        else:

            print("There is inconsistency between number of artist and list of artist\n")
            print("relaunch the command line following recommendations")

    if training_mode:

        #Example: python main.py --mode="training" --name_file_to_read="Data_test.csv" --weights_folder="weights_test"

        print("You are going to train the models on this database : \n")
        print(f'{os.path.join(data_folder,file_name_to_read)}')

        #Read database at "data_folder/file_name_to_read"
        df_read = pd.read_csv(os.path.join(
            data_folder, file_name_to_read))

        #Prepare X and y foir training and save transforms at "folder_save"
        X, y = prepare_training(df_read, folder_save)

        #Train bayes and save weights at "folder_save"
        train_bayes(X, y, folder_save)

        #Train logistic and save weights at "folder_save"
        train_logistic(X, y, folder_save)

    if prediction_mode:
        #Example: python main.py --mode="prediction" --list_artist="eminem,rihanna" --weights_folder="./weights_test"
        if artist != parser.get_default('list_artist'):
            merge_list = ''
            for item in artist:
                merge_list += item

            new_list = merge_list.split(',')
            artist = new_list

        sentence_to_ask = 'Give me some text from Lyrics between '
        names = ''

        names = ', '.join(artist)

        sentence_to_ask += names + '  '
        text = input(sentence_to_ask)

        predict_from_text(text, folder_save)
