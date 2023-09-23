import pandas as pd
import re


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


# pylint: disable=unused-argument
def apply_contour(contour_df: pd.DataFrame, data_df: pd.DataFrame) -> pd.DataFrame:
    return data_df


def main():
    contour_df = read_contour_file('PSATCMG_CAMARGOS.bln')
    data_df = read_data_file('forecast_files/ETA40_p011221a021221.dat')
    data_df = apply_contour(contour_df=contour_df, data_df=data_df)


if __name__ == '__main__':
    main()
