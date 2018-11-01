import os
import sys
import getopt

from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip

def print_help():
   print('available arguments:')
   print('\t-h # show this help')
   print('\t-c <codec> # select output codec (libx264, mpeg4, rawvideo, png, libvorbis, libvpx)')
   print('\t-l <video-length> # set fixed video length in seconds')
   print('\t-f <folder> # folder with video files to be edited')
   print('\t-o <output-folder> # output folder to store results')
   print('\t-v <video> # video to be added at the begining')
   print('\t-i <image> # image to be added at the begining')
   print('\t-t <image-time> # time for image to be displayed if image is set (default N=3)')
   print('\t-s <cut-start> # cut N seconds from begining of all video files (default N=0)')
   print('\t-e <cut-end> # cut N seconds from end of all video files (default N=0)')
   print('\t-w <watermark-image> # add watermark image into main video')
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
   print('\t--watermark=<watermark-image> # add watermark image into main video')
   print('\t--black-top=<height> # add black rectangle from top of video of length N (default N=0)')
   print('\t--black-bottom=<height> # add black rectangle from bottom of video of length N (default N=0)')

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
   codecs = {
      'libx264': 'mp4',
      'mpeg4': 'mp4',
      'rawvideo': 'avi',
      'png': 'avi',
      'libvorbis': 'ogv',
      'libvpx': 'webm',
   }

   inputFolder = None
   outputFolder = None
   videoFile = None
   videoEndFile = None
   imageFile = None
   imageEndFile = None
   imageTime = 3
   cutFromBegining = 0
   cutFromEnd = 0
   codec = None
   fixedLength = None
   watermarkImage = None
   blackTop = 0
   blackBottom = 0

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "hf:v:i:t:s:e:o:c:l:w:",
         ["help", "folder=", "output=", "video=", "video-end=", "image=",
          "image-end=", "image-time=", "cut-start=", "cut-end=", "licence",
          "watermark=", "black-top=", "black-bottom="]
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
      elif opt in ("-c"):
         codec = arg
      elif opt in ("-l"):
         fixedLength = int(arg)
      elif opt in ("-w", "--watermark"):
         watermarkImage = arg
      elif opt in ("--black-top"):
         blackTop = int(arg)
      elif opt in ("--black-bottom"):
         blackBottom = int(arg)

   fileList = []
   ffvideoFile = None
   ffvideoEndFile = None
   ffimageFile = None
   ffimageEndFile = None
   ffwatermark = None

   if not outputFolder:
      print('Output folder is not found, use -h or --help to show help message.')
      sys.exit(2)

   if not os.path.isdir(outputFolder):
      os.makedirs(outputFolder)

   if (videoFile and not os.path.isfile(videoFile)) or (videoEndFile and not os.path.isfile(videoEndFile)):
      print('Input video file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if (imageFile and not os.path.isfile(imageFile)) or (imageEndFile and not os.path.isfile(imageEndFile)):
      print('Input image file does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if (watermarkImage and not os.path.isfile(watermarkImage)):
      print('Input watermark image does not exists, use -h or --help to show help message.')
      sys.exit(2)

   if codec is not None and not codecs.has_key(codec):
      print('Unknown codec, use -h or --help to show help message.')
      sys.exit(2)

   if (videoFile):
      ffvideoFile = VideoFileClip(videoFile)

   if (videoEndFile):
      ffvideoEndFile = VideoFileClip(videoEndFile)

   if (imageFile):
      ffimageFile = ImageClip(imageFile, duration=imageTime)

   if (imageEndFile):
      ffimageEndFile = ImageClip(imageEndFile, duration=imageTime)

   if (watermarkImage):
      ffwatermark = ImageClip(watermarkImage)

   try:
      fileList = os.listdir(inputFolder)
   except:
      print('Input folder not found, use -h or --help to show help message.')
      sys.exit(2)

   for filename in fileList:
      try:
         if (os.path.isfile(os.path.join(inputFolder, filename))):
            video = VideoFileClip(os.path.join(inputFolder, filename))
            video = video.subclip(cutFromBegining, -cutFromEnd if cutFromEnd > 0 else None)
            width, height = video.size

            if (fixedLength is not None):
               video = video.subclip(0, fixedLength)

            if (blackTop > 0):
               def top_filter(frame):
                  frame[0: blackTop, 0: width] = 0
                  return frame

               video = video.fl_image(top_filter)

            if (blackBottom > 0):
               def bottom_filter(frame):
                  frame[(height - blackBottom): height, 0: width] = 0
                  return frame

               video = video.fl_image(bottom_filter)

            if (ffwatermark is not None):
               logo = (ffwatermark
                        .set_duration(video.duration)
                        .margin(right=8, top=8, opacity=0.6)
                        .set_pos(("right", "top")))
               video = CompositeVideoClip([video, logo])

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

            translated_filename = filename if codec is None else os.path.splitext(filename)[0] + "." + codecs[codec]
            result.write_videofile(os.path.join(outputFolder, translated_filename), codec=codec)
      except:
         print('Error while transfering file: ', filename)

if __name__ == "__main__":
   main(sys.argv[1:])