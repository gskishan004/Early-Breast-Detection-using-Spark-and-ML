# Distributed ML for prediction of brest cancer using histology slides


## Here we will discuss 2 ways: 1> Using personal laptop 2> Using Dumbo
## *Note that there are still lot of problems running it in dumbo*

## On Local machine 

###### Config
Spark 			            2.3
Python 						3.6
Tensorflow 		            1.4.0
JDK version 				1.8.0_222
Memory 						10 GB
Image resolution Downscaled 100x100
Keras						2.1.5
Numpy						1.17.4
Pillow						6.2.1
OS 							Ubuntu
OS Version					18.04.2 LTS

## Steps:

###### Download spark and unzip it
curl -O https://archive.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
tar xzf spark-2.3.0-bin-hadoop2.7.tgz

###### Copy the dataset in PWD
Can use FTP client such as WinSCP
Info about Data: https://web.inf.ufpr.br/vri/databases/breast-cancer-histopathological-database-breakhis/
Link to download Data: http://www.inf.ufpr.br/vri/databases/BreaKHis_v1.tar.gz

###### Clean the data and resize the images to 100x100
rm -r filtered_dataset
python data_cleaning

###### Folder structure to this point in the root should be as follows:
-BreaKHis_v1   
	-histology_slides          
-breast_cancer_train.py
-breast_cancer_eval.py
-filtered_dataset  
	-b100  
	-b200  
	-b40  
	-b400  
	-m100  
	-m200  
	-m40  
	-m400
-spark-2.3.0-bin-hadoop2.7      
-data_cleaning.py           
-spark-2.3.0-bin-hadoop2.7.tgz 

###### Code to train the model
breast_cancer_train.py

###### Code to get the results
breast_cancer_eval.py

###### To run the code
export PYSPARK_PYTHON=python3

spark-2.3.0-bin-hadoop2.7/bin/pyspark --packages databricks:spark-deep-learning:0.1.0-spark2.1-s_2.11 --driver-memory 10g 

-----------------------------------------------------------------------------------

## On Dumbo 


ssh ABC@gw.hpc.nyu.edu
ssh -Y ABC@dumbo.es.its.nyu.edu 

module load anaconda3/2019.10
module load spark/2.4.0
export PYSPARK_PYTHON=/share/apps/anaconda3/2019.10/bin/python
export PYSPARK_DRIVER_PYTHON=/share/apps/anaconda3/2019.10/bin/python
export LIB_JVM=/usr/java/latest/jre/lib/amd64/server
export LIB_HDFS=/opt/cloudera/parcels/CDH-5.15.2-1.cdh5.15.2.p0.3/lib64/

pushd "${PYSPARK_PYTHON}"
zip -r Python.zip *
popd 

###### Clean the data and resize the images
rm -r filtered_dataset
python data_cleaning

###### Make directory in HDFS
hdfs dfs -rm -r /user/ik1304/test/
hdfs dfs -mkdir /user/ik1304/test
hdfs dfs -mkdir /user/ik1304/test/b40
hdfs dfs -mkdir /user/ik1304/test/m40

###### Put the data set in HDFS
hdfs dfs -put filtered_dataset/b40 test/b40
hdfs dfs -put filtered_dataset/m40 test/m40

###### Verfify the files
hdfs dfs -ls /user/ik1304/test/

###### Do the below step only once
module load anaconda3/2019.10 
pip install --user --force-reinstall  sparkdl
pip install --user --force-reinstall tensorframes
pip install --user --force-reinstall pyspark
pip install --user --force-reinstall python2

###### Put the following as import below import tensorflow as tf, for files mentioned after that
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

/home/ik1304/.local/lib/python3.7/site-packages/sparkdl/transformers/keras_applications.py
/home/ik1304/.local/lib/python3.7/site-packages/sparkdl/transformers/utils.py
/home/ik1304/.local/lib/python3.7/site-packages/sparkdl/graph/utils.py
/home/ik1304/.local/lib/python3.7/site-packages/sparkdl/transformers/tf_image.py
/home/ik1304/.local/lib/python3.7/site-packages/tensorframes/core.py

spark = SparkSession(sc):
/home/ik1304/.local/lib/python3.7/site-packages/sparkdl/image/imageIO.py

###### Start pyspark by typing the following cmd:
pyspark

###### Code to train the model
breast_cancer_train.py

###### Code to get the results
breast_cancer_eval.py


-----------------------------------------------------------------------------------
## KNOWN ISSUES
-----------------------------------------------------------------------------------

1> On Local
	-	Different behaviour for spark-submit and pyspark, current resolution is to strictly use pyspark in interactive mode for code execution.

2> On Dumbo
	-	GLIBC 2.14 error : Most likely to be caused due to version difference in Java and Python in the cluster and master
		Resolution till now : use - pushd "${PYSPARK_PYTHON}"
		Parking this issue to focus energy on runninng it on locak