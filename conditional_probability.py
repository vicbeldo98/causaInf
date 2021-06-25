import pandas as pd

csv_path = "./MONKEY_SURVEY/data.csv"
df = pd.read_csv(csv_path)
print(df.groupby(["Enfermedad mental","Educación"]).Desempleo.value_counts())
print(df.groupby("Educación").size())
#print(df.groupby(["Desempleo"]).Empleo.value_counts())
print(df.groupby("Hospitalización").size())


