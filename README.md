# wildfire-risk-ml
Abigail Stokes Fulbright 2025 Project 
Wildfire Prediction using Geospatial Machine Learning Methods in South Central Chile
contact: abigail.stokes@fulbrightmail.org


Abstract:
Drought-driven forest fires pose significant threats to ecosystems and communities in Chile. Accurate and timely prediction of these events is crucial for effective mitigation and disaster preparedness. This research proposal aims to develop a novel bottom-up methodology utilizing machine learning methods for predicting forest fire spread in the Region of Maule, Chile using historical fire scar and ignition point data. Variables for prediction include historical climate, topography, antropic, and vegatation satelite imagery. By integrating multiple sources of remote sensing information, this project seeks to enhance prediction accuracy and enable proactive response strategies by providing real time prediction of fire spread extent.


Files in this repository and their contents:


---- NOTEBOOKS / PYTHON FILES ----

data_exploration.ipynb   ---    Notebook which does some initial data exploration primarily using the FireScar_CL_Summary_1985-2018.xlsx file. Looks general information such as number of fires per year, month, and region, spatial distribution of fires by year for the region of Maule, and some initial geospatial statistical tests such as Ripley's K and KDE plots / correlation maps.

fire_viewer.ipynb   ---   Widget to visualize fire burn scar data for Maule. Visualizes burn scar vector, NBR, and severity map, as well as pre- and post-fire images with burn scar boundary overlay

data_preprocessing.ipynb   ---   Notebook containing to visualize and plan for data pre-processing task carried out in image_processing.ipynb cropping and padding of images, and save as tif files for machine learning (mask.tif and merged.tif)

fire_scar_prediction.ipynb   ---   Notebook which creates a simple UNet model to predict fire scar base on post-fire image. Proto-type to see that code runs

image_processing.ipynb   ---   Notebook containing the code to perform  cropping and padding of images, and save as tif files for machine learning (mask.tif and merged.tif)

merged_scars.ipynb   ---   Notebook which 1) creates a merged raster file with all scars for a given season (year) and 2) creates a merged raster file for each season with the 'fire scar history' (number of previous fires in past 10 years at each pixel point). Treats multiple fires in same location in given year as one fire event as fire scar is the same. For years where 10 previous years' scars are not available, used as much previous data as possible.





----- TEXT FILES ----

File_Description.txt   ---   A text file which was downloaded from the PANGEA site which described the columns and files contained in the fire scar database.

dataset_summary.txt   ---   A text file with summary information / statistics of the FireScar_CL_Summary_1985-2018.xlsx file.




---- DATA FOLDERS ----

Fire_CL-ML_Maule   ---   Data folder containing all the historical fire burn scar data, with contains described in File_Description.txt file. Fire scar, severity, pre and post fire image, and RdNBR for each event. Used to construct other rasters in this repository.

merged_rasters   ---   Data folder with the merged binary fire scar raster files for Maule a given year from 1986 to 2018. Constructed using Fire_CL-ML_Maule data

fire_history_rasters   ---   Data folder containing the tif files for Maule which has the history of fire frequency at a given location in recent years, using up to 30 years of historical data. Constructed using merged_rasters.

prev10_rasters   ---   Data folder containing tif files for Maule which have the total number of fires at a given location over the past 10 years (using up to 10 years of available historical data). Constructed using merged_rasters.

Regiones   ---   Contains region shape files for the 16 regions of Chile.


---- Notes / Acknowledgements ----

Fire Scar Data acquired from PANGEA Historical Chilean Fire Scars FireScar-CL Database
link: https://doi.pangaea.de/10.1594/PANGAEA.941127
Principal investigator: Alejandro Miranda
Contact: Alejandro Miranda, mirandac.alejandro@gmail.cl

Project funded by Fulbright U.S. Student Program, 2025
