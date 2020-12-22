from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import json 
from datetime import datetime
import os

app = Flask(__name__)

FLIGHTS_LIST_ELEMENT_CLASS_NAME = 'zkm-schedule__departure'
FLIGHT_TIME_CLASS_NAME = 'zkm-schedule__time'
FLIGHT_CITY_CLASS_NAME = 'zkm-schedule__city'
FLIGHT_INFO_CLASS_NAME = 'zkm-schedule__flight'
FLIGHT_ROUTE_CLASS_NAME = 'zkm-schedule__route'

URL_ARRIVALS = os.environ['ARRIVALS_URL']
URL_DEPARTURES = os.environ['DEPARTURES_URL']

LANDED = 'wylądował'
STARTED = 'wystartował'

def is_current_flight(flight):
    details = flight['details'].lower()
    return LANDED not in details and STARTED not in details

def filter_already_landed(flights):
    return list(filter(lambda x: is_current_flight(x), flights))

def parse_flight_info(flight_schedule, max_number = -1):
    results = []
    for item in flight_schedule:
        flight = {}
        flight['time'] = item.find_next(class_=FLIGHT_TIME_CLASS_NAME).text.strip()
        flight['flight_city'] = item.find_next(class_=FLIGHT_CITY_CLASS_NAME).text.strip()
        flight['flight_info'] = item.find_next(class_=FLIGHT_INFO_CLASS_NAME).text.strip()
        flight['details'] = item.find_next(class_=FLIGHT_ROUTE_CLASS_NAME).text.strip()
        results.append(flight)

    filtered_results = filter_already_landed(results)

    return filtered_results if max_number == -1 else filtered_results[:max_number]

def get_flights_info(url, max_number = -1):
    page = requests.get(url)
    soup_page = BeautifulSoup(page.content, 'html.parser')
    flight_schedule = soup_page.find_all(class_= FLIGHTS_LIST_ELEMENT_CLASS_NAME)
    results = parse_flight_info(flight_schedule, max_number)

    return json.dumps(results, ensure_ascii=False)

@app.route('/arrivals')
def arrivals():
    max_number = request.args.get('max')
    if(max_number):
        return get_flights_info(URL_ARRIVALS, int(max_number))
    else:
        return get_flights_info(URL_ARRIVALS)
    
@app.route('/departures')
def departures():
    max_number = request.args.get('max')
    if(max_number):
        return get_flights_info(URL_DEPARTURES, int(max_number))
    else:
        return get_flights_info(URL_DEPARTURES)

if __name__ == '__main__':
    app.run()