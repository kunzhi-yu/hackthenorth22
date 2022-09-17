import pandas as pd

things = []
with open("example.txt", "r") as f:
    for line in f:
         things.append(line.split(" - ")[1])

with open("example.csv", "w") as f:
    accum = len(things)
    for i in range(accum):
        f.write(things[i])

#read_file = pd.read_csv('example.txt')


#read_file.to_csv('example.csv', index=None)
