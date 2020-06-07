import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker


engine=create_engine("postgres://nftrxahjiqsvls:1916d4daee0200dfb6a94962f8761fe25f55e6496326a053efa0dd88d7557f8b@ec2-54-246-85-151.eu-west-1.compute.amazonaws.com:5432/d81ib93if5c64f")
db=scoped_session(sessionmaker(bind=engine))

def main():
    #Creating the table
    db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY,username VARCHAR NOT NULL,password VARCHAR NOT NULL)")
    db.execute("CREATE TABLE reviews(isbn VARCHAR NOT NULL,review VARCHAR NOT NULL,rating INTEGER NOT NULL,username VARCHAR NOT NULL)")
    db.execute("CREATE TABLE books(isbn VARCHAR PRIMARY KEY,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")
    
    #Inserting books.csv to books table
    f=open("books.csv")
    reader=csv.reader(f)
    for isbn,title,author,year in reader:
        if isbn == "isbn":
            print("Skip the first line")
        else:
            db.execute("INSERT INTO books(isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",
            {"isbn":isbn,"title":title,"author":author,"year":year})
            
    print("Insertion completed")    
    db.commit()
if __name__=="__main__":
    main()        