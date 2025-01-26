import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Country():
    def __init__(self, name, shape, color):
        self.name=name
        self.shape = shape
        self.color = color


world = gpd.read_file('ne_10m_admin_0_countries')

# list of countries for which a map is created 'Canada'
countries = ['United States of America','Costa Rica','Australia','Japan','Netherlands','Panama','Germany','France','El Salvador','Sweden','Guatemala','United Kingdom','The Bahamas','New Zealand','Switzerland','Ireland','Austria','Belgium','Brazil','Singapore','Spain','Denmark','Philippines','Malaysia','Norway','Taiwan','Andorra','Finland','Thailand','Italy','Luxembourg','Venezuela','Mexico','Turkey','Argentina','Republic of Serbia','South Korea','Hungary','China','Chile','Indonesia','Portugal','Greece','Uruguay','Czechia','Poland','Monaco','Brunei','Morocco','Israel','Slovenia','Saudi Arabia','Kuwait','Oman','Egypt','Bulgaria','Bahrain','Latvia','United Arab Emirates','Estonia','Romania','Malta','Colombia','Slovakia','South Africa','Qatar','Honduras','Croatia','Samoa','Fiji','Liechtenstein','Lithuania','India','Peru','Jordan','Paraguay','Dominican Republic','Trinidad and Tobago','Ukraine','Cyprus','Ecuador','Suriname','Moldova','Nicaragua','Lebanon','Pakistan','Sri Lanka','Georgia','Azerbaijan','Samoa','Mauritius','Vietnam']
#countries = ['Israel','Canada','Australia','Japan'] #'Netherlands','Panama','Germany','France']
countries.sort()
# create a list containing countries that are too small to be visible on a map
small = []
for a in world.area:
    #print(a, world['ADMIN'][list(world.area).index(a)])
    if a < 2.1:
        small.append(world['ADMIN'][list(world.area).index(a)])
print(small)
for c in range(0,92,4):
    # create variable for a polygon or multipolygon representing the current country
    cur=[]
    colors = ['#f7b064', '#ff8289', '#9cff9c', '#c668c6']
    for n in range(4):
        name = countries[c+n]
        color = colors[n]
        i = list(world['SOVEREIGNT']).index(name)
        shape=world['geometry'][i]
        cur.append(Country(name=name, shape=shape, color=color))
    #for k in i:
        #cur.append(world['geometry'][k])


    #configure size and appearance of plot
    fig = plt.figure()
    fig.patch.set_alpha(0)
    fig.patch.set_facecolor('white')
    axs = fig.subplots()
    axs.set_facecolor('#ffdedd') #ff0e0022
    axs.set_ylim([-60,89])
    axs.set_xlim([-180,180])
    axs.set_xticks(ticks=[])
    axs.set_yticks(ticks=[])
    #create plot
    world.plot(ax=axs, cmap='Blues', column='MAPCOLOR7', ec='black', linewidth=0.1)

    # draw highlighted country
    for country in cur:
        if country.shape.geom_type == 'MultiPolygon': #for countries containing multiple shapes
            for mp in country.shape.geoms:
                xs, ys = mp.exterior.xy
                axs.fill(xs, ys, fc=country.color, ec='black', linewidth=0.1)

        elif country.shape.geom_type == 'Polygon': #for single polygon countries
            xs, ys = country.shape.exterior.xy
            axs.fill(xs, ys, fc=country.color, ec='black', linewidth=0.1)

        #draw circle around very small countries for visibility
        if country.name in small:
            axs.plot(country.shape.centroid.x, country.shape.centroid.y, 'o', mec=country.color, mfc='none', linewidth=0.7, markersize=12)

        i = cur.index(country)
        y = -10-15*i
        rect = patches.Rectangle((-175,y), 10,10, ec='black', color=country.color)
        axs.add_patch(rect)
        axs.text(-160, y+2, s=country.name, fontdict=None)

    # remove boykonur cosmodrome from map for cleaner appearance
    kz = world['geometry'][171]
    bxs, bys = kz.exterior.xy
    axs.fill(bxs, bys, fc='#105ba4', ec='#105ba4')



    #fig.patch.set_facecolor('white')
    #fig.patch.set_alpha(0)
    title=''
    for c in cur:
        title += c.name+'_'
    #add name of country as title and save plot
    #plt.title(title, fontsize=20)
    plt.savefig('maps_new/'+title+'.png', dpi=1000, bbox_inches='tight')
    #close plot after it is saved
    plt.close(fig)