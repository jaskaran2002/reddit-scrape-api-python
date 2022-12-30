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


@app.route('/runDuckPython/<string:query>')
def searchNews(query):
    PATH = "./geckodriver"
    data = []
    options = Options()
    PATH_TO_DEV_NULL = '/dev/null'
    options.headless = True
    driver = webdriver.Firefox(executable_path=PATH, options=options, service_log_path=PATH_TO_DEV_NULL)
    # driver = webdriver.Firefox(executable_path=PATH)
    url = f"https://duckduckgo.com/{query}"
    driver.get(url)
    # search = driver.find_element(By.ID, 'searchbox_input')
    # search.send_keys(query)
    # search.send_keys(Keys.RETURN)
    try:
        news = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, 'News')))
    except:
        print("Not Found")
        driver.quit()
        exit()
    news.click()
    try:
        cards = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'result__body')))
    except:
        print("Cards not found")
        driver.quit()
        exit()
    for card in cards:
        info = {}
        info['title'] = card.find_element(By.CLASS_NAME, 'result__a').text
        info['text'] = card.find_element(By.CLASS_NAME, 'result__snippet').text
        website = card.find_element(By.CLASS_NAME, 'result__url')
        info['website'] = website.text
        info['news-link'] = website.get_attribute('href')
        try:
            img = card.find_element(By.CLASS_NAME, 'result__image__img')
            info['image'] = img.get_attribute('src')
        except:
            print("not Found")
        data.append(info)
    driver.quit()
    return data


# query = ' '.join(sys.argv[1:])
# query="duckirony"
output = searchNews(query)
with open('output.json', 'w') as f:
    json.dump(output,f,indent=4)


    


if __name__ == '__main__':
    app.run(debug=True)
