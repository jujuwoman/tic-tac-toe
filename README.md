# Tic-Tac-Toe
The project uses Django and PostgreSQL to implement a web application for a user to play the classic [tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe) game against the computer.


## Environment
### Requirements
The application was developed under the following ecosystem. To ensure that the game works on your machine, please install or update:
> [Python 3.7](https://www.python.org/downloads/)   
> [Django 3.0.4](https://www.djangoproject.com/download/)    
> [PostgreSQL 12.2](https://www.postgresql.org/download/)  
> [macOS Catalina 10.15.3](https://www.apple.com/macos/catalina/)

To use PostgreSQL with Python, we also need the following package:
> [psycopg2-binary 2.8.4](https://pypi.org/project/psycopg2-binary/)  

**Important:** Do not use the related `psycopg2` package. The last few versions of the package will cause data migration issues.


### Debugging Tools
IDE:
> [PyCharm Professional 2019.3.3](https://www.jetbrains.com/pycharm/download/#section=mac)  

Since querying a database via CLI can be laborious, a  database client that allows us to monitor PostgreSQL data tables is essential:
> [Postico](https://eggerapps.at/postico/)


## Run
Once the player saves the `tic_tac_toe` application folder to their machine, they can run the game from an IDE that supports Django or from CLI. Since my IDE of choice is PyCharm, I've included the instructions for that particular IDE. If the IDE instructions fail, I've also included the instructions for CLI. Django automatically builds the application upon running. 

In Terminal, change directory into `tic_tac_toe`. Initialize database by entering:
> `python3 manage.py makemigrations && python3 manage.py migrate`

### PostgreSQL (Postgres)
To start PostgreSQL server now and relaunch at login:
> `brew services start postgresql`  
> `brew services stop postgresql`   

Or, if you don't need a background service you can just run:
> `pg_ctl -D /usr/local/var/postgres start` 
> `pg_ctl -D /usr/local/var/postgres stop`

Getting Postgres to work with Django may take some trial and error. Here some other useful commands:
> `pg_ctl -D /usr/local/var/postgres start && brew services start postgresql`  
> `python3 manage.py runserver`   
> `python3 manage.py startapp tic_tac_toe`  
> `python3 manage.py makemigrations tic_tac_toe`   
> `python3 manage.py makemigrations tic_tac_toe; python3 manage.py migrate`   
> `python3 manage.py makemigrations && python3 manage.py migrate`  
> `python3 manage.py migrate --fake`   
> `python3 manage.py collectstatic`   
> `python3 manage.py collectstatic --noinput --clear`   

Troubleshooting resources:
* Command to locate `pg_hba.conf` and `postgresql.conf` ([Stackoverflow](https://stackoverflow.com/questions/33015471/cannot-find-pg-hba-conf-and-postgreql-conf-file-on-os-x)):
    > `find / -iname "postgresql.conf" 2>/dev/null` 
* Location of Postgres configuration file:
    > `/usr/local/Cellar/postgresql/12.2/bin/pg_config`

### PyCharm
1. Start PyCharm and open project folder `tic_tac_toe`.
2. Since the project was constructed with Python 3.7, it is likely the safest version to use. To choose Python 3.7 as the project interpreter, go to PyCharm > Preferences > Project: tic_tac_toe > Project Interpreter. Click on the gear ⚙ icon and choose Add... In the popup, highlight System Interpreter and select Python 3.7 in the dropdown menu. Hit OK. 
3. In the Navigation Bar (View > Appearance, check Navigation Bar) dropdown menu, select tic_tac_toe and click the adjacent Run button. If the run console indicates that port 8000 is already in use, free the port by entering `lsof -i :8000` in Terminal, copy the Python PID and enter `kill -9 <PID>`. Run the application via the Navigation Bar again.
6. Visit Django's [development server](http://127.0.0.1:8000) ([admin](http://127.0.0.1:8000/admin/) site) in browser to play.

### CLI
1. In Terminal, enter `python3 manage.py runserver` while in the `tic_tac_toe` directory. If port 8000 is already in use, free the port with `Control-C`.
4. Visit Django's [development server](http://127.0.0.1:8000) ([admin](http://127.0.0.1:8000/admin/) site) in browser to play.


## Design
In classic tic-tac-toe, 2 players face off on a 3✕3 grid. I toyed with the idea of having an _n_✕_m_ grid with multiple players, but a binary rhythm superimposed on a symmetric structure has its beauty. I also did not want to sacrifice maintainability for generality. The application allows either (1) a human player to play against the computer or (2) the computer to play against itself.

### Code
- The game's graphical components are fixed to their absolute positions. Each player's move is saved to the server cache, allowing the server to maintain an internal representation of the game state at all times. This means changes in components, refreshes, or redirects do not disrupt the visual experience.

- A PostgreSQL data table keeps track of each of the two players' order, name, columns visited, rows visited, major diagonal visited, and minor diagonal visited. The data table enables the application to determine if a player's move results in one of the games terminating conditions (i.e. win or draw) by taking advantage of a constant time algorithm. Postico comes in _very_ handy when debugging and testing code that interacts with the data table.

- At the start of a new gaming session, the application clears old data from the cache and data table to ensure that the game behaves predictably. A reset button at the bottom does the same thing.

- At the start of a gaming session, the web interface prompts the player to enter their name. The name is converted to lowercase since the font choice uses the same typography for both cases.

- A delay of 300 milliseconds occurs before the computer makes a move. This allows for a more natural experience for the human player. 

- The computer makes each move by randomly choosing an unoccupied cell. You would be surprised how often this strategy beats me.

### Behavior
- In order for the game to start, the player must enter a name.

- To have the computer play against itself, enter `computer` in the name field. 


## Extension Ideas
- Incorporate new tools:
    * Heroku (cloud-based development)
    * Angular JS (unified server request framework)  
    * Mongo DB (easier-to-handle database)  
    * Bootstrap (better-looking CSS)  
    * Selenium (automatic template generation)  

    
- Allow 2 human players to play over the network.

- Incorporate a data table that keeps track of each player's history of wins, draws, losses, and last play time. We can than sort the entries by different attributes for ranking purposes.

- Improve computer's gameplay strategy beyond choosing any free cell by random.
    - The history data table mentioned above can supply training data to classification algorithms (e.g. Naïve Bayes, SVM).
    - We can have the computer play against itself to train a recurrent neural network.


---
Judy Wang   
https://www.linkedin.com/in/jujuwoman  
https://github.com/jujuwoman


