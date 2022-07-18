start_line = 20 - 1 # Line number of "Try out my Battleship game!"

def new_game(spaces : int):
    links = [f"https://github.com/RiveN000/RiveN000/issues/new?title=battleship%7Cshoot%7C{x}&body=Just+push+%27Submit+new+issue%27+without+editing+the+title.+The+README+will+be+updated+after+approximately+30+seconds." for x in range(0, 71)]

    template = f"""
**🎯 Game still didn't end! Spaces left: {spaces}**

|       | A  | B  | C  | D  | E  | F  | G  | H  |
|-------|----|----|----|----|----|----|----|----|
| **1** |[![](image)]({links[0]})|[![](image)]({links[1]})|[![](image)]({links[2]})|[![](image)]({links[3]})|[![](image)]({links[4]})|[![](image)]({links[5]})|[![](image)]({links[6]})|[![](image)]({links[7]})|
| **2** |[![](image)]({links[9]})|[![](image)]({links[10]})|[![](image)]({links[11]})|[![](image)]({links[12]})|[![](image)]({links[13]})|[![](image)]({links[14]})|[![](image)]({links[15]})|[![](image)]({links[16]})|
| **3** |[![](image)]({links[18]})|[![](image)]({links[19]})|[![](image)]({links[20]})|[![](image)]({links[21]})|[![](image)]({links[22]})|[![](image)]({links[23]})|[![](image)]({links[24]})|[![](image)]({links[25]})|
| **4** |[![](image)]({links[27]})|[![](image)]({links[28]})|[![](image)]({links[29]})|[![](image)]({links[30]})|[![](image)]({links[31]})|[![](image)]({links[32]})|[![](image)]({links[33]})|[![](image)]({links[34]})|
| **5** |[![](image)]({links[36]})|[![](image)]({links[37]})|[![](image)]({links[38]})|[![](image)]({links[39]})|[![](image)]({links[40]})|[![](image)]({links[41]})|[![](image)]({links[42]})|[![](image)]({links[43]})|
| **6** |[![](image)]({links[45]})|[![](image)]({links[46]})|[![](image)]({links[47]})|[![](image)]({links[48]})|[![](image)]({links[49]})|[![](image)]({links[50]})|[![](image)]({links[51]})|[![](image)]({links[52]})|
| **7** |[![](image)]({links[54]})|[![](image)]({links[55]})|[![](image)]({links[56]})|[![](image)]({links[57]})|[![](image)]({links[58]})|[![](image)]({links[59]})|[![](image)]({links[60]})|[![](image)]({links[61]})|
| **8** |[![](image)]({links[63]})|[![](image)]({links[64]})|[![](image)]({links[65]})|[![](image)]({links[66]})|[![](image)]({links[67]})|[![](image)]({links[68]})|[![](image)]({links[69]})|[![](image)]({links[70]})|

<br>

|⏰ Most recent moves|
|--------------------|
|                    |
|                    |
|                    |
"""
    template = template.replace("image", "https://raw.githubusercontent.com/RiveN000/RiveN000/main/assets/blank.png")

    # Read file content
    with open("README.md", "r") as f:
        file_content = f.readlines()

    # Modify the file
    for i in range(start_line + 7, start_line + 27):
        file_content[i] = ""

    file_content[start_line + 6] = template

    # Save file content
    with open("README.md", "w") as f:
        f.writelines(file_content)


def shoot(action : str, location : int, total_shots : int, players_num : int, spaces : int, msg : str, leaderboard : list):
    # Read file content
    with open("README.md", "r") as f:
        file_content = f.readlines()

    # Modify the file
    row = location // 9 + (start_line + 11)
    col = location % 9 + 2
    temp = file_content[row].split("|")
    temp[col] = f"![](https://raw.githubusercontent.com/RiveN000/RiveN000/main/assets/{action}_mark.png)"
    file_content[row] = "|".join(temp)
    file_content[start_line + 1] = f"![](https://img.shields.io/badge/Total%20shots-{total_shots}-blue)\n"
    file_content[start_line + 3] = f"![](https://img.shields.io/badge/Total%20players-{players_num}-orange)\n"
    file_content[start_line + 7] = f"**🎯 Game still didn't end! Spaces left: {spaces}**\n"
    file_content[start_line + 26] = file_content[start_line + 25]
    file_content[start_line + 25] = file_content[start_line + 24]
    file_content[start_line + 24] = msg

    for x, player in enumerate(leaderboard):
        file_content[start_line + 32 + x] = f"|[@{player['name']}](https://github.com/{player['name']})|{player['hit']}|{player['total']}|\n"

    # Save file content
    with open("README.md", "w") as f:
        f.writelines(file_content)


def game_ended(total_games : int, shots_num : int, places_left : list):
    # Read file content
    with open("README.md", "r") as f:
        file_content = f.readlines()

    # Modify the file
    file_content[start_line + 2] = f"![](https://img.shields.io/badge/Total%20games-{total_games}-brightgreen)\n"
    file_content[start_line + 7] = f"**🎉 Game ended! It took: {shots_num} shots! [Click here to start new game.](https://github.com/RiveN000/RiveN000/issues/new?title=battleship%7Cnew&body=Just+push+%27Submit+new+issue%27+without+editing+the+title.+The+README+will+be+updated+after+approximately+30+seconds.)**\n"

    # Loop through all locations that are left and change to "blank.png"
    for location in places_left:
        row = location // 9 + (start_line + 11)
        col = location % 9 + 2
        temp = file_content[row].split("|")
        temp[col] = f"![](https://raw.githubusercontent.com/RiveN000/RiveN000/main/assets/blank.png)"
        file_content[row] = "|".join(temp)

    # Save file content
    with open("README.md", "w") as f:
        f.writelines(file_content)