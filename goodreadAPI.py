import requests

def main():  
      
    res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                params={"key":"FxtMDTXu2B4X5nFYVfKfg","isbns":"0553293427"})
    
    if res.status_code != 200:
        raise Exception("Error: API request unsuccessful")
    #isbns = '0553293427'    
    data = res.json()
    #print(data)
    onebook=data['books'][0]
    count = onebook['ratings_count']
    #average_rating=data["books"]["average_rating"]
    print(f" {isbns} has rating_count {count} ")
    
if __name__ == "__main__":
    main()        
        