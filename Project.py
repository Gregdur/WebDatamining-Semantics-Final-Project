from flask import Flask, render_template,request
import folium
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

################################################################################################ SPARQL QUERIES

#Query : school of a city

# 1

def QueryCity(city, infrastructure):
    query = SPARQLWrapper("http://localhost:3030/" + infrastructure + "/query")
    if(infrastructure == "EcoleSup"):
        city = city
    else:
        city = city.upper()
    query.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX j.0: <http://schema.org/>
        SELECT ?lon ?lat ?name
        WHERE {
            ?subject j.0:commune '"""+ city +"""'.
            ?subject j.0:longitude ?lon.
            ?subject j.0:latitude ?lat.
            ?subject j.0:nom ?name}
    """)
    query.setReturnFormat(JSON)
    query_results = query.query().convert()
    coordonnee = []


    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]

        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        for i in range(len(lon_brut)):
            if lon_brut[i] == "E":
                lon_brut = float(lon_brut[:i])
                break
        for i in range(len(lat_brut)):
            if lat_brut[i] == "E":
                lat_brut = float(lat_brut[:i])
                break

        lon_brut=float(lon_brut)
        lat_brut=float(lat_brut)
        coor = [lon_brut,lat_brut, name]
        coordonnee.append(coor)

    return(coordonnee)

# 2

def QueryCity2(city, infrastructure):
    query = SPARQLWrapper("http://localhost:3030/" + infrastructure + "/query")
    if(infrastructure == "EcoleSup"):
        city = city
    else:
        city = city.upper()
    query.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX j.0: <http://schema.org/>
        SELECT ?lon ?lat ?name
        WHERE {
            ?subject j.0:commune '"""+ city +"""'.
            ?subject j.0:longitude ?lon.
            ?subject j.0:latitude ?lat.
            ?subject j.0:nom ?name}
    """)
    query.setReturnFormat(JSON)
    query_results = query.query().convert()
    coordonnee = []

    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]

        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        for i in range(len(lon_brut)):
            if lon_brut[i] == "E":
                lon_brut = float(lon_brut[:i])
                break
        for i in range(len(lat_brut)):
            if lat_brut[i] == "E":
                lat_brut = float(lat_brut[:i])
                break

        lon_brut=float(lon_brut)
        lat_brut=float(lat_brut)
        coor = [lon_brut,lat_brut, name]
        coordonnee.append(coor)

    return(coordonnee)


# Query : velib of Paris

def QueryVelib():
    query = SPARQLWrapper("http://localhost:3030/Velib/query")
    query.setQuery("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX j.0: <http://schema.org/>
                SELECT ?lon ?lat ?name ?cap
                WHERE {
                    ?subject j.0:coordonnees ?lon.
                    ?subject j.0:coordonnees ?lat.
                    ?subject j.0:capacity ?cap.
                    ?subject j.0:name ?name}
            """)
    query.setReturnFormat(JSON)
    query_results = query.query().convert()
    coordonnee = []

    # Export file
    with open('output_velib.jsonld', 'w+') as outfile:
        outfile.write("[")
        for i in range(50):
            outfile.write(str(query_results["results"]["bindings"][i]).replace("'", '"') + ",")
        outfile.write(
            str(query_results["results"]["bindings"][len(query_results["results"]["bindings"]) - 1]).replace("'", '"'))
        outfile.write("]")

    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]
        capacity = query_results["results"]["bindings"][i]["cap"]["value"]
        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        coor = [lon_brut, lat_brut, name, capacity]
        coordonnee.append(coor)
    print(coor)
    return (coordonnee)

# Query : all IDF train stations
def QueryGare():
    query = SPARQLWrapper("http://localhost:3030/Gares/query")
    query.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX j.0: <http://schema.org/>
            SELECT ?lon ?lat ?name ?line
            WHERE {
                ?subject j.0:coordonnees ?lon.
                ?subject j.0:coordonnees ?lat.
                ?subject j.0:ligne ?line.
                ?subject j.0:nom ?name}
        """)

    query.setReturnFormat(JSON)
    query_results = query.query().convert()

    coordonnee = []

    # Export file
    with open('output_gare.jsonld', 'w+') as outfile:
        outfile.write("[")
        for i in range(40):
            outfile.write(str(query_results["results"]["bindings"][i]).replace("'", '"') + ",")
        outfile.write(
            str(query_results["results"]["bindings"][len(query_results["results"]["bindings"]) - 1]).replace("'", '"'))
        outfile.write("]")


    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]
        line = query_results["results"]["bindings"][i]["line"]["value"]
        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        coor = [lon_brut,lat_brut,name,line]
        coordonnee.append(coor)

    print(coor)
    return(coordonnee)

