import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
from tflite_runtime.interpreter import Interpreter

# minimum score needed to get a correct classification of our object
min_conf_threshold = 50.0


def findPersonCoordinates(inputImage):
    # Path to the model's graph which will detect our objects
    path_to_graph = "home/pi/aiCar/tfliteModel/detect.tflite"

    # Path to labelmap
    path_to_labels = "home/pi/aiCar/tfliteModel/labelmap.txt"

    # Load the label map
    with open(path_to_labels, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    interpreter = Interpreter(model_path=path_to_graph)

    interpreter.allocate_tensors()

    # Get model input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5

    outname = output_details[0]['name']

    if ('StatefulPartitionedCall' in outname):
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    # resize the image to the input specifications made by ml model
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # run the model on our image
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # get the detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[
        0]
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[
        0]
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[
        0]

    max_index = np.argmax(scores)
    if ((scores[max_index] > min_conf_threshold) and (scores[max_index] <= 1.0)):

        ymin = int(max(1, (boxes[max_index][0] * imH)))
        xmin = int(max(1, (boxes[max_index][1] * imW)))
        ymax = int(min(imH, (boxes[max_index][2] * imH)))
        xmax = int(min(imW, (boxes[max_index][3] * imW)))

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
        # All the results have been drawn on the image, now display the image
        cv2.imshow('Object detector', image)

        # Press any key to continue to next image, or press 'q' to quit
        cv2.waitKey(0)
        return (ymin, xmin, ymax, xmax, imH, imW)
    return None
