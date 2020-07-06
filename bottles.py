import random
import pygame

import const
import colors
import graphics
import files

DEATH_EFFECTS_PATH = "data\\death_effects.json"
death_effects = files.json_read(DEATH_EFFECTS_PATH)

BENIGN_EFFECTS_PATH = "data\\benign_effects.json"
benign_effects = files.json_read(BENIGN_EFFECTS_PATH)

ALLERGENS_PATH = "data\\allergens.json"
allergens = files.json_read(ALLERGENS_PATH)

BRANDS_PATH = "data\\brands.json"
brands = files.json_read(BRANDS_PATH)

letters = [chr(a) for a in range(ord('a'), ord('z'))]


def generate_verification_code(length):
    code = []
    for _ in range(length):
        code.append(random.choice(letters))
    code.sort()
    return "".join(code)


def generate_fake_verification_code(length):
    string = generate_verification_code(length)
    code = list(string)

    # Check if the code is all the same letter
    for letter in code:
        if letter != code[0]:
            break
    # If it is, the fake algorithm won't work.  Generate a new code
    else:
        return generate_fake_verification_code(length)

    # Randomly finds two adjacent letters that aren't the same
    i = random.randint(0, length - 2)
    while code[i] == code[i + 1]:
        i = random.randint(0, length - 2)

    # Swaps the two letters
    code[i], code[i + 1] = code[i + 1], code[i]

    return "".join(code)


def verification_code_is_valid(code):
    for i in range(1, len(code)):
        if code[i - 1] > code[i]:
            return False

    return True


for index in range(len(death_effects)):
    death_effects[index] = graphics.colorize(death_effects[index], "r")


TOP_TYPES = 5
TOP_ROUND_SMALL = 0
TOP_ROUND_MEDIUM = 1
TOP_ROUND_LARGE = 2
TOP_BEVEL = 3
TOP_INVERTED = 4

EFFECTS = "effects"
BODY_WIDTH = "body_width"
BODY_HEIGHT = "body_height"
LABEL_HEIGHT = "label_height"
LABEL_Y_OFFSET = "label_y_offset"
TOP_NUM = "top_num"
BOTTOM_NUM = "bottom_num"
CAP_X = "cap_x"
CAP_HEIGHT = "cap_height"
TOTAL_WIDTH = "total_width"
TOTAL_HEIGHT = "total_height"
PALETTE_NUM = "palette_num"


class Palette:
    def __init__(self, cap_color, body_color, label_color):
        self.cap_color = cap_color
        self.body_color = body_color
        self.label_color = label_color


PALETTES = [
    Palette((113, 113, 113), (225, 225, 225), (181, 181, 181)),  # Grayscale
    Palette((196, 196, 196), (225, 225, 225), (114, 238, 114)),  # Lime grey
    Palette((114, 238, 114), (225, 225, 225), (114, 238, 114)),  # Lime lime
    Palette((196, 196, 196), (225, 225, 225), (251, 246, 114)),  # Yellow grey
    Palette((255, 164, 38), (255, 221, 85), (234, 234, 234)),  # Tangerine
    Palette((43, 43, 43), (128, 10, 0), (214, 193, 193)),  # Strawberry Jam
    Palette((187, 187, 187), (124, 0, 177), (247, 208, 108)),  # Purple orange
    Palette((0, 156, 196), (0, 182, 255), (237, 237, 237)),  # Sky
    Palette((167, 72, 255), (255, 221, 85), (255, 112, 251)),  # Orange pink
    Palette((141, 138, 198), (9, 0, 155), (253, 241, 190)),  # Royal blue
    Palette((148, 148, 148), (88, 36, 11), (139, 110, 105)),  # Mahogany
    Palette((16, 255, 0), (150, 255, 144), (218, 255, 216)),  # Bright green
    Palette((33, 231, 0), (255, 0, 96), (205, 255, 202)),  # Watermelon
    Palette((243, 255, 56), (56, 255, 173), (202, 255, 247)),  # Toothpaste
    Palette((179, 0, 255), (0, 255, 227), (219, 184, 255)),  # Neapolitan
    Palette((82, 56, 119), (65, 0, 99), (210, 185, 237)),  # Purple
    Palette((197, 197, 197), (187, 217, 225), (0, 204, 172)),  # Teal label
    ]
