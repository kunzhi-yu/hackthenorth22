import warnings

import cohere
import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from datasets import load_dataset

import app.db as db
from _cohere import messages_text_clustering

api_key = "j2yWHE4mlHBic6pUwKCGCZbeg1hfHp6xWBi7xBfs"

def task_ranking_job(messages, tasks):
    warnings.filterwarnings('ignore')
    pd.set_option('display.max_colwidth', None)

    # Paste your API key here. Remember to not share publicly
    # Create and retrieve a Cohere API key from os.cohere.ai
    co = cohere.Client(api_key)

    # Get dataset
    dataset = load_dataset("trec", split="train")

    # Import into a pandas dataframe, take only the first 1000 rows
    df = pd.DataFrame(dataset)[:1000]

    embeds = co.embed(texts=list(df['text']),
                    model="large",
                    truncate="LEFT").embeddings
    # Check the dimensions of the embeddings
    embeds = np.array(embeds)

    # Create the search index, pass the size of embedding
    search_index = AnnoyIndex(embeds.shape[1], 'angular')
    # Add all the vectors to the search index
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])

    search_index.build(10) # 10 trees
    search_index.save('test.ann')

    # with open("_cohere/_chat.txt", "r") as f:
    #         everything = f.read()
    #         queries = initial_processing.process_chat(everything)
    queries = messages_text_clustering.process_chat(messages)
    queries = list(queries.values())
    # Get the query's embedding
    chat_topics = {}
    for query in queries:
        query_embed = co.embed(texts=[query],
                        model="large",
                        truncate="LEFT").embeddings

        # Retrieve the nearest neighbors
        similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
                                                        include_distances=True)
        # Format the results
        results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'], 
                                    'distance': similar_item_ids[1]})


        # print(f"Query:'{query}'\nNearest neighbors:")

        #print(list(results["texts"]), list(results["distance"]))
        chat_topics[query] = list(results["texts"])#list(zip(results["texts"], results["distance"]))

    # now taking in the database of tasks and stuff:
    lines = [f"{i[0]}\n{i[1]}" for i in tasks]
    print(lines)
    topic_rankings = []
    for topic in lines:
        #print("                                                              ")
        query_embed = co.embed(texts=[topic],
                    model="large",
                    truncate="LEFT").embeddings

        # Retrieve the nearest neighbors
        similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
                                                        include_distances=True)
        # Format the results
        results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'], 
                                    'distance': similar_item_ids[1]})


        #print(f"Query:'{topic}'\nNearest neighbors:")

        #print(list(results["texts"]), list(results["distance"]))
        rando_list = []
        for idx, text in enumerate(results["texts"]): # list of all sentences tasks were mapped to in order of distance too
            overall_score = 0
            for chat_topic in chat_topics:
                texts = chat_topics[chat_topic] # the list of all sentences the chat topic groups were mapped to in order of distance
                try:
                    #print("OII", texts)
                    otherindex = texts.index(text)
                except:
                    otherindex = 10
                #print(abs(idx - otherindex), idx, otherindex)
                overall_score -= abs(idx - otherindex)
            rando_list += [(overall_score + len(set.intersection(set(results["texts"]), set(texts))), text)]
            #print("RANDO ", rando_list)
        topic_rankings += [(max(rando_list)[0], topic)] # the maxiumum score this todo topic has
        #print("MAIN", topic_rankings)

    final_rankings = [tup[1] for tup in sorted(topic_rankings, key=lambda x: x[0])]
    return [string.split("\n")[0] for string in final_rankings]

def main_sent_extract(all_messages, ids):
    id_to_tasks = {}
    records = db.get_all_db()
    ids = [i["id"] for i in records]
    for i in list(set(ids)):
        if i in ids:
            tasks = [[k['title'], k['description']] for k in records if k["id"].strip("\n").strip() == i]
            ranked_tasks = task_ranking_job(all_messages, tasks)
            id_to_tasks[i] = list(set(ranked_tasks))
    task_list = []
    for i in list(id_to_tasks.values()):
        for j in i:
            task_list += [k for k in records if k["title"] == j]
    return task_list






if __name__ == "__main__":

    print("bruh")

#similarity score calculation:
"""
the idea is how similar are conversation to topics. the reference is topic
amount of set intersection  - summation of difference in index of item in topic with index of item in conversation category (if not present the index of the item in coversation category is 10)

each topic then has similarity scores to each of the conversation categories. (rank based on summation of these scores:)
"""   



"""
Things we are doing here:
we have a set of tasks from the database - strings essentially
we also have a bunch of texts from discord.

what we do: 
the text from discord - cluster them and make them into groups.
the groups we will make them all like one string and then they will be compared against the main dataset
the database of tasks will also be compared against the main dataset. 
the things that have an order of similarity in the groupings of the main dataset are matched together.
"""
