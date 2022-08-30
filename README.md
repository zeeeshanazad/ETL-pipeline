## Running the docker

To get started run ``` docker-compose up ``` in root directory.
It will create the PostgresSQL database and start generating the data.
It will create an empty MySQL database.
It will launch the analytics.py script. 

Your task will be to write the ETL script inside the analytics/analytics.py file.

We need to setup cronjob for analytics.py file to run every hour. Currently whenever the app runs, it looks for the data in postgresql database and gets all entries made in last one hour, applies transformation and then save these entries into MySQL database.
