#process the dataset:

from concurrent.futures import process
from gensim.models import Word2Vec
import numpy as np
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import kneed


def process_chat(all_string):
    lines = [line.split(" ") for line in all_string]
    # got a list of all lines, with words in them seperated too:
    m = Word2Vec(sentences=lines, vector_size=50, min_count=1, sg=1)
    l = []
    for line in lines:
        l.append(vectorizer(line, m))
        # print(vectorizer(line, m).shape)
    X = np.array(l)
    wcss = []
    models = []
    for i in range(2, 50):
        kmeans = KMeans(n_clusters = i, init="k-means++" , random_state=42)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        models.append(kmeans)
    # plt.plot(range(2, 50), wcss)
    # plt.show()

    kneedle = kneed.KneeLocator(x=range(2, 50), y=wcss, curve="convex", direction="decreasing", online=True, S=1)
    knee_point = kneedle.elbow
    #print(knee_point)

    main_model = models[knee_point - 2]
    labels = main_model.fit_predict(X)
    label_dict = {}
    for idx, label in enumerate(labels):
        label_dict[label] = label_dict.get(label, "") + " ".join(lines[idx])#label_dict.get(label, []) + [ " ".join(lines[idx])]
    return label_dict

def vectorizer(sent, m):
    vec = []
    numw = 0
    for w in sent:
        try:
            if numw == 0:
                vec = m.wv[w]
            else:
                vec = np.add(vec, m.wv[w])
            numw+=1
        except:
            pass
    return np.asarray(vec)/numw

if __name__ == "__main__":
    with open("_cohere/_chat.txt", "r") as f:
        everything = f.read()
        process_chat(everything)

    
