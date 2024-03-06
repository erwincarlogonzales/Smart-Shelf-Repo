import cv2
import numpy as np

def bin_thresholds(weight_bin):

#30 minute intervals- Weight Bins 
    if weight_bin== 1:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 311, 66 #Top- Left Corner [Piattos]
        x2, y2= 381, 106 # Bottom- Right Corner [Piattos]

    if weight_bin==2:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 312, 104 #Top- Left Corner [Cream-O]
        x2, y2= 390, 136 # Bottom- Right Corner [Cream-O]

    if weight_bin==3:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 309, 138 #Top- Left Corner [Whattatops]
        x2, y2= 399, 171 # Bottom- Right Corner [Whattatops]

    if weight_bin==4:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 310, 213 #Top- Left Corner [Loaded]
        x2, y2= 382, 242 # Bottom- Right Corner [Loaded]

    if weight_bin==5:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 309, 240 #Top- Left Corner [Bingo]
        x2, y2= 386, 274 # Bottom- Right Corner [Bingo]

    if weight_bin==6:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 311, 280 #Top- Left Corner [Lemon Square Cheesecake]
        x2, y2= 391, 323 # Bottom- Right Corner [Lemon Square Cheesecake]

    if weight_bin==7:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1 = 219, 82  # Top-left corner [Water Bottles]
        x2, y2 = 281, 100  # Bottom-right corner [Watter Bottles]

    if weight_bin==8:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 215, 94 #Top- Left Corner [Zesto]
        x2, y2= 279, 117 # Bottom- Right Corner [Zesto]

    if weight_bin==9:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 209, 121 #Top- Left Corner [Beef Noodles]
        x2, y2= 286, 171 # Bottom- Right Corner [Beef Noodles]

    if weight_bin==10:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
        x1, y1= 225, 201 #Top- Left Corner [Mogu-Mogu]
        x2, y2= 291, 246 # Bottom- Right Corner [Mogu-Mogu]

    if weight_bin==11:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
         x1, y1= 208, 235 #Top- Left Corner [Zesto]
         x2, y2= 291, 266 # Bottom- Right Corner [Zesto]


    if weight_bin==12:
        # Define the coordinates for the top-left and bottom-right corners of the rectangle
         x1, y1= 201, 262 #Top- Left Corner [Pancit Canton Calamansi]
         x2, y2= 292, 332 # Bottom- Right Corner [Pancit Canton Calamansi]

# Continous CCTV
    if weight_bin== 1:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 338, 33 #Top- Left Corner [Piattos]
            x2, y2= 418, 86 # Bottom- Right Corner [Piattos]

    if weight_bin==2:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 339, 90 #Top- Left Corner [Cream-O]
            x2, y2= 422, 125 # Bottom- Right Corner [Cream-O]

    if weight_bin==3:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 337, 117 #Top- Left Corner [Whattatops]
            x2, y2= 427, 162 # Bottom- Right Corner [Whattatops]

    if weight_bin==4:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 338, 185 #Top- Left Corner [Loaded]
            x2, y2= 416, 216 # Bottom- Right Corner [Loaded]

    if weight_bin==5:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 334, 210 #Top- Left Corner [Bingo]
            x2, y2= 419, 260 # Bottom- Right Corner [Bingo]

    if weight_bin==6:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 337, 257 #Top- Left Corner [Lemon Square Cheesecake]
            x2, y2= 424, 311 # Bottom- Right Corner [Lemon Square Cheesecake]

    if weight_bin==7:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1 = 246, 25  # Top-left corner [Water Bottles]
            x2, y2 = 322, 74  # Bottom-right corner [Watter Bottles]

    if weight_bin==8:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 243, 69 #Top- Left Corner [Zesto]
            x2, y2= 313, 107 # Bottom- Right Corner [Zesto]

    if weight_bin==9:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 231, 100 #Top- Left Corner [Beef Noodles]
            x2, y2= 321, 161 # Bottom- Right Corner [Beef Noodles]

    if weight_bin==10:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 251, 184 #Top- Left Corner [Mogu-Mogu]
            x2, y2= 318, 221 # Bottom- Right Corner [Mogu-Mogu

    if weight_bin==11:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 247, 211 #Top- Left Corner [Zesto]
            x2, y2= 316, 249 # Bottom- Right Corner [Zesto]

    if weight_bin==12:
            # Define the coordinates for the top-left and bottom-right corners of the rectangle
            x1, y1= 240, 248 #Top- Left Corner [Pancit Canton Calamansi]
            x2, y2= 324, 313 # Bottom- Right Corner [Pancit Canton Calamansi]

    # Initialize a list to store the coordinates inside the rectangle
    coordinates_inside_rectangle = []

    # Iterate through the rectangle region and record the coordinates
    for y in range(y1, y2):
        for x in range(x1, x2):
            coordinates_inside_rectangle.append((x, y))

    return coordinates_inside_rectangle