import csv
from csvw.dsv import UnicodeDictReader
import re


output = [[
    "ID", "Language_ID", "Parameter_ID", "Value", "Certainty", "Comment", "Source", "Year"
]]

with UnicodeDictReader("gata_raw.csv", delimiter=',') as reader:
    for line in reader:
        ref = line["Reference"]

        if " y pp. " in ref:
            ref = str.replace(ref, " y pp. ", ",")

        if "pp. " in ref:
            ref = str.replace(ref, "pp. ", "")

        elif re.search("[0-9]*:", ref):
            ref = re.split("[0-9]*:", ref)[1]
            ref = str.replace(ref, ")", "")
            # print(ref)

        elif "pp" in ref:
            ref = str.replace(ref, "pp.", "")
            ref = str.replace(ref, "pp", "")
            ref = str.replace(ref, " ", "")

        elif "De Oliveira" in ref:
            ref = str.replace(ref, "De Oliveira (", "")
            ref = str.replace(ref, ")", "")
            # print(ref)

        elif re.search("[A-Z]", ref):
            ref = ""

        if ref != "":
            line["Source"] = line["Source"] + "[" + ref + "]"

        output.append([
            line["ID"],
            line["Language_ID"],
            line["Parameter_ID"],
            line["Value"],
            line["Certainty"],
            line["Comment"],
            line["Source"],
            line["Year"]
        ])

    with open('out.csv', 'w', encoding="utf8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerows(output)