################################################################
#BONUS
################################################################

# Query : all the train station of a specific line

def QueryGareLigne(ligne):
    query = SPARQLWrapper("http://localhost:3030/Gares/query")
    query.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX j.0: <http://schema.org/>
            SELECT ?lon ?lat ?name
            WHERE {
                ?subject j.0:coordonnees ?lon.
                ?subject j.0:coordonnees ?lat.
                ?subject j.0:ligne '"""+ ligne +"""'.
                ?subject j.0:nom ?name}
        """)
    query.setReturnFormat(JSON)
    query_results = query.query().convert()
    coordonnee = []

    # Export file
    with open('output_gare-'+ligne+'.jsonld', 'w+') as outfile:
        outfile.write("[")
        for i in range(len(query_results["results"]["bindings"]) - 1):
            outfile.write(str(query_results["results"]["bindings"][i]).replace("'", '"') + ",")
        outfile.write(
            str(query_results["results"]["bindings"][len(query_results["results"]["bindings"]) - 1]).replace("'", '"'))
        outfile.write("]")

    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]
        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        coor = [lon_brut,lat_brut,name]
        coordonnee.append(coor)

    print(coor)
    return(coordonnee)

# Query : all the post offices in a city of a specific zip code

def QueryCode_Postal(code, infra):
    query = SPARQLWrapper("http://localhost:3030/" + infra + "/query")
    query.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX j.0: <http://schema.org/>
        SELECT ?lon ?lat ?name
        WHERE {
      		?subject j.0:code_postal """ + code +""".
      		?subject j.0:longitude ?lon.
            ?subject j.0:latitude ?lat.
            ?subject j.0:nom ?name}
    """)
    query.setReturnFormat(JSON)
    query_results = query.query().convert()
    coordonnee = []

    # Export file
    with open('output_poste-office-'+code+'.jsonld', 'w+') as outfile:
        outfile.write("[")
        for i in range(len(query_results["results"]["bindings"]) - 1):
            outfile.write(str(query_results["results"]["bindings"][i]).replace("'", '"') + ",")
        outfile.write(
            str(query_results["results"]["bindings"][len(query_results["results"]["bindings"]) - 1]).replace("'", '"'))
        outfile.write("]")

    for i in range(len(query_results["results"]["bindings"])):
        name = query_results["results"]["bindings"][i]["name"]["value"]

        lon_brut = (query_results["results"]["bindings"][i]["lon"]["value"])
        lat_brut = (query_results["results"]["bindings"][i]["lat"]["value"])

        for i in range(len(lon_brut)):
            if lon_brut[i] == "E":
                lon_brut = float(lon_brut[:i])
                break
        for i in range(len(lat_brut)):
            if lat_brut[i] == "E":
                lat_brut = float(lat_brut[:i])
                break

        lon_brut = float(lon_brut)
        lat_brut = float(lat_brut)
        coor = [lon_brut, lat_brut, name]
        coordonnee.append(coor)

    return (coordonnee)
###########################################################################################################



#===========================================================================================================
#Static Option of School
#===========================================================================================================
@app.route("/Lyon")
def baseLyon():

    coordonneeEcoleSup = QueryCity2("Lyon", "EcoleSup")

    # this is base map
    map = folium.Map(
        location=[45.75801,4.8001016],
        zoom_start=12
    )

    for i in range(len(coordonneeEcoleSup)):
        folium.Marker(
            location=[coordonneeEcoleSup[i][1], coordonneeEcoleSup[i][0]],
            popup=coordonneeEcoleSup[i][2],
            icon=folium.Icon(color='red')
        ).add_to(map)


    return map._repr_html_()


@app.route("/Lille")
def baseLille():

    coordonneeEcoleSup = QueryCity2("Lille", "EcoleSup")

    # this is base map
    map = folium.Map(
        location=[50.6311167,3.0121411],
        zoom_start=12
    )

    for i in range(len(coordonneeEcoleSup)):
        folium.Marker(
            location=[coordonneeEcoleSup[i][1], coordonneeEcoleSup[i][0]],
            popup=coordonneeEcoleSup[i][2],
            icon=folium.Icon(color='red')
        ).add_to(map)


    return map._repr_html_()


@app.route("/Bordeaux")
def baseBordeaux():

    coordonneeEcoleSup = QueryCity2("Bordeaux", "EcoleSup")

    # this is base map
    map = folium.Map(
        location=[44.8637834,-0.6211603],
        zoom_start=12
    )

    for i in range(len(coordonneeEcoleSup)):
        folium.Marker(
            location=[coordonneeEcoleSup[i][1], coordonneeEcoleSup[i][0]],
            popup=coordonneeEcoleSup[i][2],
            icon=folium.Icon(color='red')
        ).add_to(map)



    return map._repr_html_()



