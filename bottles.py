import random
import pygame

import const
import graphics

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


TOP_TYPES = 5
TOP_ROUND_SMALL = 0
TOP_ROUND_MEDIUM = 1
TOP_ROUND_LARGE = 2
TOP_BEVEL = 3
TOP_INVERTED = 4


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
    ]


TOP_COUNT = 3
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

        # Main body
        self.body_width = random.randint(100, 250)
        self.body_height = random.randint(150, 200)

        # Label
        self.label_height = random.randint(75, self.body_height - 30)
        upper_bound = self.body_height - self.label_height - 10
        self.label_y_offset = random.randint(10, upper_bound)

        # Top and bottom curve of the bottle's body
        self.top = random.choice(tops)
        self.bottom = random.choice(bottoms)

        # Cap
        top_width = self.top.single_width
        self.cap_x = random.randint(top_width - 15, top_width - 2)
        self.cap_height = random.randint(20, 30)

        self.total_width = self.body_width
        total_height = 0
        total_height += self.cap_height
        total_height += self.body_height
        total_height += self.top.single_height
        total_height += self.bottom.single_height
        self.total_height = total_height
        self.total_size = (self.total_width, self.total_height)

        self.palette = random.choice(PALETTES)

    def render_text(self):
        text = ", ".join(self.effects)
        font = graphics.tahoma
        max_width = self.body_width
        return graphics.text_block(text, font, const.BLACK, max_width)

    def render(self):
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

        # Applies text to the bottle
        side_effects = self.render_text()
        surface.blit(side_effects, (3, label_y + 3))

        return surface


def generate_benign():
    bottle = Bottle()

    effect_count = random.randint(6, 9)

    # Generates random benign effects
    for effect in range(effect_count - 1):
        effect = random.choice(benign_effects)
        while effect in bottle.effects:
            effect = random.choice(benign_effects)
        bottle.effects.append(effect)

    random.shuffle(bottle.effects)

    return bottle


def generate_lethal():
    bottle = generate_benign()

    # Replaces one benign effect with a lethal effect
    position = random.randint(0, len(bottle.effects) - 1)
    bottle.effects[position] = random.choice(death_effects)
    bottle.lethal = True

    return bottle


class BottleGenerator:

    def __init__(self):
        self.level = 0
        self.bottles_until_safe = random.randint(0, 3)

    def next_item(self):
        if self.bottles_until_safe == 0:
            self.bottles_until_safe = random.randint(0, 3)
            bottle = generate_benign()

        else:
            self.bottles_until_safe -= 1
            bottle = generate_lethal()

        # If the text overflows the label, then extend the label
        text_height = bottle.render_text().get_height()
        if bottle.label_height < text_height:
            bottle.label_height = text_height + 10

        return bottle
