# FastAPI Boilerplate
╰─ python3 main.py --env local --debug for starting

create virtual environment, with conda or python environment:

```shell
conda create -n template python=3.11
conda activate template
```  
or make sure you have python3 and python3-venv installed, and you are in the project directory, then:  

```shell
python3 -m venv template
source template/bin/activate
```

install poetry package:  
```shell
pip3 install poetry 
```  

install dependencies packages: 
```shell
poetry install 
```  
run app for development:
```shell
python3 main.py --env local --debug
```


## Folder structure:



```.
├── api    [contains the api routes for entities]
│   ├── auth [entity]
│   │   ├── auth.py
│   │   ├── request
│   │   │   ├── auth.py  [dto]
│   │   └── response
│   │       ├── auth.py  [dto]
│   └── user  [entity]
│       └── v1
│           ├── request
│           │   └── user.py [dto]
│           ├── response
│           │   └── user.py  [dto]
│           └── user.py   [contains all the routes]
|
├── app    [contains the model, db schema and services for entities]
│   ├── auth
│   │   ├── schemas
│   │   │   └── jwt.py
│   │   └── services
│   │       └──  jwt.py
│   ├── database
│   │   ├── schemas
│   │   │   └── database.py
│   │   └── services
│   │       └──  database.py
│   ├── server.py   [creates app instance]
│   └── user
│       ├── enums
│       │   └── user.py
│       ├── models
│       │   └── user.py
│       ├── schemas
│       │   └── user.py
│       └── services
│           └── user.py
├── core    [contains core elements of the project like db, dependencies etc]
│   ├── config.py
│   ├── db
│   │   ├── mixins
│   │   │   └── timestamp_mixin.py
│   │   ├── session.py
│   │   ├── standalone_session.py
│   │   └── transactional.py
│   ├── exceptions
│   │   ├── base.py
│   │   ├── database.py
│   │   ├── token.py
│   │   └── user.py
│   ├── fastapi
│   │   ├── dependencies
│   │   │   ├── logging.py
│   │   │   ├── permission.py
│   │   └── schemas
│   │       ├── current_user.py
│   └── utils
│       └── token_helper.py
├── docker  [docker files]
│   ├── api
│   │   ├── Dockerfile
│   │   └── startup.sh
│   └── db
│       └── Dockerfile
├── docker-compose.yml
├── main.py
├── migrations
│   └── versions
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests    [for test]
    ├── app
    │   └── user
    │       └── services
    │           └── test_user.py
    └── conftest.py
```
