# News

To start the project you have to clone it from GitHub

    git clone https://github.com/raccoongang/news.git
    
Create virtual enviroment
    
    virtualenv news
    source news/bin/activate
    
Install all dependencies form requirements.txt

    pip install -r requirements.txt
    
Create *local_settings.py* and add database settings and twitter keys to it.

    APP_KEY = ''
    APP_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
 
 If you want to use sqlite, you don't have to do anything else. **But with sqlite text filtering will be the register sensetive only.**
 
 If you want to use mySQL, yot have to create table with right charset first:
 
        mysql -u <your username> -p; #to enter mysql console
        
    And create database:
      
        create DATABASE <your db name> DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
 
 
 
Make migrations
    
    python manage.py migrate
    
Start the project 
    
    python manage.py runserver
    
**To run the spiders:**
 
 Install redis from http://redis.io/
 
 Start it with default settings
 
    redis-server
 
 Start celery

    celery -A news_pro worker -B  --concurrency=1 --loglevel=INFO

**That's all, you did it and you awesome!**
