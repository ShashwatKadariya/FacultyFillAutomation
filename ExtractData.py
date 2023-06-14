from json import dumps
import pandas as pd
from nepali_unicode_converter.convert import Converter
converter = Converter()
csv_file = './File/faculty.csv'

df = pd.read_csv(csv_file)[1:]
df = df.drop('S.N.', axis=1)


def create_description(value):
    gender, name, degree, university, faculty = value['gender'], value[
        'name'], value['degree'], value['university'], value['faculty']
    vowels = ['a', 'e', 'i', 'o', 'u']
    facultySeperated = faculty.split(",")

    desc = ""

    AnOrAnd = "an" if facultySeperated[0][0].lower() in vowels else "a"
    facultyWording = f'{AnOrAnd} {facultySeperated[0]}' if len(
        facultySeperated) < 2 else f'{AnOrAnd} {facultySeperated[0]} in{ facultySeperated[1]}'

    # if no degree
    if (degree):
        desc = f"{gender}. {name} is {facultyWording}"
        return desc

    desc = f" {gender}. {name} holds a {degree} from {university}. {gender}. {name} is {facultyWording}"
    return desc


def generateValues(df):
    df_length = len(df.index[1:])
    columnValues = [column for column in df.columns]
    columnValues.append("description")
    columnValues.append("nepali_name")
    FinalValue = {}

    for i in range(1, df_length):
        FinalValue[i] = {}
        for j in columnValues[:-2]:
            FinalValue[i][j.lower()] = df.loc[i][j]

        FinalValue[i]["description"] = create_description(FinalValue[i])
        FinalValue[i]["nepali_name"] = converter.convert(FinalValue[i]['name'])
    return FinalValue


Value = generateValues(df=df)
