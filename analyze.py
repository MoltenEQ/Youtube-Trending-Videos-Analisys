import pandas as pd
import plotly
import io

pd.set_option('display.float_format', lambda x: '%.2f' % x) # Set numeric value print format
pd.options.plotting.backend = "plotly" # Use plotly to generate visualizations


# REGIONS = ["CA","DE","FR","GB","IN","JP","KR","RU","MX","US"] # TODO fix Russia

REGIONS = ["CA"] # Canada only

videos = []
categories = []

for region_code in REGIONS:
    videos.append(pd.read_csv(f"data/{region_code}videos.csv",encoding="utf-16-be",on_bad_lines='skip'))
    categories.append(pd.read_json(f"data/{region_code}_category_id.json"))
    print("Read files for region: " + region_code)

## Leírás generálás
# for i in range(10):
#     print("### " + REGIONS[i] + " ###")
#     # print(videos[i].info())
#     print(videos[i].describe())

ca_vid = videos[0]

ca_vid_tag_count = []

# Na értékek aránya
for row in range(len(ca_vid.index)): # Number of rows
    raw_tags = ca_vid['tags'][row]
    tags_split = raw_tags.split('|')
    for i in range(len(tags_split)):
        tags_split[i] = tags_split[i].strip('\"') # idézőjelek törlése
    if len(tags_split) == 1: 
        if not tags_split[0] or tags_split[0] == "[none]": # ha üres string akkor hamissal tér vissza
            tags_split = []
    ca_vid_tag_count.append(len(tags_split))

# Beillesztés

ca_vid.insert(len(ca_vid.columns),"tag_count",ca_vid_tag_count)

boxplot = ca_vid[["tag_count"]].boxplot()
boxplot.show()


# raw_tags = ca_vid['tags'][1]
# tags_split = raw_tags.split('|')
# for i in range(len(tags_split)):
#     tags_split[i] = tags_split[i].strip('\"') # idézőjelek törlése
# print(f"{1}: {len(tags_split)}")
# print(tags_split)



## Boxplotokhoz
# boxplot = ca_vid[["views"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["likes"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["dislikes"]].boxplot()
# boxplot.show()
# boxplot = ca_vid[["comment_count"]].boxplot()
# boxplot.show()
# print("plot")

## Egyedi értékek aránya
# print(ca_vid.describe())
# for col in ca_vid:
#     print(ca_vid[col].nunique())