## Data pre-processing
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import rasterio
from rasterio.plot import plotting_extent
import geopandas as gpd
from rasterio.plot import show
import rasterio.features
import rasterio.warp
from matplotlib import pyplot
import geopandas as gdp
from rasterio.warp import reproject, Resampling
from rasterio.transform import rowcol
from rasterio.windows import Window
from matplotlib.colors import Normalize
from rasterio.transform import Affine
from tqdm import tqdm
import os

# Read in the data
df = pd.read_excel("FireScar_CL_Summary_1985-2018.xlsx") #excel meta-data file with file names and locations
df = df[df['FireScar'] == 1]  # Filter to just files that have fire scar available
df = df[df['Region_CONAF'] == 'Maule'] # Filter to just Maule
df = df.reset_index()

# Create output folders 
os.makedirs("data/merged", exist_ok=True)
os.makedirs("data/mask", exist_ok=True)

# Loop through all fire events
for fire_id, example_fire in df.iterrows():
    try:
        print(f"Processing FireID: {example_fire['FireID']}")

        fire_season = example_fire["FireSeason"]
        ign_date = pd.to_datetime(example_fire["IgnitionDate_CONAF"])
        control_date = pd.to_datetime(example_fire["ControlDate_CONAF"])
        fire_month = ign_date.strftime("%m")
        prev_month = f"{(ign_date.month - 1) % 12 or 12:02d}"
        duration = control_date - ign_date + pd.Timedelta(days=1)

        folder = f"Fire_CL-ML_Maule/FireScar_CL-ML_Maule_{fire_season}"
        scar_folder = f"capas/incendio/FireScars"
        severity_folder = f"capas/incendio/Severity"


        pre_fire_path = os.path.join(folder, example_fire["PreFireImgName"])
        post_fire_path = os.path.join(folder, example_fire["PostFireImgName"])
        severity_path = os.path.join(severity_folder, example_fire["SeverityImgName"])
        fire_scar_path = os.path.join(scar_folder, example_fire["FireScarImgName"])


        # Establish window from post-fire image
        dim_dest = 512
        with rasterio.open(post_fire_path) as base_src:
            crs_target = base_src.crs
            transform_target = base_src.transform
            width, height = base_src.width, base_src.height
            center_x, center_y = width // 2, height // 2
            window = Window(center_x - dim_dest/2, center_y - dim_dest/2, dim_dest, dim_dest)
            window_transform = base_src.window_transform(window)

        # Crop helper
        def crop_and_reproject_to_window(src_path, window_transform, crs_target, shape=(dim_dest, dim_dest), resampling=Resampling.nearest):
            with rasterio.open(src_path) as src:
                data_raw = src.read(1)
                dst = np.zeros(shape, dtype=np.float32)
                reproject(
                    source=data_raw,
                    destination=dst,
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=window_transform,
                    dst_crs=crs_target,
                    dst_shape=shape,
                    resampling=resampling
                )
            return dst
        def crop(path, resample=Resampling.nearest):
            return crop_and_reproject_to_window(path, window_transform, crs_target, resampling=resample)

        # Cropped variables
        severity_crop = crop(severity_path)
        scar_crop = crop(fire_scar_path)
        ign_crop = crop(f"capas/incendio/ignition_probability_maps/ignition_prob_{fire_season}.tif", Resampling.bilinear)
        dist_water_crop = crop("capas/topografia/distance_to_water_ML.tif", Resampling.bilinear)
        hl_crop = crop("capas/topografia/heat_load_ML.tif", Resampling.bilinear)
        tc_crop = crop("capas/topografia/topo_complexity_ML.tif", Resampling.bilinear)
        slope_crop = crop("capas/topografia/slope_ML.tif", Resampling.bilinear)
        elev_crop = crop("capas/topografia/elevation_ML.tif", Resampling.bilinear)
        aspect_crop = crop("capas/topografia/aspect_ML.tif", Resampling.bilinear)
        ndvi_crop = crop(f"capas/vegetacion/ndvi/MA_NDVI_{fire_season-1}.tif", Resampling.bilinear)
        fh_crop = crop(f"capas/incendio/fire_history_rasters_30yr/Maule_FireFreq_{fire_season}.tif", Resampling.bilinear)
        tslf_crop = crop(f"capas/incendio/time_since_last_fire/time_since_last_fire_{fire_season}.tif")
        temp_anom_crop = crop(f"capas/clima/WorldClim_Maule/max_temp_anomaly/anomaly_wc2.1_2.5m_tmax_{fire_season}-{prev_month}.tif", Resampling.bilinear)
        min_temp_crop = crop(f"capas/clima/WorldClim_Maule/min_temp_anomaly/anomaly_wc2.1_2.5m_tmin_{fire_season}-{prev_month}.tif", Resampling.bilinear)
        precip_anom_crop = crop(f"capas/clima/WorldClim_Maule/precipitation_anomaly/anomaly_wc2.1_2.5m_prec_{fire_season}-{prev_month}.tif", Resampling.bilinear)
        sr_crop = crop(f"capas/clima/WorldClim_Maule/solar_radiation/wc2.1_30s_srad_{fire_month}.tif", Resampling.bilinear)
        wvp_crop = crop(f"capas/clima/WorldClim_Maule/water_vapor_pressure/wc2.1_30s_vapr_{fire_month}.tif", Resampling.bilinear)
        ws_crop = crop(f"capas/clima/WorldClim_Maule/wind_speed/wc2.1_30s_wind_{fire_month}.tif", Resampling.bilinear)
        dist_road_crop = crop("capas/antropico/distance_to_camino_ML.tif", Resampling.bilinear)
        dist_pop_crop = crop("capas/antropico/distance_to_populated_ML.tif", Resampling.bilinear)
        pop_dens_crop = crop("capas/antropico/pop_density_ML.tif", Resampling.bilinear)

        stacked_array = np.stack([
            ign_crop, dist_water_crop, hl_crop, tc_crop, slope_crop, elev_crop, aspect_crop,
            ndvi_crop, fh_crop, tslf_crop, temp_anom_crop, min_temp_crop, precip_anom_crop,
            sr_crop, wvp_crop, ws_crop, dist_road_crop, dist_pop_crop, pop_dens_crop
        ])

        band_names = [
            'Ignition Point', 'Distance to Water', 'Heat Load', 'Topographic Complexity', 'Slope',
            'Elevation', 'Aspect', 'NDVI', 'Fire History', 'Time Since Last Fire', 'Temperature Anomaly',
            'Minimum Temperature Anomaly', 'Precipitation Anomaly', 'Solar Radiation',
            'Water Vapor Pressure', 'Wind Speed', 'Distance to Road', 'Distance to Population', 'Population Density'
        ]

        fire_id_str = str(example_fire["FireID"])
        out_merged = f"data/merged/merged_{fire_id_str}.tif"
        out_mask = f"data/mask/mask_{fire_id_str}.tif"

        # Save multiband raster
        with rasterio.open(
            out_merged, 'w', driver='GTiff', height=dim_dest, width=dim_dest,
            count=stacked_array.shape[0], dtype=stacked_array.dtype,
            crs=crs_target, transform=window_transform
        ) as dst:
            for i in range(stacked_array.shape[0]):
                dst.write(stacked_array[i], i + 1)
                dst.set_band_description(i + 1, band_names[i])
        print(f"Saved multiband raster to {out_merged}")

        # Save mask

        # For severity raster
       # with rasterio.open(
       #     out_mask, 'w', driver='GTiff', height=dim_dest, width=dim_dest,
       #     count=1, dtype=severity_crop.dtype, crs=crs_target, transform=window_transform
       # ) as dst:
       #     dst.write(severity_crop, 1)
       # print(f"Saved mask raster to {out_mask}")

        # For binary scar mask
        with rasterio.open(
            out_mask, 'w', driver='GTiff', height=dim_dest, width=dim_dest,
            count=1, dtype=scar_crop.dtype, crs=crs_target, transform=window_transform
        ) as dst:
            dst.write(scar_crop, 1)
        print(f"Saved mask raster to {out_mask}")

    except Exception as e:
        print(f"Failed on FireID {example_fire['FireID']}: {e}")
