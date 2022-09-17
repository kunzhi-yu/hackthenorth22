import cohere
import pandas as pd
pd.set_option('display.max_colwidth', None)

def gettasks()
    co = cohere.Client('M6me67HOZMMJsVSq2l0102rcX9Xxe2iwfi8cl0wt')

    with open("prompt") as f:
        prompt = f.readline()
    prompt = prompt.strip()

    response = co.generate(
        model='large',
        prompt=prompt,
        max_tokens=20,
        temperature=0.6,
        k=1,
        p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"],
        return_likelihoods='NONE')

    print('Prediction: {}'.format(response.generations[0].text).strip("\\n--"))


    return
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
