# dev_dive_backend

## Dev Dive 
#### This is a Q&A platform with a built-in gpt-like bot, which provides all the means to search for interesting data and communicate with other people

## Used technologies:
- Python 3.11
- FastAPI + Uvicorn
- PostgreSQL
- Asyncpg + SQLAlchemy 2.x
- Alembic
- Redis
- Docker Compose
- Black + Isort + Mypy

## Database Schema and User Roles
#### You can find it here: https://drive.google.com/drive/folders/1cQf850SrOaV7ylaP537uy-gp5M5kXU0B?dmr=1&ec=wgc-drive-globalnav-goto

## Set up with Docker Compose:
1) Go to terminal
2) Clone repo
```
git clone https://github.com/Neurotrier/dev_dive_backend.git
```
3) Open dev_dive_backend folder
4) Create `.env` file based on `.env.example`
5) Start docker compose containers in terminal from current folder
```
docker compose up --build
```
6) Start uvicorn
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
7) Go to `0.0.0.0:8000/docs` in your browser - SwaggerAPI