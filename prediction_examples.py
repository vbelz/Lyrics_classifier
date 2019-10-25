from prediction import predict_from_text

#Examples

folder = './weights'

Text1 = """But that's alright, because I like the way
        it hurts Just gonna stand there and hear me cry """

Text2 = """I drew a line for you Oh what a thing to do
        And it was all yellow Look at the stars Look how
        they shine for you And all the things that you do"""

Text3 = """He's married to the game, like a fuck you for Christmas
    His gift is a curse, forget the Earth, he's got the urge to pull
    his dick from the dirt And fuck the whole universe
    I'm not afraid (I'm not afraid)"""

Text4 = """Wish we never broke up right now, na na
        We need to link up right now, na na I wanna
        make up right now, na na"""

Text5 = """Nobody wanna see us together
but """

predict_from_text(Text3, folder)

# #Examples terminal
# artist=['Coldplay','Rihanna','Eminem','Akon','Metronomy']
#
# folder_save='./weights'
#
# sentence_to_ask = 'Give me some text from Lyrics between '
# names =''
#
# names = ', '.join(artist)
#
# sentence_to_ask += names
# text = input(sentence_to_ask)
#
# predict_from_text(text, folder_save)
