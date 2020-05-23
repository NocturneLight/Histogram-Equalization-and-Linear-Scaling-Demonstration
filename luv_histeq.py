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

def _OpenCVHistogramEqualization(image, width1, height1, width2, height2):
    # Create a copy of the image argument for manipulation and
    # convert it to the LUV color channels.
    imgCopy = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)

    # Create a black image the size of the image slice.
    imgSlice = np.zeros(imgCopy.shape[:2], np.uint8)

    # Traverse each pixel of the image.
    for i in range(height1, height2 + 1):
        for j in range(width1, width2 + 1):
            # Store the l, u, and v channels of the pixel inside variables.
            l, u, v = imgCopy[i, j]

            # Next, we compute a grayscale value for the pixel.
            #grayValue = round(0.3 * l + 0.6 * u + 0.1 * v + 0.5)

            # Store the pixels inside the user-defined area in the image slice.
            imgSlice[i, j] = l #[l, u, v]

    # Equalize the image slice's luminescence channels using the built-in function.
    imgSlice = cv2.equalizeHist(imgSlice[:, :])
    
    # Place the equalized slice into the luminescence channels of all the pixels in the user
    # defined area of the image copy.
    imgCopy[height1:height2, width1:width2, 0] = imgSlice[height1:height2, width1:width2]

    # Convert the image back to BGR from LUV.
    imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_LUV2BGR)

    # Display the image.
    cv2.imshow(imageOutput + ": OpenCV Histogram Equalization Applied", imgCopy)

    # Write the output image to a file.
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

# Apply the OpenCV Histogram Equalization function to the copy image.
_OpenCVHistogramEqualization(inputImage, w1, h1, w2, h2)

# Wait for the user to press any key before destroying and exiting.
cv2.waitKey(0)
cv2.destroyAllWindows()
