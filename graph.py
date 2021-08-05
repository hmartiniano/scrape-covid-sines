import os
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
df = df.drop(columns=["dia", "mes", "ano"])
df = df[["data"] + [col for col in df.columns if col != "data"]]
df.to_csv("data/table.csv", index=False)

df2 = pd.melt(df, id_vars="data",
             value_vars=[col for col in df.columns if col != "data"],
             value_name="casos", var_name="tipo")
df2.casos = df2.casos.astype(int)
print(df2.head())
print(df2.dtypes)
lp = sns.lineplot(data=df2, x="data", y="casos", hue="tipo")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time-series.png', dpi=300)



with open("README.md", "w") as f:
    f.write("## graph\n\n![](time-series.png)\n\n##Last 15 data points.\n\n")
    df["data"] = df["data"].dt.strftime('%d-%m-%Y')
    df.tail(15).to_markdown(f, index=False)

