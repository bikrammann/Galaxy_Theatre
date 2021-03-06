import json, time
from datetime import datetime
from operator import itemgetter
from bs4 import BeautifulSoup
from selenium import webdriver

data = {}
sortedJson = {}

# Note: This program will work without phantomjs.exe as the current page
# that we are processing is static(You can use requests library to get the page contents).
# However there are other pages on the website
# where content is loaded via JavaScript for them you will need to download phantomjs.exe
browser = webdriver.PhantomJS("./phantomjs.exe")
browser.get('http://www.galaxytheatres.com/Browsing/Cinemas/Details/3')

# Parse html
soup = BeautifulSoup(browser.page_source, "html.parser")
gData = soup.find_all('div', {'class': 'film-showtimes'})

# Total number of movies
movieTotal = len([movie.text for movie in soup.find_all('h3', {'class': 'film-title'})])

for i in range(movieTotal):
    # Get movie image
    image = gData[i].findPreviousSibling('div').find_all('div')[1].get('style')
    startPos = image.find("//") + 2
    imageUrl = image[startPos:-2]

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
    data.update({i: {'name': movieTitle, 'date': movieDate, 'timing': movieTiming, 'url':imageUrl}})

# Sorting dictionary by date
sortedData = sorted(data.values(), key=itemgetter('date'))

# Creating List with Dictionaries sorted by Date
for i,values in enumerate(sortedData):
    sortedJson.update({i:{'name': values['name'],
                       'timing': values['timing'],
                       'url': values['url'],
                       'date': str(datetime.fromtimestamp(int(values['date'])).strftime("%d %B %Y"))
                       }})

# Writing data to json file
with open('movie.json', 'w') as f:
    json.dump(sortedJson, f, indent=2)
