# Create import statements here.
import sys
import cv2
import numpy as np

# Create functions here.
def _CheckArgs():
    # If there are seven arguments, then we're good and can pass.
    if len(sys.argv) == 7:
        # Create local variables here.
        widthOne = float(sys.argv[1])
        heightOne = float(sys.argv[2])
        widthTwo = float(sys.argv[3])
        heightTwo = float(sys.argv[4])

        # Check for correctness of the dimension values. Exit if incorrect.
        if widthOne < 0 or heightOne < 0 or widthTwo > 1 or heightTwo > 1 or widthTwo <= widthOne or heightTwo <= heightOne:
            print("The arguments must satisfy the following: 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1.")
            
            print("Please try again.")
            
            sys.exit(0)

    # If there aren't 7 arguments, then we inform the user and then exit the program.
    else:
        print("Too few or too many arguments.\n Please include only an input and output file name, and 4 dimensions.")
        
        sys.exit(0)

def _ClassHistogramEqualization(image, width1, height1, width2, height2):
    # Create a counter to get the size of the image.
    imageSize = 0

    # Create a copy of the image argument for manipulation.
    imgCopy = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)

    # Create an entirely black image to use as a mask.
    #mask = np.zeros(image.shape[:2], np.uint8)

    # Fill the mask with white in the area we want a histogram of.
    #mask[height1:height2, width1:width2] = 255

    # Calculate the histogram by getting the number of occurrences of each value
    # in the luminosity channel.
    newHisto = _makeHistogram(imgCopy, width1, width2, height1, height2)

    # A 256x1 array that serves as a histogram. The index is a value
    # from 0 to 255. The value at the index is the number of times 
    # said index value occurs in the provided image slice.
    #histogram = cv2.calcHist([imgCopy], [1], mask, [256], [0, 256])

    # Traverse the user-selected area and get the number 
    # of pixels in the program.
    for i in range(height1, height2 + 1):
        for j in range(width1, width2 + 1):
            imageSize += 1
    
    # Apply histogram equalization to the retrieved histogram and
    # store it in the equalHisto list.
    equalHisto = _EqualizeHistogram(newHisto, imageSize)

    # Traverse the user-defined area of the image.
    for i in range(height1, height2 + 1):
        for j in range(width1, width2 + 1):
            # Get just the luminance channel since that
            # is all we're concerned with here.
            y = image[i, j][1]

            # Replace the current luminance values in the image
            # with the equalized values.
            imgCopy[i, j][1] = equalHisto[y]

    # Convert the image back to BGR from the XYZ color space.
    imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_XYZ2BGR)

    # Show the manipulated image on screen.
    cv2.imshow(imageOutput + ": Histogram Equalization Applied", imgCopy)

    # Write the output image to a file.
    cv2.imwrite(imageOutput, imgCopy)


def _makeHistogram(image, width1, width2, height1, height2):
    # Create a list of size 256.
    histogram = [0] * 256

    # Traverse the user-defined area of the image.
    for i in range(height1, height2 + 1):
        for j in range(width1, width2 + 1):
            # Get the values of the pixel in each channel.
            x, y, z = image[i, j]

            # Depending on the number we get, increment that spot 
            # in the array by one.
            histogram[y] += 1

    # Return our newly formed histogram.
    return histogram


def _EqualizeHistogram(histo, imageSize):
    # Create variables here.
    equalizedList = []
    prevNum = 0

    # Traverse the histogram and find the number of pixels in range and
    # then apply the equalization equation.
    for value in histo:
        # Calculate the number of pixels in the range between 0 and now.
        sumVal = value + prevNum
    
        # Calculate the equalization value and then floor it.
        #equalizeResult = np.floor(((prevNum + sumVal) / 2) * (256 / imageSize))
        equalizeResult = np.floor((256 * (prevNum + sumVal)) / (2 * imageSize))

        # Clamp the value if greater than 255 or less than 0.
        if equalizeResult > 255:
            equalizeResult = 255
        elif equalizeResult < 0:
            equalizeResult = 0

        # Append the value to the list unchanged.
        equalizedList.append(equalizeResult)
        
        # Store the current number for use on the next iteration.
        prevNum = sumVal
        
    # Return the newly equalized histogram.
    return equalizedList
  

# Check the command line arguments.
_CheckArgs()

# Create variables here since all values are correct.
imageInput = sys.argv[5]
imageOutput = sys.argv[6]
widthOne = float(sys.argv[1])
widthTwo = float(sys.argv[3])
heightOne = float(sys.argv[2])
heightTwo = float(sys.argv[4])


# Retrieve the input image.
inputImage = cv2.imread(imageInput, cv2.IMREAD_COLOR)

# Inform the user and then exit if there is nothing in the variable.
if inputImage is None:
    print("There was a problem with reading the file. Please try again.")

    sys.exit(0)

# Show the unedited image on-screen for later comparison.
# The first argument is the title of the window. The second
# argument is the image to open.
cv2.imshow("Input Image: " + imageInput, inputImage)

# Now we convert our dimension values to pixel locations.
rows, columns, bands = inputImage.shape
w1 = round(widthOne * (columns - 1))
h1 = round(heightOne * (rows - 1))
w2 = round(widthTwo * (columns - 1))
h2 = round(heightTwo * (rows - 1))

# Apply the OpenCV Histogram Equalization function to the copy image.
_ClassHistogramEqualization(inputImage, w1, h1, w2, h2)

# Wait for the user to press any key before destroying and exiting.
cv2.waitKey(0)
cv2.destroyAllWindows()
