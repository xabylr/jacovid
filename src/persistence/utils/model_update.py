import logging
from datetime import date, datetime

logger = logging.getLogger()

def update_measures_model(existing, new):
    existing.pdia_14d_rate = new.pdia_14d_rate
    existing.date_reg = date.today()
    existing.dt_mod = datetime.now()