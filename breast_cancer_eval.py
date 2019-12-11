from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import sparkdl as dl
import tensorflow as tf
import pyspark.sql.functions as f
import sparkdl as dl
from pyspark.sql.functions import lit
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline

img_dir = "filtered_dataset/"
magnifications = ['40','100', '200', '400']

for m in magnifications:

	b_df = dl.readImages(img_dir + "/b" + m).withColumn("label", lit(1))
	m_df = dl.readImages(img_dir + "/m" + m).withColumn("label", lit(0))


	#Splitting the data into training and test in the ratio 80% & 20%
	trainb, testb = b_df.randomSplit([80.00, 20.00], seed=42)
	trainm, testm = m_df.randomSplit([80.00, 20.00], seed=42)

	#combining the dataset benign and malignanent for the training and testing
	trainDF = trainb.unionAll(trainm)
	testDF = testb.unionAll(testm)

	lr_test = LogisticRegressionModel.load('./test-'+m)

	# Use a featurizer to use trained features from an existing model
	featurizer_test = dl.DeepImageFeaturizer(inputCol = "image", outputCol = "features", modelName = "InceptionV3")

	# Setup a pipeline
	p_lr_test = PipelineModel(stages=[featurizer_test, lr_test])

	# Test and evaluate
	tested_lr_test = p_lr_test.transform(testDF)
	evaluator_lr_test = MulticlassClassificationEvaluator(metricName = "accuracy")
	print("Logistic Regression Model: Test set accuracy = " + str(evaluator_lr_test.evaluate(tested_lr_test.select("prediction", "label"))))

	tested_lr_test.select("label", "probability", "prediction").show(20, False)