TRANSPARENT_PALETTE = Palette(colors.TRANSPARENT, colors.TRANSPARENT, colors.TRANSPARENT)


TOP_COUNT = 6
tops = graphics.load_multiple_columns("images/bottle_top_%d.png", TOP_COUNT, 1)

BOTTOM_COUNT = 2
bottoms = graphics.load_multiple_columns("images/bottle_bottom_%d.png", BOTTOM_COUNT, 1)


CAP_PLACEHOLDER_COLOR = (100, 100, 100)
BODY_PLACEHOLDER_COLOR = (150, 150, 150)
LABEL_PLACEHOLDER_COLOR = (200, 200, 200)


def draw_wedge(surface, position, sprite, width, color):
    """ Draws two sprites on both sides of a rectangle.

    sprite is a SpriteColumn with 2 sprites in it, the first which will be
    on the left side of the rectangle, and the second which will be on the
    right.
    """

    # Draws left sprite
    sprite.draw(surface, position, 0)

    # Flips left sprite to make right sprite
    temp_surface = graphics.new_surface(sprite.single_size)
    sprite.draw(temp_surface, (0, 0), 0)
    flip_sprite = pygame.transform.flip(temp_surface, True, False)

    # Draws right sprite
    right_x = position[0] + width - sprite.single_width
    surface.blit(flip_sprite, (right_x, position[1]))

    # Draws middle rect
    middle_x = position[0] + sprite.single_width
    middle_width = position[0] + width - sprite.single_width * 2
    top_rect = (middle_x, position[1], middle_width, sprite.single_height)
    pygame.draw.rect(surface, color, top_rect)


