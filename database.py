import sqlite3 as lite
import pandas as pd

conn = lite.connect('city_weather.db')

conn.execute("DROP TABLE IF EXISTS cities")
conn.execute("DROP TABLE IF EXISTS weather")

conn.execute("CREATE TABLE cities (name text, state text)")
conn.execute("CREATE TABLE weather(city text, year integer, warm_month text, cold_month text, average_high integer)")

cityList = (
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA'),
    ('Las Vegas', 'NV'),
    ('Atlanta', 'GA')
    )

weatherList = (
    ('New York City', 2013, 'July', 'January', 62),
    ('Boston', 2013, 'July', 'January', 59),
    ('Chicago', 2013, 'July', 'January', 59),
    ('Miami', 2013, 'August', 'January', 84),
    ('Dallas', 2013, 'July', 'January', 77),
    ('Seattle', 2013, 'July', 'January', 61),
    ('Portland', 2013, 'July', 'December', 63),
    ('San Franciso', 2013, 'September', 'December', 64),
    ('Los Angeles', 2013, 'September', 'December', 75),
    ('Las Vegas', 2013, 'July', 'December', 95),
    ('Atlanta', 2013, 'July', 'January', 90)
   )

monthChoice = 'July'

with conn:
    cur = conn.cursor()
    cur.executemany("INSERT INTO cities VALUES(?,?)", cityList)
    cur.executemany("INSERT INTO weather VALUES(?,?,?,?,?)", weatherList)

    cur.execute("""
        SELECT city, state, warm_month, average_high
        FROM weather
        JOIN cities
            ON city = name
        WHERE warm_month = ?
        ORDER BY average_high DESC
        """, 
        (monthChoice,)
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=cols)
    
# print df

# print df['state']

def outputText(monthChoice, cityList, stateList):

    baseString = "The cities that are warmest in %s are: " % (monthChoice)

    cityStateTups = zip(cityList, stateList)

    def stringPairFromTup(tup):
        return "%s, %s" % (tup[0],tup[1])

    stringPairList = map(stringPairFromTup, cityStateTups)

    stringPairList[-1] = "and " + stringPairList[-1] + "."

    stringPairOut = "; ".join(stringPairList)

    textString = baseString + stringPairOut

    return textString

print outputText(monthChoice, df['city'].values.tolist(), df['state'].values.tolist())