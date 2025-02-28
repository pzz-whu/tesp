# Copyright (C) 2021-2022 Battelle Memorial Institute
# file: ercot_map.py

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import csv
import networkx as nx
import numpy as np
import sys
import zipfile
import os

featureScale = '50m'  # 10, 50 0r 110
shapePath = './Texas_SHP/'

def feature_from_archive (shp_path, zip_name, shp_root, asFeature=True):
  zf = zipfile.ZipFile (shp_path + zip_name)
  for ext in ['shp', 'shx', 'dbf']:
    fname = '{:s}{:s}.{:s}'.format (shp_path, shp_root, ext)
    if not os.path.isfile (fname):
      zf.extract (shp_root + '.' + ext, shp_path)
  rdr = shpreader.Reader (shp_path + shp_root)
  if asFeature:
    f = cfeature.ShapelyFeature (list(rdr.geometries()), ccrs.PlateCarree())
  else:
    f = list(rdr.geometries())
  zf.close()
  return f

COUNTIES = feature_from_archive (shapePath, 'Tx_Census_CntyGeneralCoast_TTU.zip', 'Tx_Census_CntyGeneralCoast_TTU')
ROADS = feature_from_archive (shapePath, 'Tx_Interstates_General_NE.zip', 'Tx_Interstates_General_NE')
WIND = feature_from_archive (shapePath, 'Tx_WindTurbines_USGS.zip', 'Tx_WindTurbines_USGS', False)
URBAN = feature_from_archive (shapePath, 'TxDOT_Urbanized_Areas.zip', 'Urbanized_Area')

plt.figure(figsize=(8, 8))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND.with_scale(featureScale), facecolor = 'honeydew')
ax.add_feature(cfeature.STATES.with_scale(featureScale))
ax.add_feature(cfeature.OCEAN.with_scale(featureScale))
ax.add_feature(cfeature.RIVERS.with_scale(featureScale), zorder=2)
ax.add_feature(cfeature.LAKES.with_scale(featureScale), zorder=2)
ax.add_feature(COUNTIES, facecolor='none', edgecolor='gray')
ax.add_feature(ROADS, facecolor='none', edgecolor='magenta')
ax.add_feature(URBAN, zorder=10, facecolor='orange', edgecolor='orange', alpha=0.3)
ax.scatter([point.x for point in WIND], [point.y for point in WIND], 
           transform=ccrs.PlateCarree(), s=2, c='cyan')
ax.coastlines(featureScale)

ax.set_extent([-107.0, -93.0, 25.0, 37.0])
ax.gridlines (draw_labels=True)
ax.set_xmargin (0)
ax.set_ymargin (0)

# name,bus1,bus2,kV,length[miles],#parallel,r1[Ohms/mile],x1[Ohms/mile],b1[MVAR/mile],ampacity,capacity[MW]
dlines = np.genfromtxt('Lines8.csv', dtype=str, skip_header=1, delimiter=',') # ['U',int,int,float,float,int,float,float,float,float,float], skip_header=1, delimiter=',')
# bus,zone,lon,lat,load,gen,diff,caps
dbuses = np.genfromtxt('Buses8.csv', dtype=[int, int, float, float, float, float, float, float], skip_header=1, delimiter=',')
# idx,bus,mvabase,pmin,qmin,qmax,c2,c1,c0
dunits = np.genfromtxt('Units8.csv', dtype=[int, int, float, float, float, float, float, float, float], skip_header=1, delimiter=',')

lbl345 = {}
e345 = set()
n345 = set()
lst345 = []
w345 = []
graph = nx.Graph()
for e in dlines:
	if '//' not in e[0]:
		n1 = int(e[1])
		n2 = int(e[2])
		npar = int(e[5])
		graph.add_edge (n1, n2)
		n345.add (n1)
		n345.add (n2)
		lbl345[(n1, n2)] = e[0]
		e345.add ((n1, n2))
		lst345.append ((n1, n2))
		w345.append (1.25 * npar)

xy = {}
for b in dbuses:
	xy[b[0]] = [b[2], b[3]]

gnodes345 = nx.draw_networkx_nodes (graph, xy, nodelist=list(n345), node_color='k', node_size=60, ax=ax) # , alpha=0.3)
glines345 = nx.draw_networkx_edges (graph, xy, edgelist=lst345, edge_color='r', width=w345, ax=ax) # , alpha=0.8)

gnodes345.set_zorder(20)
glines345.set_zorder(18)

lroad = mlines.Line2D ([0,1], [0,1], color='magenta')
lurban = mpatches.Rectangle ((0, 0), 1, 1, facecolor='orange')
lwind = mpatches.Rectangle ((0, 0), 1, 1, facecolor='cyan')
ax.legend ([lroad, lurban, lwind, gnodes345, glines345], 
           ['Interstate', 'Urbanized', 'WindGen', 'EHV Sub', 'EHV Line'], loc='lower left')

plt.title ('Retained Buses and Lines - 345 kV')
plt.xlabel ('Longitude [deg]')
plt.ylabel ('Latitude [deg N]')
plt.grid(linestyle='dotted')

# Save the plot by calling plt.savefig() BEFORE plt.show()
plt.savefig('Ercot8.png', pad_inches=0.1, bbox_inches = 'tight')

plt.show()
