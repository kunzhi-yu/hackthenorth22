from discord import *
import app.db as db
from _cohere.cohere_semantic_extraction import *

thing = []
with open("t.txt", "r") as f:
    for line in f:
        thing.append((line.split(", ")[0], line.split(",")[1]))
thing1 = []
thing2 = []
for i in thing:

    thing1.append(i[0].strip("\n").strip())
    thing2.append(i[1].strip("\n").strip())
print(main_sent_extract(thing1, thing2))
