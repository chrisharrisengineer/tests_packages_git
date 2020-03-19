#use python 3.6 - run from fast.ai environment
#!/home/bha/fastai36/bin/activate
import os
import glob
import sys
from fastai.vision import *
import numpy as np
from PIL import Image, ImageDraw
import matplotlib
matplotlib.use('TkAgg')
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import cv2
from statsmodels.tsa.filters import hp_filter
from natsort import natsorted, ns
import time
from __main__ import *


def tube_ready_not_ready_function():
    #print('in function')
    #path to all
    path = Path('analysis')

    #path for non live testing
    #picture_path = Path('clotting_test_2')

    #path for live test
    picture_path= Path('cropped_pics')

    #path_to_IMG = Path(/home/llu-2/Desktop/lluFolder/masterProgram/01_26_19/cropped)


    classes = ['tube_ready','tube_not_ready' ]

    full_clot_probability_array = []
    frame_number = 1

    full_path = Path("analysis/cropped_pics")

    endpoint = []
    frame_endpoint_time = []
    endpoint_final_frame_number = []
    #clotting_endpoint_time = []

    #numpy rolling averages function
    def movingaverage (values, window):
        weights = np.repeat(1.0, window)/window
        sma = np.convolve(values, weights, 'valid')
        return sma

    clotting_endpoint_time = 0
    num_analysis_done = 0
    seconds_array = [] 
    endpoint_from_trend = 0

    #make graph object
    fig, ax = plt.subplots()





    while True:
        if num_analysis_done == len(os.listdir(path/picture_path)):
            time.sleep(1)
            if num_analysis_done == len(os.listdir(path/picture_path)):
                time.sleep(1)
                if num_analysis_done == len(os.listdir(path/picture_path)):
                    files = glob.glob('/home/chris/Desktop/Soluble_Fibrin/analysis/cropped_pics/*')
                    for f in files:
                        os.remove(f)
                    break

        files = natsorted(os.listdir(path/picture_path))
        filename = files[num_analysis_done]   

        img = open_image(path/picture_path/filename)
        


        learn = load_learner(path, file='export_tube_not_ready_mar12.pkl')
  
        pred_class,pred_idx,outputs = learn.predict(img)
        #print(filename)

        #pred_class2,pred_idx2,outputs2 = learn.predict(imgM2)

        #this_image = os.path.join('/home/bha/Desktop/lluFolder/masterProgram/01_26_19/analysis/cropped_pics', filename)
        this_image = os.path.join('/home/chris/Desktop/Soluble_Fibrin/analysis/cropped_pics', filename)
        image_read = cv2.imread(this_image)
        

        resized_image = cv2.resize(image_read, (1800, 400))
        #resized_image = cv2.resize(image_read, (1200, 250))
        #cv2.imshow("Tube Ready / Not ready", resized_image)   

        #convert torch.Tensor to nparray
        #print(type(outputs))
        tensor_to_np = outputs.numpy()
        #print(tensor_to_np)
    
        #grab clot probability from each output
        grab_clot_probability = 1 - tensor_to_np[0]
        #print(grab_clot_probability)
    
        #add each new clot probability to end of array
      
        full_clot_probability_array.append(grab_clot_probability)
        #print("probability array is")
        #print(full_clot_probability_array)

        #get seconds for each frame, extract first whole integer set before .extension in "image"
        file = filename
        seconds = None
        position = file.index('.')
        #gets filename position two before last(.) until last(.)                      
        seconds = filename.split('.')
        seconds = seconds[1] + '.' + seconds[2]
        seconds = float(seconds)
        seconds_array.append(seconds)
   

        plt.title('Tube Ready / Not Ready')
        #mngr = plt.get_current_fig_manager()
        #mngr.window.SetPosition(0,0)   
        #plt.xticks(np.arange(min(seconds_array), max(seconds_array)+1, 1.0))
        plt.plot(seconds_array, full_clot_probability_array)	
        plt.get_current_fig_manager().window.wm_geometry("+1300+0") # move the window    
        plt.draw()
        plt.pause(.001)	
    


        #smooth graph/remove noise with hp filter; store the smoothed values in "trend", and plot on same graph
        if frame_number > 1:
            cycle, trend = hp_filter.hpfilter(full_clot_probability_array, lamb=100000)
            #print("trend is")
            #print(trend[-1])
            plt.plot(seconds_array, trend)
            plt.draw()
            plt.pause(.001)
            plt.clf()
    
        #numpy rolling average
        if frame_number > 1:
            clot_moving_average = movingaverage(full_clot_probability_array, 20)
            plt.plot(clot_moving_average)
            plt.draw()



        #use trend to find endpoint
        if frame_number >1 and endpoint_from_trend==0 and trend[-1] > .5:
            endpoint_from_trend = seconds_array[-1]
                       
           
        if endpoint_from_trend!=0:
            #print("endpoint frame is")  
            #print(endpoint_final_frame_number)       
            plt.axvline(x=endpoint_from_trend, color='r', linestyle='--')
            #stdout = sys.stdout.write(str(endpoint_from_trend))        
            break
   
        num_analysis_done = num_analysis_done +1
        frame_number = frame_number + 1

    endpoint_from_trend = str(endpoint_from_trend)
    sys.stderr.write(endpoint_from_trend)


tube_ready_not_ready_function()


