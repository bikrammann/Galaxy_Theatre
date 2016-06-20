import json, time
from datetime import datetime
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver

data = {}
sortedJson = []

browser = webdriver.PhantomJS("./phantomjs.exe")
browser.get('http://www.galaxytheatres.com/Browsing/Cinemas/Details/3')

# Parse html
soup = BeautifulSoup(browser.page_source, "html.parser")
gData = soup.find_all('div', {'class': 'film-showtimes'})

# Total number of movies
movieTotal = len([movie.text for movie in soup.find_all('h3', {'class': 'film-title'})])

for i in range(movieTotal):
    # Get movie name
    movieTitle = gData[i].find('h3', {'class': 'film-title'}).text

    # Get date when move is showing
    movieDate = gData[i].find('h4', {'class': 'session-date'}).text
    movieDate = movieDate.split(',')[1].strip()
    movieDate = time.mktime(datetime.strptime(movieDate, "%d %B %Y").timetuple())

    # Get movie Timings
    Timing = list(gData[i].find('div', {'class': 'session-times'}))
    Timing = [element for element in Timing if element != '\n']  # Remove '\n' from the timing list
    movieTiming = [time.find('time').text for time in Timing]

    # Storing everything in json format
    data.update({i: {'name': movieTitle, 'date': movieDate, 'timing': movieTiming}})

# Sorting dictionary by date
sortedData = sorted(data.values(), key=itemgetter('date'))

# Creating List with Dictionaries sorted by Date
for values in sortedData:
    sortedJson.append({'name': values['name'],
                       'timing': values['timing'],
                       'date': datetime.fromtimestamp(int(values['date'])).strftime("%d %B %Y")
                       })

# Writing data to json file
with open('movie.json', 'w') as f:
    json.dump(sortedJson, f, indent=2)
