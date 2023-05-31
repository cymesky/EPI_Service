import xlrd
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from data.db_tools.models import EexGermany
from sqlalchemy.orm import Session


def process_data(session: Session, driver: WebDriver):
    # Go to url
    driver.get('https://www.eex.com/en/market-data/power/indices')

    # Find <a> tag with link to file
    element = driver.find_element(By.XPATH, '//a[contains(@href, ".xls")]')

    # Get url to file
    xls_url = element.get_attribute('href')

    # Close browser
    driver.quit()

    # Get XLS file content from url
    response = requests.get(xls_url)

    # Open XLS content
    workbook = xlrd.open_workbook(file_contents=response.content)

    # Select sheet in document
    sheet = workbook.sheet_by_index(0)

    # Get data from cells and update db
    start_row = 4
    objects = []

    for row in range(start_row, sheet.nrows):
        row_data = sheet.row_values(row)

        quarter = (row_data[0])[1]
        year = (row_data[0])[3:]
        price = str(row_data[1]).replace(',', '.')

        obj = EexGermany(quarter=quarter, year=year, price=price)

        exists = session.query(EexGermany).filter(
            EexGermany.quarter == obj.quarter,
            EexGermany.year == obj.year
        ).first()

        if not exists:
            objects.append(obj)

    session.bulk_save_objects(objects)
    session.commit()
