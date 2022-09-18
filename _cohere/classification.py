import cohere
from cohere.classify import Example


def classifyPrediction(tasks):
    co = cohere.Client('U3iaLJOqWedYQl7Rmj5uUBGIjL6U05OwLABV8A7N')

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
    #print(response)

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


def classifyPredictionSpam(tasks):
    import cohere
    co = cohere.Client('U3iaLJOqWedYQl7Rmj5uUBGIjL6U05OwLABV8A7N')
    response = co.classify(
        model='large',
        inputs=tasks,
        examples=[Example("Elon Musk says Twitter Blue subscribers should be able to pay with dogecoin", "Not Tasks"),
                  Example("Probability of a US recession in the next 12 months, via WSJ", "Not Tasks"),
                  Example("How was your weekend?", "Tasks"), Example("NASDAQ rises 2% to ATH", "Not Tasks"),
                  Example("Did you know that FTX Founder is one of the world\'s richest crypto billionaires?",
                          "Not Tasks"),
                  Example("Sweet Potato Macaroni Cheese is #RecipeOfTheDay, and I’m very happy about it!", "Not Tasks"),
                  Example("3-Ingredient Slow Cooker recipes", "Not Tasks"),
                  Example("This is by far the BEST biscuit recipe I’ve ever tried", "Not Tasks"),
                  Example("Baking my first loaf of banana bread...", "Not Tasks"),
                  Example("From the queen of Italian cooking, this is one of the most iconic tomato sauce recipes ever",
                          "Not Tasks"), Example("I want to read Rice and Men", "Tasks"),
                  Example("I want to watch Today’s Daily Cartoon", "Tasks"), Example(
                "Get a glimpse of the stage adaptation of Hayao Miyazaki’s 2001 Oscar-winning animated feature Spirited Away",
                "Tasks"), Example("The #Banksy Exhibit in Cambridge, MA is absolutely terrific. You should watch it!!",
                                  "Tasks"),
                  Example("“A Whisper in Time” large abstract paining 48’ x 48’", "Not Tasks"),
                  Example("0589127941", "Spam"), Example("Hello Alex, please find the median in a datastream", "Tasks"),
                  Example("Can you take out the trash?", "Tasks"), Example("Buy tea from Loblaws", "Tasks"),
                  Example("Add 3 pdfs to website before tomorrow evening.", "Tasks"),
                  Example("Thanks for attending my party!", "Not Tasks"),
                  Example("Attend party at Liam\'s house on Sunday", "Tasks"),
                  Example("Hi Alex, the fridge needs to be cleaned", "Tasks"),
                  Example("I will be very angry if you don\'t get me this paper done by tomorrow.", "Tasks"),
                  Example("Help me pack my ski gear tonight", "Tasks"),
                  Example("Can you find a new meeting time for UGs on Tuesdays?", "Tasks"),
                  Example("Thank you so much for the gift", "Not Tasks"), Example("Find a gift for boyfriend", "Tasks"),
                  Example("Congratulations to all of this years @OliverAwards winners!", "Not Tasks"),
                  Example("efwaefw gergaerg343498qhoil", "Spam"),
                  Example("we09jio3r2 io9685r7tfughgudytghjkuyu", "Spam"), Example("g", "Spam"),
                  Example("ukjf", "Spam"), Example("1t4", "Spam")])

    goodtasks = []
    length = len(response.classifications)

    for i in range(length):
        try:
            task = response.classifications[i].input
            #print(response.classifications[i])
            values = [k.confidence for k in response.classifications[i].confidence]
            max_val = max([k.confidence for k in response.classifications[i].confidence])
            category = response.classifications[i].confidence[values.index(max_val)].label
            #print(category)
            if category == "Tasks" and max_val > 0.5:

                goodtasks.append(task)
        except IndexError:
            pass

    return goodtasks
