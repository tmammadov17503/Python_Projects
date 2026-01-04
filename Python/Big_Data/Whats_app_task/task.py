import os
import shutil
import kagglehub
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression, NaiveBayes, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline

project_dir = r"C:\Users\ASUS\PycharmProjects\Python\Big_Data\Whats_app_task"
target_csv_name = "whatsapp_reviews.csv"
target_file_path = os.path.join(project_dir, target_csv_name)

os.makedirs(project_dir, exist_ok=True)

# first we download the dataset from kaggle
if os.path.exists(target_file_path):
    print(f"Found existing dataset at: {target_file_path}")
else:
    print("Dataset not found locally. Downloading via KaggleHub...")

    # and we download it using KaggleHub
    download_path = kagglehub.dataset_download("sonalshinde123/whatsapp-user-reviews-dataset")

    # now we find the downloaded CSV and move it to our project folder
    found_csv = False
    for root, dirs, files in os.walk(download_path):
        for file in files:
            if file.endswith(".csv"):
                source_path = os.path.join(root, file)
                print(f"   -> Moving {file} to your project folder...")
                shutil.copy(source_path, target_file_path)
                found_csv = True
                break
        if found_csv:
            break

    if found_csv:
        print(f"Dataset saved successfully to: {target_file_path}")
    else:
        raise FileNotFoundError("Could not find a .csv file in the downloaded Kaggle dataset.")

# here I set "local[*]" to use all available CPU cores for speed
spark = SparkSession.builder \
    .appName("WhatsApp_Comment_Classification") \
    .master("local[*]") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# loading and preprocessing of data
print("\nLoading data...")
df = spark.read.csv(target_file_path, header=True, inferSchema=True)

# here we handle potential column naming differences automatically
columns = df.columns
text_col = "review_content" if "review_content" in columns else columns[0]
rating_col = "rating" if "rating" in columns else columns[1]

print(f"Using text column: '{text_col}' and rating column: '{rating_col}'")

# here the label = 1 if Rating > 3 (Positive), else 0 (Negative)
df_clean = df.filter(col(text_col).isNotNull()) \
    .withColumn("label", when(col(rating_col) > 3, 1.0).otherwise(0.0))

# splitting of data (80% Train, 20% Test)
train_data, test_data = df_clean.randomSplit([0.8, 0.2], seed=42)

# pipeline
tokenizer = RegexTokenizer(inputCol=text_col, outputCol="words", pattern="\\W")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=1000)
idf = IDF(inputCol="rawFeatures", outputCol="features")

# training of the model
lr = LogisticRegression(labelCol="label", featuresCol="features", maxIter=10)
nb = NaiveBayes(labelCol="label", featuresCol="features")
rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=20)

# three models used
models = {
    "Logistic Regression": lr,
    "Naive Bayes": nb,
    "Random Forest": rf
}

evaluator = MulticlassClassificationEvaluator(labelCol="label", metricName="accuracy")

print("\n" + "=" * 40)
print("MODEL PERFORMANCE REPORT")
print("=" * 40)

best_model_name = ""
best_accuracy = 0.0

for name, classifier in models.items():
    # here we construct Pipeline
    pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, classifier])

    # train
    print(f"Training {name}...")
    model = pipeline.fit(train_data)

    # predict
    predictions = model.transform(test_data)

    # and finally evaluate
    accuracy = evaluator.evaluate(predictions)
    print(f"   -> Accuracy: {accuracy:.2%}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model_name = name

print("\n" + "=" * 40)
print(f"BEST MODEL: {best_model_name}")
print(f"ACCURACY:   {best_accuracy:.2%}")
print("=" * 40)

# stopping of Spark
spark.stop()