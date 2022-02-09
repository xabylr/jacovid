import datetime
import logging

from persistence.database import Session
from persistence.models.measures import MeasuresCodeComparator
from persistence.utils import model_update, queries
from tracking import json_source

logger = logging.getLogger()


def populate_places(insert_measures=True):
    """Used for the first time, it will populate the list of places in database.
       It will also add insert the first measures for those places if parameter set to True.
    """

    measures_json_lists = json_source.get_measures_json_list()
    places_list = json_source.get_places(measures_json_lists)

    session = Session()

    session.bulk_save_objects(places_list)

    session.commit()
    session.close()

    if insert_measures:
        pull_measures(measures_json_lists)


def pull_measures(measures_json_list=None, date=datetime.date.today()):
    """It will use the specified JSON or query it to the API for inserting measures
    for the selected datetime"""

    import os
    # Get the process ID of
    # the current process
    pid = os.getpid()
    # Print the process ID of
    # the current process
    print(f'process id: {pid}') 

    received_measures_list = json_source.get_measures(measures_json_list)
    received_measures_list_comp = {MeasuresCodeComparator(i) for i in received_measures_list}
    # logger.info("Received lenght: "+str(len(received_measures_list_comp)))

    session = Session()

    # TODO implement merge with measures from same date
    db_date_measures_list = queries.retrieve_measures_from_date(date, session)

    db_date_measures_list_comp = {MeasuresCodeComparator(i) for i in db_date_measures_list}
    # logger.info("DB lenght: "+str(len((db_date_measures_list_comp))))

    new_measures_list_comp = list(received_measures_list_comp - db_date_measures_list_comp)
    # logger.info("New length "+str(len((new_measures_list_comp))))

    new_measures_list = [ml.measures for ml in new_measures_list_comp]

    session.bulk_save_objects(new_measures_list)

    for existing_measures in list(MeasuresCodeComparator(i) for i in db_date_measures_list):
        matching = next((rmlc for rmlc in received_measures_list_comp if existing_measures == rmlc), None)
        if matching is not None:
            model_update.update_measures_model(existing_measures.measures, matching.measures)

    session.commit()
    session.close()
