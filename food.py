import random

death_effects = [
    "instant death",
    "becoming dead",
    "dying instantly",
    "loss of life",
    "not living",
    "becoming a corpse",
    "transforming into a corpse",
    "loss of existence",

    "heart attack",
    "heart failure",
    "failure of the heart",
    "heart stops beating",
]

benign_effects = [
    "deafness",
    "stomachache",
    "loss of wife",
    "not thriving",
    "loss of excitement",
    "loss of hearing",
    "headache",
    "desire to die",
    "living the life",
    "strange thoughts",
    "hallucination",
    "dying on the inside",
    "becoming deaf",
    "becoming corporate",
    "malnutrition",
    "stomach pangs",
    "attraction to death",

    "hearing failure",
    "heart beats faster",

    "liver vibrations",
]

class Food:
    """ Defaults to not lethal with no effects. """
    def __init__(self):
        self.lethal = False
        self.effects = []

class FoodGenerator:

    def __init__(self):
        self.level = 0
        self.foods_until_safe = random.randint(0, 3)

    def generate_benign(self):
        food = Food()

        effect_count = random.randint(6, 9)

        # Generates random benign effects
        for effect in range(effect_count - 1):
            effect = random.choice(benign_effects)
            while effect in food.effects:
                effect = random.choice(benign_effects)
            food.effects.append(effect)

        random.shuffle(food.effects)

        return food

    def generate_lethal(self):
        food = self.generate_benign()

        # Replaces one benign effect with a lethal effect
        position = random.randint(0, len(food.effects) - 1)
        food.effects[position] = random.choice(death_effects)
        food.lethal = True

        return food

    def next_item(self):
        if self.foods_until_safe == 0:
            self.foods_until_safe = random.randint(0, 3)
            return self.generate_benign()

        else:
            self.foods_until_safe -= 1
            return self.generate_lethal()