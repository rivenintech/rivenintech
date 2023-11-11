import random
from os import getenv
from string import ascii_uppercase

import modify_readme
import pymongo

# MongoDB Setup
cluster = pymongo.MongoClient(getenv("MONGODB_KEY"))
db = cluster["battleship"]
data = db["data"]
players = db["players"]

# Get some data from database
info = data.find_one({"_id": "current_game"})
ships_location = info["ships_location"]
location_shot = info["location_shot"]

# These values can be changed to change the game
ships = [2, 3, 3, 4, 5]
rows = 8
cols = 8

# Don't change these values
# https://rivenintech.com/projects/battleship-game-in-readme#board-representation
places = set(range(0, rows * (cols + 1)))
# Remove extra column and location shot from available places
places = places.difference(list(places)[cols :: cols + 1])
col = list(ascii_uppercase[:cols])
row = list(range(1, rows + 1))
user = getenv("EVENT_USER")


# Finds a place for ships on the board
def place_ships():
    global ships_location
    available_places = places

    for ship_size in ships:
        while True:
            points = []
            direction = random.choice(
                [1, 9]
            )  # Pick random direction (Right/left or up/down)

            while True:  # Choose random available place on board
                start_point = random.choice(list(available_places))
                points.append(start_point)
                break

            for _ in range(
                ship_size - 1
            ):  # Pick other places for ship going from start_point
                points.sort()

                choices = [  # Direction choices
                    points[0] + (direction * -1),
                    points[len(points) - 1] + direction,
                ]

                x = random.randint(0, 1)

                if (
                    choices[x] not in available_places
                ):  # Place picked is incorrect or not available
                    x = abs(x - 1)

                    if (
                        choices[x] not in available_places
                    ):  # Place picked is incorrect or not available
                        break  # Can't place ship, no available space

                points.append(choices[x])

            if len(points) == ship_size:  # Return if places where picked correctly
                ships_location += points
                available_places -= get_surrounding_places(points, rows, cols)
                break


def get_surrounding_places(points, rows, cols):
    surrounding_points = set()

    for point in points:
        row_idx = point // cols
        col_idx = point % cols

        # Add the current point
        surrounding_points.add(point)

        # Add left, right, up, down
        if col_idx > 0:
            surrounding_points.add(point - 1)
        if col_idx < cols - 1:
            surrounding_points.add(point + 1)
        if row_idx > 0:
            surrounding_points.add(point - cols)
        if row_idx < rows - 1:
            surrounding_points.add(point + cols)

        # Add diagonals
        if col_idx > 0 and row_idx > 0:
            surrounding_points.add(point - cols - 1)
        if col_idx < cols - 1 and row_idx > 0:
            surrounding_points.add(point - cols + 1)
        if col_idx > 0 and row_idx < rows - 1:
            surrounding_points.add(point + cols - 1)
        if col_idx < cols - 1 and row_idx < rows - 1:
            surrounding_points.add(point + cols + 1)

    return surrounding_points


def create_game():
    if ships_location:  # Not empty - game didn't end yet
        raise Exception(
            f"@{user} :x: Game didn't end yet! Finish it, before creating new one.\n"
        )

    # Finds place for all ships on the board and adds them to "ships_location"
    place_ships()

    # Database - Adds ships location, clears location shot and number of shots
    data.update_one(
        {"_id": "current_game"},
        {
            "$set": {
                "ships_location": ships_location,
                "location_shot": [],
                "shots_num": 0,
            }
        },
    )

    # Render README
    modify_readme.new_game(len(ships_location))

    return f"@{user} started a new game\n"


def shoot(location: int):
    global ships_location

    loc = f"{col[location % 9]}{row[location // 9]}"

    # Update and get updated documents from database
    current_game = data.find_one_and_update(
        {"_id": "current_game"},
        {"$inc": {"shots_num": 1}, "$push": {"location_shot": location}},
        return_document=pymongo.ReturnDocument.AFTER,
    )

    stats = data.find_one_and_update(
        {"_id": "stats"},
        {"$inc": {"total_moves": 1}},
        return_document=pymongo.ReturnDocument.AFTER,
    )

    # Update player's database document
    players.update_one(
        {"_id": getenv("EVENT_USER_ID")},
        {"$set": {"name": getenv("EVENT_USER")}, "$inc": {"total": 1, "hit": 0}},
        upsert=True,
    )

    # Hit ship (count ships left, update database and get leaderboard)
    if location in ships_location:
        ships_left = len(ships_location) - 1
        data.update_one(
            {"_id": "current_game"}, {"$pull": {"ships_location": location}}
        )
        players.update_one({"_id": getenv("EVENT_USER_ID")}, {"$inc": {"hit": 1}})
        leaderboard = (
            players.find()
            .sort({"hit": pymongo.DESCENDING, "total": pymongo.DESCENDING})
            .limit(5)
        )

        # Create alert (for commit and recent moves)
        msg = (
            f"[@{user}](https://github.com/{user}) hit the ship at location **{loc}**\n"
        )

        # Render README
        modify_readme.shoot(
            "hit",
            location,
            stats["total_moves"],
            players.count_documents({}),
            ships_left,
            msg,
            leaderboard,
        )

        # No ships left. Game ended
        if ships_left == 0:
            data.update_one({"_id": "stats"}, {"$inc": {"total_games": 1}})

            modify_readme.game_ended(
                stats["total_games"] + 1,
                current_game["shots_num"],
                list(places.difference(location_shot)),
            )

        return f"@{user} hit the ship at location {loc}\n"

    else:  # Missed ship
        # Create alert (for commit and recent moves)
        msg = f"[@{user}](https://github.com/{user}) missed the ship at location **{loc}**\n"

        # Get leaderboard
        leaderboard = (
            players.find()
            .sort({"hit": pymongo.DESCENDING, "total": pymongo.DESCENDING})
            .limit(5)
        )

        # Render README
        modify_readme.shoot(
            "miss",
            location,
            stats["total_moves"],
            players.count_documents({}),
            len(ships_location),
            msg,
            leaderboard,
        )

        return f"@{user} missed the ship at location {loc}\n"


if __name__ == "__main__":
    try:
        title = getenv("EVENT_ISSUE_TITLE").split("|")

        if title[1] == "new":  # Create new game
            msg = create_game()
        elif title[1] == "shoot":
            location = int(title[2])  # Location to shoot

            # Game already ended
            if not ships_location:
                raise Exception(
                    f"@{user} :x: Game already ended! Start new game first.\n"
                )

            # Incorrect location
            if location not in places.difference(location_shot):
                raise Exception(
                    f"@{user} :x: Location is incorrect. Did you modify the issue title?\n"
                )

            msg = shoot(location)

        issue_msg = ":white_check_mark: README just got updated!\n"

        with open(getenv("GITHUB_ENV"), "a") as f:  # Creating custom commit message
            f.write(f"COMMIT_MSG={msg}")

    except Exception as error:  # If someone modifies issue title
        issue_msg = error

    with open(getenv("GITHUB_ENV"), "a") as f:  # Creating custom issue comment
        f.write(f"ISSUE_MSG={issue_msg}")
