import cohere
import pandas as pd
pd.set_option('display.max_colwidth', None)

def gettasks():
    co = cohere.Client('M6me67HOZMMJsVSq2l0102rcX9Xxe2iwfi8cl0wt')

    with open("prompt.txt") as f:
        prompt = f.readline()
    # prompt = str(prompt).strip()
    response = co.generate(
        model='large',
        prompt='Find the best fitting task from the list of tasks from the following conversation.\n[12:14, 9/15/2021] Mishaal Kandapath: Good morning I need help with tasks.\n[12:17, 9/15/2021] Mishaal Kandapath: @Alex Yu take out the trash.\n[12:14, 9/15/2021] Alex Yu: Fine.\n[12:17, 9/15/2021] Mishaal Kandapath: Can @Alex Yu check the finance spreadsheet at the end of today?\n[12:19, 9/15/2021] Alex Yu: Sounds good! \nTo-Do: Take out the trash, Check the finance spreadsheet at the end of today.\n--\nFind the best fitting task from the list of tasks from the following conversation.\n2022-09-17, 11:00 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n2022-09-17, 11:00 - Alex Yu: Hi\n2022-09-17, 11:01 - Ricky Liu: How\'s it going\n2022-09-17, 11:02 - Alex Yu: it\'s going well! Can you please check the weather?\n2022-09-17, 11:02 - Ricky Liu: Yes.\n2022-09-17, 11:03 - Alex Yu: Thanks. Can you find the median in a datastream?\n2022-09-17, 11:05 - Ricky: Of course.\n2022-09-17, 11:03 - Alex Yu: Great work. Make sure to iron your clothes by tonight.\n2022-09-17, 11:05 - Ricky: Yessir.\nTo-Do: Check the weather, Find the median in a datastream, Iron clothes by tonight.\n--\nFind all the To-Do items for Alex Yu in the following conversation. \n2022-09-17, 11:00 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n2022-09-17, 11:00 - Alex Yu: Hi\n2022-09-17, 11:01 - Ricky Liu: How\'s it going\n2022-09-17, 11:02 - Alex Yu: it\'s going well! how\'s your piano going?\n2022-09-17, 11:02 - Ricky Liu: I recently took my last RCM exam! hbu?\n2022-09-17, 11:03 - Alex Yu: wow congrats!\n2022-09-17, 11:03 - Alex Yu: I want to practice 1 hour a day to improve\n2022-09-17, 11:04 - Ricky Liu: You got this!\n2022-09-17, 11:06 - Alex Yu: How has California been?\n2022-09-17, 11:06 - Ricky Liu: I\'m actually coming back in town soon.\n2022-09-17, 11:06 - Alex Yu: We should get lunch sometime when you come back.\n2022-09-17, 11:08 - Ricky Liu: YES we should. \nTo-Do:',
        max_tokens=25,
        temperature=0,
        k=1,
        p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"],
        return_likelihoods='NONE')
    print('Prediction: {}'.format(response.generations[0].text))
    tasks = response.generations[0].text.strip("\\n--").split(",")
    print(tasks)

    return tasks
gettasks()
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
