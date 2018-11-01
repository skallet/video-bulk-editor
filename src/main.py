import os
import sys
import getopt

from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.resize import resize
from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

def print_help():
   print('available arguments:')
   print('\t-h # show this help')
   print('\t-f <folder> # folder with video files to be edited')
   print('\t-o <output-folder> # output folder to store results')
   print('\t-v <video> # video to be added at the begining')
   print('\t-i <image> # image to be added at the begining')
   print('\t-t <image-time> # time for image to be displayed if image is set')
   print('\t-s <cut-start> # cut N seconds from begining of all video files (default N=3)')
   print('\t-e <cut-end> # cut N seconds from end of all video files (default N=3)')
   print('aliases:')
   print('\t--help # show this help')
   print('\t--folder=<folder> # folder with video files to be edited')
   print('\t--output=<output-folder> # output folder to store results')
   print('\t--video=<video> # video to be added at the begining')
   print('\t--image=<image> # image to be added at the begining')
   print('\t--image-time=<image-time> # time for image to be displayed if image is set')
   print('\t--cut-start=<cut-start> # cut N seconds from begining of all video files (default N=3)')
   print('\t--cut-end=<cut-end> # cut N seconds from end of all video files (default N=3)')

def print_licence():
   print('''
   Video bulk editor
   Copyright (C) 2018 Milan Blazek

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.
   ''')

def print_short_licence():
   print('''
   Video Bulk editor  Copyright (C) 2018 Milan Blazek
   This program comes with ABSOLUTELY NO WARRANTY; for details type `--licence'.
   This is free software, and you are welcome to redistribute it
   under certain conditions; type `--licence' for details.
   ''')

def main(argv):
   inputFolder = None
   outputFolder = None
   videoFile = None
   imageFile = None
   imageTime = 3
   cutFromBegining = 3
   cutFromEnd = 3

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "hf:v:i:t:s:e:o:",
         ["help", "folder=", "output=", "video=", "image=", "image-time=", "cut-start=", "cut-end=", "licence"]
      )
   except getopt.GetoptError:
      print_help()
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print_help()
         sys.exit()

      if opt == '--licence':
         print_licence()
         sys.exit()
      elif opt in ("-f", "--folder"):
         inputFolder = arg
      elif opt in ("-o", "--output"):
         outputFolder = arg
      elif opt in ("-v", "--video"):
         videoFile = arg
      elif opt in ("-s", "--cut-start"):
         cutFromBegining = max(0, int(arg))
      elif opt in ("-e", "--cut-end"):
         cutFromEnd = max(0, int(arg))
      elif opt in ("-t", "--image-time"):
         imageTime = max(1, int(arg))
      elif opt in ("-i", "--image"):
         imageFile = arg

   fileList = []
   ffvideoFile = None
   ffimageFile = None

   if not outputFolder:
      print('Output folder is not found, use -h or --help to show help message.')
      sys.exit(2)

   if not os.path.isdir(outputFolder):
      os.makedirs(outputFolder)

   if videoFile and not os.path.isfile(videoFile):
      print('Input video file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if imageFile and not os.path.isfile(imageFile):
      print('Input image file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if (videoFile):
      ffvideoFile = VideoFileClip(videoFile)

   if (imageFile):
      ffimageFile = ImageClip(imageFile, duration=imageTime)

   try:
      fileList = os.listdir(inputFolder)
   except:
      print('Input folder not found, use -h or --help to show help message.')
      sys.exit(2)

   for filename in fileList:
      try:
         if (os.path.isfile(os.path.join(inputFolder, filename))):
            video = VideoFileClip(os.path.join(inputFolder, filename))
            video = video.subclip(cutFromBegining, -cutFromEnd)

            videos = []
            if (ffvideoFile):
               videos.append(ffvideoFile.resize(video.size))

            if (ffimageFile):
               videos.append(ffimageFile.resize(video.size))
            videos.append(video)

            result = concatenate_videoclips(videos)
            result.write_videofile(os.path.join(outputFolder, filename))
      except:
         print('Error while transfering file: ', filename)

if __name__ == "__main__":
   main(sys.argv[1:])