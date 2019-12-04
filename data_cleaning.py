#compressing the images just on the basis of magnification and type (i.e, benign and malignant)
# for eg: b200 => benign    images with 200 magnification
#         m40  => malignant images with 40  magnification
import os
import shutil

folders = ['b40', 'b100', 'b200', 'b400', 'm40', 'm100', 'm200', 'm400']
root_folder = "filtered_dataset"

if not os.path.exists(root_folder):
    os.mkdir(root_folder)

for d in folders:
    if not os.path.exists(root_folder+"/"+d):
        os.mkdir(root_folder+"/"+d)


# Profiling the data only on basis of type of cancer cell and magnification and ignoring further subclassification
for root, dirs, files in os.walk("BreaKHis_v1"):
    path = root.split(os.sep)
    for file in files:
        
        if "benign" in path:
            source = '/'.join(path)+'/'+file
            destination = ''
            
            if "40X" in path:
                destination = "b40"+"/"+file
                
            elif "100X" in path:
                destination = "b100"+"/"+file
                
            elif "200X" in path:
                destination = "b200"+"/"+file
                
            elif "400X" in path:
                destination = "b400"+"/"+file
                
            if (destination != ""): shutil.copyfile(source, root_folder+"/"+destination)
                
        elif "malignant" in path:
            source = '/'.join(path)+'/'+file
            destination = ''
            
            if "40X" in path:
                destination = "m40"+"/"+file
                
            elif "100X" in path:
                destination = "m100"+"/"+file
                
            elif "200X" in path:
                destination = "m200"+"/"+file
                
            elif "400X" in path:
                destination = "m400"+"/"+file
            
            if (destination != ""): shutil.copyfile(source, root_folder+"/"+destination)
        
from PIL import Image
import statistics


def find_avg_res(folder):
    results_w = []
    results_h = []
    count     = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith('.png')]: # to loop over all images you have on the diresctory
            with Image.open(folder+"/"+filename) as img:
                width, height = img.size
                results_w.append(width)
                results_h.append(height)
                count+=1
    print ("AVG HxW = ", statistics.mean(results_w), statistics.mean(results_h), "for folder ", folder, " No of images:", count)

for f in folders:
    find_avg_res(root_folder+'/'+f)

#As the images are of different size for Malignant, we will resize them
def image_resizer(folder, w,h):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith('.png')]: # to loop over all images you have on the diresctory
            with Image.open(folder+"/"+filename) as img:
                width, height = img.size
                if (width != w or height !=h):
                    new_image = img.resize((w, h), Image.NEAREST)
                    new_image.save(folder+"/"+filename) 


for f in folders:
    image_resizer(root_folder+'/'+f, 100, 100)

#confirming the image size:
for f in folders:
    find_avg_res(root_folder+'/'+f)