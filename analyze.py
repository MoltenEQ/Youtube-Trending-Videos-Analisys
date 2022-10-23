import pandas as pd
import plotly
import io

pd.set_option('display.float_format', lambda x: '%.2f' % x) # Set numeric value print format
pd.options.plotting.backend = "plotly" # Use plotly to generate visualizations


REGIONS = ["CA","DE","FR","GB","IN","JP","KR","RU","MX","US"] # TODO fix Russia

videos = []
categories = []

for region_code in REGIONS:
    videos.append(pd.read_csv(f"data/{region_code}videos.csv",encoding="utf-16-be",on_bad_lines='skip'))
    categories.append(pd.read_json(f"data/{region_code}_category_id.json"))
    print("Read files for region: " + region_code)

# for i in range(10):
#     print("### " + REGIONS[i] + " ###")
#     # print(videos[i].info())
#     print(videos[i].describe())

ca_vid = videos[0]


for col in ca_vid.columns:
    print(f"{col}: {ca_vid[col].isna().sum()} - {ca_vid[col].isna().sum()/ca_vid[col].count()}")

# boxplot = ca_vid[["views"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["likes"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["dislikes"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["comment_count"]].boxplot()
# boxplot.show()
# print("plot")

# print(ca_vid.describe())
# for col in ca_vid:
#     print(ca_vid[col].nunique())