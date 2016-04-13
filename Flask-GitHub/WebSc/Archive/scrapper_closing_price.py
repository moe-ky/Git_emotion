from pandas.io.data import DataReader
from datetime import datetime


def get_price(year, month, day):
    try:
        face_book = DataReader("FB","yahoo", datetime(year, month, day), datetime(year, month, day))

        closing = face_book['Close']

        print(closing[0])
    except BaseException as e:
        print(0)



'''
face_book_price = []
for i in closing:
    print(i)
    face_book_price.append(i)
print (face_book_price)
'''