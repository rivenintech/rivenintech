# ⛵ Github Battleship - How does it work?

## Table of Contents
1. [Components needed](#everything-works-by-using-a-few-components)
2. [Board representation](#board-representation)
3. [Github Actions](#github-actions)
4. [Creating a new game](#creating-a-new-game)
    1. [Database](#database)
    2. [Modifying the README.md](#modifying-the-README)
    3. [Commiting, pushing and closing the issue](#commiting,-pushing-and-closing-the-issue)
5. [Playing the game](#playing-the-game)
6. [Cool additions](#cool-additions)
7. [Inspirations](#inspirations)

### Everything works by using a few components:
- **Github Actions** - to run your code when someone an issue is created
- **Python script** - to take care of game logic (back-end)
- **Database (MongoDB)** - to store data
- **README.md file** - to make everything look pleasant (front-end)

## Board representation
To represent the board, I created this [bitboard](https://en.wikipedia.org/wiki/Bitboard) to represent each table cell by a different number. When someone makes a move, I can easily (with the use of math) find its location. It's also easy to generate ships with this method. I can choose one random number and then go horizontally or vertically to get the rest of the ship.

*Note the extra numbers on the right. All of these numbers are treated as incorrect. This way Python script knows when the row ends.*

```
+---------------------------------------+
| 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  |  8   
| 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 |  17
| 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |  26
| 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 |  35
| 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 |  44
| 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 |  53
| 54 | 55 | 56 | 57 | 58 | 59 | 60 | 61 |  62
| 63 | 64 | 65 | 66 | 67 | 68 | 69 | 70 |  71
+---------------------------------------+
```

## Github Actions
Whenever an issue with the prefix `battleship|action|location` is opened, it triggers the Github Actions workflow. The title of the issue and your username is passed as environment variables to a Python script, which then splits the issue title every `|` and decides if it should create a new game or make a move based on `action`.

## Creating a new game
When a new game has to get created, we need to make a blank board with ships placed randomly. To do it, we call the `create_game()` function that calls the` place_ships()` function, which generates a ship by choosing one random place on board and then generating the rest of it from this point (horizontally or vertically).

### Database
Now we have to store ships location somewhere. We could place them in a plain text file, but then everyone could see where the ships are, so we have to hide them elsewhere. That's when a proper database comes in handy. I used MongoDB for this as it fits my needs.

### Modifying the README
Time to change our board visually by modifying the `README` file. We can do it using the same method we would use to [modify a text file](https://www.w3schools.com/python/python_file_handling.asp). First, we read the file line by line and save content to a variable. We can then [modify the specific lines we want](https://www.adamsmith.haus/python/answers/how-to-edit-a-specific-line-in-a-text-file-in-python). To create an empty table cell, I used a blank image with a link by using this format `[![](image link)](link that creates issue)`.

### Commiting, pushing and closing the issue
The last step is to commit and push everything to Github. We can do it with Github Actions with a few commands (***battleships.yml > Commit and push***). Then to keep everything clean, we should close the issue by using [`peter-evans/close-issue@v2`](https://github.com/marketplace/actions/close-issue) with Github Actions.

## Playing the game
The process is the same as with [creating a new game](#creating-new-game). Instead, we have to check if the location shot has the ship or not by using our database and modifying this location in README with either a white or red mark image.

## Cool additions
- The statistics under the game title were made with [shields.io](https://shields.io).
- A leaderboard is made by storing all users with their statistics and sorting the database by shots hit.

<br>

### Inspirations
- Connect Four game by [@JonathanGin52](https://github.com/JonathanGin52)
- Tic-Tac-Toe by [@DoubleGremlin181](https://github.com/DoubleGremlin181)