# Intro
BaseAPI is a FastAPI backend with Core modules as a base for future freelance projects (Auth, Notifications, Email,...) </br></br>
[Trello](https://trello.com/b/E7HIwW12/baseapi) Board 
## 0. Prerequisites
  - python3
  - pip3
  - virtualenv [pip3 install virtualenv]
  - redis (I use the docker image)

## 1. Run:
- ### Create virtual environment 
  `python3 -m virtualenv [env_name]`
- ### Activate environment 
  `source [env_name]/bin/activate`
- ### Install requirements 
  `pip install -r requirements.txt`
- ### run the server
  `uvicorn main:app --reload --port 8000`
- ### use the docker-compose file
  from the root directory run `docker-compose up --build` 
## Note:
  `main.py` origins object contains allowed hosts, make sure your client is in it before sending requests.
  
