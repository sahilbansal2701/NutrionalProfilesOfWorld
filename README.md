# The Nourishing Four Final Project: Nutritional Profile of Countries Around the World

**Reports:**

- The report for the data deliverable will be found in the pathway `data_deliverable` where there will be a README with a link to a Google Doc with the final Data Deliverable document.

- The report for the analysis deliverable will be found in the pathway `analysis_deliverable` where there will be a README with a link to a Google Doc with the final Analysis Deliverable document.

- The report for the final deliverable will be found in the pathway `final_deliverable` where there will be a README with a link to a Google Doc with the Final Deliverable document, and the interactive component link. The poster and video can be found in the folder also.

**Data:**

- `data`: This folder contains multiple folders that document the process of creating and cleaning our database.

    - `data/1-raw`: This is where the raw datasets that are being used are stored. The raw datasets we are using are CSV files we found mainly on the Our World in Data and FAOSTAT websites.

    - `data/2-turned_into_one_db`: This stage is where the tables are combined into one large database with each raw dataset converted to an table within the database. In addition, the column names are cleaned.

    - `data/3-remove_columns`: This stage is where all the uncessary columns of each table are removed.

    - `data/4-move_units`: This stage is where all the units for value information was moved from exiting as a separate column to now being part of the value column name. This mainly pertained to the FAOSTAT tables.

    - `data/5-keep_time_range`: This stage is where all the entries predating the year 2000 were removed because this project deals with data in the 21st century, so year 2000 onwards

    - `data/6-joined_our_world_in_data`: This stage is where all the Our World In Data tables, which had the same primary keys, were joined together to create the diet_and_life table. The old tables were then deleted to keep the file size small, and since the separate tables were no longer needed.

    - `data/7-joined_imports_exports`: This stage is where the import and export tables, which had the same primary keys, were joined together to create the imports_and_exports table. The old tables were then deleted to keep the file size small, and since the separate tables were no longer needed.

    - `data/8-aggregate`: This stage is where a column, total_kc_pp_pd, has been created which is the summation of all the other kc_pp_pd columns to get the total amount of kilocalories a person has per day.

    - `data/9-percentages`: This stage is where multiple columns were created, one corresponding to each kc_pp_pd value, except total_kc_pp_pd, which is the column in question divided by total_kc_pp_pd multiplied by 100 to get the percentage of calories of that food group eaten per person per day.

    - `data/scripts`: The scripts folder contains all the python scripts that we have written to create, convert, and clean the data.

        - `data/scripts/conversion_scripts`: This folder contains all the python code that does the actual conversion and modifying of the database and tables. The scripts are named so that you can tell, which script corresponds to which part of the conversion pipeline.

        - `data/scripts/input_files`: This folder contains the input files that were passed into the conversion scripts. This is necessary because the conversion scripts were written to be flexible and allow working with different datasets.

**Code:**

- `data_deliverable`: This folder contains things that are directly important to the data deliverable.

    - `data_deliverable/scatter_graph_scripts`: This folder contains the scripts that were used to create scatter graphs for particular attributes to visualize the data.

- `analysis_deliverable`: This folder contains all the things that are directly important to the analysis deliverable.

    - `analysis_deliverable/code`: This folder contains all the python scripts that we have written to run the tests for analysis, and to run the ML models.

        - `analysis_deliverable/code/run_tests.py`: This python script holds the code which we used to run the tests for all our hypotheses.

        - `analysis_deliverable/code/ml_models.py`: This python scripts holds the code for our ML models.

        - `analysis_deliverable/code/util.py`: This python file holds functions that are generally useful.

- `final_deliverable`: This folder contains all the things that are directly important to the final deliverable. It contains the poster, interactive component link and video for the final deliverable.

    - `final_deliverable/data_jsons`: This folder contains a script, and all the jsons of the statistics calculated in the analysis deliverable.

    - `final_deliverable/interactive_component`: This contains the ReactJS code for our interactive component. Our interactive component allows you to type in a country name and year, and find all the countries that had a similar nutrional profile to that country in that year. It compares nutritional profiles based on fat, protein and carbohydrate percentages.

    - `final_deliverable/visualizations`: This contains the scripts and graphs for visualizations of our project. This is elaborated on in our final deliverable document.