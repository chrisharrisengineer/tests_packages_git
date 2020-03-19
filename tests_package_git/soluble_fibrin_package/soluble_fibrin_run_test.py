#soluble_fibrin_run_test
import os, sys
import subprocess

#go up two folders and add all to path
p = os.path.abspath('../..')
if p not in sys.path:
    sys.path.append(p)

#import needed analysis functions and activate their environments
#from tests_package.tube_ready_not_ready_analysis_convert_to_function import tube_ready_not_ready_function
#from tests_package.Tensorflow.models.research.object_detection.object_detection_image_soluble_fibrin_to_function import soluble_fibrin_object_detection_function

#import object_detection_image_soluble_fibrin

tube_ready_seconds = 0

#initiate tube_ready_not_ready test
#from current folder

#this goes into all analysis functions

#for testing
path_to_images = '/Soluble_Fibrin/analysis/cropped_pics'



def get_endpoint_from_obj_detection(soluble_fibrin_input):

    #get actual endpoint from soluble fibrin endpoint, currently its everything that gets printed
    # go backwards in soluble_fibrin_endpoint, storing everything until the n
    soluble_fibrin_endpoint = soluble_fibrin_input

    soluble_fibrin_endpoint = str(soluble_fibrin_endpoint)
    endpoint_list = list(soluble_fibrin_endpoint) 

    endpoint = []
    #soluble_fibrin_endpoint = split[-1]
    for element in reversed(endpoint_list):
        if element == 'n':
            break
        else:    
            endpoint.append(element)
                     
    endpoint.reverse()
    #take off last " ' "
    endpoint = endpoint[:-1]
    #concatenate list into string
    concatenated_endpoint = ""
    for element in endpoint:  
        concatenated_endpoint += element    

    print("soluble fibrin endpoint")
    print(concatenated_endpoint)     



def run_soluble_fibrin_test(path_to_images):
    print("in run soluble fibrin test")
    
    #get seconds back that tube is ready
    #run a subprocess, activate that environment, get value back
    tube_ready_subprocess = subprocess.Popen(["/home/chris/anaconda3/envs/fastai/bin/python3.7", "tube_ready_not_ready_analysis_convert_to_function.py"], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)    
    tube_ready_seconds = (tube_ready_subprocess.communicate()[0])
    #tube_ready_seconds = str(tube_ready_seconds)
    print("tube ready seconds is")
    print(tube_ready_seconds)

   
    
    #start soluble fibrin object detection subprocess
    #tube_ready_text = open("tube_ready_seconds.txt", "w")
    #n = tube_ready_text.write(tube_ready_seconds)
    #tube_ready_text.close()
    file_std_out = open("stdout.txt", "w")
    
    soluble_fibrin_obj_det_subprocess = subprocess.Popen([os.path.join(os.getcwd(), "activate_tf_gpu")], stdin=subprocess.PIPE, stdout=file_std_out, stderr = subprocess.STDOUT, shell=True)

    #send tube ready seconds through pipe to obj detection program
    soluble_fibrin_obj_det_subprocess.communicate(tube_ready_seconds)
     

    #send tube ready seconds number to soluble fibrin obj det subrprocess function in "activate_tf_gpu"
    #soluble_fibrin_obj_det_subprocess.communicate(input=b'tube_ready_seconds')


    #get seconds back from soluble fibrin endpoint obj detection function 
    #soluble_fibrin_endpoint = soluble_fibrin_obj_det_subprocess.communicate()[0]
    
    #t = get_endpoint_from_obj_detection(soluble_fibrin_endpoint)

    

    



    


    

    #send endpoint seconds to main machine

    #put seconds into table, return SF value







run_soluble_fibrin_test(path_to_images)



