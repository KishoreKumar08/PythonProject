# from collections import OrderedDict
from collections import Counter

para = "\"Data engineering is a critical part of modern analytics. Data engineers build systems that collect, manage, and convert raw data into usable information for data scientists and business analysts. The role requires a deep understanding of databases, data pipelines, and programming skills.\""
paraSplit=para.replace("\"","").replace(",","").replace(".","").lower().split(" ")
count = Counter(paraSplit)
print(count)
count.pop('and')
count.pop('is')
count.pop('the')
print(count)
values = list(count.values())
print(values)
values.sort(reverse=True)
print(values)
topfive = values[:5]
print(topfive)
counter = 0
for i,j in count.items():
    if j in topfive:
        if j == 1:
            topfive.remove(j)
        print(f"{i}:{j}")



