from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3

"""
This script generates a map with the geo location of the tweeters
iformation gathered in our database.
"""

conn = sqlite3.connect('db/tweetBank.db')

c = conn.cursor()

print ("Reading from the database...")

# We select all the tweets with geo position information in the db
c.execute("SELECT LAT, LONG FROM TWEETS WHERE LAT IS NOT NULL "
          + "AND LONG IS NOT NULL");

cursor = list(c)
lats  = [record[0] for record in cursor]
longs = [record[1] for record in cursor]

print("Generating map...")

"""
Here we generate a map and put a red point at all the locations
of every tweet stored in the database which has geo-information.
The map is plotted at the end.
"""
# Intermediate resolution
# Cylindrical Equidistant projection
m = Basemap(projection='cyl', resolution='i')
# Display shaded relief image (from http://www.shadedrelief.com) 
# as map background
m.shadedrelief()
x, y = m(longs, lats)
# We set the red dots on the map
m.scatter(x, y, s=3, color='#ff0000', marker='o', alpha=0.3)

plt.show()
