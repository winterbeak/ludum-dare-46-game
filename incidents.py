import const
import bottles
import time_math


class Incident:
    def __init__(self, number, bottle, text, ambulance_time, homunculus_time, bottle_time):
        self.number = number
        self.bottle = bottle
        self.text = text
        self.ambulance_time = ambulance_time
        self.homunculus_time = homunculus_time
        self.bottle_time = bottle_time
        self.alternating = False


def effects_incident_bottle():
    bottle = bottles.Bottle()

    bottle.body_width = 120
    bottle.body_height = 200

    # Label
    bottle.label_height = 100
    bottle.label_y_offset = 20

    # Top and bottom curve of the bottle's body
    bottle.top_num = 0
    bottle.bottom_num = 0

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
    bottle.top_num = 2
    bottle.bottom_num = 1

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width - 5
    bottle.cap_height = 20

    bottle.total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle.total_height = total_height

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
    bottle.top_num = 5
    bottle.bottom_num = 1

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width - 5
    bottle.cap_height = 30

    bottle.total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle.total_height = total_height

    bottle.palette = bottles.PALETTES[7]

    return bottle


def effects_allergens_incident_bottle():
    bottle = bottles.Bottle()

    bottle.body_width = 130
    bottle.body_height = 160

    # Label
    bottle.label_height = 100
    bottle.label_y_offset = 20

    # Top and bottom curve of the bottle's body
    bottle.top_num = 1
    bottle.bottom_num = 0

    # Cap
    top_width = bottle.top.single_width
    bottle.cap_x = top_width
    bottle.cap_height = 24

    bottle.total_width = bottle.body_width
    total_height = 0
    total_height += bottle.cap_height
    total_height += bottle.body_height
    total_height += bottle.top.single_height
    total_height += bottle.bottom.single_height
    bottle.total_height = total_height

    bottle.palette = bottles.PALETTES[6]

    return bottle


