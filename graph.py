import glob
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


fnames = glob.glob("data/*json")
df = pd.DataFrame([json.load(open(fname)) for fname in fnames])
df["data"] = pd.to_datetime(df.dia.astype(str) + "-" + df.mes.astype(str) + "-"
                            + df.ano.astype(str), format='%d-%m-%Y',)
df = df.sort_values(by="data")
print(df.head())
#df["por 100 mil hab."] = df["ativos"].astype(int) / 13647 * 100000
df = df.drop(columns=["dia", "mes", "ano"])
df2 = pd.melt(df, id_vars="data",
             #value_vars=["ativos", "recuperados", "obitos", "por 100 mil hab."],
             value_vars=["ativos", "recuperados", "obitos"],
             value_name="casos", var_name="tipo")
df2.casos = df2.casos.astype(int)
print(df2.head())
print(df2.dtypes)
lp = sns.lineplot(data=df2, x="data", y="casos", hue="tipo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time-series.png', dpi=300)

for col in ["ativos", "recuperados", "obitos"]:
    df[col] = df[col].astype(int)

df["ativos_novos"] = df["ativos"].diff()
df["recuperados_novos"] = df["recuperados"].diff()
df["obitos_novos"] = df["obitos"].diff()
df["casos_novos"] = df["ativos_novos"] + df["recuperados_novos"] + df["obitos_novos"]

fig = plt.figure()

df = pd.melt(df, id_vars="data",
             #value_vars=["ativos", "recuperados", "obitos", "por 100 mil hab."],
             value_vars=["obitos_novos",
                         "casos_novos"],
             value_name="casos", var_name="tipo")
#df.casos = df.casos.astype(int)
print(df.head())
print(df.dtypes)
lp = sns.lineplot(data=df, x="data", y="casos", hue="tipo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time-series-novos.png', dpi=300)
