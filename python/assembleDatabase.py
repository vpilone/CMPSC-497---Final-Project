import csv

with open(
    "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseSeperated.csv"
) as csvFile:
    reader = csv.reader(csvFile)
    train = True
    writeRow = ["question", "approach"]
    for row in reader:
        writeRow[1] = row[1]
        writeRow[0] = ""
        for section in row[2:]:
            writeRow[0] = writeRow[0] + section
        toWrite = (
            "Given a research question similar to the one in Question, create an Artificial Intelligence Apporach to solve it similar to the one in Approach. \n\nQuestion: "
            + writeRow[1]
            + "\n\nApproach: "
            + writeRow[0]
        )
        toWrite = toWrite.replace("\n", " ")
        toWriteList = [toWrite]
        stringLen = len(toWrite.split(" "))
        block_size = 250
        if stringLen > block_size:
            toWriteList = []
            for i in range(0, stringLen, block_size):
                toWriteList.append(toWrite[i : i + block_size])
        if train:
            train = False
            with open(
                "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTrain.csv",
                "+a",
            ) as csvWrite:
                writer = csv.writer(csvWrite)
                for i in range(len(toWriteList)):
                    writer.writerow([toWriteList[i]])
        else:
            train = True
            with open(
                "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTest.csv",
                "+a",
            ) as csvWrite:
                writer = csv.writer(csvWrite)
                for i in range(len(toWriteList)):
                    writer.writerow([toWriteList[i]])

    ##OLD VERSION WITH Q AND A##
    # for row in reader:
    #     writeRow[1] = row[1]
    #     writeRow[0] = ""
    #     for section in row[2:]:
    #         writeRow[0] = writeRow[0] + section
    #     if train:
    #         train = False
    #         with open(
    #             "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTrain.csv",
    #             "+a",
    #         ) as csvWrite:
    #             writer = csv.writer(csvWrite)
    #             writer.writerow(writeRow)
    #     else:
    #         train = True
    #         with open(
    #             "/Users/vpilone/Documents/Classes SP25/CMPSC 497/Final Project/python/databaseTest.csv",
    #             "+a",
    #         ) as csvWrite:
    #             writer = csv.writer(csvWrite)
    #             writer.writerow(writeRow)
