import const
import bottles


class Incident:
    def __init__(self, number, bottle, text, ambulance_time, homunculus_time, bottle_time):
        self.number = number
        self.bottle = bottle
        self.text = text
        self.ambulance_time = ambulance_time
        self.homunculus_time = homunculus_time
        self.bottle_time = bottle_time


def basic_incident_bottle():
    bottle = bottles.Bottle()
    bottle.effects.append("1:55 goal time <br> 0:30 start time <br> +15 seconds per bottle <br> Side effects only")

    bottle.body_width = 120
    bottle.body_height = 200

    # Label
    bottle.label_height = 100
    bottle.label_y_offset = 20

    # Top and bottom curve of the bottle's body
    bottle.top = bottles.tops[0]
    bottle.bottom = bottles.bottoms[0]

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width - 5
    bottle.cap_height = 15

    bottle.total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle.total_height = total_height
    bottle.total_size = (bottle.total_width, bottle.total_height)

    bottle.palette = bottles.PALETTES[1]

    return bottle


def fast_incident_bottle():
    bottle = bottles.Bottle()
    bottle.effects.append("1:30 goal time <br> 0:15 start time <br> +7 seconds per bottle <br> Side effects only")

    bottle.body_width = 150
    bottle.body_height = 180

    # Label
    bottle.label_height = 150
    bottle.label_y_offset = 20

    # Top and bottom curve of the bottle's body
    bottle.top = bottles.tops[2]
    bottle.bottom = bottles.bottoms[1]

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width - 5
    bottle.cap_height = 15

    bottle.total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle.total_height = total_height
    bottle.total_size = (bottle.total_width, bottle.total_height)

    bottle.palette = bottles.PALETTES[5]

    return bottle


def generate_basic_incident():
    text = (
        'Incident 1 <br> '
        'Year: 2054 <br> <br> '
        'Several thousand years ago, some great ancestor of mine sealed away a cosmological shadow monster into this <o>weird orange puppet<k> thing.  If the puppet dies, the monster gets out, so my lineage has been tasked with taking care of it.  Unfortunately, it seems those hero genes have worn out over the centuries, because I, Mark Colison, have managed to spill hot coffee all over the puppet for the twenty seventh-time in my life!  Fortunately, it happened in a drugstore, so there’s plenty of medication to keep it alive until the ambulance arrives.  I just need to avoid feeding it anything with <r>lethal side effects...<k> <br> <br> '
        '"911 here.  What’s your emergency?" <br> "Hahaha.  Haha.  You won’t believe - " <br> "Okay, Mark.  We’re sending the ambulance over right away." <br> <br> '
        'PRESS SPACE TO START'
    )
    bottle = basic_incident_bottle()
    ambulance_time = 115000
    homunculus_time = 30000
    bottle_time = 15000

    number = const.BASIC_INCIDENT

    return Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)


def generate_fast_incident():
    text = (
        'Incident 2 <br> '
        'Year: 2070 <br> <br> '
        'They just don\'t make medicine like they used to. <br> <br> '
        'PRESS SPACE TO START'
    )
    bottle = fast_incident_bottle()
    ambulance_time = 90000
    homunculus_time = 15000
    bottle_time = 7000

    number = const.FAST_INCIDENT

    return Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
