import os
import psycopg2 # for database connection
import hashlib # included with Python; no install needed
from flask import Flask, session ,render_template , request , redirect , url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import bindparam
import requests
from flask import jsonify
from flask import flash 
from sqlalchemy_utils import create_database, database_exists
app = Flask(__name__)

# Check for environment variable
#if not os.getenv("postgres://nftrxahjiqsvls:1916d4daee0200dfb6a94962f8761fe25f55e6496326a053efa0dd88d7557f8b@ec2-54-246-85-151.eu-west-1.compute.amazonaws.com:5432/d81ib93if5c64f"):
    #raise RuntimeError("DATABASE_URL is not set")
    
#engine = create_engine("sqlite:///data.db", encoding='latin1', echo=True)

    

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'secretkey'
#Session(app)


# Set up database
engine = create_engine("postgres://nftrxahjiqsvls:1916d4daee0200dfb6a94962f8761fe25f55e6496326a053efa0dd88d7557f8b@ec2-54-246-85-151.eu-west-1.compute.amazonaws.com:5432/d81ib93if5c64f")
#engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'username' in session:
        flash('Already Signed in')
        return render_template('index.html')
    else:
        return render_template('index.html')
    
@app.route("/home")
def home():
    return render_template('index.html')          
        
@app.route("/login", methods = ['POST','GET'])
def login():
    
    if request.method=="POST":
        session['username'] = request.form.get("uname")
        username=session['username']
        password = request.form.get("pswd")
        #Hash the password they entered into a encrypted hex string
        t_hashed = hashlib.sha256(password.encode())
        t_password = t_hashed.hexdigest()
        #print (t_password)
        users=db.execute("SELECT username,password FROM users WHERE username=:username AND password=:password",{"username":username,"password":t_password}).fetchone()
        #print(users.username)
        if users:
            return render_template("search.html",name=users.username,password=users.password)           
        else:
            return "Invalid Login Details"
    else:
        return render_template("login.html")   
    
    
    #return render_template("login.html")  
    
    
    
@app.route("/registration", methods = ['POST','GET'])
def registration():
    ###### New user registration #####
    if request.method=="POST":
        print("inside registration post")
        username = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        #Hash the password they entered into a encrypted hex string
        t_hashed = hashlib.sha256(password.encode())
        t_password = t_hashed.hexdigest()
        check_user_exist=db.execute("SELECT * FROM users WHERE username=:username",
            {"username":username}).fetchone()
        if check_user_exist:
            return render_template("registration.html",message="Already Regisered") 
        else:     
            db.execute("INSERT INTO users(username,password) VALUES(:username,:password)",
                {"username":username,"password":t_password})
            db.commit()
            return redirect(url_for('index',message="Registered Successfully"))
    else:
        return render_template("registration.html")     
    
@app.route("/search",methods=["GET","POST"])
def search():
    
    name=session['username']
    
    if request.method=="POST":
        radiovalue = request.form.get("optradio")          
        textvalue = request.form.get("searchtext")
        
        if len(textvalue)!=0:
            if radiovalue == "author":
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE author ILIKE :textvalue LIMIT 20",
                        {"textvalue":"%"+textvalue+"%"}).fetchall()
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)       
                  
            elif radiovalue == "title":  
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE title ILIKE :textvalue LIMIT 20",
                    {"textvalue":"%"+textvalue+"%"}).fetchall()
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)     
                 
            elif radiovalue == "isbn":  
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE isbn ILIKE :textvalue  LIMIT 20",
                    {"textvalue":"%"+textvalue+"%"}).fetchall() 
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)   
                  
            elif radiovalue == "year": 
                query = "SELECT isbn,author,title,year FROM books WHERE year LIKE :textvalue LIMIT 20"
                books=db.execute(query,{"textvalue":"%"+textvalue+"%"}).fetchall()                 
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name) 
        else:
            error="No Results Found"
            return render_template("search.html",error=error,name=name)
            
    return render_template("search.html",name=name)         

        
