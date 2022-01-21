import urllib.request
import lxml.html
#import parse
import json
from unicodedata import normalize

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
#cases = html.xpath("/html/body/div[4]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/h3/strong")[0].text_content()
new_cases = html.xpath("//div[@class='writer_text']")[0].text_content()
print(new_cases)
#r = parse.parse(str("Novos casos confirmados: {novos}\nCumulativo novos casos confirmados 14 dias: {novos_cum}\nÍndice de Incidência (*): {incidencia}\nÓbitos (histórico): {obitos}"))
#r = parse.parse("{ativos} casos confirmados ativos{recuperados} casos recuperados{obitos} óbitos", cases)

d = {}
for line in new_cases.split("\r\n"):
    if ":" in line:
        line = normalize("NFKD", line).split(":")
        print(line)
        if line[1] == "":
            #data = parse.parse("Atualização a {dia:d} de {mes} de {ano:d}", line[0])
            tokens = line[0].split(" ")
            print(tokens)
            d["dia"] = int(tokens[2]) 
            d["mes"] = meses[tokens[4]]
            d["ano"] = int(tokens[6])
        else:
            d[line[0]] = int(line[1])      
print(d)

#data.named["mes"] = meses[data.named["mes"]]
#d.update(data.named)
with open("data/{dia:02d}-{mes:02d}-{ano}.json".format(**d), "w") as f:
    json.dump(d, f)


