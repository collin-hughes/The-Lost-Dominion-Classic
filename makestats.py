"""Bren Stace: Creates the stats for the mob, using the wave as a parameter"""

def makeHealth(wave):
	healthbase = 9
	health = healthbase + (wave)**1.20
	return health
def makeStrength(wave):
	strbase = 0
	strength = strbase + (wave**1.15)/10
	return strength
