# -*- coding: UTF-8 -*-


import os


##########################################################################################
# CHARACTER GENERATION
##########################################################################################

# Player and opponent oriented vocation list.
ADVENTURE_VOCATION = ["assassin", "guerrier", "mage", "paladin",
                   "pirate", "pretre", "ranger", "voleur"]


# NPC oriented vocation list.
COMMON_VOCATION= ["ambassadeur", "aubergiste", "bourgeois",
                 "bucheron", "conducteur de caleche", "couturier",
                 "fermier", "forgeron", "garde", "ivrogne", "menestrel",
                 "marchand", "mineur", "noble", "pretre",
                 "roturier", "sentinelle","tanneur", "vagabon",
                 "voyageur"]


# All existing origins for players or NPCs.
ORIGIN = ["barbare", "demi-elfe", "demi-orc", "elfe noir",
           "elfe sylvain", "gnome", "goblin",
           "haut-elfe", "hobbit", "humain", "nain", "ogre", "orc", "corrompu"]


# A generic list of names, one male and one female starting by each letter of the alphabet.
NAME = ["Alan", "Bernard", "Christophe", "Daniel", "Ethan",
       "Francis", "Guillaume", "Henry", "Isidore", "Julien",
       "Karl", "Laurent", "Marc", "Nathan", "Oscar", "Pierre",
       "Quentin", "Raphael", "Steve", "Tristan", "Umberto",
       "Victor", "Walter", "Xavier", "Yves", "Zaccaria", "Alice",
       "Betty", "Clara", "Diana", "Eline", "Francoise", "Gaia",
       "Helene", "Iris", "Juliane", "Keira", "Lina", "Manon",
       "Nathalie", "Oceane", "Paprika", "Quistis", "Rose",
       "Sarah", "Talya", "Ulyssia", "Valentine", "Wendy", "Xena",
       "Yolanda", "Zoe"]


# The postures each character can play.
POSTURES = ["offensive", "défensive", "focus", "sans posture"]

##########################################################################################
# BONUS / MALUS
##########################################################################################

# Bonus / Malus list of events. Can be used by a player as bonus or by the GM as malus.
BONUS_MALUS = ["Mouvement", "Posture", "In-Extremis"]


##########################################################################################
# TIMER EVENTS
##########################################################################################

# Useful events happening when the timer runs out. 
TIMER_EVENT = ["apparition de corrompus", "apparition d'ennemis", 
                "corruption de prêtre noir", "chant d'un prêtre noir",
                "ouverture de portail imminente", "quelqu'un vous observe",
                "grondement au loin"]

RANDOM_NPC_WAVE = ["Vague aléatoire de races mixte", "Vague aléatoire de race identique"]


##########################################################################################
# PATHS
##########################################################################################

PATH = os.path.dirname(os.path.abspath(__file__))
AUDIO_PATH = "{}/audio/".format(PATH)
AUDIO_FILES = sorted([os.path.splitext(file)[0] for file in os.listdir(AUDIO_PATH)])
AUDIO_DIRECTORIES = sorted([file for file in os.listdir(AUDIO_PATH) if os.path.isdir("{}/{}".format(AUDIO_PATH, file))])


##########################################################################################
# SOUND BOX
##########################################################################################

SOUNDBOX_BUTTONS_PER_ROW = 5


##########################################################################################
# FONT SIZE
##########################################################################################

FONT_SIZE = "font-size : 18px"