# Copycat Connections

The Copycat Connections app is a Django web application that allows users to play a word-based game 
where they need to group words that share a common thread. This game is heavily inspired by the 
New York Times Connections game, and uses their puzzles. 

## Features

- Word-based game with puzzles to solve.
- Group words that have a common connection.
- Play and enjoy the challenging puzzles.
- An archive of puzzles allows users to play older puzzles that they missed
- Registration and login features allow users to sign up and keep track of which puzzles they've
completed

## Getting Started
1. Ensure Django is installed
2. Navigate to the project directory
3. **If you are using an empty database**, you will need to run the commands [python manage.py makemigrations]
and [python manage.py migrate]. Then, you will need to populate the database by running the add_puzzles 
function in add_puzzle.py. One way this can be done is by opening the /connections/apps.py file and 
un-commenting the CopycatAppConfig.ready() method. This will populate the database at server startup.
4. Run the command [python manage.py runserver] to start the development server. Click on the URL to open
it in a browser window and interact with the app.

Built and tested with Python version 3.10


Usage
Access the app by visiting http://localhost:8000.
In order to play, select four words that you think go together, and click 'submit.' Be careful, as
you only get four guesses. If you use up all your guesses, the answers will be revealed.
Have fun!
