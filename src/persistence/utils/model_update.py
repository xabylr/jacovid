import logging
from datetime import date, datetime

logger = logging.getLogger()

def update_measures_model(existing, new):
    existing.population = new.population
    existing.pdia_confirmed = new.pdia_confirmed
    existing.pdia_14d_confirmed = new.pdia_14d_confirmed
    existing.pdia_14d_rate = new.pdia_14d_rate
    existing.pdia_7d_confirmed = new.pdia_7d_confirmed
    existing.total_confirmed = new.total_confirmed
    existing.cured = new.cured
    existing.deceased = new.deceased

    existing.dt_mod = datetime.now()