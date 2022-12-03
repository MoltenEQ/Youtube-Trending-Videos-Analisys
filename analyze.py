import pandas as pd
import bamboolib as bam
import json

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
REGIONS = ["CA","DE","FR","GB","IN","JP","KR","RU","MX","US"]

# REGIONS = ["CA"] # Korea only

video_lists = []
raw_categories = []
categories = []
joined_data = []

for region_code in REGIONS:
    # videos.append(pd.read_csv(f"data/{region_code}videos.csv",encoding="utf-16-be",on_bad_lines='skip'))
    video_lists.append(pd.read_csv(f"data/{region_code}videos.csv",on_bad_lines='skip'))
    with open(f"data/{region_code}_category_id.json") as data_file:    
        data = json.load(data_file) 
    row_category_normalized = pd.json_normalize(data, ["items"], )
    raw_categories.append(row_category_normalized)
    print("Read files for region: " + region_code)

# Make categories usuable
for i in range(len(REGIONS)):
    print("Make categories usable for: " + REGIONS[i])
    raw_category = raw_categories[i]
    ids = raw_category["id"]
    titles = raw_category["snippet.title"]
    dict = {"id":ids,"category_title":titles}
    category = pd.DataFrame(dict)
    category['id'] = category['id'].astype(str)
    categories.append(category)

# Fix bad data
for i in range(len(REGIONS)):
    print("Fixing bad data for region: " + REGIONS[i])
    video_list = video_lists[i]

    #Force column dtypes
    video_list['video_id'] = video_list['video_id'].astype(str)
    video_list['trending_date'] = video_list['trending_date'].astype(str)
    video_list['title'] = video_list['title'].astype(str)
    video_list['channel_title'] = video_list['channel_title'].astype(str)
    video_list['category_id'] = video_list['category_id'].astype(str)
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

#Tags are bad, let's fix that
for i in range(len(REGIONS)):
    print("Fixing tags: " + REGIONS[i])
    video_list = video_lists[i]
    fixed_tags = []
    for row in range(len(video_list.index)):
        row_raw_tags = video_list['tags'][1]
        row_tags_split = row_raw_tags.split('|')
        for i in range(len(row_tags_split)):
            row_tags_split[i] = row_tags_split[i].strip('\"') # replace quotation marks
        # Tags may have "[None]" in them
        if len(row_tags_split) == 1: 
            if not row_tags_split[0] or row_tags_split[0] == "[none]": # empy lists are falsy
                row_tags_split = []
        fixed_tags.append(row_tags_split)

    fixed_tags_tupple = {'tags': fixed_tags}
    fixed_tags_df = pd.DataFrame(fixed_tags_tupple)
    video_list['tags'] = fixed_tags_df['tags'].values

    # Fix trending dates (from string to date)
    video_list['trending_date'] = pd.to_datetime(video_list['trending_date'],format='%y.%d.%m')

    # Fix publish time (from string to date)
    video_list['publish_time'] = pd.to_datetime(video_list['publish_time'])

# Insert more data
for i in range(len(REGIONS)):
    print("Insert more data into: " + REGIONS[i])

    #Insert count of tags
    video_list = video_lists[i]
    tag_count = []
    for row in video_list['tags']:
        tag_count.append(len(row))
    video_list.insert(len(video_list.columns),"tag_count",tag_count)

    # Insert length of description. NOTE: I've had to replace descriptions for the RU region
    description_lengths = []
    video_list['description'] = video_list['description'].fillna('') # We don't want NaN values, as they are considered float
    for row in video_list['description']:
        description_lengths.append(len(row))
    video_list.insert(len(video_list.columns),"description_length",description_lengths)

    # Add region
    region = [REGIONS[i]] * len(video_list.index)
    video_list.insert(len(video_list.columns),"region",region)

# Join categories and videos
for i in range(len(REGIONS)):
    video_list = video_lists[i]
    category = categories[i]
    joined = video_list.join(category.set_index("id"), on="category_id")
    joined_data.append(joined)

# Merge all of them into one BIG set
full_data = pd.concat(joined_data)

# Describe the data
for i in range(len(REGIONS)):
    print(f"**====================================**")
    print(f"**====== REGION : {REGIONS[i]} =======**")
    print(f"**====================================**")
    data = joined_data[i]
    print(data.info())
    print(data.describe())


print(f"**====================================**")
print(f"**================ TOTAL =============**")
print(f"**====================================**")
print(full_data.info())
print(full_data.describe())


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
