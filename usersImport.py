import os
import csv
import psycopg2 # for database connection
import hashlib # included with Python; no install needed
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker



engine=create_engine("postgres://nftrxahjiqsvls:1916d4daee0200dfb6a94962f8761fe25f55e6496326a053efa0dd88d7557f8b@ec2-54-246-85-151.eu-west-1.compute.amazonaws.com:5432/d81ib93if5c64f")
db=scoped_session(sessionmaker(bind=engine))

def main():
    
    t_name_user = "admin"
    t_password = "admin"
    #Hash the password they entered into a encrypted hex string
    t_hashed = hashlib.sha256(t_password.encode())
    t_password = t_hashed.hexdigest()
      
      #Inserting admin user to users table
    db.execute("INSERT INTO users(username,password) VALUES (:username,:password)",
    {"username":t_name_user,"password":t_password})
    
    print("Insertion completed")    
    db.commit()
if __name__=="__main__":
    main() 
    
         
           