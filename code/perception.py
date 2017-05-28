import numpy as np
import cv2

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

# Define a function to convert to rover-centric coordinates
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to apply a rotation to pixel positions
def rotate_pix(xpix, ypix, yaw):
    # TODO:
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    # Apply a rotation
    xpix_rotated = xpix * np.cos(yaw_rad) - ypix * np.sin(yaw_rad)
    ypix_rotated = xpix * np.sin(yaw_rad) + ypix * np.cos(yaw_rad)
    # Return the result  
    return xpix_rotated, ypix_rotated

# Define a function to perform a translation
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # TODO:
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    dst_size =5
    bottom_offset =6
    source = np.float32([[47, 128], [283 ,133],[202, 96], [125, 96]])
    destination = np.float32([[Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - bottom_offset],
                  [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - bottom_offset],
                  [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset], 
                  [Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],
                  ])
    # 2) Apply perspective transform
    birds_view = perspect_transform(Rover.img, source, destination)
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    thresholded_terrain = color_thresh(birds_view, rgb_thresh=(220, 220, 200))
    thresholded_obstacles = color_thresh(birds_view, rgb_thresh=(90, 90, 90))
    thresholded_rocks = color_thresh(birds_view, rgb_thresh=(100,100,100))
     # 4) Update Rover.vision_image (this will be displayed on left side of screen)
    Rover.vision_image[:,:,0] = thresholded_terrain * 255
    Rover.vision_image[:,:,1] = thresholded_rocks * 255
    Rover.vision_image[:,:,2] = thresholded_obstacles * 255
    # 5) Convert map image pixel values to rover-centric coords
    terrain_xpix, terrain_ypix = rover_coords(thresholded_terrain)
    obstacles_xpix, obstacles_ypix = rover_coords(thresholded_obstacles)
    rocks_xpix, rocks_ypix = rover_coords(thresholded_rocks)
    # 6) Convert rover-centric pixel values to world coordinates
    scale = 10    
    worldmap = np.zeros((200, 200))
    obstacle_world = pix_to_world(obstacles_xpix, obstacles_ypix, Rover.pos[0], Rover.pos[1], Rover.yaw, 200, scale)
    rock_world = pix_to_world(rocks_xpix, obstacles_ypix, Rover.pos[0], Rover.pos[1], Rover.yaw, 200, scale)
    navigable_world = pix_to_world(terrain_xpix, terrain_ypix, Rover.pos[0], Rover.pos[1], Rover.yaw, 200, scale)
    # 7) Update Rover worldmap (to be displayed on right side of screen)
        # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    Rover.worldmap[terrain_y_world, terrain_x_world, 2] +=1
    Rover.worldmap[obstacles_y_world, obstacles_x_world, 0] +=1
    Rover.worldmap[rocks_y_world, rocks_x_world, 1] +=1
    
    
    # 8) Convert rover-centric pixel positions to polar coordinates

    # Update Rover pixel distances and angles
    Rover.nav_dists, Rover.nav_angles = to_polar_coords(xpix2, ypix2)
    
 
    
    
    return Rover