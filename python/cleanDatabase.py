import csv

with open(
    "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseSeperated.csv"
) as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        try:
            startIndex = row[1].index("<think>")
            endIndex = row[1].index("</think>")
            row[1] = row[1][:startIndex] + row[1][endIndex + 8 :]
        except:
            print("substring not found")
        with open(
            "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseClean.csv",
            "+a",
        ) as csvWrite:
            writer = csv.writer(csvWrite)
            writer.writerow(row)
