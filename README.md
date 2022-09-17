# Hack the North 2022 Submission
# Hack the North 2022 Submission

## Prototype 1
Adaptive to-do list
- You always have things you don't want to do
- Based off your schedule it will recommend you to do things
- For exmaple, if you are busy, it won't give you that many things
- Java app front end. 
	- Set up server first
	- Get an API running
	- API will be client side, 
- Figure out the data structure, so we can
- APP UI
	- Today tomorrow ONLY
		- Suggestions for that
		- When to do and what to do 
	- Side bar see all tasks
	- App makes a post request, server sauces json
		- Type of request
		- Title of task
		- Description
		- Type: display or add in
		- Use mySQL

- Server
	- When the client puts a task they want to do at some point 
		- Name of the task (m)
		- Descprition (optinal, 140 chr cap)
		- Is complete (m deafult is no)
	- Take the calender stuff and the possible tasks,
		- Assign a task that is not complete and a time
		- Shit out an HTML
	- If the time has past and hasn't been marked complete, app asks the server to reassign a time
