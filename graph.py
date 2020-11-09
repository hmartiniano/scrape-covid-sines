import pandas as pd
import glob
fnames = glob.glob("data/*json")
import json
df = pd.DataFrame([json.load(open(fname)) for fname in fnames])
df["data"] = pd.to_datetime(df.dia.astype(str) + "-" + df.mes.astype(str) + "-"
                            + df.ano.astype(str), format='%d-%m-%Y',)
df = df.sort_values(by="data")
print(df.head())
import seaborn as sns
import matplotlib.pyplot as plt
df = df.drop(columns=["dia", "mes", "ano"])
df = pd.melt(df, id_vars="data", value_vars=["ativos", "recuperados", "obitos"])
df.value = df.value.astype(int)
print(df.head())
print(df.dtypes)
lp = sns.lineplot(data=df, x="data", y="value", hue="variable")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time-series.png', dpi=300)


