# Login Example DP

An implementation of a website with login using Django and PostgreSQL built in docker (In Progress)

## Getting Started

### Prerequisites

* Have docker and docker-compose installed

## Deployment

* in './login_example_DP/' rename '.env-example' to '.env' and optionally change the config for your needs.
* run 'docker-compose up'

Webpage runs at localhost:8080

## Logging into database manually

* log into db with 'sudo docker exec -ti login-example-dp_db_1 psql -U postgres -d postgres'

## Running the tests

* run 'sudo docker exec -ti login-example-dp_web_1 python manage.py test'

## Test Data Generation

* I'll show a couple different methods of adding data...
* For user just sign up using the website (could also do admin console)
* For forum data:
    * Create at least 1 board (Showing DB method):
        * exec into postgres docker container and log into postgres
        * run 'INSERT INTO boards_board (name, description) VALUES ('Django', 'For Django discussion');
    * Create a bunch of threads and comments (Showing interactive shell method):
        * exec into app docker container
        * run 'python manage.py python' to enter interactive python shell
        * run the code below 
    
```
from django.contrib.auth.models import User
from boards.models import Board, Thread, Comment

user = User.objects.first() # need to have created a user with the webpage
board = Board.objects.get(name='Django')

for i in range(40):
    title = f'Thread test #{i}'
    thread = Thread.objects.create(title=title, board=board, creator=user)

    for j in range(40):
        Comment.objects.create(text=f'Lorem ipsum...{j}', thread=thread, created_by=user)


```

## Built With

* [Django](https://www.djangoproject.com/) - Web Framework
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Docker](https://www.docker.com/) - Containerization

## Authors

* **Taylor Hoss** - [hosstay](https://github.com/hosstay)
