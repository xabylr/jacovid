import requests
from persistence.models.place import Place
from persistence.models.measures import Measures
from tracking.json_config import urls_config as urls_config

import logging

logger = logging.getLogger()


def get_measures_json_list():
    measures_list = []

    for config in urls_config.values():
        measures = None
        while measures is None:
            try:
                measures = requests.get(config["url"], verify=True).json()
                measures_list.append(measures)
                #logger.info("Measures retrieved successfully")
            except:
                logger.warning("Error retrieving JSON, trying again...")

    return measures_list

def get_places(json_list=None):
    """ Requests or receives a JSON measures list and returns a list of database entries
        according to the place (Community, Province, District, Municipality)
    """
    places_list = []

    if json_list is None:
        json_list = get_measures_json_list()

    for measures_json in json_list: # List of JSON
        json_id = measures_json["metainfo"]["id"]
        config = urls_config[json_id]

        for entry in measures_json["data"]: # List of entries in a JSON
            codes = entry[0]["cod"]
            code_idx = len(codes)-1
            code = codes[code_idx]
            place = config["places"][code_idx]
            type = place["type"]

            if place["register_place"]:
                name = entry[0]["des"]
                parent_code = None
                parent_type = None
                if code_idx > 0:
                    parent_code = codes[code_idx -1]
                    parent_type = config["places"][code_idx -1]["type"]

                entity = Place(code=code, type=type,
                     parent=parent_code, parent_type=parent_type, name=name)

                places_list.append(entity)

    return places_list

def get_measures(json_list=None):
    """ Requests or receives a JSON measures list and returns a list
        of database Measures
    """
    measures_list = []

    if json_list is None:
        json_list = get_measures_json_list()

    for measures_json in json_list: # List of JSON
        json_id = measures_json["metainfo"]["id"]
        config = urls_config[json_id]

        measure_types = measures_json["measures"]

        measures_idx = {}
        for measure_type in measure_types: # List of measure config for a JSON
            try:
                measure_name = config["measures"][measure_type["id"]]
                measures_idx[measure_name] = measure_type["order"]
            except:
                pass # There are discarded measures that are not used everywhere

        for measures_entry in measures_json["data"]: # List of data entries in a JSON
            codes = measures_entry[0]["cod"]
            code_idx = len(codes)-1
            code = codes[code_idx]
            place = config["places"][code_idx]
            type = place["type"]
            
            if place["register_measures"]:
                measures_dict = {}
                for measure, idx in measures_idx.items():
                    value = measures_entry[idx+1]["val"]
                    if value == "":
                        value = None
                    measures_dict[measure] = value

                entity = Measures(place_code = code, place_type=type, **measures_dict)

                measures_list.append(entity)

    return measures_list