class Bottle:
    """ Defaults to not lethal with no effects. """
    def __init__(self):
        self.lethal = False
        self.effects = []
        self.allergens = []
        self.allergies = []
        self.brand = ""
        self._bootleg = False
        self.code = ""

        # Main body
        self.body_width = random.randint(100, 230)
        self.body_height = random.randint(150, 200)

        # Label
        self.label_height = random.randint(75, self.body_height - 30)
        upper_bound = self.body_height - self.label_height - 10
        self.label_y_offset = random.randint(10, upper_bound)

        # Top and bottom curve of the bottle's body
        self.top_num = random.randint(0, len(tops) - 1)
        self.bottom_num = random.randint(0, len(bottoms) - 1)

        # Cap
        top_width = self.top.single_width
        self.cap_x = random.randint(top_width - 15, top_width - 2)
        self.cap_height = random.randint(20, 30)

        self._total_width = self.body_width
        total_height = 0
        total_height += self.cap_height
        total_height += self.body_height
        total_height += self.top.single_height
        total_height += self.bottom.single_height
        self._total_height = total_height
        self._total_size = (self._total_width, self._total_height)

        self.palette_num = random.randint(0, len(PALETTES) - 1)

        self.eaten = False
        self.adds_allergies = []

    @property
    def total_height(self):
        return self._total_height

    @total_height.setter
    def total_height(self, value):
        self._total_height = value
        self._total_size = (self._total_width, value)

    @property
    def total_width(self):
        return self._total_width

    @total_width.setter
    def total_width(self, value):
        self._total_width = value
        self._total_size = (value, self._total_height)

    @property
    def total_size(self):
        return self._total_size

    @total_size.setter
    def total_size(self, value):
        self._total_size = value
        self._total_width = value[0]
        self._total_height = value[1]

    @property
    def top_num(self):
        return self._top_num

    @top_num.setter
    def top_num(self, value):
        if value >= len(tops):
            raise IndexError("The requested top number (%d) is greater than"
                             " the maximum top number (%d)!"
                             % (value, len(tops) - 1)
                             )
        self._top_num = value
        self._top = tops[value]

    @property
    def bottom_num(self):
        return self._bottom_num

    @bottom_num.setter
    def bottom_num(self, value):
        if value >= len(bottoms):
            raise IndexError("The requested bottom number (%d) is greater than"
                             " the maximum bottom number (%d)!"
                             % (value, len(bottoms) - 1)
                             )
        self._bottom_num = value
        self._bottom = bottoms[value]

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    @property
    def palette_num(self):
        return self._palette_num

    @palette_num.setter
    def palette_num(self, value):
        if value >= len(PALETTES):
            raise IndexError("The requested palette number (%d) is greater than"
                             " the maximum palette number (%d)!"
                             % (value, len(PALETTES) - 1)
                             )
        self._palette_num = value
        self._palette = PALETTES[self._palette_num]

    @property
    def palette(self):
        return self._palette

    def render_text(self, colored=False):
        text = ""
        if self.brand:
            text += "Brand: %s <br> " % self.brand

        if self.allergens:
            text += "Contains: "
            text += ", ".join(self.allergens)
            text += " <br> "

        if self.brand or self.allergens or self.code:
            text += "Side Effects: "
        text += ", ".join(self.effects)
        text += " <br> "

        if self.code:
            text += "Code: %s <br> " % self.code

        # Removes the final <br>
        if text.endswith(" <br> "):
            text = text[:-len(" <br> ")]

        font = graphics.tahoma
        max_width = self.body_width

        if colored:
            return graphics.text_block_color_codes(text, font, max_width - 10)

        else:
            return graphics.text_block(text, font, colors.BLACK, max_width - 10)

    def render_textless(self):
        surface = graphics.new_surface(self.total_size)

        # Draws the cap of the bottle
        cap_width = self.body_width - self.cap_x * 2
        cap_rect = (self.cap_x, 0, cap_width, self.cap_height)
        pygame.draw.rect(surface, CAP_PLACEHOLDER_COLOR, cap_rect)

        # Draws the top of the bottle (the part that curves into the cap)
        top_y = self.cap_height
        color = BODY_PLACEHOLDER_COLOR
        draw_wedge(surface, (0, top_y), self.top, self.body_width, color)

        # Draws the body of the bottle
        body_y = top_y + self.top.single_height
        body_rect = (0, body_y, self.body_width, self.body_height)
        pygame.draw.rect(surface, BODY_PLACEHOLDER_COLOR, body_rect)

        label_y = body_y + self.label_y_offset
        label_rect = (0, label_y, self.body_width, self.label_height)
        pygame.draw.rect(surface, LABEL_PLACEHOLDER_COLOR, label_rect)

        # Draws the bottom of the bottle
        bottom_y = body_y + self.body_height
        color = BODY_PLACEHOLDER_COLOR
        draw_wedge(surface, (0, bottom_y), self.bottom, self.body_width, color)

        # Colors in the bottle
        pixel_array = pygame.PixelArray(surface)
        pixel_array.replace(CAP_PLACEHOLDER_COLOR, self.palette.cap_color)
        pixel_array.replace(BODY_PLACEHOLDER_COLOR, self.palette.body_color)
        pixel_array.replace(LABEL_PLACEHOLDER_COLOR, self.palette.label_color)
        pixel_array.close()

        return surface

    def render(self):
        surface = self.render_textless()

        label_y = self.cap_height + self.top.single_height + self.label_y_offset

        # Applies text to the bottle
        side_effects = self.render_text()
        surface.blit(side_effects, (5, label_y + 3))

        return surface

    def render_color_codes(self):
        surface = self.render_textless()

        label_y = self.cap_height + self.top.single_height + self.label_y_offset

        # Applies text to the bottle
        side_effects = self.render_text(True)
        surface.blit(side_effects, (5, label_y + 3))

        return surface

    def add_benign(self, count):
        # Adds a certain amount of benign effects to this bottle
        for _ in range(count):
            effect = random.choice(benign_effects)
            while effect in self.effects:
                effect = random.choice(benign_effects)
            self.effects.append(effect)

    def add_allergens(self, count):
        for _ in range(count):
            allergen = random.choice(allergens)
            while allergen in self.allergens or allergen in self.allergies:
                allergen = random.choice(allergens)
            self.allergens.append(allergen)

    def add_allergy(self, count):
        for _ in range(count):
            allergen = random.choice(allergens)
            while allergen in self.allergens or allergen in self.allergies:
                allergen = random.choice(allergens)
            self.allergies.append(allergen)
            self.effects.append(allergen + " allergy")

    def add_lethal(self, count):
        self.lethal = True
        for _ in range(count):
            effect = random.choice(death_effects)
            while effect in self.effects:
                effect = random.choice(death_effects)
            self.effects.append(effect)

    def add_brand(self):
        self.brand = random.choice(brands)

    def become_bootleg(self):
        self._bootleg = True
        for effect in self.effects:
            if effect in benign_effects:
                duplicate = effect
                break
        else:
            raise Exception("Can't make a bottle with no benign effects "
                            "into a bootleg!")

        self.effects.append(duplicate)

    def add_verification(self):
        self.code = generate_verification_code(random.randint(3, 5))

    def add_fake_verification(self):
        self.code = generate_fake_verification_code(random.randint(3, 5))

    @property
    def bootleg(self):
        return self._bootleg

    def shuffle(self):
        random.shuffle(self.effects)

    def to_dict(self):
        d = {
            EFFECTS: self.effects,

            BODY_WIDTH: self.body_width,
            BODY_HEIGHT: self.body_height,

            LABEL_HEIGHT: self.label_height,
            LABEL_Y_OFFSET: self.label_y_offset,

            TOP_NUM: self.top_num,
            BOTTOM_NUM: self.bottom_num,
            PALETTE_NUM: self.palette_num,

            CAP_X: self.cap_x,
            CAP_HEIGHT: self.cap_height,

            TOTAL_WIDTH: self.total_width,
            TOTAL_HEIGHT: self.total_height,
        }
        return d


