import ExtractData


values = ExtractData.generateValues(df=ExtractData.df)


def writeToFile(values):
    with open("data.txt", "w", encoding='utf-8') as dataFile:
        for (key, values) in values.items():
            dataFile.write(f"{key}: \n")
            for value in values:
                dataFile.write(f"{value}: {values[value]}\n")
            print('\n')


writeToFile(values)
