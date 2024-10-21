import geopandas as gpd
import matplotlib.pyplot as plt

world = gpd.read_file('ne_10m_admin_0_countries')

# list of countries for which a map is created
countries = ['United States of America','Canada','Costa Rica','Australia','Japan','Netherlands','Panama','Germany','France','El Salvador','Sweden','Guatemala','United Kingdom','The Bahamas','New Zealand','Switzerland','Ireland','Austria','Belgium','Brazil','Singapore','Spain','Denmark','Philippines','Malaysia','Norway','Taiwan','Andorra','Finland','Thailand','Italy','Luxembourg','Venezuela','Mexico','Turkey','Argentina','Republic of Serbia','South Korea','Hungary','China','Chile','Indonesia','Portugal','Greece','Uruguay','Czechia','Poland','Monaco','Brunei','Morocco','Israel','Slovenia','Saudi Arabia','Kuwait','Oman','Egypt','Bulgaria','Bahrain','Latvia','United Arab Emirates','Estonia','Romania','Malta','Colombia','Slovakia','South Africa','Qatar','Honduras','Croatia','Samoa','Fiji','Liechtenstein','Lithuania','India','Peru','Jordan','Paraguay','Dominican Republic','Trinidad and Tobago','Ukraine','Cyprus','Ecuador','Suriname','Moldova','Nicaragua','Lebanon','Pakistan','Sri Lanka','Georgia','Azerbaijan','Samoa','Mauritius','Vietnam']

# create a list containing countries that are too small to be visible on a list
small = []
for a in world.area:
    if a < 0.5:
        small.append(world['ADMIN'][list(world.area).index(a)])

for c in countries:
    # create variable for a polygon or multipolygon representing the current country
    i = list(world['SOVEREIGNT']).index(c)
    cur = world['geometry'][i]

    #configure size and appearance of plot
    fig, axs = plt.subplots()
    axs.set_facecolor('#ff0e0022')
    axs.set_ylim([-90,90])
    axs.set_xlim([-180,180])
    axs.set_xticks(ticks=[])
    axs.set_yticks(ticks=[])
    #create plot
    world.plot(ax=axs, cmap='Blues', column='SOVEREIGNT', ec='black', linewidth=0.1)

    # draw highlighted country
    if cur.geom_type == 'MultiPolygon': #for countries containing multiple shapes
        for mp in cur.geoms:
            xs, ys = mp.exterior.xy
            axs.fill(xs, ys, fc='#ff4c4c', ec='black', linewidth=0.1)

    elif cur.geom_type == 'Polygon': #for single polygon countries
        xs, ys = cur.exterior.xy
        axs.fill(xs, ys, fc='#ff4c4c', ec='black', linewidth=0.1)

    #draw circle around very small countries for visibility
    if c in small:
        axs.plot(cur.centroid.x, cur.centroid.y, 'o', mec='r', alpha=0.8, mfc='none', linewidth=0.5)

    # remove boykonur cosmodrome from map for cleaner appearance
    kz = world['geometry'][171]
    bxs, bys = kz.exterior.xy
    axs.fill(bxs, bys, fc='#84bcdb', ec='#84bcdb')

    #add name of country as title and save plot
    plt.title(c)
    plt.savefig('Maps/'+c+'.png', dpi=2000, bbox_inches='tight')
    #close plot after it is saved
    plt.close(fig)