## Dependency Code
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .constants import BCV_URL, ENPARALELO_URL
from .models import Rate

def BCVStringToDate(dateString: str) -> tuple:
    monthToInt = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }
    date = dateString.split(",")[1]
    dmy = date.split()

    day = int(dmy[0])
    month = monthToInt[dmy[1].lower()]
    year = int(dmy[2])

    result = (day, month, year)
    return result

def today_string() -> str:
    today = datetime.now()
    return today.strftime('%m-%d-%Y')

def getBCVUpdate() -> dict:
    try:
        response = requests.get(BCV_URL, verify=False)
    except Exception as e:
        print('ERROR:', e)
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # parsing from bs4
    rateusd = float(soup.select("#dolar")[0].select(".centrado")[0].strong.contents[0].replace(",","."))
    datestring = soup.select(".date-display-single")[0].contents[0]

    # extra prep
    day, month, year = BCVStringToDate(datestring)
    dateofupdate = "{:02}-{:02}-{:04}".format(month, day, year)
    datetime_update = datetime.strptime(dateofupdate, "%m-%d-%Y")

    rateObject = Rate(rateusd, datetime_update, datetime.now(), 'Bs', 'BCV', dateofupdate)
    return rateObject.to_dict()

# EnParalelo scraper

def scrape_telegram_group() -> list:
    try:
        response = requests.get(ENPARALELO_URL)
    except Exception as e:
        # Return 400
        print(f'ERROR: {e}')
        return None
    
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    messages = soup.find_all('div', class_='tgme_widget_message_text')

    message_strings = []
    for message in messages:
        message_strings.append(message.text)

    return message_strings

def padHour(hourString: str) -> str:
    if len(hourString) == 4:
        return '0' + hourString
    return hourString

def isRate(message: str) -> bool:
    dateEmojiIndex = message.find('🗓')
    timeEmojiIndex = message.find('🕒')
    moneyEmojiIndex = message.find('💵')
    if dateEmojiIndex != -1 and timeEmojiIndex != -1 and moneyEmojiIndex != -1:
        return (dateEmojiIndex, timeEmojiIndex, moneyEmojiIndex)
    return None

def parseRatestring(rate_string: str) -> float:
    _, rate = rate_string.split(' ')
    rate = rate.replace(',', '.')
    return float(rate)

def parseMessage(message: str, indices: tuple):
    dateEmojiIndex, timeEmojiIndex, moneyEmojiIndex = indices

    date = message[dateEmojiIndex+1:timeEmojiIndex].strip()
    time = message[timeEmojiIndex+1:moneyEmojiIndex].strip()
    rate = message[moneyEmojiIndex+1:moneyEmojiIndex+11].strip()
    rate = parseRatestring(rate)

    hour, am_pm = filter(lambda x: len(x) > 0, time.split(' '))
    hour = padHour(hour)
    date_string = f'{date} {hour} {am_pm}'

    dateObject = datetime.strptime(date_string, '%d/%m/%Y %I:%M %p')
    uniqueName = date.replace('/', '-') + am_pm

    rateObject = Rate(rate, dateObject, datetime.now(), 'Bs', 'Paralelo', uniqueName)
    return rateObject.to_dict()

def getParaleloUpdates():
    parsed_messages = []
    messages = scrape_telegram_group()
    if not messages:
        return None
    for message in messages:
        indeces = isRate(message)
        if not indeces:
            continue
        parsed_message = parseMessage(message, indeces)
        parsed_messages.append(parsed_message)
    return parsed_messages
