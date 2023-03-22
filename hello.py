from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():
    return "<p>Hello, World!</p>"

@app.route("/search", methods=['post','get'])
def search():
    return render_template('search_form.html')

@app.route("/search/api")
def search_api():
    loc = request.args['fname']
    # print(loc)
    url = "https://www.openrice.com/zh/hongkong"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    elem = driver.find_elements(By.CLASS_NAME, "quick-search-input-field")
    elem[1].send_keys(loc)
    driver.find_element(By.CSS_SELECTOR, ".quick-search-button").click()

    lis = driver.find_elements(By.CSS_SELECTOR, ".sr1-listing-content-cell.pois-restaurant-list-cell")

    temp = []
    for li in lis:
        id = li.find_element(By.CSS_SELECTOR, 'section.js-openrice-bookmark.openrice-bookmark').get_attribute('data-poi-id')
        name = li.find_element(By.CLASS_NAME, "title-name").text
        address = li.find_element(By.CLASS_NAME, "address").text
        temp.append([id, name, address])

    op_df = pd.DataFrame(temp, columns=['ID', 'Name','Address'])

    driver.quit()

    if temp == []:
        return 'No result. Please search again.'
    else:
        return render_template('result.html', column_names=op_df.columns.values, row_data=list(op_df.values.tolist()), zip=zip)



    # print(list(op_df.values.tolist()))
    # print(op_df.columns.values)

    # df = pd.DataFrame({'Patient Name': ["Some name", "Another name"],
    #                    "Patient ID": [123, 456],
    #                    "Misc Data Point": [8, 53]})