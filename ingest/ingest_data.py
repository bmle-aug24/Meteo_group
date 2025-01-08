from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import numpy as np

from url_dict import URL_DICT

def check_none_fill(value, float_=False):
    if value == '\xa0':
        return np.nan
    else:
        if float_: 
            return float(value)
        else:
            return value

def ingest_data(location):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    url = URL_DICT[location]
    if url: 
        r = requests.get(url, headers=headers)
    else:
        return None

    if r.status_code == 200:
        try:
            soup = bs(r.content, 'html5lib')
            table = soup.find("tbody")
            row = table.find_all("tr")[-2]
            values_row = [value.text for value in row]
        except AttributeError:
            return None

        date = datetime.today().strftime('%Y-%m-') + row.find("th", class_="rb").text.zfill(2)
        location = location
        minTemp = check_none_fill(values_row[2], float_=True)
        maxTemp = check_none_fill(values_row[3], float_=True)
        rainfall = check_none_fill(values_row[4], float_=True)
        evaporation = check_none_fill(values_row[5], float_=True)
        sunshine = check_none_fill(values_row[6], float_=True)
        windgustdir = check_none_fill(values_row[7])
        windgustspeed = check_none_fill(values_row[8], float_=True)
        winddir9am = check_none_fill(values_row[13])
        winddir3pm = check_none_fill(values_row[19])
        windspeed9am = check_none_fill(values_row[14], float_=True)
        windspeed3pm = check_none_fill(values_row[20], float_=True)
        humidity9am = check_none_fill(values_row[11], float_=True)
        humidity3pm = check_none_fill(values_row[17], float_=True)
        pressure9am = check_none_fill(values_row[15], float_=True)
        pressure3pm = check_none_fill(values_row[21], float_=True)
        cloud9am = check_none_fill(values_row[12], float_=True)
        cloud3pm = check_none_fill(values_row[18], float_=True)
        temp9am = check_none_fill(values_row[10], float_=True)
        temp3pm = check_none_fill(values_row[16], float_=True)
        raintoday = 'Yes' if rainfall >=1 else 'No'

        data = {
            'Date': date,
            'Location': location,
            'MinTemp': minTemp,
            'MaxTemp': maxTemp,
            'Rainfall': rainfall,
            'Evaporation': evaporation,
            'Sunshine': sunshine,
            'WindGustDir' : windgustdir,
            'WindGustSpeed': windgustspeed,
            'WindDir9am': winddir9am,
            'WindDir3pm': winddir3pm,
            'WindSpeed9am': windspeed9am,
            'WindSpeed3pm': windspeed3pm,
            'Humidity9am': humidity9am,
            'Humidity3pm': humidity3pm,
            'Pressure9am': pressure9am,
            'Pressure3pm': pressure3pm,
            'Cloud9am': cloud9am,
            'Cloud3pm': cloud3pm,
            'Temp9am' : temp9am,
            'Temp3pm': temp3pm,
            'RainToday': raintoday,
            'RainTomorrow': np.nan
        }

        return data
    else:
        return None

def get_day_data():
    return [{location:ingest_data(location)} for location in URL_DICT if URL_DICT[location]]

def main():
    data = get_day_data()
    print(data)
    print("All processed")

if __name__ == "__main__":
    main()
    