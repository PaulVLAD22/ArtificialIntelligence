import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
train_images = np.loadtxt('data/train_images.txt') # incarcam imaginile
train_labels = np.loadtxt('data/train_labels.txt', 'int') # incarcam etichetele avand
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')
 #tipul de date int
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

# sa ris
# taci in mm

# from sklearn.naive_bayes import MultinomialNB
# naive_bayes_model = MultinomialNB()
# naive_bayes_model.fit(train_images, train_labels)
# score = naive_bayes_model.score(test_images, test_labels)
#
# print(score)

# num_bins = 5
# bins = np.linspace(start = 150, stop=190,num=num_bins)
# data = [(160,"F"), (165, "F"), (155, "F"), (172, "F"), (175, "B"), (180, "B"), (177, "B"), (190, "B")]
# print(bins)
#
# f = [i for (i,j) in data if j == "F"]
# b = [i for (i,j) in data if j == "B"]
#
#
# f_to_bins = np.digitize(f,bins)
# print(f_to_bins)
# b_to_bins = np.digitize(b,bins)
# print(b_to_bins)
#
# n_f_178 = len([i for i in f_to_bins if i == 3])
# n_b_178 = len([i for i in b_to_bins if i == 3])
# p_f_178 = n_f_178/(n_f_178+n_b_178)
# p_b_178 = n_b_178/(n_f_178+n_b_178)
# print(p_f_178)
# print(p_b_178)

# def values_to_bins(img,bins):
#     img_to_bins = np.digitize(img, bins) # returneaza pentru fiecare element intervalul
#     print(img_to_bins)
#
# num_bins = 3
# bins = np.linspace(start = 0, stop=255.1,num=num_bins)
# print(bins)
# x = np.reshape(train_images[0], (28, 28))
# values_to_bins(x,bins)
# for num_bins in [3,5,7,9,11]:
#     bins = np.linspace(start = 0, stop=255.1,num=num_bins)
#     naive_bayes_model = MultinomialNB()
#     naive_bayes_model.fit(train_images, train_labels,num_bins)
#     p = naive_bayes_model.predict(test_images)
#     print(p)
#     score = naive_bayes_model.score(test_images, test_labels)
#     print(score)


#5
num_bins = 5
naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(train_images, train_labels,num_bins)
p = naive_bayes_model.predict(test_images)
print(p)
score = naive_bayes_model.score(test_images, test_labels)
print(score)
for i in range(len(p)):
    if p[i] != test_labels[i]:
        print(i)