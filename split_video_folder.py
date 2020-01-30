import os
import cv2
import json
import argparse
import subprocess
import numpy as np


def get_video_length(video_name):
  length_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_name]
  length = subprocess.check_output(length_cmd).strip()
  
  return int(float(length))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(usage='python3.6 split_video_folder.py -i ... -s split_info.json')
  parser.add_argument('-i', '--input_dir', required=True, help="Directory with video to split")
  parser.add_argument('-s', '--split_file', required=True, help="JSON file with split info")
  args = parser.parse_args()

  if args.split_file.split('.')[-1] != 'json':
    print("Split info must be in a JSON file")
    exit()
    
  with open(args.split_file) as json_file:
    split_info = json.load(json_file)

  os.makedirs(os.path.join(args.input_dir, 'splitted'), exist_ok=True)

  for video_info in split_info:
    video_path = os.path.join(args.input_dir, video_info['name'])
    split_cmd = ['ffmpeg', '-i', video_path, '-vcodec', 'copy', '-acodec', 'copy', '-y']
    
    split_points = video_info['split_time']
    if split_points[0] != 0:
      split_points.insert(0, 0)
    
    video_name, video_ext = video_path.split('/')[-1].split('.')

    split_count = 0
    for i in range(len(split_points)):
      split_start = split_points[i]
      split_end = split_points[i+1] if i+1 < len(split_points) else get_video_length(video_path)
      split_name = os.path.join(args.input_dir, 'splitted', video_name + '_' + str(split_count) + '.' + video_ext)

      split_args = ['-ss', str(split_start), '-t', str(split_end-split_start), split_name]
      subprocess.check_output(split_cmd+split_args)

      split_count += 1
