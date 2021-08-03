# Login Example DP

An implementation of a website with login using Django and PostgreSQL built in docker (In Progress)

## Getting Started

### Prerequisites

* Have docker and docker-compose installed

## Deployment

* in './login_example_DP/' rename '.env-example' to '.env' and put your own secret key inside.
* get container id  for app by finding it via 'sudo docker ps'
* exec into docker container with 'sudo docker exec -t -i <container-id> bash'
* run 'python manage.py makemigrations'
* run 'python manage.py migrate'
* run 'docker-compose up'

Webpage runs at localhost:8080

## Logging into database manually

* get container id for db by finding it via 'sudo docker ps'
* exec into docker container with 'sudo docker exec -t -i <container-id> bash'
* log into db with 'psql -U postgres -d postgres'

## Running the tests

* get container id  for app by finding it via 'sudo docker ps'
* exec into docker container with 'sudo docker exec -t -i <container-id> bash'
* run 'python manage.py test'

## Test Data Generation

* I'll show a couple different methods of adding data...
* For user just sign up using the website (could also do admin console)
* For forum data:
    * Create at least 1 board (Showing DB method):
        * exec into postgres docker container and log into postgres
        * run 'INSERT INTO boards_board (name, description) VALUES ('Django', 'For Django discussion');
    * Create a bunch of threads and posts (Showing interactive shell method):
        * exec into app docker container
        * run 'python manage.py python' to enter interactive python shell
        * run the code below 
    
```
from django.contrib.auth.models import User
from boards.models import Board, Thread, Post

user = User.objects.first() # need to have created a user with the webpage
board = Board.objects.get(name='Django')

for i in range(40):
    subject = f'Thread test #{i}'
    thread = Thread.objects.create(subject=subject, board=board, starter=user)

    for j in range(40):
        Post.objects.create(message=f'Lorem ipsum...{j}', thread=thread, created_by=user)


```

## Built With

* [Django](https://www.djangoproject.com/) - Web Framework
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Docker](https://www.docker.com/) - Containerization

## Authors

* **Taylor Hoss** - [hosstay](https://github.com/hosstay)
