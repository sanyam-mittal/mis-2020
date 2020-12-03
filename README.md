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

### Usage

* To Create Super User

    ``` python
    python manage.py createsuperuser
    ```
  
* To Runserver

    ``` python
    python manage.py runserver
    ```