def bottle_from_dict(d):
    bottle = Bottle()

    bottle.effects = d[EFFECTS]

    bottle.body_width = d[BODY_WIDTH]
    bottle.body_height = d[BODY_HEIGHT]

    # Label
    bottle.label_height = d[LABEL_HEIGHT]
    bottle.label_y_offset = d[LABEL_Y_OFFSET]

    # Top and bottom curve of the bottle's body
    bottle.top_num = d[TOP_NUM]
    bottle.bottom_num = d[BOTTOM_NUM]

    # Cap
    bottle.cap_x = d[CAP_X]
    bottle.cap_height = d[CAP_HEIGHT]

    bottle.total_width = d[TOTAL_WIDTH]
    bottle.total_height = d[TOTAL_HEIGHT]

    bottle.palette_num = d[PALETTE_NUM]

    return bottle


ghost_bottle = Bottle()
ghost_bottle._palette = TRANSPARENT_PALETTE


class BottleGenerator:

    def __init__(self):
        self.level = 0
        self.bottles_until_safe = random.randint(0, 3)
        self.safes_in_a_row = 0
        self.deadlies_in_a_row = 0

    def next_item(self):

        # Fast level generator
        if self.level == const.INCIDENT_FAST:
            bottle = Bottle()
            bottle.add_benign(random.randint(3, 5))

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 3)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop()
                bottle.add_lethal(1)

        # Faster level generator
        elif self.level == const.INCIDENT_FASTER:
            bottle = Bottle()

            # The more safes you get in a row, the less likely the next
            # bottle is safe.  Likewise for deadlies.
            # It's impossible to get 6 safes/deadlies in a row.
            safe_chance = 0.5
            safe_chance += self.deadlies_in_a_row * 0.09
            safe_chance -= self.safes_in_a_row * 0.09
            if random.random() < safe_chance:
                self.deadlies_in_a_row = 0
                self.safes_in_a_row += 1
                bottle.add_benign(1)
            else:
                self.deadlies_in_a_row += 1
                self.safes_in_a_row = 0
                bottle.add_lethal(1)

        # Allergen level generator
        elif self.level == const.INCIDENT_ALLERGENS:
            bottle = Bottle()
            bottle.add_allergens(random.randint(1, 3))
            bottle.add_allergy(1)

        # Effects and allergens level generator
        elif self.level == const.INCIDENT_EFFECTS_ALLERGENS or self.level == const.INCIDENT_EFFECTS_ALLERGENS_HARD:
            bottle = Bottle()
            bottle.add_benign(random.randint(3, 5))
            bottle.add_allergens(random.randint(1, 4))

            if random.random() < 0.50:
                bottle.effects.pop()
                bottle.add_allergy(1)

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 1)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop(0)  # Pop at start so that it doesn't pop the allergy
                bottle.add_lethal(1)

        # Effects and brand level generator
        elif self.level == const.INCIDENT_EFFECTS_BRANDS:
            bottle = Bottle()
            bottle.add_benign(random.randint(3, 5))
            bottle.add_brand()

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 2)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop()
                bottle.add_lethal(1)

        # Effects, allergens, and brands level generator
        elif self.level == const.INCIDENT_EFFECTS_ALLERGENS_BRANDS:
            bottle = Bottle()
            bottle.add_benign(random.randint(3, 5))
            bottle.add_allergens(random.randint(1, 2))
            bottle.add_brand()

            if random.random() < 0.75:
                bottle.effects.pop()
                bottle.add_allergy(1)

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 1)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop(0)  # Pop at start so that it doesn't pop the allergy
                bottle.add_lethal(1)

        # Effects and bootlegs level generator
        elif self.level == const.INCIDENT_EFFECTS_BOOTLEGS:
            bottle = Bottle()
            bottle.add_benign(random.randint(5, 8))

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 3)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop()

                # 70% chance of being a bootleg
                if random.random() < 0.7:
                    bottle.become_bootleg()

                # 30% chance of just being normally deadly
                else:
                    bottle.add_lethal(1)

        # Effects and verification level generator
        elif self.level == const.INCIDENT_EFFECTS_VERIFICATION:
            bottle = Bottle()
            bottle.add_benign(random.randint(3, 5))

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 2)
            else:
                self.bottles_until_safe -= 1

                # 70% chance of being a fake code
                if random.random() < 0.7:
                    bottle.add_fake_verification()
                else:
                    bottle.effects.pop()
                    bottle.add_lethal(1)

            # Adds verification, if a fake one hasn't already been made
            if not bottle.code:
                bottle.add_verification()

        # Effects and alternation level generator
        elif self.level == const.INCIDENT_EFFECTS_ALTERNATION:
            bottle = Bottle()
            bottle.add_benign(random.randint(5, 8))

            # The more safes you get in a row, the less likely the next
            # bottle is safe.  Likewise for deadlies.
            # It's impossible to get 4 safes/deadlies in a row.
            safe_chance = 0.5
            safe_chance += self.deadlies_in_a_row * 0.13
            safe_chance -= self.safes_in_a_row * 0.13
            if random.random() < safe_chance:
                self.deadlies_in_a_row = 0
                self.safes_in_a_row += 1
            else:
                self.deadlies_in_a_row += 1
                self.safes_in_a_row = 0
                bottle.effects.pop()
                bottle.add_lethal(1)

        # Effects-only level generator (also includes the hard version)
        else:
            bottle = Bottle()
            bottle.add_benign(random.randint(5, 8))

            if self.bottles_until_safe == 0:
                self.bottles_until_safe = random.randint(0, 3)
            else:
                self.bottles_until_safe -= 1
                bottle.effects.pop()
                bottle.add_lethal(1)

        bottle.shuffle()

        # If the text overflows the label, then extend the label
        text_height = bottle.render_text().get_height()
        if bottle.label_height < text_height + 10:
            bottle.label_height = text_height + 10

            if bottle.label_y_offset + bottle.label_height > bottle.body_height:
                previous = bottle.body_height
                bottle.body_height = bottle.label_y_offset + bottle.label_height + 10
                bottle.total_height += bottle.body_height - previous

        return bottle
