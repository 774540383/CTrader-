"""
database/database.py
Simple session-context helper on top of database/models.py, kept as a
separate module to match the requested project layout.
"""
from contextlib import contextmanager
from database.models import get_session


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
