import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
train_images = np.loadtxt('train_images.txt') # incarcam imaginile
train_labels = np.loadtxt('train_labels.txt', 'int') # incarcam etichetele avand
test_images = np.loadtxt('test_images.txt')
test_labels = np.loadtxt('test_labels.txt', 'int')

# image = train_images[0, :] # prima imagine
# image = np.reshape(image, (28, 28))
# plt.imshow(image.astype(np.uint8), cmap='gray')
# plt.show()
# num_bins = 255
# x = np.reshape(train_images[0],(28,28))
# bins = np.linspace(start=0, stop=255, num=num_bins) # returneaza intervalele
# print(bins)
# x_to_bins = np.digitize(x, bins) # returneaza pentru fiecare element intervalul
# print(x_to_bins)
# # plt.imshow(x_to_bins, cmap='gray')
# # plt.show()
# # plt.show()
# # # # # print(x_to_bins)
# #
# # # print(np.reshape(train_images[1],(28,28)))
# # for i in [[int(i) for i in j] for j in np.reshape(train_images[0],(28,28))]:
# #     print(*i)


#ex1

bins = np.linspace(start = 150, stop=190,num=5)
input = [(160,"F"), (165, "F"), (155, "F"), (172, "F"), (175, "B"), (180, "B"), (177, "B"), (190, "B")]
f=[]
b=[]
for h,g in input:
    if (g=="F"):
        f.append(h)
    else:
        b.append(h)
f_interval = np.digitize(f,bins)
b_interval = np.digitize(b,bins)
n_f,n_b = 0,0
for i in (f_interval):
    if (i==3):
        n_f+=1
for j in (b_interval):
    if (j==3):
        n_b+=1
pF = n_f/(n_f+n_b)
pB=n_b/(n_f+n_b)

# p_f_178 = n_f_178/(n_f_178+n_b_178)
# p_b_178 = n_b_178/(n_f_178+n_b_178)
# print(p_f_178)
# print(p_b_178)

#
# #exercitiul 2
# def values_to_bins(img,bins):
#     img_to_bins = np.digitize(img, bins) # returneaza pentru fiecare element intervalul
#     print(img_to_bins)
#
# num_bins = 3
# bins = np.linspace(start = 0, stop=255,num=num_bins)
# print(bins)
# x = np.reshape(train_images[0], (28, 28))
# values_to_bins(x,bins)


#ex 3
num_bins=5
bins = np.linspace(start = 0, stop=255,num=num_bins)
naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(train_images, train_labels,num_bins)
p = naive_bayes_model.predict(test_images)
score = naive_bayes_model.score(test_images, test_labels)
print(score)




for num_bins in [3,5,7,9,11]:
    bins = np.linspace(start = 0, stop=255.1,num=num_bins)
    naive_bayes_model = MultinomialNB()
    naive_bayes_model.fit(train_images, train_labels,num_bins)
    p = naive_bayes_model.predict(test_images)
    score = naive_bayes_model.score(test_images, test_labels)
    print(score)


#5
num_bins = 5
naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(train_images, train_labels,num_bins)
p = naive_bayes_model.predict(test_images)
score = naive_bayes_model.score(test_images, test_labels)
for i in range(len(p)):
    if p[i] != test_labels[i]:
        print(i)


#solutii laborator

