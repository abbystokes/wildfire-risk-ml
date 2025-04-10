# wildfire-risk-ml
Abigail Stokes Fulbright 2025 Project 
Wildfire Prediction using Geospatial Machine Learning Methods in South Central Chile
contact: abigail.stokes@fulbrightmail.org

Files in this repository and their contents:

data_exploration.ipynb   ---    Notebook which does some initial data exploration primarily using the FireScar_CL_Summary_1985-2018.xlsx file. Looks general information such as number of fires per year, month, and region, spatial distribution of fires by year for the region of Maule, and some initial geospatial statistical tests such as Ripley's K and KDE plots / correlation maps.

fire_viewer.ipynb   ---   Widget to visualize fire burn scar data for Maule. Visualizes burn scar vector, NBR, and severity map, as well as pre- and post-fire images with burn scar boundary overlay

data_preprocessing.ipynb   ---   Notebook containing to visualize and plan for data pre-processing task carried out in image_processing.ipynb cropping and padding of images, and save as tif files for machine learning (mask.tif and merged.tif)

fire_scar_prediction.ipynb   ---   Notebook which creates a simple UNet model to predict fire scar base on post-fire image. Proto-type to see that code runs

image_processing.ipynb   ---   Notebook containing the code to perform  cropping and padding of images, and save as tif files for machine learning (mask.tif and merged.tif)

merged_scars.ipynb   ---   Notebook which 1) creates a merged raster file with all scars for a given season (year) and 2) creates a merged raster file for each season with the 'fire scar history' (number of previous fires in past 10 years at each pixel point). Treats multiple fires in same location in given year as one fire event as fire scar is the same. For years where 10 previous years' scars are not available, used as much previous data as possible.


File_Description.txt   ---   A text file which was downloaded from the PANGEA site which described the columns and files contained in the fire scar database.

dataset_summary.txt   ---   A text file with summary information / statistics of the FireScar_CL_Summary_1985-2018.xlsx file.

classification_example.ipynb   ---   A notebook which contains an example of supervised learning classification of land cover using GEE functionalities.

Fire Scar Data acquired from PANGEA Historical Chilean Fire Scars FireScar-CL Database
link: https://doi.pangaea.de/10.1594/PANGAEA.941127
Principal investigator: Alejandro Miranda
Contact: Alejandro Miranda, mirandac.alejandro@gmail.cl
