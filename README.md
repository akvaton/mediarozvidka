# News

To start the project you have to clone it from GitHub

    git clone https://github.com/raccoongang/news.git
    
Create virtual enviroment
    
    virtualenv news
    source news/bin/activate
    
Install all dependencies form requirements.txt

    pip install -r requirements.txt
    
Create *local_settings.py* and add database settings to it or, if you want to use sqlite, you don't have to
 do anything. **But with sqlite text filtering will be the register sensetive only.**
 
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
