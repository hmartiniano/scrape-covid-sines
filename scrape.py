import urllib.request
import lxml.html
import parse
import json

meses = {"janeiro": 1,
         "fevereiro": 2,
         "março": 3,
         "abril": 4,
         "maio": 5,
         "junho": 6,
         "julho": 7,
         "agosto": 8,
         "setembro": 9,
         "outubro": 10,
         "novembro": 11,
         "dezembro": 12,
        }

url = urllib.request.urlopen("https://www.sines.pt/pages/862?news_id=1986")
html = lxml.html.parse(url)
cases = html.xpath("/html/body/div[4]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/h3/strong")[0].text_content()
print(cases)
r = parse.parse("{ativos} casos confirmados ativos{recuperados} casos recuperados{obitos} óbitos", cases)
if r is None:
    r = parse.parse("{ativos} caso confirmado ativo{recuperados} casos recuperados{obitos} óbitos", cases)
print(r.named)

date = html.xpath("/html/body/div[4]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/p[2]/strong")[0].text_content()
print(date)
data = parse.parse("{dia:d} de {mes} de {ano:d}", date)
if data is None:
    data = parse.parse("{dia:d}\xa0de {mes} de {ano:d}", date)
print(data.named)
data.named["mes"] = meses[data.named["mes"]]
data.named.update(r.named)
print(data.named)

with open("data/{dia:02d}-{mes:02d}-{ano}.json".format(**data.named), "w") as f:
    json.dump(data.named, f)


