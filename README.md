# Gdańsk airport API 

## Description
It's a web scraper and API. It parses page https://komunikacja.trojmiasto.pl/lotnisko/?odloty to get arrivals and departures of Gdańsk airport and exposes it by two endpoints. I looked for some smart API but couldn't find anything which could fulfill my needs. 

## How it works?
It parses web page and converts html list into list of `Flight` objects. 
Structure looks like this:
```
[
    {
        "time": "12:30",
        "flight_city": "Kraków",
        "flight_info": "WZ 620",
        "details": "Odwołany"

    },
    ...
]
```

## Prerequisites 
Just add two env variables:
1. `ARRIVALS_URL` (https://komunikacja.trojmiasto.pl/lotnisko/)
2. `DEPARTURES_URL` (https://komunikacja.trojmiasto.pl/lotnisko/?odloty)