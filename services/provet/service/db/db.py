from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from db.schema import Cookie


class CookiesTable:

    engine = None
    SessionLocal = None

    @classmethod
    def connect(cls, config):
        url = f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/provet"
        cls.engine = create_engine(url)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

    @classmethod
    def store_cookies(cls, cookies: list[dict]):
        session = cls.SessionLocal()
        try:

            for cookie_dict in cookies:
                expires = cookie_dict.get('expires')
                expiration_dt = None
                if expires and expires > 0:
                    expiration_dt = datetime.fromtimestamp(expires)
                stored_cookie = session.query(Cookie).filter_by(
                    domain=cookie_dict['domain'],
                    name=cookie_dict['name']).first()
                if stored_cookie:
                    stored_cookie.value = cookie_dict['value']
                    stored_cookie.expiration = expiration_dt
                else:
                    session.add(Cookie(
                        domain=cookie_dict['domain'],
                        name=cookie_dict['name'],
                        value=cookie_dict['value'],
                        expiration=expiration_dt))
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Warning: Duplicate cookie(s) detected (unique domain-name pair).")
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @classmethod
    def get_cookies(cls, domain: str, names: list[str]) -> list[Cookie]:
        session = cls.SessionLocal()
        try:
            results = session.query(Cookie).filter(
                Cookie.domain == domain,
                Cookie.name.in_(names)
            ).all()
            return results
        finally:
            session.close()

    @classmethod
    def remove_cookies(cls, cookies: list[Cookie]) -> int:
        session = cls.SessionLocal()
        if len(cookies) == 0:
            return 0
        try:
            cookie_ids = [cookie.id for cookie in cookies]
            deleted_count = session.query(Cookie).filter(
                Cookie.id.in_(cookie_ids)
            ).delete(synchronize_session=False)
            session.commit()
            return deleted_count
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
