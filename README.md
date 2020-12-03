# mis-project

### Installation

* Setup

    ```Python
    virtualenv  env
    source env/bin/activate
    ```

    ```Python
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    ```

* Install Redis

    https://redislabs.com/blog/redis-on-windows-8-1-and-previous-versions/
    
    Start Redis Server
        
    ```Python
    redis-server
    ```

### Usage

* To Create Super User

    ``` python
    python manage.py createsuperuser
    ```
  
* To Runserver

    ``` python
    python manage.py runserver
    celery -A project worker -l info
    ```