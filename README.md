## Prerequisites
Python 

Django 

Djangorestframework

# Installation
## Clone the repository fro github
    git clone https://github.com/gauravwarise/BackendAssignment.git

## Navigate to the folder
    cd .\BackendAssignment\   
    
## Install required frameworks and libraries

    pip install -r .\requirements.txt

## Navigate to the project directory

    cd .\Backend_Assignment_Onefin\  

## Perform Migrations

    python manage.py makemigrations
    python manage.py migrate


## Start Server
    python manage.py runserver
    

# Authentication

This project uses JWT token authentication for API requests. To authenticate API requests, include the JWT token in the Authorization header (access_token) of your HTTP requests.


# Endpoints :
The following API endpoints are available:

## User Registration:
### Request

`POST /register`

    {
        "username":"demo1",
        "password":"Demo1.@#"
    }

### Response
    {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwMTgxNDA5LCJpYXQiOjE3
                            MTAxNzc4MDksImp0aSI6ImE3ZjYyODgxNmVmMzQwNWJiODgyN2YzZGExNmMwOGMyIiwidXNlcl9pZCI6Mn0.vPbBy5RLix0sGQ35SXlMCdZ0F9MlULiHcaadiKtbXxY"
    }


## Get Movie List:
### Request

`GET /movies`

### Response
    {
    "data": {
        "count": 45466,
        "next": "https://demo.credy.in/api/v1/maya/movies/?page=2",
        "previous": null,
        "results": [
            {
                "title": "Queerama",
                "description": "50 years after decriminalisation of homosexuality in the UK, director Daisy Asquith mines the jewels of the BFI archive to take us into the relationships, desires, fears and expressions of gay men and women in the 20th century.",
                "genres": "",
                "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d"
            }...
            ]
        }
    }


## Add Collection:
### Request

`POST /collection`


### Response
    {
    "title":"collection1",
    "description":"my collection1",
    "movies":[
        {
                "title": "Betrayal",
                "description": "When one of her hits goes wrong, a professional assassin ends up with a suitcase full of a million dollars belonging to a mob boss ...",
                "genres": "Action,Drama,Thriller",
                "uuid": "720e8796-5397-4e81-9bd7-763789463707"
            }
        ]
    }


## Get all Collections:
### Request

`GET /collection`

No Request Body needed

### Response
    {
    "is_success": true,
    "data": {
        "collection": [
            {
                "uuid": "45817561-09c8-484f-bf84-aa9408e58939",
                "title": "collection1",
                "description": "my collection1"
            }
        ]
    },
    "favourite_genres": "Action,Drama,Thriller"
}

## Get Perticular Collections:
### Request

`GET /collection/<collection_uuid>/`

No Request Body needed

### Response
    {
    "title": "collection1",
    "description": "my collection1",
    "movies": [
        {
            "uuid": "720e8796-5397-4e81-9bd7-763789463707",
            "title": "Betrayal",
            "description": "When one of her hits goes wrong, a professional assassin ends up with a suitcase full of a million dollars belonging to a mob boss ...",
            "genres": "Action,Drama,Thriller"
        }
    ]
}

## Update Collection:
### Request

`PUT /collection/<collection_uuid>/`

    {
        "title":"updated collection1",
        "description":"updated my collection1",
        "movies":[
            {
                    "title": "Betrayal",
                    "description": "When one of her hits goes wrong, a professional assassin ends up with a suitcase full of a million dollars belonging to a mob boss ...",
                    "genres": "Action,Drama,Thriller",
                    "uuid": "720e8796-5397-4e81-9bd7-763789463707"
                }
        ]
    }

### Response
    {
        "details": "updated"
    }



## Delete Content:
### Request

`DELETE /collection/<collection_uuid>/`


### Response
    {
        "detail": "Successfully deleted."
    }

## Get user request count:
### Request

`GET /request-count`


### Response
    {
        "requests": 35
    }


## Reset user request count:
### Request

`GET /request-count/reset/`


### Response
    {
        "message": "request count reset successfully"
    }



# Execute tests cases:
## Ensure that redis is configured in your system

## accounts app:

    python manage.py test apps.accounts

## movies app: 

    python manage.py test apps.movies  


