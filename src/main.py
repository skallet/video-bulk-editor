import os
import sys
import getopt

from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

def print_help():
   print('available arguments:')
   print('\t-h # show this help')
   print('\t-f <folder> # folder with video files to be edited')
   print('\t-o <output-folder> # output folder to store results')
   print('\t-v <video> # video to be added at the begining')
   print('\t-i <image> # image to be added at the begining')
   print('\t-t <image-time> # time for image to be displayed if image is set (default N=3)')
   print('\t-s <cut-start> # cut N seconds from begining of all video files (default N=0)')
   print('\t-e <cut-end> # cut N seconds from end of all video files (default N=0)')
   print('aliases:')
   print('\t--help # show this help')
   print('\t--folder=<folder> # folder with video files to be edited')
   print('\t--output=<output-folder> # output folder to store results')
   print('\t--video=<video> # video to be added at the begining')
   print('\t--video-end=<video> # video to be added at the end')
   print('\t--image=<image> # image to be added at the begining')
   print('\t--image-end=<image> # image to be added at the end')
   print('\t--image-time=<image-time> # time for image to be displayed if image is set (default N=3)')
   print('\t--cut-start=<cut-start> # cut N seconds from begining of all video files (default N=0)')
   print('\t--cut-end=<cut-end> # cut N seconds from end of all video files (default N=0)')

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
   videoEndFile = None
   imageFile = None
   imageEndFile = None
   imageTime = 3
   cutFromBegining = 0
   cutFromEnd = 0

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "hf:v:i:t:s:e:o:",
         ["help", "folder=", "output=", "video=", "video-end=", "image=", "image-end=", "image-time=", "cut-start=", "cut-end=", "licence"]
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
      elif opt in ("--image-end"):
         imageEndFile = arg
      elif opt in ("--video-end"):
         videoEndFile = arg

   fileList = []
   ffvideoFile = None
   ffvideoEndFile = None
   ffimageFile = None
   ffimageEndFile = None

   if not outputFolder:
      print('Output folder is not found, use -h or --help to show help message.')
      sys.exit(2)

   if not os.path.isdir(outputFolder):
      os.makedirs(outputFolder)

   if (videoFile and not os.path.isfile(videoFile)) or (videoEndFile and not os.path.isfile(videoEndFile:
      print('Input video file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if (imageFile and not os.path.isfile(imageFile)) or (imageEndFile and not os.path.isfile(imageEndFile)):
      print('Input image file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if (videoFile):
      ffvideoFile = VideoFileClip(videoFile)

   if (videoEndFile):
      ffvideoEndFile = VideoFileClip(videoEndFile)

   if (imageFile):
      ffimageFile = ImageClip(imageFile, duration=imageTime)

   if (imageEndFile):
      ffimageEndFile = ImageClip(imageFile, duration=imageFile)

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

            if (ffvideoEndFile):
               videos.append(ffvideoEndFile.resize(video.size))

            if (ffimageEndFile):
               videos.append(ffimageEndFile.resize(video.size))

            result = concatenate_videoclips(videos)
            result.write_videofile(os.path.join(outputFolder, filename))
      except:
         print('Error while transfering file: ', filename)

if __name__ == "__main__":
   main(sys.argv[1:])