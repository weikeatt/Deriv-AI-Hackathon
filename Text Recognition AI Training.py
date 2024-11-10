import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df=pd.read_csv("A_Z Handwritten Data.csv")
alphabets = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
data_array = np.array(df,dtype=np.uint8)

labels = data_array[:,0]
#print(len(labels))
x = data_array[:,1:].reshape(372450,28,28)/255.
# print((data_array[:,1:]).shape)
#del data_array
unique, counts = np.unique(labels, return_counts=True)
alphabets_list = list(zip(alphabets, counts))
# for i in alphabets_list:
#     print(i[0],' : ',i[1])

# fig=plt.figure(figsize=(15,6))
# plt.xlabel('Alphabets',fontsize=14)
# plt.ylabel('Count of datapoints for each alphabet',fontsize=14)
# plt.bar(alphabets,counts)
# plt.show()


a=np.random.randint(low=0,high=372449,size=400)
fig=plt.figure(figsize=(30,30))
c=1
for i in a:
    fig.add_subplot(20,20,c)
    plt.xticks([]);    plt.yticks([]);    plt.imshow(x[i],cmap='gray')
    c+=1
del a

del c, alphabets_list, counts, unique #deleting further not required variables due to memory issues 

from sklearn.model_selection import train_test_split as train_test_split

#x=x.reshape(372450,28,28,1)
x_train,x_test,y_train,y_test = train_test_split(x,labels,test_size=0.01)
# print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)


from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense,Dropout
from keras.layers import Flatten
from keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adadelta
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import load_model

nn_model = Sequential([Conv2D(128,(3,3),activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1),padding='same'),
                    Conv2D(64,(3,3),activation='relu', kernel_initializer='he_uniform',padding='same'),
                    MaxPooling2D(2,2),
                    Conv2D(64,(3,3),activation='relu', kernel_initializer='he_uniform',padding='same'),
                    Conv2D(64,(3,3),activation='relu', kernel_initializer='he_uniform',padding='same'),
                    BatchNormalization(),
                    MaxPooling2D(2,2),
                    Flatten(),
                    Dense(100,activation='relu',kernel_initializer='he_uniform'),
                    Dropout(0.1),
                    Dense(64,activation='relu',kernel_initializer='he_uniform'),
                    Dropout(0.125),
                    BatchNormalization(),
                    Dense(26,activation='softmax')])
nn_model.compile(loss='sparse_categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9),metrics=['accuracy'])
nn_model.summary()

nn_model_fit = nn_model.fit(x=x_train,y=y_train,validation_split=0.1,epochs=1)
nn_model.save('handwritten_alphabet_model.h5')
print("Model saved successfully!")

# nn_model = load_model('handwritten_alphabet_model.h5')

def test_images(n=225):
    index=np.random.randint(low=0,high=3720,size=n)
    fig=plt.figure(figsize=(30,40))
    for i in range(n):
        [pred]=nn_model.predict(x_test[index[i]].reshape(1,28,28,1))
        pred=np.argmax(pred)
        actual=y_test[index[i]]
        fig.add_subplot(15,15,i+1)
        plt.xticks([])
        plt.yticks([])
        if actual==pred:
            plt.title(alphabets[pred],color='green',fontsize=25,fontweight="bold")
        else:
            plt.title(alphabets[pred],color='red',fontsize=25,fontweight="bold")
        plt.imshow(x_test[index[i]].reshape(28,28),cmap='gray')

    plt.show()

test_images()


import cv2
alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
def unseendata_test(filepath):
    image = cv2.imread(filepath)
    blur_image=cv2.medianBlur(image,7)

    grey = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(grey,200,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,41,25)

    contours,hierarchy= cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    preprocessed_digits = []

    
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),key=lambda b:b[1][0], reverse=False))


    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        
        cv2.rectangle(blur_image, (x,y), (x+w, y+h), color=(255, 0, 0), thickness=2)
        
        digit = thresh[y:y+h, x:x+w]
         
        resized_digit = cv2.resize(digit, (18,18))
        
        padded_digit = np.pad(resized_digit, ((5,5),(5,5)), "constant", constant_values=0)
        
        preprocessed_digits.append(padded_digit)
    # plt.xticks([])
    # plt.yticks([])
    # plt.title("Input Image",color='red')
    # plt.imshow(image, cmap="gray")
    # plt.show()

    inp = np.array(preprocessed_digits)
    figr=plt.figure(figsize=(len(inp),4))
    i=1
    alphabets_unseen=[]
    for digit in preprocessed_digits:
        [prediction] = nn_model.predict(digit.reshape(1, 28, 28, 1)/255.)
        pred=alpha[np.argmax(prediction)]
        alphabets_unseen.append(pred)
        figr.add_subplot(1,len(inp),i)
        i+=1
        plt.xticks([])
        plt.yticks([])
        plt.imshow(digit.reshape(28, 28), cmap="gray")
        plt.title(pred,color='green',fontsize=18,fontweight="bold")
    print("Alphabets detected : " ,*alphabets_unseen)


unseendata_test('name.png')