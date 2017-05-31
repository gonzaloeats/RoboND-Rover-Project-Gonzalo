## Project: Search and Sample Return

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[image4]: ./misc/fidelity_proof.jpg
[image5]: ./misc/perception_bit.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

For the most part Jupyter Notebook was plug and play from the classroom instructions. Figuring out how the maps displayed on the video took me a long time. The openCV img.shape method was tricky to understand. I received plenty of help from other mentors and started getting comfortable with the opencv documentation.

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

For some reason I was unable to get my videos to record for loner then 6 seconds. My code finally started producing videos, though a few times I had to experiment with manually changing semi colons to colons. What was most odd was that it worked fin with the default test data but everything would break when I recorded new test data. Usually it had to do with incompatible data types. As soon as I restored to the original simulator I was able to create movies. But I was still not able to figure out how to make them longer. 

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

![alt text][image5]
I've taken a few python tutorials each have mentioned classes, but it hasn't been until this project that I've really wrapped my head around the concept. I've attached this bit of code because it was how I was able to increase fidelity. I was able to use layers and use a bitwise operator(never used before) to achieve more well over the required fidelity. Early in my runs I was able to get as high as 80 percent but it steadily decreased as the robot kept mapping over portions of the world it had already mapped. The key would have been to figure out how to not double back on areas already mapped.

Initially I thought tweaks to the decision_step() would improve fidelity but once I created an algorithm with the inputs from the rover class to update the controls that managed to make sure the robot did not get suck any where and generally steered 4 degrees by default I was able to get him to explore most of the environment. 
And the perception step and tunning down the threshold for mappable areas proved to be the right strategy.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup. 

![alt text][image4]


Finally I was able to get above 60% fidelity. The rocks were easy to point out, and mapping the terrain wasn't difficult once I figured out how to keep the robot from getting stuck. This project proved to be quite a challenge for me. With a little bit of help with the perception code from one the mentors I was able to get the right threshold to properly update my map. I think I could still map a bit faster and more accurate if I improve the decision code a bit further. It took me a while to figure out I needed to stop turn the go to escape from the rocks. I wanted to add a dithering element to the movements as to more effectively get unstuck but I had a difficult time just meeting the minimum requirements.

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.** 

I used 720x480 resolution at fantastic at 25 frames per second in the rover environment to produce passing results. The different version of the simulator played havoc on my system. I was not initially effected by the memory leak or the semi colons vs colons, but only after spending hours revising my perception code did I realize I wasn't unable to get autonomous running because some part of the simulator was hanging up after each trail. It made it difficult to tell if I was making proper changes to my code. I did not only have to restart the drive.py but I had to close all my terminals and start them back up for my changes in the code to take effect. Once I got everything working, the following day the simulator changed and it broke my code in the jupyter notebook. I ended up having to uninstall the new version of the rover and run the original to get anything to work.

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further. 

This was a pretty intensive learning experience for me, I was able to see how object oriented programing really works. Rover was the first class I've ever used and applied outside a tutorial context. I was impressed by the use of decorators and how everything came together. At first I had no idea how everything worked but little by little I was able to start putting things together. I did end up wasting a lot of time just trying to get the autonomous mode to work. I lost a few hours due to glitches between the programs but thankfully I was eventually able to spot issues, and did a lot of learning on the way. In the future I would like to figure out a way to actually collect the rocks. Also I would like to display the robot's position on the map.