def generate_effects_incident():
    text = (
        "Incident 1 <br> "
        "Year: 2054 <br> <br> "
        "Several thousand years ago, some great ancestor of mine sealed"
        " away a cosmological shadow monster into this <o>weird orange"
        " puppet<k> thing.  If the puppet dies, the monster gets out, so"
        " my lineage has been tasked with taking care of it.  Unfortunately,"
        " it seems those hero genes have worn out over the centuries,"
        " because I, Mark Colison, have managed to spill hot coffee all"
        " over the puppet for the twenty-seventh time in my"
        " life!  Fortunately, it happened in a drugstore, so there's"
        " plenty of medication to keep it alive until the ambulance"
        " arrives.  I just need to avoid feeding it anything with <r>lethal"
        " side effects...<k> <br> <br> "
        
        "\"911 here.  What's your emergency?\" <br> "
        "\"Hahaha.  Haha.  You won't believe - \" <br> "
        "\"Okay, Mark.  We're sending the ambulance over right away.\" <br> <br> "
        
        "PRESS SPACE TO START"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "1:55 goal time <br> "
        "0:30 start time <br> "
        "+15 seconds per bottle <br> "
        "Side effects only"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 55, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 30, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 15, 0))

    number = const.INCIDENT_EFFECTS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_fast_incident():
    text = (
        "Incident 4 <br> "
        "Year: 2020 <br> <br> "
        "It is I, Lercalo Colison, esteemed time traveller"
        " extraordinaire!  In 2945, I went back in time to 2020, taking"
        " with me my exquisite companion, <o>Patchwork,<k> to record the"
        " history of the twenty-first century!  Astoundingly, <r>medicine"
        " used to be allergy-free, and the amount of side effects are"
        " extraordinarily low!  Though the effectiveness seems to have"
        " dropped a tad.<k>  Very interesting, indeed... <br> <br> "
        
        "Oh!  Is that an ancestor I see?  Most curious.  I'd love to"
        " chat, but that could create a paradox.  So, I'll just have to"
        " watch from a distance.  He's talking to the person behind the"
        " counter and in response they've filled a cup full of some"
        " strange brown liquid.  Ahaha!  He spilt it all over his version"
        " of Patchwork!  That's gotta be quite the pain, not to mention"
        " a threat to the integrity of the universe.  But that was 900"
        " years ago, and comedy is just tragedy plus time, so I do"
        " suppose that's quite the hilarity, eh,"
        " Patchy? ... Patchy?  Where'd you go?"
    )
    bottle = fast_incident_bottle()
    bottle.effects.append(
        "1:30 goal time <br> "
        "0:15 start time <br> "
        "+7 seconds per bottle <br> "
        "Side effects only"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 30, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 15, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 7, 0))

    number = const.INCIDENT_FAST

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_allergen_incident():
    text = (
        "Incident 2 <br> "
        "Year: 2132 <br> <br> "
        "Jauntra Colison here.  Today I took the <o>orange thing<k> to"
        " the local allergery.  It's a specialized drugstore that only"
        " sells allergy medicine.  No, the medicine doesn't cure your"
        " allergies.  It <r>gives you them.<k>  And they're not the fun"
        " kind of allergy that knocks you out for a few hours so you can"
        " skip your grandfather's funeral.  These are the kinds of"
        " allergies that will <r>immediately kill you.<k>  Unfortunately,"
        " the more of these allergies you have, the \"cooler\" you are.  In"
        " an attempt to save the lives of every kid in town, I did the"
        " responsible thing and set fire to the building.  Unfortunately,"
        " the homunculus also caught on fire, and has suffered third degree"
        " burns for the fifty-fourth time in its life (the first fifty-tree"
        " were why I didn't go to your funeral, Mark).  Well, at least"
        " there's medicine here, I just have to <r>keep track of all the"
        " allergies...<k> <br> <br> "
        
        "Note that medicine will never cause an allergy to one of its"
        " own ingredients."
    )
    bottle = allergen_incident_bottle()
    bottle.effects.append(
        "1:25 goal time <br> "
        "0:20 start time <br> "
        "+10 seconds per bottle <br> "
        "Allergens only"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 25, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 20, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 10, 0))

    number = const.INCIDENT_ALLERGENS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_allergens_incident():
    text = (
        "Incident 3 <br> "
        "Year: 2285 <br> <br> "
        "WHAT?  You're telling me that you've never heard of THE"
        " FABULOUS, THE DIVINE, THE ONE AND ONLY DOCTOR BUNA"
        " COLISON?  The scientist known WORLDWIDE for adding <r>ALLERGY"
        " EFFECTS to NORMAL MEDICINE?<k>  Oh... you've really never"
        " heard of me.  Well, I'll have you know that I'm not as"
        " legendary of an idiot as a certain Mark Colison.  However,"
        " today I did forget to keep my gratimesium and my butane at"
        " least five centimeters apart, causing an explosion.  But,"
        " FEAR NOT, for I REMEMBERED to keep the <o>orange flesh sack<k>"
        " at least twenty meters away from my work!  Through the"
        " marvelous application of the latest technology, A LOCKED CAGE,"
        " I have managed to keep good ol' <o>Homunculorange<k> safe"
        " from fire and flame.  Now, hold on a moment as I scream"
        " internally at the sight of an open door. <br> <br> "
        
        "Ah, that's better.  Yes, I've got tons of medicine from my"
        " allergy experiments.  Yes, yes, this'll do fine."
    )
    bottle = effects_allergens_incident_bottle()
    bottle.effects.append(
        "1:55 goal time <br> "
        "0:15 start time <br> "
        "+15 seconds per bottle <br> "
        "Side effects and allergens"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 55, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 15, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 15, 0))

    number = const.INCIDENT_EFFECTS_ALLERGENS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_hard_incident():
    text = (
        "Incident ? <br> "
        "Harder version of incident 1"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "3:00 goal time <br> "
        "0:18 start time <br> "
        "+12 seconds per bottle <br> "
        "Side effects only"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((3, 0, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 18, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 12, 0))

    number = const.INCIDENT_EFFECTS_HARD

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_allergens_hard_incident():
    text = (
        "Incident ? <br> "
        "Harder version of incident 3"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "3:00 goal time <br> "
        "0:18 start time <br> "
        "+12 seconds per bottle <br> "
        "Side effects and allergens"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((3, 0, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 18, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 12, 0))

    number = const.INCIDENT_EFFECTS_ALLERGENS_HARD

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_faster_incident():
    text = (
        "Incident ? <br> "
        "Quickest reader in the west"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "1:30 goal time <br> "
        "0:10 start time <br> "
        "+3 seconds per bottle <br> "
        "Side effects only"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 30, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 10, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 3, 0))

    number = const.INCIDENT_FASTER

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_brands_incident():
    text = (
        "Incident ? <br> "
        "Intro to brands <br> <br> "
        "In an effort to prevent monopolies and promote"
        " competition, a scientist has made a contagious viral infection"
        " which kills you if you eat two medicines from the same brand"
        " in a row."
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "1:30 goal time <br> "
        "0:15 start time <br> "
        "+10 seconds per bottle <br> "
        "Side effects and brands"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 30, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 15, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 10, 0))

    number = const.INCIDENT_EFFECTS_BRANDS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_allergens_brands_incident():
    text = (
        "Incident ? <br> "
        "Brands, side effects, and allergens"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "2:25 goal time <br> "
        "0:30 start time <br> "
        "+15 seconds per bottle <br> "
        "Side effects, allergens, and brands"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((2, 25, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 30, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 15, 0))

    number = const.INCIDENT_EFFECTS_ALLERGENS_BRANDS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_bootlegs_incident():
    text = (
        "Incident ? <br> "
        "Intro to bootlegs <br> <br> "
        "To cash in on the medicine craze, bootleg companies have started"
        " making their own medicine.  These are all made with the cheapest"
        " possible ingredient, which just so happens to be poison.  However,"
        " due to the general incompetence of bootleggers, all of these fake"
        " medicines contain a printing error where one of the side effects"
        " is listed twice. <br> "
        "Possibly the only bootlegs incident, since other game types"
        " have only 3-5 side effects, at which point duplicates become"
        " easier to spot. <br> "
        "Maybe the ingredients can be duplicate?  Though, those would"
        " be easy to spot too, plus they would also require a separate"
        " explanation."
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "2:05 goal time <br> "
        "0:20 start time <br> "
        "+12 seconds per bottle <br> "
        "Side effects and bootlegs"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((2, 5, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 20, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 12, 0))

    number = const.INCIDENT_EFFECTS_BOOTLEGS

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_verification_incident():
    text = (
        "Incident ? <br> "
        "Intro to verification codes <br> <br> "
        "Bootleg medicine has become a rampant problem in the"
        " industry.  However, companies have come up with an ingenious"
        " solution; using a verification code.  Each medicine has a code which"
        " follows a pattern too complex for bootleg companies to understand:"
        " <r>the letters in the code must be in alphabetical order.<k>  Of"
        " course, bootleg companies aren't completely incompetent: they"
        " have used neural networks to analyze the pattern of these letters."
        " So, they can produce codes that are almost correct, but never"
        " exactly correct. <br> <br> "
        "Example valid code: aabcf <br> "
        "Example invalid code: aa<r>cb<k>f"
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "1:50 goal time <br> "
        "0:20 start time <br> "
        "+12 seconds per bottle <br> "
        "Side effects and verification codes"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 50, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 20, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 12, 0))

    number = const.INCIDENT_EFFECTS_VERIFICATION

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    return incident


def generate_effects_alternating_incident():
    text = (
        "Incident ? <br> "
        "Intro to alternation <br> <br> "
        "Due to the recent collapse of society, food has become extremely"
        " scarce!  Thankfully, scientists have invented a beneficial virus"
        " that lets you eat things that are typically inedible, as long as you"
        " eat something edible afterwards.  Unthankfully, unforseen"
        " complications have made it so that the reverse is also true: after"
        " everything edible, you must eat something inedible!  You have to"
        " alternate between eating something deadly and something not deadly."
    )
    bottle = effects_incident_bottle()
    bottle.effects.append(
        "1:55 goal time <br> "
        "0:20 start time <br> "
        "+10 seconds per bottle <br> "
        "Side effects and alternation"
    )

    ambulance_time = time_math.min_sec_ms_to_ms((1, 55, 0))
    homunculus_time = time_math.min_sec_ms_to_ms((0, 20, 0))
    bottle_time = time_math.min_sec_ms_to_ms((0, 10, 0))

    number = const.INCIDENT_EFFECTS_ALTERNATION

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    incident.alternating = True
    return incident
