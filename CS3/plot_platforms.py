import folium
import pandas as pd

# Load the OSPAR database CSV file
df = pd.read_csv('ospar_offshore_installations_2019_01_002.csv')
# Filter the installations with the 'above water production' function
df = df[df['Function'] == 'Above water production']
# Filter the installations with the 'oil' Primary_pr
df = df[df['Primary_pr'] == 'Oil']
# filter for coordinates in the North Sea between 48 and 62 degrees latitude and 0 and 10 degrees longitude
df = df[(df['Latitude'] > 48) & (df['Latitude'] < 62) & (df['Longitude'] > -1.3) & (df['Longitude'] < 6.5)]

# create a list of the coordinates of the installation with demark as country
denmark = df[df['Country'] == 'Denmark']
denmark = denmark[['Latitude', 'Longitude']]
denmark = denmark.values.tolist()
