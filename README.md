# CyberGreen

# Getting Started
For this web app to work, both the frontend and the backend must be running. This can be done simultaneously in two different terminal windows.

## Frontend
1. Change (`cd`) into `cybergreen_frontend`.
2. Run `npm i`.
3. Run `npm run start`.
4. Navigate to the new page which opens on `localhost`. This is the CyberGreen app!

## Backend
1. Change (`cd`) into `cybergreen_backend`.
2. Run `pip3 install -r requirements.txt`. If you're on a Mac ARM processor and getting a ModuleNotFound error with `openai`, try `export PATH=“/git/openai-quickstart-python:${PATH}”`.
3. Run `python app.py`. (If you are running with Python3, run `python3 app.py`.)

## Env variables that need to be set:
- OPENAI_API_KEY (openai)
- MONGO_LINK (mongoDB atlas)
