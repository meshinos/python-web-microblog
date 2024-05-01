from flask import Flask, render_template,request
from pymongo import MongoClient 
import datetime
import os
from dotenv import load_dotenv


load_dotenv()
 

def create_app():
    app = Flask(__name__)
    # client = MongoClient("mongodb+srv://meshinos97:meshi1234@microblogapp.asto0ha.mongodb.net/")
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog # microblog is the database we created in our cluster. we want to put this db value inside app

    @app.route("/",methods=["GET","POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry_content,"date":formatted_date}) # insert the user log into the entries collection 
            

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
            )
            for entry in  app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)
    
    
    return app
    

