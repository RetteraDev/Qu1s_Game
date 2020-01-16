# PartyGame

![](https://img.shields.io/github/stars/Qu1s/PartyGame?style=for-the-badge) ![](https://img.shields.io/github/forks/Qu1s/PartyGame?style=for-the-badge) ![](https://img.shields.io/github/issues/Qu1s/PartyGame?style=for-the-badge) ![](https://img.shields.io/github/license/Qu1s/PartyGame?style=for-the-badge)

###What is it?
It is game for company(2-8 players), where you can spend time with your friends by playing different small rounds.
###Setup
- Make virtual environment like
>virtualenv venv --python=python3
source venv/bin/activate


- Install requirements.txt with pip 
>pip3 install < requirements.txt

- Create site/app/secret.py file and enter
> secret_key  = "YOUR_SECRET_KEY"
- Run site/app/setupDB.py for create DataBase
- Run site/app/main.py for start Flask web-application
- Run desktop/pygametest.py in new terminal
- Open URL 192.168.43.217:8080 in your browser on PC or Android

###Features
- ~~Login from browser~~
- ~~Database logging~~
- ~~Rooms for players~~
- ~~Simple game lobby in PC client~~
- Write JS code for browsers on socketio, that can receive tasks and sent answers
- Make some tasks for game
- Make code better and cleaner
- Write documentation
- Debugging
