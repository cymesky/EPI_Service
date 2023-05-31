from selenium import webdriver
from settings import set_chrome_options
from db_tools.engine import create_database_engine
from db_tools.models import EexGermany
from markets import eex_germany
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


def process_eex_germany():
    engine = create_database_engine()

    if not EexGermany.table_exists(engine):
        EexGermany.create_table(engine)
    driver = webdriver.Chrome(options=set_chrome_options())
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        eex_germany.process_data(session, driver)
    except SQLAlchemyError as e:
        print(str(e))
    finally:
        driver.quit()
        session.close()


def main():
    process_eex_germany()


if __name__ == '__main__':
    main()
