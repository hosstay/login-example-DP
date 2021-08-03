# Login Example DP

An implementation of a website with login using Django and PostgreSQL built in docker (In Progress)

## Getting Started

### Prerequisites

* Have docker and docker-compose installed

## Deployment

* in './login_example_DP/' rename '.env-example' to '.env' and put your own secret key inside.
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

## Built With

* [Django](https://www.djangoproject.com/) - Web Framework
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Docker](https://www.docker.com/) - Containerization

## Authors

* **Taylor Hoss** - [hosstay](https://github.com/hosstay)
