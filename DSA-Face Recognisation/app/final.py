from deepface import DeepFace
import os
import cv2
import numpy as np
import pickle
embeddings = {}
labels = {}
with open('app\embeddings_and_labels.pkl', 'rb') as pickle_file:
    data = pickle.load(pickle_file)

embeddings = data["embeddings"]
labels = data["labels"]
import numpy as np
def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

def getroll(t):
    
        
    name=''
    a=5
    e=t
        
    for i in range(1,87):
       x=findCosineDistance(embeddings[i]['embedding'],e)
   
       if(x<a):
         a=x
         name=labels[i]
  
    return str(name)
def roll(imgpath):
    lab=[]
    embedding_objs1 = DeepFace.represent(img_path = imgpath,detector_backend='retinaface',enforce_detection=False)
    
    import csv
    csv_file = 'app/marking.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['index','Name', 'Status'])
    index1=1
    for a in embedding_objs1:
        x=a['facial_area']['x']
        y=a['facial_area']['y']
        w=a['facial_area']['w']
        h=a['facial_area']['h']
       
        label=getroll(a['embedding'])
        print(label)
        lab.append(label)

        if len(label)==1:
            label='22000100'+label
        else:    
            label='2200010'+label
        
        with open(csv_file, 'a', newline='') as file:
        
            
            
            writer = csv.writer(file)

            record=[index1,label, 'Present']
            writer.writerow(record)
            index1=index1+1

    return lab
   