#!/user/bin/env python3
from collections import OrderedDict
import datetime
import sys
import os

from peewee import *


db = SqliteDatabase('blog.db')

class Entry(Model):
    # content
    content = TextField()
    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """Create the database and table if it doesn't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """show the menu"""
    choice = None  # create an empty variable
    while choice != 'q':  # while choice is not quit
        clear()
        print("Press 'Q' To Leave")  # on going display
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))  # displays choice options and the function it triggers
        choice = input('Action: ').strip().lower()  # input
        if choice in menu:  # if they choose an available key...
            clear()
            menu[choice]()  # trigger function where [choice] is value


def add_entry():
    """Add an Entry"""
    print("Enter your entry, press ctrl+d to finish.")
    data = sys.stdin.read().strip()

    if data:
        if input("Save Entry? [Y/N]: ").lower() != 'n':
            Entry.create(content=data)
            print('Saved')


def view_entry(search_query=None):
    """View Previous Entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d %y %I %M%p')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print("\n")
        print(entry.content)
        print('\n\n' + '='*len(timestamp))
        print("n) For Next Entry")
        print("d) Delete Entry")
        print("q) To Return to Main Menu")

        next_action = input('Action: '.lower().strip())
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entry():
    """Search entries for a string"""
    view_entry(input('Search Query: '))


def delete_entry(entry):
    """delete an entry"""
    if input("Are You Sure? [Y/N]: ").lower() == 'y':
        entry.delete_instance()
        print("Entry Deleted")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entry),
    ('d', delete_entry)
])


if __name__ == '__main__':
    initialize()
    menu_loop()
