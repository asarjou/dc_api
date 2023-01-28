Author: Arman Sarjou

This directory contains the necessary Python files to read the Dynamic Containment Auction results (via API) and saving the current day's result to a local database.

You should find the following files in this directory:

1. main.py
2. db.py
3. Dockerfile
4. requirements.txt
5. API/Constants.py
6. API/make_request.py
7. API/preprocessing.py
8. database/make_connection.py
9. database/query.py
10. database/run_query.py

There is also an empty directory named dcdb

The software uses SQLAlchemyORM (Object Relational Mapper) with a sqlite database to create a local database and run operations within it. The structure of the database can be seen in the db.py file. There are 2 tables in the relational database - NGESO_DC (holds auction results) and Unit_Information_DC (Holds information on the units owned by Habitat). In the NGESO_DC table, a unique id is used which is created using the unit name, delivery start and clearing price. This unique id is the primary key with the unit name being a foreign key. The Unit_Information_DC table uses the unit name as a primary key. 

The data is retrieved using get requests to the ESO CKAN API. In order to ensure that all records are retrieved (there is a limit from the CKAN API), logic is written to utilise the 'next' links for data which is included in the response body. 

To ensure that the software can run on all devices with ease, a docker container is used. To ensure that the database results persist, a volume is created and mounted into the container.

To run this software:

In the same directory that this README.md is placed in please run the following commands

docker build --tag dc_api . 
docker run --mount type=volume,src=dcapidb,target=/dcdb dc_api python db.py 
docker run --mount type=volume,src=dcapidb,target=/dcdb dc_api python main.py

These will create an empty database and then write to it. To see that the db exists in the docker container please run: 

docker run --mount type=volume,src=dcapidb,target=/dcdb dc_api ls dcdb

This should show a single file named dc.db within it. 

PLEASE RUN python main.py -help for information on possible input arguments. If you want to output data then you will need to mount the docker container to save the file that is produced in the directory. When running UPDATE or DELETE operations I would recommend adding the record ID you would like to delete or update - if no id is provided one is hardcoded in for testing.

Given more time I would include: 

- More robust data validation pipeline, at the moment there isn't really any/much validation used.
- Unit testing for the operations.

Please see the comments in the code for small notes on what I would have liked to do having been given more time. 

