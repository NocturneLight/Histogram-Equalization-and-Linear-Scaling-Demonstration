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

def _HistogramStretch(image, width1, height1, width2, height2):
    # Create a copy of the image argument for manipulation and
    # convert it to the XYZ color channels.
    imgCopy = cv2.cvtColor(image, cv2.COLOR_BGR2XYZ)
    
    # Get the user-defined portion of the image.
    imgSlice = imgCopy[height1:height2, width1:width2]

    # Get the min and max values in the portion of the 
    # image and store them for later use.
    minNum, maxNum = cv2.minMaxLoc(imgSlice[1])[:2]

    # Traverse the image to perform linear scaling.
    for i in range(height1, height2 + 1):
        for j in range(width1, width2 + 1):
            # Get the luminosity value of the pixel we're on and 
            # store it in a variable for convenience.
            y = imgCopy[i, j][1]

            # Calculate the linear stretching value using the luminance value.
            linStretch = (((y - minNum) * (255 - 0)) / (maxNum - minNum)) + 0
            
            # If the number exceeds 255, set the value to 255.
            if linStretch > 255: 
                linStretch = 255
            # If the number is less than 0, set the value to 0.
            elif linStretch < 0:
                linStretch = 0
            
            # Replace the luminance value in the image copy with the new
            # value calculated through linear stretching.
            imgCopy[i, j][1] = linStretch

    # Convert the image copy from XYZ back to BGR.
    imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_XYZ2BGR)

    # Display the newly manipulated image copy.
    cv2.imshow(imageOutput + ": Linear Scaling Applied", imgCopy)

    # Save the manipulated image to a file in the same
    # directory as this program.
    cv2.imwrite(imageOutput, imgCopy)


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

# Apply linear scaling/histogram stretching to the copy image.
_HistogramStretch(inputImage, w1, h1, w2, h2)

# Wait for the user to press any key before destroying and exiting.
cv2.waitKey(0)
cv2.destroyAllWindows()
