# scoreboard.py

## Description
Create PNG images for various types of scoreboards.


## Usage
```py
from scoreboard import Leaderboard

ranking = [
    ("Player 1", 30),
    ("Player 2", 15),
    ("Player 3", 50)
]

# Save png image
lb = Leaderboard(ranking)
lb.save_image("leaderboard.png")

# Save base 64 encoded image
b64_leaderboard = lb.b64_image()
with open("leaderboard.b64", "wb") as f:
    f.write(b64_leaderboard)
```

## Image Examples

### Leaderboard

![Leaderboard Image](https://raw.githubusercontent.com/lucasvanmol/scoreboard/main/example_images/leaderboard.png)

```py
from scoreboard import Leaderboard, Head2Head

# Save Leaderboard png with default settings
# Background is transparent by default
ranking = [("A really long username", 30), ("Player 1", 15), ("Player 2", 50)]
lb = Leaderboard(ranking, title="Ranking")
lb.save_image("example_images/leaderboard.png")
```

### Head2head

![Head2head Image](https://raw.githubusercontent.com/lucasvanmol/scoreboard/main/example_images/head2head.png)

```py
# Head2head with some custom colors
teams = [("New York PoNY", 12), ("Seattle Sockeye", 8)]
h2h = Head2Head(
    teams, 
    fill_color=(241, 250, 238),
    text_color=(69, 123, 157),
    score_color=(29, 53, 87),
    rectangle_color=(230, 57, 70)
)
h2h.save_image("example_images/head2head.png")
```
