#Hack the North 2022 Submission
## Inspiration
Everyone has a list of ideas that we forget about or conversations we wish we could remember. Organizing reminders or tasks for far flung reaches of the internet is a pain. With so little time, how can we achieve our small, but important, goals in life?

## What it does
The functionality of our discord bot is twofold. 
1. Suggests and saves tasks in your conversations (let's get dinner sometime).
2. From suggested tasks and manually added tasks, the bot suggests tasks based off your current interests.

## How we built it
**Front End**: Python, Discord API, Flask.

**Back End**:  **Co:Here API**, Python, NumPy, Pandas,  PostGreSQL, bit.io.

## Challenges we ran into
We spent a lot of time discussing the user design. Since the to-do list was made to remove the trouble of remembering to do tasks, we wanted it to be as easy to use as possible. However, we are happy that we spent the time debating because it implied our product development and allowed us to produce the best work.

## Accomplishments that we're proud of
We're extremely proud of the machine learning engineering that went into our application. We used the co:here API **four** times!! First, it was used to determine if a group of messages were a task. This involved using co:here's chat summarization API, which we optimized using prompt engineering. A difficulty we ran into was that the bot got confused when there was chat spam. Thus, we used a classification model in co:here to identify spam. We used unsupervised clustering and Annoy algorithm to identify a category a conversation was in and what conversations were similar to a task. 

## What we learned
We learned a lot about natural language processing. It was our first time using co:here's API, which we found to be easy to use and allowed use to spend more time on the design rather than implementation.

## What's next for Adaptive To-Do List 
**1. Integration with Google / Apple / Outlook Calendar**: Allow users to add an task, reminder, or event on their personal calendar. The personal calendar can also give the AI a better idea of what tasks to suggest! 
**2. Try making it into a mobile app**: Make a mobile app version that is able to read messages from multiple messaging platforms.
