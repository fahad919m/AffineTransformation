import cv2
import numpy as np

#Read source image and it size
mainImg = cv2.imread("homewithpoints.jpg")
rows, cols, ch = mainImg.shape

#identify the two triangles
FirstMatrix = np.float32([[375.0, 102.0, 1.0,0,0,0],[244.0, 193.0, 1.0,0,0,0],[503.0, 193.0, 1.0,0,0,0],[0,0,0,375.0, 102.0, 1.0]
                        ,[0,0,0,244.0, 193.0, 1.0],[0,0,0,503.0, 193.0, 1.0]])
SecondMatrix = np.float32([188.0,290.0,210.0,207.0,200.0,284.0])

#finding the transformation Matrix
transformMatrix = np.float32(np.linalg.inv(FirstMatrix).dot(SecondMatrix))


#rearrange transformation Matrix
transformMatrixArranged = np.float32([[transformMatrix[0],transformMatrix[1],transformMatrix[2]],
                   [transformMatrix[3],transformMatrix[4],transformMatrix[5]],
                   [0,0,1]])

#finding the inverse of the transformation matrix
invsOfTransMatrix = np.array(np.linalg.inv(transformMatrixArranged))


#find the size of the destination image
def findSize(transMatrix,max_x,max_y):
    for i in range(0,rows):
        for j in range(0,cols):
            y = i * transMatrix[0] + j * transMatrix[1] + transMatrix[2]
            x = i * transMatrix[3] + j * transMatrix[4] + transMatrix[5]
            if x > max_x:
                xresult = x
            if y >max_y:
                yresult = y

    return xresult,yresult


max_x,max_y = findSize(transformMatrix,0,0)


#initialize the destination image with the size we found
result_img = np.zeros((int(max_x),int(max_y), 3))
height, width, c = result_img.shape

#finding the corresponding coordinates
def findingCoords(u, v, invMatrixCopy):
    x = v * invMatrixCopy.item(3) + u * invMatrixCopy.item(4) + invMatrixCopy.item(5)
    y = v * invMatrixCopy.item(0) + u * invMatrixCopy.item(1) + invMatrixCopy.item(2)
    return x, y


#check if its inside the limits or not
def insideTheLimits(cor1, cor2 , nRows, nCols):
    return (cor1 >= 0 and cor1 < nRows and cor2 >= 0 and cor2 < nCols)


#loop through destination image and copy colors
for specH in range(0, height):
    for specW in range(0, width):
        x, y = findingCoords(specH, specW, invsOfTransMatrix)
        if insideTheLimits(x, y, rows,cols):
            result_img[specH, specW, 0] = mainImg[int(x), int(y), 0]
            result_img[specH, specW, 1] = mainImg[int(x), int(y), 1]
            result_img[specH, specW, 2] = mainImg[int(x), int(y), 2]



#save the result
cv2.imwrite('resultedPic.png', result_img)

