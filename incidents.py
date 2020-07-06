import bottles
import time_math
import files


NUMBER = "number"
BOTTLE = "bottle"
TEXT = "text"
AMBULANCE_TIME = "ambulance_time"
HOMUNCULUS_TIME = "homunculus_time"
BOTTLE_TIME = "bottle_time"
ALTERNATING = "alternating"

EFFECTS = "effects"
ALLERGENS = "allergens"
EFFECTS_ALLERGENS = "effects_allergens"
FAST = "fast"
EFFECTS_HARD = "effects_hard"
EFFECTS_ALLERGENS_HARD = "effects_allergens_hard"
FASTER = "faster"
EFFECTS_BRANDS = "effects_brands"
EFFECTS_ALLERGENS_BRANDS = "effects_allergens_brands"
EFFECTS_BOOTLEGS = "effects_bootlegs"
EFFECTS_VERIFICATION = "effects_verification"
EFFECTS_ALTERNATION = "effects_alternation"


class Incident:
    def __init__(self, number, bottle, text, ambulance_time, homunculus_time, bottle_time):
        self.number = number
        self.bottle = bottle
        self.text = text
        self.ambulance_time = ambulance_time
        self.homunculus_time = homunculus_time
        self.bottle_time = bottle_time
        self.alternating = False

    def to_dict(self):
        d = {
            NUMBER: self.number,
            BOTTLE: self.bottle.to_dict(),
            TEXT: self.text,
            AMBULANCE_TIME: time_math.ms_to_min_sec_ms(self.ambulance_time),
            HOMUNCULUS_TIME: time_math.ms_to_min_sec_ms(self.homunculus_time),
            BOTTLE_TIME: time_math.ms_to_min_sec_ms(self.bottle_time),
            ALTERNATING: self.alternating,
        }
        return d


def incident_from_dict(d):
    number = d[NUMBER]
    bottle = bottles.bottle_from_dict(d[BOTTLE])
    text = d[TEXT]
    ambulance_time = time_math.min_sec_ms_to_ms(d[AMBULANCE_TIME])
    homunculus_time = time_math.min_sec_ms_to_ms(d[HOMUNCULUS_TIME])
    bottle_time = time_math.min_sec_ms_to_ms(d[BOTTLE_TIME])

    incident = Incident(number, bottle, text, ambulance_time, homunculus_time, bottle_time)
    incident.alternating = d[ALTERNATING]

    return incident


def load_incident(path, incident_name):
    data = files.json_read(path)
    incident = incident_from_dict(data[incident_name])

    return incident


def load_incidents(path, incident_names):
    data = files.json_read(path)

    incidents = []
    for incident_name in incident_names:
        incident = incident_from_dict(data[incident_name])
        incidents.append(incident)

    return incidents


def incident_list_to_dict(incident_list, names):
    data = {}
    for incident, name in zip(incident_list, names):
        data[name] = incident.to_dict()

    return data


def write_incidents(path, incident_list, names):
    data = incident_list_to_dict(incident_list, names)
    files.json_write(path, data)