@app.route("/fetch",methods=["GET","POST"])
def fetch():
    if request.method=="POST":
        radiovalue = request.form.get("optradio")          
        textvalue = request.form.get("searchtext")
        name=session['username']
        if len(textvalue)!=0:
            if radiovalue == "author":
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE author ILIKE :textvalue LIMIT 20",
                        {"textvalue":"%"+textvalue+"%"}).fetchall()
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)       
                  
            elif radiovalue == "title":  
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE title ILIKE :textvalue LIMIT 20",
                    {"textvalue":"%"+textvalue+"%"}).fetchall()
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)     
                 
            elif radiovalue == "isbn":  
                books=db.execute("SELECT isbn,author,title,year FROM books WHERE isbn ILIKE :textvalue  LIMIT 20",
                    {"textvalue":"%"+textvalue+"%"}).fetchall() 
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name)   
                  
            elif radiovalue == "year": 
                query = "SELECT isbn,author,title,year FROM books WHERE year LIKE :textvalue LIMIT 20"
                books=db.execute(query,{"textvalue":"%"+textvalue+"%"}).fetchall()                 
                if books:
                    return render_template("search.html",books=books,name=name)  
                else:
                    error="No Results Found"
                    return render_template("search.html",error=error,name=name) 
        else:
            error="No Results Found"
            return render_template("search.html",error=error,name=name)
            
@app.route("/bookdetails",methods=["GET","POST"])
def bookdetails():
        title=request.args.get('title')
        author=request.args.get('author')
        isbn=request.args.get('isbn')
        year=request.args.get('year')
        
        #####API JSON CALL###
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key":"FxtMDTXu2B4X5nFYVfKfg","isbns":isbn})
        if res.status_code != 200:
            raise Exception("Error: API request unsuccessful")
        apidata = res.json()    
                    
        session['title']=title
        session['author']=author
        session['isbn']=isbn
        session['year']=year
        session['apidata']=apidata
        username = session['username']
        
        reviews=db.execute("SELECT rating,review,username FROM reviews WHERE isbn=:isbn",
                            {"isbn":isbn}).fetchall()
        print (reviews)            
        if reviews:
            return render_template("bookdetails.html",title=title,author=author,isbn=isbn,year=year,reviews=reviews,apidata=apidata,name=username)
        else:
            return render_template("bookdetails.html",title=title,author=author,isbn=isbn,year=year,error="--No Review--",apidata=apidata,name=username)             
                               
            #return render_template("bookdetails.html",reviews=reviews)
            
@app.route("/updatereview",methods=["GET","POST"])
def updatereview():   
        if request.method == "POST":
            print("inside review post method")
            
            title=session['title']
            author=session['author']
            isbn=session['isbn']
            year=session['year']
            apidata=session['apidata']
            username=session['username']
            
            review = request.form.get('reviewtext')
            rating = request.form.get('optradio')  
            reviews=db.execute("SELECT rating,review,username FROM reviews WHERE isbn=:isbn AND username=:username",
                                        {"isbn":isbn,"username":username}).fetchone()  
            print(reviews)
            if reviews:    
                #return render_template("bookdetails.html",reviewerror="Review already submitted") 
                reviews=db.execute("SELECT rating,review,username FROM reviews WHERE isbn=:isbn",
                                            {"isbn":isbn}).fetchall()
                return render_template("bookdetails.html",title=title,author=author,isbn=isbn,year=year,reviews=reviews,reviewerror="Review already submitted",apidata=apidata,name=username)
            else:
                db.execute("INSERT INTO reviews(isbn,review,rating,username) VALUES(:isbn,:review,:rating,:username)",
                        {"isbn":isbn,"review":review,"rating":rating,"username":username})
                print("Reviews inserted sucessfully")
                db.commit()
                reviews=db.execute("SELECT rating,review,username FROM reviews WHERE isbn=:isbn",
                                            {"isbn":isbn}).fetchall()
        return render_template("bookdetails.html",title=title,author=author,isbn=isbn,year=year,reviews=reviews,apidata=apidata,name=username)      
               
@app.route('/signout')
def signout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('password', None)

        flash('Signed out successfully', 'info')
        return redirect(url_for('index'))
    else:
        flash('Already Singed out')
        return  redirect(url_for('index'))              
                
@app.route("/book/api/<string:isbn>")
def api(isbn):
    if 'username' in session: 
        data=db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
        if data==None:
            #return render_template('404.html')
            return "no data from table"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                    params={"key":"FxtMDTXu2B4X5nFYVfKfg","isbns":"0553293427"})
        average_rating=res.json()['books'][0]['average_rating']
        work_ratings_count=res.json()['books'][0]['work_ratings_count']
        x = {
        "title": data.title,
        "author": data.author,
        "year": data.year,
        "isbn": isbn,
        "review_count": work_ratings_count,
        "average_rating": average_rating
        }
        # api=json.dumps(x)
        # return render_template("api.json",api=api)
        return  jsonify(x)
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
            
if __name__== "__main__":
    main()             
                        
                
                
                
                 
        
        
            
               
        
        
    #return render_template("search.html")     
    
    
    
    
