import requests
import time
import schedule
import pyodbc


conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
    SERVER=LGGRAM\SQLEXPRESS; Database=Socket_MMT; UID=lc; PWD=1;')


def writeData(countries):
    cursor = conn.cursor()
    cursor.execute("DELETE Countries WHERE _date = CONVERT(VARCHAR(10), GETDATE(), 103)")

    for country in countries:
        if country['active'] == None and country['recovered'] == None:
            cursor.execute(f"INSERT INTO Countries(_date, _country, _totalCases, _todayCases, _deaths, _todayDeaths, _critical) values (CONVERT(VARCHAR(10), GETDATE(), 103), '{country['country']}', {country['cases']}, {country['todayCases']}, {country['deaths']}, {country['todayDeaths']}, {country['critical']})")
        elif country['active'] == None:
            cursor.execute(f"INSERT INTO Countries(_date, _country, _totalCases, _todayCases, _deaths, _todayDeaths, _recovered, _critical) values (CONVERT(VARCHAR(10), GETDATE(), 103), '{country['country']}', {country['cases']}, {country['todayCases']}, {country['deaths']}, {country['todayDeaths']}, {country['recovered']}, {country['critical']})")
        elif country['recovered'] == None:
            cursor.execute(f"INSERT INTO Countries(_date, _country, _totalCases, _todayCases, _active, _deaths, _todayDeaths, _critical) values (CONVERT(VARCHAR(10), GETDATE(), 103), '{country['country']}', {country['cases']}, {country['todayCases']}, {country['active']}, {country['deaths']}, {country['todayDeaths']}, {country['critical']})")
        else:
            cursor.execute(f"INSERT Countries values (CONVERT(VARCHAR(10), GETDATE(), 103), '{country['country']}', {country['cases']}, {country['todayCases']}, {country['active']}, {country['deaths']}, {country['todayDeaths']}, {country['recovered']}, {country['critical']})")

    cursor.commit()


def getAPI():
    url = "https://coronavirus-19-api.herokuapp.com/countries"
    res = requests.get(url)
    countries = res.json()
    writeData(countries)

def cycleGetAPI():
    schedule.every(3600).seconds.do(getAPI)
    while True:
        schedule.run_pending()
        time.sleep(60)

def all_data():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Countries")
    all_data_covid = cursor.fetchall()
    return all_data_covid

def search(dayCt, monthCt, yearCt, nameCt):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Countries WHERE _country = '{nameCt}' AND _date = '{dayCt}/{monthCt}/{yearCt}'")
    data = cursor.fetchall()
    return data