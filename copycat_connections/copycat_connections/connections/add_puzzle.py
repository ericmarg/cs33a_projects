from datetime import datetime

from .models import Puzzle


def add_puzzles():
    file_path = "/connections/data/connections.txt"
    with open(file_path) as file:
        line = file.readline()
        puzzle = {}
        date, numer = None, None
        counter = 0
        while line:
            s = line.split('#')
            if len(s) == 2:
                # A new date indicates a new puzzle
                puzzle.clear()

                # Lines split by a hash will have a date and number
                date, number = s[0].strip(), s[1].strip()

                # Define the format of the date string
                date_format = "%b %d, %Y"

                # Parse the date string into a date object
                date = datetime.strptime(date, date_format).date()
            else:
                s = line.split(':')
                if len(s) == 2:
                    counter += 1
                    category, words = s[0].strip(), s[1].strip()
                    # Split the words separated by commas and strip whitespace and put them back into a list
                    words = [word.strip() for word in words.split(',')]
                    puzzle.update({f'row-{counter}': {category: words}})

            if counter == 4:
                counter = 0
                Puzzle.objects.create(date=date, number=number, puzzle=puzzle)
                puzzle.clear()

            line = file.readline()
