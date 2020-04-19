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

    bottle._total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle._total_height = total_height
    bottle.total_size = (bottle._total_width, bottle._total_height)

    bottle.palette = bottles.PALETTES[1]

    return bottle


def fast_incident_bottle():
    bottle = bottles.Bottle()

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
    bottle.cap_height = 20

    bottle._total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle._total_height = total_height
    bottle.total_size = (bottle._total_width, bottle._total_height)

    bottle.palette = bottles.PALETTES[14]

    return bottle


def allergen_incident_bottle():
    bottle = bottles.Bottle()

    bottle.body_width = 230
    bottle.body_height = 150

    # Label
    bottle.label_height = 100
    bottle.label_y_offset = 40

    # Top and bottom curve of the bottle's body
    bottle.top = bottles.tops[5]
    bottle.bottom = bottles.bottoms[1]

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width - 5
    bottle.cap_height = 30

    bottle._total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle._total_height = total_height
    bottle.total_size = (bottle._total_width, bottle._total_height)

    bottle.palette = bottles.PALETTES[7]

    return bottle


def mixed_incident_bottle():
    bottle = bottles.Bottle()

    bottle.body_width = 130
    bottle.body_height = 160

    # Label
    bottle.label_height = 100
    bottle.label_y_offset = 20

    # Top and bottom curve of the bottle's body
    bottle.top = bottles.tops[1]
    bottle.bottom = bottles.bottoms[0]

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width
    bottle.cap_height = 24

    bottle._total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle._total_height = total_height
    bottle.total_size = (bottle._total_width, bottle._total_height)

    bottle.palette = bottles.PALETTES[6]

    return bottle


def generate_basic_incident():
    text = (
        'Incident 1 <br> '
        'Year: 2054 <br> <br> '
        'Several thousand years ago, some great ancestor of mine sealed away a cosmological shadow monster into this <o>weird orange puppet<k> thing.  If the puppet dies, the monster gets out, so my lineage has been tasked with taking care of it.  Unfortunately, it seems those hero genes have worn out over the centuries, because I, Mark Colison, have managed to spill hot coffee all over the puppet for the twenty-seventh time in my life!  Fortunately, it happened in a drugstore, so there’s plenty of medication to keep it alive until the ambulance arrives.  I just need to avoid feeding it anything with <r>lethal side effects...<k> <br> <br> '
        '"911 here.  What’s your emergency?" <br> "Hahaha.  Haha.  You won’t believe - " <br> "Okay, Mark.  We’re sending the ambulance over right away." <br> <br> '
        'PRESS SPACE TO START'
    )
    bottle = basic_incident_bottle()
    bottle.effects.append("1:55 goal time <br> 0:30 start time <br> +15 seconds per bottle <br> Side effects only")

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
    bottle.effects.append("1:30 goal time <br> 0:15 start time <br> +7 seconds per bottle <br> Side effects only")

    ambulance_time = 90000
    homunculus_time = 15000
    bottle_time = 7000

    number = const.FAST_INCIDENT

    return Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)


def generate_allergen_incident():
    text = (
        'Incident 2 <br> '
        'Year: 2132 <br> <br> '
        'Jauntra Colison here.  Today I took the <o>orange thing<k> to the local allergery.  It\'s a specialized drugstore that only sells allergy medicine.  No, the medicine doesn\'t cure your allergies.  It <r>gives you them.<k>  And they\'re not the fun kind of allergy that knocks you out for a few hours so you can skip your grandfather\'s funeral.  These are the kinds of allergy that will <r>immediately kill you.<k>  Unfortunately, the more of these allergies you have, the "cooler" you are.  In an attempt to save the lives of every kid in town, I did the responsible thing and set fire to the building.  Unfortunately, the homunculus also caught on fire, and has suffered third degree burns for the fifty-fourth time in its life (the first fifty-tree were why I didn\'t go to your funeral, Mark).  Well, at least there\'s medicine here, I just have to <r>keep track of all the allergies...<k> <br> <br> '
        'Note that some medicines cause an allergic reaction to one of its own ingredients.  That\'s lethal.'
    )
    bottle = allergen_incident_bottle()
    bottle.effects.append("1:15 goal time <br> 0:20 start time <br> +12 seconds per bottle <br> Allergens only")

    ambulance_time = 90000
    homunculus_time = 20000
    bottle_time = 12000

    number = const.ALLERGEN_INCIDENT

    return Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)


def generate_mixed_incident():
    text = (
        'Incident 3 <br> '
        'Year: 2285 <br> <br> '
        'WHAT?  You\'re telling me that you\'ve never heard of THE FABULOUS, THE DIVINE, THE ONE AND ONLY DOCTOR BUNA COLISON?  The scientist known WORLDWIDE for adding <r>ALLERGY EFFECTS to NORMAL MEDICINE?<k>  Oh... you\'ve really never heard of me.  Well, I\'ll have you know that I\'m not as legendary of an idiot as a certain Mark Colison.  However, today I did forget to keep my gratimesium and my butane at least five centimeters apart, causing an explosion.  But, FEAR NOT, for I REMEMBERED to keep the <o>orange flesh sack<k> at least twenty meters away from my work!  Through the marvelous application of the latest technology, A LOCKED CAGE, I have managed to keep good ol\' <o>Homunculorange<k> safe from fire and flame.  Now, hold on a moment as I scream internally at the sight of an open door. <br> <br> '
        'Ah, that\'s better.  Yes, I\'ve got tons of medicine from my allergy experiments.  Yes, yes, this\'ll do fine.'
    )
    bottle = mixed_incident_bottle()
    bottle.effects.append("1:55 goal time <br> 0:15 start time <br> +15 seconds per bottle <br> Side effects and allergens")

    ambulance_time = 115000
    homunculus_time = 15000
    bottle_time = 15000

    number = const.MIXED_INCIDENT

    return Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
