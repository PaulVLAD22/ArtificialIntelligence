import numpy as np
import matplotlib.pyplot as plt
from skimage import io
'''
p_list =[1,2,3]

a = np.array([1,2,3])

print(a)

print(a.dtype)

b=np.array([[1,2,3],[4,5,6]])

print(b.shape)#2 pe 3

print(b[1,2]) # b[1][2]

print(b[1])

print(np.ones((2,3)))

print(np.eye(5))
# I5 matricea

print(np.full((3,4),9))
# matrice de 3 4 plina de 9

np.random.random((2,3))*100
#o variabila discreta random cred

norm=np.random.normal(100,15,(4,5)).astype(int)
print(norm)
print(norm[:3,3:])

print(np.arange(0,100,5))

for idx,val in enumerate([1,4,6]):
    print(idx,val)

#slice-eul este o referinta

sub_norm = norm[1:3,1:4]

print(sub_norm)

sub_norm[0,1]=1000

print(sub_norm,norm)

print(np.ravel(norm))
# o sg linie

print(np.reshape(norm,(2,10)))
# face matrice de 4 5 in de 2 pe 10

norm.flatten()
#o singura linie

print(norm[[0,1],[0,1]]) #elem 0 0 si 1 1

sir = np.arange(0,20)

print( sir % 2 ==1)
# pt fiecare element aplica % 2 == 1 (returneaza bool)

print(norm[True])
# nu stiu ce face exact

print(norm[False])
# nu situ


x = np.array ([[1,2],[3,4]])
y = np.array ([[5,6],[7,8]])

print(x*y) # inmulteste fiecare element cu fiecare , nu e inmultirea normala a matricelor
#aplica pe toata matricea
np.sqrt(x)

#inmultirea matricilor
np.matmul(x,y)

#transpusa matricei X
x.T

#inversul
np.linalg.inv(x)

#suma tuturor
np.sum(norm)

#suma axei 1
np.sum(norm,axis=0)


#matplotlib
x=np.arange(0,3*np.pi,0.1)
y_1=np.sin(x)
y_2=np.cos(x)

plt.plot(x,y_1,'g')
plt.plot(x,y_2,'r')
plt.show()
'''
plt.imshow(np.load('./lab1/images/car_6.npy').astype(np.uint8),cmap='gray')
plt.show()
#mai uite te tu


#ex
#a
imgs = np.zeros((9, 400, 600))
for i in range(0, 9):
    imgs[i] = np.load(f'lab1./images/car_{i}.npy')
print(imgs)
print('\n'*10)
#b
print(np.sum(imgs,axis=(1,2))) # luam dor axa 0 , imgs fiind de 3 axe
#adica il impartim in 9 vectori
print('\n'*10)
#c
for i in range (0,9):
    print(sum(imgs[i]))
print('\n'*10)
#d
print(np.argmax(np.sum(imgs, axis=(1, 2))))
print('\n'*10)
#e
mean_image = np.mean(imgs, axis = 0) 
io.imshow(mean_image.astype(np.uint8))
io.show()

print('\n'*10)
#e
print(np.std(imgs))
print('\n'*10)
#h
sliced = imgs[:, 200:300, 280:400]

# np argmax (norm) returneaza index-ul celui cel mai mic elem
