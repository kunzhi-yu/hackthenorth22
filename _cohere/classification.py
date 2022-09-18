import cohere
from cohere.classify import Example


def classifyPrediction(tasks):
    co = cohere.Client('M6me67HOZMMJsVSq2l0102rcX9Xxe2iwfi8cl0wt')

    response = co.classify(
        model='large',
        inputs=tasks,
        examples=[Example("Elon Musk says Twitter Blue subscribers should be able to pay with dogecoin", "Not Task"),
                  Example("Probability of a US recession in the next 12 months, via WSJ", "Not Task"),
                  Example("European futures slide", "Not Task"), Example("NASDAQ rises 2% to ATH", "Not Task"), Example(
                "FTX Founder is one of the world\'s richest crypto billionaires, with a fortune valued at $20 billion.",
                "Not Task"),
                  Example("Sweet Potato Macaroni Cheese is #RecipeOfTheDay, and I’m very happy about it!", "Not Task"),
                  Example("3-Ingredient Slow Cooker recipes", "Not Task"),
                  Example("This is by far the BEST biscuit recipe I’ve ever tried", "Not Task"),
                  Example("Baking my first loaf of banana bread...", "Not Task"),
                  Example("From the queen of Italian cooking, this is one of the most iconic tomato sauce recipes ever",
                          "Not Task"), Example("I want to read Rice and Men", "Task"),
                  Example("Draw a cartoon", "Task"),
                  Example(
                      "Get a glimpse of the stage adaptation of Hayao Miyazaki’s 2001 Oscar-winning animated feature Spirited Away",
                      "Not Task"), Example("The #Banksy Exhibit in Cambridge, MA is absolutely terrific.", "Not Task"),
                  Example("“A Whisper in Time” large abstract paining 48’ x 48’", "Not Task"),
                  Example("Hello Alex, please find the median in a datastream", "Task"),
                  Example("Can you take out the trash?", "Task"), Example("Buy tea from Loblaws", "Task"),
                  Example("Add 3 pdfs to website before tomorrow evening.", "Task"),
                  Example("Thanks for attending my party!", "Not Task"),
                  Example("Attend party at Liam\'s house on Sunday", "Task"),
                  Example("Hi Alex, the fridge needs to be cleaned", "Task"),
                  Example("Get me this paper done by tomorrow.", "Task")])
    print(response)

    goodtasks = []
    length = len(response.classifications)
    for i in range(length):
        try:
            task = response.classifications[i].input
            if response.classifications[i].confidence[0].confidence < 0.65:
                goodtasks.append(task)
        except IndexError:
            pass

    return goodtasks
