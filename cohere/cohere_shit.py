import cohere
import pandas as pd
import requests
import datetime
from tqdm import tqdm
pd.set_option('display.max_colwidth', None)

co = cohere.Client('M6me67HOZMMJsVSq2l0102rcX9Xxe2iwfi8cl0wt')

# prompts = [("Find new times for the UG meeting", "Elexandra Tran ResearchAward: Hey alex, can you find new times for the UG meeting based on tiny.cc/iaischedule? give me the best 3 time options there are"),
#            ("None", "Alex Yu: yes yes. I'll lyk after I get out of class"),
#            ("None", "no rush - we just need to determine the new time by Saturday"),
#            ]


response = co.generate(
    model='large',
    prompt='Find all the To-Do items for Alex Yu in the following conversation. \n[13:59, 9/14/2022] Elexandra Tran ResearchAward: Hey alex, can you find new times for the UG meeting based on tiny.cc/iaischedule? give me the best 3 time options there are\n[14:06, 9/14/2022] Alex Yu: yes yes. I\'ll lyk after I get out of class\n[14:06, 9/14/2022] Elexandra Tran ResearchAward: no rush - we just need to determine the new time by Saturday\n[12:59, 9/14/2022] Elexandra Tran ResearchAward: What is tNhe difference between skim and 2% milk?\n[14:06, 9/14/2022] Alex Yu: I\'m at a hackathon rn. Remind me to tell you later.\n[14:06, 9/14/2022] Elexandra Tran ResearchAward: Okay\nTo-Do: Find new times for the UG meeting by Saturday, Remind me to explain what the difference between skim and 2% milk to Elexandra.\n--\nFind all the To-Do items for Alex Yu in the following conversation. \n[12:57, 9/15/2022] Joseph Williams: Congratulations on CHI everyone!\n[12:59, 9/15/2022] Joseph Williams: @Alex Yu @Huayin Luo Volunteer can you all add into adint.ca/chigoto pdf of every submitted CHI paper, create adint.ca/ links to them starting with p?\nTo-Do: Add a pdf of every submitted CHI paper.\n--\nFind all the To-Do items for Alex Yu in the following conversation. \n[12:14, 9/15/2021] Mishaal Kandapath: Good morning I need help with tasks.\n[12:17, 9/15/2021] Mishaal Kandapath: @Alex Yu take out the trash.\n[12:14, 9/15/2021] Alex Yu: Fine.\n[12:17, 9/15/2021] Mishaal Kandapath: Can @Alex Yu check the finance spreadsheet at the end of today?\n[12:19, 9/15/2021] Alex Yu: Sounds good! \nTo-Do: Take out the trash, Check the finance spreadsheet at the end of today.\n--\nFind all the To-Do items for Alex Yu in the following conversation. \n2022-09-17, 11:00 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n2022-09-17, 11:00 - Alex Yu: Hi\n2022-09-17, 11:01 - Ricky Liu: How\'s it going\n2022-09-17, 11:02 - Alex Yu: it\'s going well! how\'s your piano going?\n2022-09-17, 11:02 - Ricky Liu: I recently took my last RCM exam! hbu?\n2022-09-17, 11:03 - Alex Yu: wow congrats!\n2022-09-17, 11:03 - Alex Yu: I want to practice 1 hour a day this week to get better\n2022-09-17, 11:03 - Alex Yu: and be just like you\n2022-09-17, 11:04 - Ricky Liu: You got this!\n2022-09-17, 11:06 - Alex Yu: do you want to grab lunch sometime?\n2022-09-17, 11:06 - Ricky Liu: sure\n2022-09-17, 11:06 - Ricky Liu: I\'ll let you know when I have time on my lunch break\n2022-09-17, 11:06 - Alex Yu: Sounds good\nTo-Do: ',
    max_tokens=20,
    temperature=0.6,
    k=0,
    p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["--"],
    return_likelihoods='NONE')
print('Prediction: {}'.format(response.generations[0].text))
#
# class cohereExtractor():
#     def __init__(self, examples, example_labels, labels, task_desciption, example_prompt):
#         self.examples = examples
#         self.example_labels = example_labels
#         self.labels = labels
#         self.task_desciption = task_desciption
#         self.example_prompt = example_prompt
#
#     def make_prompt(self, example):
#         examples = self.examples + [example]
#         labels = self.example_labels + [""]
#         return (self.task_desciption +
#                 "\n---\n".join( [examples[i] + "\n" +
#                                  self.example_prompt +
#                                  labels[i] for i in range(len(examples))]))
#
#     def extract(self, example):
#         extraction = cohere.generate(
#             model='large',
#             prompt=self.make_prompt(example),
#             max_tokens=10,
#             temperature=0.1,
#             stop_sequences=["\n"])
#         return(extraction.generations[0].text[:-1])
#
#
# cohereMovieExtractor = cohereExtractor([e[1] for e in examples],
#                                        [e[0] for e in examples], [],
#                                        "", "")
#
# results = []
# for text in tqdm([]):
#     try:
#         extracted_text = cohereMovieExtractor.extract(text)
#         results.append(extracted_text)
#     except Exception as e:
#         print('ERROR: ', e)
#
# from concurrent.futures import ThreadPoolExecutor
#
# test_df = pd.read_csv('somecsv',index_col=0)
#
# extracted = []
# # Run the model to extract the entities
# with ThreadPoolExecutor(max_workers=8) as executor:
#     for i in executor.map(cohereMovieExtractor.extract, test_df['text']):
#         extracted.append(str(i).strip())
# # Save results
# test_df['extracted_text'] = extracted
