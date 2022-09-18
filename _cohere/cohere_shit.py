import cohere
import pandas as pd
pd.set_option('display.max_colwidth', None)

def gettasks(prompt, name):
    co = cohere.Client('geaFySoqp5B8hvybxEjMPQ5dW6T0JO8CPjijQo92')
    shit = "This finds a list of tasks from a conversation. \n[12:14, 9/15/2021] Mishaal Kandapath: Good morning I need help with tasks.\n[12:17, 9/15/2021] Mishaal Kandapath: @Alex Yu take out the trash.\n[12:14, 9/15/2021] Alex Yu: Fine.\n[12:17, 9/15/2021] Mishaal Kandapath: Can @Alex Yu check the finance spreadsheet at the end of today?\n[12:19, 9/15/2021] Alex Yu: Sounds good! \nTasks: Take out the trash, Check the finance spreadsheet at the end of today.\n--\n2022-09-17, 11:00 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n2022-09-17, 11:00 - Alex Yu: Hi\n2022-09-17, 11:01 - Ricky Liu: How\'s it going\n2022-09-17, 11:02 - Alex Yu: it\'s going well! Can you please check the weather?\n2022-09-17, 11:02 - Ricky Liu: Yes.\n2022-09-17, 11:03 - Alex Yu: Thanks. Can you find the median in a datastream?\n2022-09-17, 11:05 - Ricky: Of course.\n2022-09-17, 11:03 - Alex Yu: Great work. Make sure to iron your clothes by tonight.\n2022-09-17, 11:05 - Ricky: Yessir.\nTasks: Check the weather, Find the median in a datastream, Iron clothes by tonight.\n--\n2022-09-17, 11:00 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.\n2022-09-17, 11:00 - Alex Yu: Hi\n2022-09-17, 11:01 - Ricky Liu: How\'s it going\n2022-09-17, 11:02 - Alex Yu: it\'s going well! how\'s your piano going?\n2022-09-17, 11:02 - Ricky Liu: I recently took my last RCM exam! hbu?\n2022-09-17, 11:03 - Alex Yu: wow congrats!\n2022-09-17, 11:03 - Alex Yu: I want to practice 1 hour a day to improve\n2022-09-17, 11:04 - Ricky Liu: You got this!\n2022-09-17, 11:06 - Alex Yu: How has California been?\n2022-09-17, 11:06 - Ricky Liu: I\'m actually coming back in town soon.\n2022-09-17, 11:06 - Alex Yu: We should get lunch sometime when you come back.\n2022-09-17, 11:08 - Ricky Liu: YES we should. \nTask: Practice 1 hour a day, Get lunch with Ricky Liu when he comes back.\n--\n2022-09-17, 13:06 - Alex Yu: wefearhgeh hEEGRGDd 567\n2022-09-17, 14:06 - Ricky Liu: Iwafawfaqr23432wj;enjjf I FWEfannf124\n2022-09-17, 15:06 - Alex Yu: \]\]-=2394))(#*&\n2022-09-17, 18:10 - Ricky Liu: qwr23rfew\nTask: None\n--\n2022-09-17, 11:06 - Alex Yu: w5tsrg\n2022-09-17, 11:06 - Ricky Liu: Isergsegsergeg444\nTask: None\n--\n"
    shit += f"Find all the To-Do items for {str(name)} in the following conversation. \n {str(prompt)}\nTo-Do: "
    response = co.generate(
        model='large',
        prompt=shit,
        max_tokens=40,
        temperature=0.8,
        k=1,
        p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["--"],
        return_likelihoods='NONE')
    # print('Prediction: {}'.format(response.generations[0].text))
    # print(response.generations[0].text)
    tasks = response.generations[0].text.strip("\\n--").split(",")
    for i in tasks:
        i.strip("\\n").strip(" ")
    # print(tasks)

    return tasks
