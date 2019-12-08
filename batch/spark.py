from pyspark import SparkContext


def getPairs(item):
    item_list = list(item)
    return [(item_list[i], item_list[j]) for i in range(len(item_list)) for j in range(i+1, len(item_list))]


sc = SparkContext("spark://spark-master:7077", "PopularItems")

# Each worker loads a piece of the data file
data = sc.textFile("/tmp/data/view_count.log", 2)
# Filter out all duplicate rows from RDD
data = data.distinct()
# Tell each worker to split each line of its partition
pairs = data.map(lambda line: line.split(","))

# Group data into (user_id, [item1, item2, item3, etc.])
user_group_items = pairs.groupByKey()
# Get the list of items ex. [item1, item2, etc.]
items = user_group_items.map(lambda x: x[1])
# Get all of the pairs ex. [(item1, item2), (item1, item3), etc.]
coclicks = items.flatMap(lambda item: getPairs(item))
# Map each coclick to a value of 1 ex. ((item1, item2), 1)
coclicks = coclicks.map(lambda item: (item, 1))
# Use reduceByKey to get the counts of them ex. ((item1, item2), 4)
count = coclicks.reduceByKey(lambda x, y: int(x)+int(y))
# Filter to remove the ones with less than 3 co-clicks
final = count.filter(lambda x: x[1] >= 3)

# bring the data back to the master node so we can print it out
output = final.collect()
for out in output:
    print(out)
print("Popular items done")

sc.stop()
