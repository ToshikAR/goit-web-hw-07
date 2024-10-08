import logging
import sys
import os
from functools import wraps

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from sqlalchemy.exc import SQLAlchemyError
from database.db import session


def decorator_seed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except SQLAlchemyError as err:
            logging.error(f"SQLAlchemyError: => {err}")
            session.rollback()
        finally:
            session.close()

    return wrapper


def error_select(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as err:
            logging.error(f"SQLAlchemyError: => {err}")
        except Exception as err:
            logging.error(f"Exception: => {err}")
        return None

    return wrapper
