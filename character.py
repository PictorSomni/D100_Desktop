from random import randint as rng
from random import choice
import CONSTANT


class Character:
    """Creation of random NPCs"""

    def __init__(self, **kwargs):
        super(Character, self).__init__()
        self.name = kwargs.get("name", choice(CONSTANT.NAME))
        self.origin = kwargs.get("origin", choice(CONSTANT.ORIGIN))
        self.vocation = kwargs.get("vocation", choice(CONSTANT.COMMON_VOCATION))
        self.physic = kwargs.get("physic", 50)
        self.social = kwargs.get("social", 50)
        self.mental = kwargs.get("mental", 50)
        self.health = kwargs.get("health", 10)
        self.mana = kwargs.get("mana", rng(0, 2))
        self.posture = kwargs.get("posture", CONSTANT.POSTURES[-1])


        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self) :
        return ("{}, {} {}\nPhysique = {}, Social = {}, Mental = {}".format(self.name, self.origin, self.vocation, self.physic, self.social, self.mental))


    def get_character(self) :
        return [self.name, self.origin, self.vocation, self.physic,
                    self.social, self.mental, self.health, self.mana, self.posture]

    def get_key(self) :
        return ["Nom", "Origine", "Vocation", "Physique",
                    "Social", "Mental", "Vie", "Mana", "Posture"]