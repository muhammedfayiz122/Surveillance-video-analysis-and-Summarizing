import subprocess
import time

import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

from glob import glob

import IPython.display as ipd
from tqdm import tqdm

import subprocess
import time

s_time = time.time()

def convert_video(input_path, output_path, threads=4):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-threads', str(threads),
        output_path
    ]
    #minimize log after final code

    try:
        subprocess.run(command, check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Example usage:
input_video = 'video.mov'
output_video = 'movie.mp4'
convert_video(input_video, output_video, threads=4)

est_time = time.time() - s_time 
print(f"estimated time is {est_time:.2f} seconds")

def convert_video(input_path, output_path, threads=4):
    # command = [
    #     'ffmpeg',
    #     '-i', input_path,
    #     '-qscale','0',
    #     '-threads', str(threads),
    #     output_path
    # ]
    command = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'mpeg4',
        '-b:v', video_bitrate,
        '-c:a', 'aac',
        '-threads', str(threads),
        output_path
    ]
    

    try:
        subprocess.run(command, check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Example usage:
input_video = 'video.mov'
output_video = 'output_video2.mp4'
convert_video(input_video, output_video, threads=6, video_bitrate='500k')
est_time = time.time() - s_time 
print(f"estimated time is {est_time:.2f} seconds")
