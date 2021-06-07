from scoreboard import Leaderboard, Head2Head

# Save Leaderboard png with default settings
# Background is transparent by default
ranking = [("A really long username", 30), ("Player 1", 15), ("Player 2", 50)]
lb = Leaderboard(ranking, title="Ranking")
lb.save_image("example_images/leaderboard.png")


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