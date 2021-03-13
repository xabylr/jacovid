import logging
import tracking.json_source as source
from datetime import date
import persistence.utils.queries as queries
import persistence.database as database
from persistence.models.measures import MeasuresCodeComparator
import persistence.utils.model_update as model_update

logger = logging.getLogger()


def populate_places(insert_measures=True):
    """Used for the first time, it will populate the list of places in database.
       It will also add insert the first measures for those places if parameter set to True.
    """

    measures_list_json = source.get_measures_json()
    places_list = source.get_places(measures_list_json)

    session = database.get_session()

    session.bulk_save_objects(places_list)

    session.commit()
    session.close()
    
    if insert_measures:
        pull_measures(measures_list_json)

    

def pull_measures(measures_json=None, date=date.today()):
    """It will use the specified JSON or query it to the API for inserting measures
    for the selected datetime"""

    received_measures_list = source.get_measures(measures_json)
    received_measures_list_comp = {MeasuresCodeComparator(i) for i in received_measures_list}
    #logger.info("Received lenght: "+str(len(received_measures_list_comp)))

    session = database.get_session()

    # TODO implement merge with measures from same date
    db_date_measures_list = queries.retrieve_measures_from_date(date, session)

    db_date_measures_list_comp = {MeasuresCodeComparator(i) for i in db_date_measures_list} 
    #logger.info("DB lenght: "+str(len((db_date_measures_list_comp))))

    new_measures_list_comp = list(received_measures_list_comp - db_date_measures_list_comp)
    #logger.info("New length "+str(len((new_measures_list_comp))))

    new_measures_list = [ml.measures for ml in new_measures_list_comp]

    session.bulk_save_objects(new_measures_list)

    for existing_measures in list(MeasuresCodeComparator(i) for i in db_date_measures_list):
        matching = next((rmlc for rmlc in received_measures_list_comp if existing_measures == rmlc), None)
        if matching is not None:
            model_update.update_measures_model(existing_measures.measures, matching.measures)

    session.commit()
    session.close()
  