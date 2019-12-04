from PIL import Image
import statistics
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy


def find_avg_res(folder):
    results_size = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith('.png')]: # to loop over all images you have on the diresctory
            results_size.append(os.path.getsize(folder+"/"+filename)*0.000001)
    print ("AVG size = ",str(round(statistics.mean(results_size), 2)) , "MB for folder", folder)
    np_results = np.array(results_size) # to make results a numpy array
    plt.hist(np_results)
    plt.suptitle(folder)
    plt.show() # to show the histogram
    

for f in folders:
    find_avg_res(root_folder+'/'+f)


# y-axis is the number of occurrences of each os those values
# x-axis means the intensity of the images

folders = ['b40', 'b100', 'b200', 'b400', 'm40', 'm100', 'm200', 'm400']
root_folder = "filtered_dataset"


def find_avg_color(folder):
    results = [] 
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith('.png')]: # to loop over all images you have on the diresctory
            img = cv2.imread(folder+"/"+filename)
            avg_color_per_row = numpy.average(img, axis=0)
            avg_color = numpy.average(avg_color_per_row, axis=0)
            results.append(avg_color)
    np_results = np.array(results) # to make results a numpy array
    plt.hist(np_results)
    plt.suptitle(folder)
    plt.show() # to show the histogram
    
    
for f in folders:
    find_avg_color(root_folder+'/'+f)