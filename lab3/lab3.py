from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

class KnnClassifier:
    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels

    def classify_image(self, test_image, num_neighbors = 3, metric ='l2'):

        distances = []
        for i in range(len(self.train_images)):
            x = distance(self.train_images[i],test_image,metric)
            distances.append((x,self.train_labels[i]))
        distances.sort(key=lambda a : a[0])
        neighbours = []
        labels = {}
        for i in range(num_neighbors):
            neighbours.append(distances[i])
            if distances[i][1] not in labels.keys():
                labels[distances[i][1]] = 1
            else:
                labels[distances[i][1]] += 1
        l = [(labels[i],i) for i in labels.keys()]
        m = max(l,key=lambda a : a[0])
        return m[1]

def distance(img1,img2,metric = 'l2'):
    d = 0
    for i in range(len(img1)):
        if metric == 'l2':
            d += (img1[i]-img2[i])**2
        else:
            d += abs(img1[i] - img2[i])
    if metric == 'l2':
        d = sqrt(d)
    return d

def display_img(img):
    x = np.reshape(img,(28,28))
    plt.imshow(x, cmap='gray')
    plt.show()

train_images = np.loadtxt('data/train_images.txt') # incarcam imaginile
train_labels = np.loadtxt('data/train_labels.txt', 'int') # incarcam etichetele avand
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')

obj = KnnClassifier(train_images,train_labels)
# n = len(test_images)
n = 10
print(n)
not_good = 0
for i in range(n):
    if (obj.classify_image(test_images[i]) != test_labels[i]):
        not_good +=1
print((n-not_good)/n*100)