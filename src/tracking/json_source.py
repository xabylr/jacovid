import requests
from persistence.models.community import Community
from persistence.models.province import Province
from persistence.models.district import District
from persistence.models.municipality import Municipality
from persistence.models.measures import Measures


json_measures_url = 'https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/42798'

def _get_code_table_and_col(codes):
    if len(codes) == 1: # Community
        code = codes[0]
        table = Community
        col = 'community_code'

    elif len(codes) == 2: # Province
        code = codes[1]
        table = Province
        col = 'province_code'

    elif len(codes) == 3: # District
        code = codes[2]
        table = District
        col = 'district_code'

    elif len(codes) == 4: # Municipality
        code = codes[3]
        table = Municipality
        col = 'municipality_code'

    return code, table, col

def get_measures_json():
    return requests.get(json_measures_url, verify=True).json()


def get_places(measures_json=None):
    """ Requests or receives a JSON measures list and returns a list of database entries
        according to the place (Community, Province, District, Municipality)
    """
    places_list = []

    if measures_json is None:
        measures_json = get_measures_json()

    for measures in measures_json["data"]:
        name = measures[0]["des"]
        codes = measures[0]["cod"]

        code, table, _ = _get_code_table_and_col(codes)

        # Create and add the place in the corresponding table
        places_list.append(table(code=code, name=name))

    return places_list

def get_measures(measures_json=None):
    """ Requests or receives a JSON measures list and returns a list
        of database Measures
    """
    measure_list = []

    if measures_json == None:
        measures_json = get_measures_json()

    measure_indexes = measures_json["measures"]
        
    for measure_idx in measure_indexes:
        if measure_idx["id"] == 276104:
            population_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242502:
            pdia_confirmed_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242528:
            pdia_rate_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242503:
            pdia_14d_confirmed_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242529:
            pdia_14d_rate_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242504:
            pdia_7d_confirmed_idx = int(measure_idx["order"])
        
        elif measure_idx["id"] == 242530:
            pdia_7d_rate_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242505:
            total_confirmed_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242531:
            total_rate_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242506:
            cured_idx = int(measure_idx["order"])

        elif measure_idx["id"] == 242507:
            deceased_idx = int(measure_idx["order"])


    for measures in measures_json["data"]:
        code, _, fk_col = _get_code_table_and_col(measures[0]["cod"])
        columns = {}

        columns[fk_col] = code
        columns["pdia_14d_rate"] = measures[pdia_14d_rate_idx+1]["val"] or None

        #TODO add all columns

        measure_list.append(Measures(**columns))
    
    return measure_list

