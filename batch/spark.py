from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
# each worker loads a piece of the data file
data = sc.textFile("view_count.log", 2)
# tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split(","))

# 2. Group data into (user_id, list of item ids they clicked on)
group_by_key = pairs.groupByKey()

# 3. Transform into (user_id, (item1, item2)
coview = group_by_key.flatMap(lambda x: map(lambda e: (x[0], e), x[1]))

# 4. Transform into ((item1, item2), list of user1, user2 etc)
# where users are all the ones who co-clicked (item1, item2)

# 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)


# 6. Filter out any results where less than 3 users co-clicked the same pair of items

# re-layout the data to ignore the user id
pages = pairs.map(lambda pair: (pair[1], 1))
# shuffle the data so that each key is only on one worker

# and then reduce all the values by adding them together
count = pages.reduceByKey(lambda x, y: int(x)+int(y))

# bring the data back to the master node so we can print it out
output = count.collect()
for page_id, count in output:
    print("page_id %s count %d" % (page_id, count))
print("Popular items done")

sc.stop()
