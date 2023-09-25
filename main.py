import re
import os

import geopandas as gpd
import plotly.express as px
import pandas as pd
from shapely.geometry import Polygon


def read_data_file(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_file = f.readlines()

    list_dados = [line.split() for line in raw_file]
    float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
    return pd.DataFrame(float_raw_lines, columns=['long', 'lat', 'data_value'])


def read_contour_file(file_path: str) -> pd.DataFrame:
    line_split_comp = re.compile(r'\s*,')

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_file = f.readlines()

    l_raw_lines = [line_split_comp.split(raw_file_line.strip()) for raw_file_line in raw_file]
    l_raw_lines = list(filter(lambda item: bool(item[0]), l_raw_lines))
    float_raw_lines = [list(map(float, raw_line))[:2] for raw_line in l_raw_lines]
    header_line = float_raw_lines.pop(0)
    assert len(float_raw_lines) == int(header_line[0])
    return pd.DataFrame(float_raw_lines, columns=['long', 'lat'])


def apply_contour(contour_df: pd.DataFrame, data_df: pd.DataFrame) -> pd.DataFrame:
    """Clip `data_dt` points with polygon defined by `contour_df`"""
    geometry = gpd.points_from_xy(contour_df['long'], contour_df['lat'])
    boundary = Polygon(geometry)

    geometry = gpd.points_from_xy(data_df['long'], data_df['lat'])
    data_gdf = gpd.GeoDataFrame(data_df['data_value'], geometry=geometry)
    data_gdf = gpd.clip(data_gdf, boundary)

    ix = data_gdf.index
    return data_df.loc[ix]

def get_files(
        data_pattern='ETA40_p([0-9]*)a([0-9]*).dat',
        data_path='forecast_files'
    ) -> tuple[str, tuple[str, str]]:
    """Get all files in `data_path` that match `data_pattern`"""
    for filename in os.listdir(data_path):
        if match := re.match(data_pattern, filename):
            print('Processing file: ', filename)
            yield os.path.join(data_path, filename), match.groups()


def main():
    contour_name = 'PSATCMG_CAMARGOS.bln'
    data_path = 'forecast_files'
    data_pattern = 'ETA40_p([0-9]*)a([0-9]*).dat'

    data_dfs: list[pd.DataFrame] = []
    contour_df = read_contour_file(contour_name)

    for path, groups in get_files(data_pattern, data_path):
        forecast_date, forecasted_date = groups
        data_df = read_data_file(path)
        data_df = apply_contour(contour_df, data_df)
        data_df['forecast_date'] = pd.to_datetime(forecast_date, format='%d%m%y')
        data_df['forecasted_date'] = pd.to_datetime(forecasted_date, format='%d%m%y')
        data_dfs.append(data_df)

    data_df = pd.concat(data_dfs).reset_index(drop=True)

    # Data Analytics
    total_precipitation = data_df.groupby('forecast_date')[['data_value']].sum().reset_index()
    precipitation_by_date = data_df.groupby(['forecast_date', 'forecasted_date'])[['data_value']].sum().reset_index()

    precipitation_by_date = precipitation_by_date.sort_values('forecasted_date')
    cumulative = precipitation_by_date.groupby('forecast_date')[['data_value']].cumsum()
    precipitation_by_date['cumulative'] = cumulative

    # Data Visualization
    print('Total precipitation:', total_precipitation['data_value'].sum())

    plot = px.line(
        precipitation_by_date,
        x='forecasted_date',
        y='data_value',
        labels={'forecasted_date': 'Data prevista', 'data_value': 'Precipitação'},
        title='Precipitação por data prevista em Camargos (ref. 01/12/2021)',
    )
    plot.show()

    plot = px.line(
        precipitation_by_date,
        x='forecasted_date',
        y='cumulative',
        labels={'forecasted_date': 'Data prevista', 'cumulative': 'Precipitação acumulada até a data'},
        title='Precipitação acumulada em Camargos (ref. 01/12/2021)',
    )
    plot.show()


if __name__ == '__main__':
    main()
