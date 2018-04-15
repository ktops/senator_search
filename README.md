# senator_search
206 final project

DATA SOURCES USED:
No API's were used in this project, I simply scraped my information from 3 websites by way of crawling:
      https://www.senate.gov/senators/index.htm
      https://www.senate.gov/senators/ListofWomenSenators.htm
      https://www.senate.gov/senators/EthnicDiversityintheSenate.htm

BRIEF CODE OVERVIEW:
After scraping my pages, I store the data into a Senator class, because all the information is relevant for each senator. My most important functions are the get_senators_from_state(), which allows the user to input a state abbreviation and get back the senators from that state and their information, and my "breakdown" functions, which allow the user to see a plot of things like race, sex, and party differentiation in the current senate based on their input.

USER GUIDE:
When initially starting the program, it will take just a little bit longer than expected to load, but after that, things should move at a normal pace. It will ask for input, and if you type "help" all of your options will appear, along with a description of what they do. In short, you have the option to look up senators by state, see graphs of things like race, sex, and party by state and of the senate as a whole, and you can open the contact page to find out how to directly contact your senator.

Enjoy!
