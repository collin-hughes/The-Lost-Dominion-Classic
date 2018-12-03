"""Collaborative: Function to check the player's current wave against the saved highscore file if the file exists. If the file does not exist, the file is created."""
"""If the player has a higher wave than the recorded highscore, the highscore is replaced with the new highscore"""

def check_high_score(wave):
    try:
        high = int(open("highscore.txt", "r").read())
        if wave > high:
            writeIt = open("highscore.txt","w")
            writeIt.write(str(wave))
            return wave
        else:
            return high
    except FileNotFoundError:
        score = open("highscore.txt", "w")
        score.write(str(wave))

"""Bren Stace: Function writes the highscore 1 to the highscore file - Bren Stace"""
def reset_high_score():
    score = open("highscore.txt","w")
    score.write("1")
