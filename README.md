# foodie
#### Video Demo:  <https://youtu.be/xy2COcv9lmA>
#### Description:
foodie is an app that was created for people who can never decide where to eat (like me!), as part of the course requirements for [CS50's Introduction to Computer Science](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x). Users can register for an account and save the names of places that they liked eating at, so the next time they are unable to decide where to eat, they will be able to use foodie to randomly generate ideas for them based on their personal saved places.
The design is largely based on PSET 9 of CS50, Finance.
Languages and frameworks used:
* Front end: HTML, CSS, Bootstrap
* Back end: Python, SQL, Flask, Jinja

**application.py** :
This file contains all the Python code that helps the website to run. Flask and Jinja configurations are similar to PSET9. It also configures the CS50 library to use project.db as its database. 
The following routes are included in application.py:
* @/ (default): When logged in, this section routes to the homepage for users and allows them to see the five most recent places that they've saved. If the user is new and has yet to save any places, it renders the new user template which prompts users to get started by saving a place.
* @/add: This section routes to a page where users can add new places that they've liked eating at to their own records. Users can also include the location, description and price of the food.
* @/pick: This section routes to a page that randomly generates ideas for users on where to eat, based on the places that they've saved. Refreshing this page allows for a new idea to be randomly generated.
* @/explore: This section routes to a page where users can explore what others have been saving, if they want to discover places that perhaps they don't know about.
* @/login: This section routes to the login page for users.
* @/logout: This section logs the user out. 
* @/register: This section allows new users to register for an account.

**helpers.py** :
This file contains code that helps the main file, application.py, to run smoothly. Similar to PSET 9, it includes an implementation of apology that renders when an error occurs, for example when a user tries to register with a username that already exists. It also implements login_required so that the main functions of foodie are only accessible to users who have logged in.

**project.db** :
This file contains the database for foodie. It contains two tables: users and entries.
* Users: This table stores users' usernames and passwords.
* Entries: This table stores users' entries. It records their username via their ID, as well as the name, location, description and price of the place they wish to save.

**add.html** :
This file contains the HTML code for the "@/add" route, featuring a form that users can enter input into in order to save a new place to their records.

**apology.html** :
This file contains the HTML code for error messages.

**explore.html** :
This file contains the HTML code for the "@/explore" route. Rather than generating options based on their own saved places, users are able to explore what others have been saving for a change. They are unable to see who saved each place due to privacy concerns, but can see the name, location, description and price of the place. Users can view up to 10 randomized entries from other users and can refresh the page to see more.

**index.html** :
This file contains the HTML code for the "@/" route. This is the homepage where users can see the five most recent places that they've saved. 

**layout.html** :
This file contains the HTML code for the layout of the website, which other templates in the directory use as well. It features a navigation bar from Bootstrap, as well as defines where the main section of each template file should be.

**login.html** :
This file contains the HTML code for the "@/login" route. It is the default page for new and returning users who have yet to log in.

**newuser.html** :
This file contains the HTML code for new users, and redirects from "@/" when the user has yet to save any places.

**pick.html** :
This file contains the HTML code for the "@/pick" route, and randomly brings back an entry that the user has previously saved to generate ideas. Users can refresh the page to generate another idea.

**register.html** :
This file contains the HTML code for the "@/register" route. It allows users to register for a new account.

**styles.css** :
This file contains the CSS code for all web pages.
