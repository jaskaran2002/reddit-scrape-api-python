from flask import Flask,jsonify

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import json


app=Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/runredditPython/<string:query>')
def searchReddit(query):
    PATH = "./geckodriver"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=PATH, options=options)
    query.replace(' ', "%20")
    url = f"https://www.reddit.com/search/?q={query}"
    driver.get(url)
    driver.implicitly_wait(5)
    data = []

    cards = driver.find_elements(By.CLASS_NAME, '_2i5O0KNpb9tDq0bsNOZB_Q')
    for card in cards:
        info = {}

        currData = card.text.split('\n')

        info['subreddit'] = currData[0]
        info['user'] = currData[3]
        info['title'] = currData[5]
        info['upvotes'] = currData[-3].replace('upvotes', ' ').strip()
        info['comments'] = currData[-2].replace('comments', ' ').strip()
        info['awards'] = currData[-1].replace('awards', ' ').strip()
        data.append(info)

    driver.quit()
    return data


query = 'usa'
data = searchReddit(query)
with open('./test.json', 'w') as f:
    json.dump(data,f,indent=4)




if __name__ == '__main__':
    app.run(debug=True)
