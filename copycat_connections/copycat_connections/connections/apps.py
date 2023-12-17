from django.apps import AppConfig


class CopycatAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "connections"

    # Use this method to add puzzles if there are none in the database
    # def ready(self):
    #     from .add_puzzle import add_puzzles
    #     # Add the puzzles to the database from the connections.txt file
    #     add_puzzles()
