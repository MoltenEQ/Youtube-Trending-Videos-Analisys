import pandas as pd
import plotly
import io

pd.set_option('display.float_format', lambda x: '%.2f' % x) # Set numeric value print format
pd.options.plotting.backend = "plotly" # Use plotly to generate visualizations

# COLS = ['video_id':str,
# 'trending_date':str,
# 'title':str,
# 'channel_title':str,
# 'category_id':int,
# 'publish_time':str,
# 'tags':str,
# 'views':int,
# 'likes':int,
# 'dislikes':int,
# 'comment_count':int,
# 'thumbnail_link':str,
# 'comments_disabled':bool,
# 'ratings_disabled':bool,
# 'video_error_or_removed':bool,
# 'description':str,
# ]
REGIONS = ["CA","DE","FR","GB","IN","JP","KR","RU","MX","US"] # TODO fix Korea if we can

# REGIONS = ["KR"] # Korea only

video_lists = []
categories = []

for region_code in REGIONS:
    # videos.append(pd.read_csv(f"data/{region_code}videos.csv",encoding="utf-16-be",on_bad_lines='skip'))
    video_lists.append(pd.read_csv(f"data/{region_code}videos.csv",on_bad_lines='skip'))
    categories.append(pd.read_json(f"data/{region_code}_category_id.json"))
    print("Read files for region: " + region_code)

for i in range(len(REGIONS)):
    print("Fixing bad data for region: " + REGIONS[i])
    video_list = video_lists[i]
    #Force column dtypes
    video_list['video_id'] = video_list['video_id'].astype(str)
    video_list['trending_date'] = video_list['trending_date'].astype(str)
    video_list['title'] = video_list['title'].astype(str)
    video_list['channel_title'] = video_list['channel_title'].astype(str)
    video_list['category_id'] = video_list['category_id'].astype(int)
    video_list['publish_time'] = video_list['publish_time'].astype(str)
    video_list['tags'] = video_list['tags'].astype(str)
    #We had errors with RU views
    video_list['views'] = pd.to_numeric(video_list['views'], errors='coerce')
    video_list = video_list.dropna(subset=['views'])

    video_list['views'] = video_list['views'].astype(int)
    video_list['likes'] = video_list['likes'].astype(int)
    video_list['dislikes'] = video_list['dislikes'].astype(int)
    video_list['comment_count'] = video_list['comment_count'].astype(int)
    video_list['thumbnail_link'] = video_list['video_id'].astype(str)
    video_list['comments_disabled'] = video_list['video_id'].astype(bool)
    video_list['ratings_disabled'] = video_list['video_id'].astype(bool)
    video_list['video_error_or_removed'] = video_list['video_id'].astype(bool)
    video_list['description'] = video_list['video_id'].astype(str)

for i in range(len(REGIONS)):
    print("Info for region: " + REGIONS[i])
    video_list = video_lists[i]
    #Tags are bad, let's fix that
    fixed_tags = []
    for row in range(len(video_list.index)):
        row_raw_tags = video_list['tags'][1]
        row_tags_split = row_raw_tags.split('|')
        for i in range(len(row_tags_split)):
            row_tags_split[i] = row_tags_split[i].strip('\"') # replace quotation marks
        fixed_tags.append(row_tags_split)

    fixed_tags_tupple = {'tags': fixed_tags}
    fixed_tags_df = pd.DataFrame(fixed_tags_tupple)
    video_list['tags'] = fixed_tags_df['tags'].values

    # Fix trending dates (from string to date)
    video_list['trending_date'] = pd.to_datetime(video_list['trending_date'],format='%y.%d.%m')

    # Fix publish time (from string to date)
    video_list['publish_time'] = pd.to_datetime(video_list['publish_time'])

    # Describe the list
    print("===============")
    print(video_list.info())
    print(video_list.describe())





# ca_vid = videos[0]

# ca_vid_tag_count = []

# # Na értékek aránya
# for row in range(len(ca_vid.index)): # Number of rows
#     raw_tags = ca_vid['tags'][row]
#     tags_split = raw_tags.split('|')
#     for i in range(len(tags_split)):
#         tags_split[i] = tags_split[i].strip('\"') # idézőjelek törlése
#     if len(tags_split) == 1: 
#         if not tags_split[0] or tags_split[0] == "[none]": # ha üres string akkor hamissal tér vissza
#             tags_split = []
#     ca_vid_tag_count.append(len(tags_split))

# # Beillesztés

# ca_vid.insert(len(ca_vid.columns),"tag_count",ca_vid_tag_count)







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