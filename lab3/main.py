# from math import sqrt
# import numpy as np
# import matplotlib.pyplot as plt
#
# class KnnClassifier:
#     def __init__(self, train_images, train_labels):
#         self.train_images = train_images
#         self.train_labels = train_labels
#
#     def classify_image(self, test_image, num_neighbors = 3, metric ='l2'):
#
#         distances = []
#         for i in range(len(self.train_images)):
#             x = distance(self.train_images[i],test_image,metric)
#             distances.append((x,self.train_labels[i]))
#         distances.sort(key=lambda a : a[0])
#         neighbours = []
#         labels = {}
#         for i in range(num_neighbors):
#             neighbours.append(distances[i])
#             if distances[i][1] not in labels.keys():
#                 labels[distances[i][1]] = 1
#             else:
#                 labels[distances[i][1]] += 1
#         #print(neighbours)
#         print(labels)
#         l = [(labels[i],i) for i in labels.keys()]
#         m = max(l,key=lambda a : a[0])
#         return m[1]
#
# def distance(img1,img2,metric = 'l2'):
#     d = 0
#     for i in range(len(img1)):
#         if metric == 'l2':
#             d += (img1[i]-img2[i])**2
#         else:
#             d += abs(img1[i] - img2[i])
#     if metric == 'l2':
#         d = sqrt(d)
#     return d
#
# def display_img(img):
#     x = np.reshape(img,(28,28))
#     plt.imshow(x, cmap='gray')
#     plt.show()
#
# train_images = np.loadtxt('data/train_images.txt') # incarcam imaginile
# train_labels = np.loadtxt('data/train_labels.txt', 'int') # incarcam etichetele avand
# test_images = np.loadtxt('data/test_images.txt')
# test_labels = np.loadtxt('data/test_labels.txt', 'int')

#
# # n = len(test_images)
# n = 10
# print(n)
# not_good = 0
# for i in range(n):
#     if (obj.classify_image(test_images[i]) != test_labels[i]):
#         not_good +=1
# print((n-not_good)/n*100)
# with open("predictii_3nn_l2_mnist.txt","w") as g:
#     obj = KnnClassifier(train_images,train_labels)
#     n = len(test_images)
#     not_good = 0
#     for i in range(n):
#         c = obj.classify_image(test_images[i])
#         g.write(str(c)+" "+str(test_labels[i])+'\n')
#         if (c != test_labels[i]):
#              not_good +=1
#     print((n - not_good) / n * 100)





        # x = np.reshape(test_images[i], (28, 28))
        # plt.imshow(x, cmap='gray')
        # plt.show()

import sklearn.datasets as datasets
import numpy as np

class KnnRegressor:

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def classify_sample(self, t, num_neighbors=3, metric='l2'):
        if metric == 'l1':
            distances = np.sum(abs(self.X - y), axis=1)
        else:
            distances = np.sqrt(np.sum((self.X - y) ** 2, axis=1))

        indx = np.argsort(distances)
        vec = indx[:num_neighbors]  # vecinii
        label_vecini = self.y[vec]
        print(vec)
        # CODE GOES HERE
        result = sum(self.X[vec])/len(self.X[vec])

        return result

    def classify_samples(self, ts, num_neighbors=3, metric='l2'):
        nr = ts.shape[0]
        predict = np.zeros(nr, np.int)

        for i in range(nr):
            predict[i] = self.classify_sample(ts[i, :], num_neighbors=num_neighbors, metric=metric)

        return predict

x,y = datasets.load_boston(return_X_y=True)
# print(x,y)
knn = KnnRegressor(x,y)
print(knn.classify_sample(x[0]))