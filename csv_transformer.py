import pandas as pd

df = pd.read_csv("./MONKEY_SURVEY/original_data.csv")
df = df.drop(columns=['I have my own computer separate from a smart phone',
                      'How many days were you hospitalized for your mental illness', 'I have my regular access to the internet', 'Lenght gaps',
                      'Annual income (including any social welfare programs) in USD', 'I read outside of work and school', 'Annual income from social welfare programs',
                      'I receive food stamps', 'I am on section 8 housing', 'How many times were you hospitalized for your mental illness', 'Lack of concentration',
                      'Depression', 'Obsessive thinking', 'Mood swings', 'Panic attacks', 'Compulsive behavior', 'Tiredness', 'Household Income', 'Region', 'Device Type'])
print(df.columns)
df.columns = ['Empleo', 'Enfermedad Mental', 'Educación', 'Hospitalización', 'Discapacidad',
              'Vivir Padres', 'Periodo Sin Trabajar', 'Cobrar Desempleo', 'Ansiedad', 'Edad', 'Género']
mappings = {
    "Male": 0,
    "Female": 1,
    "Completed Masters": 6,
    "Completed Phd": 8,
    "Completed Undergraduate": 1,
    "High School or GED": 4,
    "Some Phd": 7,
    "Some Undergraduate": 2,
    "Some highschool": 3,
    "Some Masters": 5,
    "18-29": 1,
    "30-44": 2,
    "45-60": 3,
    "> 60": 4,
}
print(df.columns)
df = df.replace(["Male", "Female", "Completed Masters", "Completed Phd", "Completed Undergraduate",
                "High School or GED", "Some Phd", "Some Undergraduate", "Some highschool", "Some Masters",
                "18-29", "30-44", "45-60", "> 60"], [0, 1, 6, 8, 1, 4, 7, 2, 3, 5, 1, 2, 3, 4])
df.to_csv('./MONKEY_SURVEY/data.csv', index=False)
print(df.head)
for column in df.columns:
    print(column)
    print(df[column].isnull().values.any())
