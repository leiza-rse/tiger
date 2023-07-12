__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2023, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "beta"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@leiza.de"
__status__ = "beta"
__update__ = "2023-07-11"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib
import sys
import hashlib

# set UTF8 as default
importlib.reload(sys)
print("*****************************************")

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# set paths
file_name = "CA2MapBritannia.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))
file_in = dir_path.replace("\\py", "\\src") + "\\" + file_name

# read csv file
data = pd.read_csv(
    file_in,
    encoding='utf-8',
    sep='|',
    usecols=['id', 'site', 'lon', 'lat', 'x', 'y', 'norm', 'hex'],
    na_values=['.', '??', 'NULL']  # take any '.' or '??' values as NA
)
print(data.info())

# create triples from dataframe
lineNo = 2
outStr = ""
lines = []
ids = []
for index, row in data.iterrows():
    # print(lineNo)
    tmpno = lineNo - 2
    if tmpno % 1000 == 0:
        print(tmpno)
    lineNo += 1

    # site metadata
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "rdf:type" + " lado:Location .")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "rdf:type" + " lado:DiscoverySite .")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "rdf:type" + " lado:TiGeR_Event .")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "lado:hasType" + " lado:DiscoverySite .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "rdfs:label" +
                 " " + "'" + str(row['site']).replace('\'', '`') + "'@en" + ".")
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "dc:identifier" + " " + "" + str(row['id']) + "" + ".")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "lado:tiger_eventname" +
                 " " + "'" + str(row['site']).replace('\'', '`') + "'@en" + ".")
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "lado:tiger_id" + " " + "" + str(row['id']) + "" + ".")
    ids.append(str(row['id']))

    # geom
    point = "POINT(" + str(float(row['lon'])) + \
        " " + str(float(row['lat'])) + ")"
    point = "\"<http://www.opengis.net/def/crs/EPSG/0/4326> " + \
        point + "\"^^geosparql:wktLiteral"
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "geosparql:hasGeometry" + " samian:loc_ds_" + str(row['id']) + "_geom .")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + "_geom " + "rdf:type" + " sf:Point .")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + "_geom " + "geosparql:asWKT " + point + ".")

    # correspondance analysis result
    x4 = round(float(str(row['x'])), 4)
    y4 = round(float(str(row['y'])), 4)
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "lado:tiger_cax" + " " + str(x4) + ".")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "lado:tiger_cay" + " " + str(y4) + ".")
    norm01 = float(str(row['norm'])) / 100
    norm01 = round(norm01, 5)
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "lado:tiger_cax_norm" + " " + str(norm01) + ".")
    lines.append("samian:loc_ds_" +
                 str(row['id']) + " " + "lado:tiger_cax_hex" + " \'" + str(row['hex']) + "\' .")

    # license
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "dct:license" +
                 " <" + "https://creativecommons.org/licenses/by/4.0/deed.de" + "> .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "dct:creator" +
                 " <" + "https://orcid.org/0000-0002-3246-3531" + "> .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "dct:rightsHolder" +
                 " <" + "https://orcid.org/0000-0002-3246-3531" + "> .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " + "dct:rightsHolder" +
                 " <" + "https://orcid.org/0000-0002-7634-5342" + "> .")

    # prov-o
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "prov:wasAttributedTo" + " samian:ImportPythonScript_TiGerR .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "prov:wasDerivedFrom" + " <http://www.wikidata.org/entity/Q90412636> .")
    lines.append("samian:loc_ds_" + str(row['id']) + " " +
                 "prov:wasGeneratedBy" + " samian:activity_loc_ds_" + str(row['id']) + " .")
    lines.append("samian:activity_loc_ds_" +
                 str(row['id']) + " " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("samian:activity_loc_ds_" +
                 str(row['id']) + " " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("samian:activity_loc_ds_" + str(row['id']) + " " + "prov:endedAtTime '" +
                 datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("samian:activity_loc_ds_" + str(
        row['id']) + " " + "prov:wasAssociatedWith" + " samian:ImportPythonScript_TiGerR .")

    lines.append("")

# Allen after
i = 0
while i < len(ids)-1:
    #print(ids[i] + ">" + ids[i+1])
    lines.append("samian:loc_ds_" + str(ids[i]) + " " +
                 "time:intervalBefore" + " " + "samian:loc_ds_" + str(ids[i+1]) + ".")
    i = i + 1


files = (len(lines) / 100000) + 1
print("triples", len(lines), "files", int(files))
thiscount = len(lines)

# write output files
f = 0
step = 100000
prefixes = ""
prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
prefixes += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\r\n"
prefixes += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
prefixes += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
prefixes += "@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\r\n"
prefixes += "@prefix dc: <http://purl.org/dc/elements/1.1/> .\r\n"
prefixes += "@prefix dct: <http://purl.org/dc/terms/> .\r\n"
prefixes += "@prefix sf: <http://www.opengis.net/ont/sf#> .\r\n"
prefixes += "@prefix prov: <http://www.w3.org/ns/prov#> .\r\n"
prefixes += "@prefix lado: <http://archaeology.link/ontology#> .\r\n"
prefixes += "@prefix samian: <http://data.archaeology.link/data/samian/> .\r\n"
prefixes += "@prefix time: <http://www.w3.org/2006/time#> .\r\n"
prefixes += "\r\n"

for x in range(1, int(files) + 1):
    strX = str(x)
    filename = dir_path.replace("\\py", "\\rdf") + \
        "\\" + file_name.replace(".csv", "") + ".ttl"
    file = codecs.open(filename, "w", "utf-8")
    file.write("# create triples from " + file_name + " \r\n")
    file.write(
        "# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print(" > " + file_name.replace(".csv", "") + ".ttl")
    file.close()

print("*****************************************")
print("SUCCESS: closing script")
print("*****************************************")
