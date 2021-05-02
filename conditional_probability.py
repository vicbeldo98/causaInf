import pandas as pd
csv_path = './LUCAS-EXAMPLE/lucas.csv'
df = pd.read_csv(csv_path)
print(df.groupby('Smoking').Lung_Cancer.value_counts())