@app.route("/Paris")
def baseParis():

    coordonneeEcoleSup = QueryCity2("Paris", "EcoleSup")

    # this is base map
    map = folium.Map(
        location=[48.8589507,2.2770205],
        zoom_start=12
    )

    for i in range(len(coordonneeEcoleSup)):
        folium.Marker(
            location=[coordonneeEcoleSup[i][1], coordonneeEcoleSup[i][0]],
            popup=coordonneeEcoleSup[i][2],
            icon=folium.Icon(color='blue')
        ).add_to(map)



    return map._repr_html_()

#===========================================================================================================
#Static Option of Velib
#===========================================================================================================

@app.route("/Velib")
def baseVelib():
    coordonneeVelib = QueryVelib()

    # this is base map
    map = folium.Map(
        location=[48.8589507, 2.2770205],
        zoom_start=12
    )

    for i in range(len(coordonneeVelib)):
        folium.Marker(
            location=[coordonneeVelib[i][1], coordonneeVelib[i][0]],
            popup=coordonneeVelib[i][2] + "\nCapacity: " + coordonneeVelib[i][3],
            icon=folium.Icon(color='green')
        ).add_to(map)

    return map._repr_html_()

#===========================================================================================================
#Static Option of Gares
#===========================================================================================================
@app.route("/Gares")
def baseGare():
    coordonneeGare = QueryGare()


    # this is base map
    map = folium.Map(
        location=[48.8589507, 2.2770205],
        zoom_start=12
    )

    for i in range(len(coordonneeGare)):
        folium.Marker(
            location=[coordonneeGare[i][1], coordonneeGare[i][0]],
            popup=coordonneeGare[i][2]+" "+coordonneeGare[i][3],
            icon=folium.Icon(color='red')
        ).add_to(map)


    return map._repr_html_()


################################################################
#BONUS
################################################################

#===========================================================================================================
#Dynamic Option of Gares - given a lines
#===========================================================================================================
@app.route("/Gares/ligne", methods=['POST'])
def baseGareLigne():
    line = str(request.form['x2'])
    coordonneeGare = QueryGareLigne(line)


    # this is base map
    map = folium.Map(
        location=[48.8589507, 2.2770205],
        zoom_start=12
    )

    for i in range(len(coordonneeGare)):
        folium.Marker(
            location=[coordonneeGare[i][1], coordonneeGare[i][0]],
            popup=coordonneeGare[i][2]+" "+line,
            icon=folium.Icon(color='red')
        ).add_to(map)


    return map._repr_html_()



#===========================================================================================================
#Dynamic Option of Post offices - given a zipcode
#===========================================================================================================
@app.route("/Postes", methods=['POST'])
def basePostes():
    cp=str(request.form['x1'])

    coordonneePoste = QueryCode_Postal(cp, "Postes")


    # this is base map
    map = folium.Map(
        location=[46.6043207, 2.533633],
        zoom_start=6
    )


    for i in range(len(coordonneePoste)):
        folium.Marker(
            location=[coordonneePoste[i][1], coordonneePoste[i][0]],
            popup=coordonneePoste[i][2],
            icon=folium.Icon(color='green')
        ).add_to(map)

    return map._repr_html_()



@app.route("/Paris/University/Mobility")
def baseVelibGareUni():
    coordonneeGare = QueryGare()
    coordonneeVelib =QueryVelib()
    coordonneeEcoleSup = QueryCity("Paris", "EcoleSup")

    # this is base map
    map = folium.Map(
        location=[48.8589507, 2.2770205],
        zoom_start=12
    )

    for i in range(len(coordonneeGare)):
        folium.Marker(
            location=[coordonneeGare[i][1], coordonneeGare[i][0]],
            popup=coordonneeGare[i][2]+" "+coordonneeGare[i][3],
            icon=folium.Icon(color='red')
        ).add_to(map)

    for i in range(len(coordonneeEcoleSup)):
        folium.Marker(
            location=[coordonneeEcoleSup[i][1], coordonneeEcoleSup[i][0]],
            popup=coordonneeEcoleSup[i][2],
            icon=folium.Icon(color='blue')
        ).add_to(map)

    for i in range(len(coordonneeVelib)):
        folium.Marker(
            location=[coordonneeVelib[i][1], coordonneeVelib[i][0]],
            popup=coordonneeVelib[i][2]+" "+coordonneeVelib[i][3],
            icon=folium.Icon(color='green')
        ).add_to(map)

    return map._repr_html_()




@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)