from pyspark.sql import SparkSession
from pyspark.sql import types as T
import json
from pyspark.sql.functions import transform
from pyspark.sql.functions import udf
import math

def get_emoji(buffer):
    spark = SparkSession.builder \
        .master("local") \
        .appName("EmojiAggregation") \
        .getOrCreate()

    schema = T.StructType([
        T.StructField("user_id", T.StringType(), True),
        T.StructField("emoji_type", T.StringType(), True),
        T.StructField("timestamp", T.StringType(), True)
    ])
    
    data = buffer
    
    df = spark.createDataFrame(data, schema=schema)
    
    df = df.dropDuplicates(["user_id", "timestamp"])

    
    emoji_counts = df.groupBy("emoji_type").count().orderBy("count", ascending=False)
    
    scale_counts = udf(lambda x: int(math.ceil(x/100)))
    emoji_counts_scaled = emoji_counts.select("emoji_type","count",scale_counts("count").alias("scaled_count"))
    #emoji_counts_scaled.show(truncate=False)
    
    result = []
    for i in emoji_counts_scaled.collect():
    	temp = []
    	temp.append(str(i["emoji_type"]))
    	result.extend(temp*int(i["scaled_count"]))
    print(result)
    return result


if __name__=='__main__':
	f = open('./emoji_dataset.json')
	buffer = json.load(f)
	get_emoji(buffer[:2100])
