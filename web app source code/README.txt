PLEASE NOTE: The source codes provided in this folder cannot be run as is. These source codes were included only to provide some proof of our work. To run this locally would require more work on your part, e.g. to install the necessary packages listed below, and setup the ~1.4GB BERT model, which can be downloaded from our MS Teams page (link provided below).

Required packages:
numpy
pandas
tensorflow
tweepy
unidecode
ktrain
dash
dash-renderer
plotly 
dash-core-components
dash-html-components
dash_bootstrap_components 
sqlalchemy
psycopg2
flask
flask_sqlalchemy

BERT model:
https://teams.microsoft.com/_#/school/files/P_Team%201_Disaster%20Tweets%20-%20Real%20or%20Not%20Natural%20Lan?threadId=19%3A45ebedd491ba4310930569351206ed76%40thread.tacv2&ctx=channel&context=bert%2520model&rootfolder=%252Fsites%252FLE-ENG40002020-2021TeamsP-AG-P_Team1_DisasterTweets-RealorNotNaturalLan%252FShared%2520Documents%252FP_Team%25201_Disaster%2520Tweets%2520-%2520Real%2520or%2520Not%2520Natural%2520Lan%252Fbert%2520model

A guide for installing and running the web app is also included in case you really wish to run this locally. Please note, however, that this was originally meant and written for my groupmates to help them set-up on an earlier version of the web app.

----------------------------------------------------------------------

The source codes in this folder can be divided into 3 parts, each fulfilling a primary role in building the web app:

1. Streamer app
	> stream-keyword.py -- consumes tweets streamed by the Twitter API, classifies them, and stores the tweets along with several metadata to our PostgreSQL database.

2. Database scripts
	> dbconfig.py -- database configuration settings
	> dbmodels.py -- defines class representations of the tables in our database
	> dbcrud.py   -- connects to the database server and creates the tables defined in dbmodels

3. Places script
	> places folder with geographical data on specific locations
	> places.py -- reads the data from the places folder and inserts the information to the database

4. Web application
	> assets folder	-- contains images and css files used by the web app
	> model folder	-- placeholder folder for the BERT model
	> app.py	-- sets up the flask back-end and table definitions used by the web app
	> main_layout1.py -- main entrypoint of the dash web app when run
	> dashboard_main.py -- renders and handles callbacks of the main page
	> livefeed.py	-- renders and handles callbacks of the live feed page
	> pbnj2.py	-- defines global variables and functions used by the web app
	> about_us.py, feedback.py, help_hotlines.py, how_to_use.py, disclaimer.py, page_404.py, page_wip.py -- other pages of the web app. note that some of these pages are still a work-in-progress.



