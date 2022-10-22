from sre_parse import CATEGORIES
from tarfile import ENCODING
import pandas as pd
import io

pd.set_option('display.float_format', lambda x: '%.2f' % x)


REGIONS = ["CA","DE","FR","GB","IN","JP","KR","RU","MX","US"] # TODO fix Russia

videos = []
categories = []

for region_code in REGIONS:
    videos.append(pd.read_csv(f"data/{region_code}videos.csv",encoding="utf-16-be",on_bad_lines='skip'))
    categories.append(pd.read_json(f"data/{region_code}_category_id.json"))
    print("Read files for region: " + region_code)

for i in range(10):
    print("### " + REGIONS[i] + " ###")
    # print(videos[i].info())
    print(videos[i].describe())
    