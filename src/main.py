import os
import sys
import getopt

from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, vfx

codecs = {
   'libx264': 'mp4',
   'mpeg4': 'mp4',
   'rawvideo': 'avi',
   'msmpeg4v2': 'avi',
   'wmv1': 'avi',
   'png': 'avi',
   'libvorbis': 'ogv',
   'libvpx': 'webm',
   'copy': 'avi',
}

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
   print('\t-u # cut units are in percents instead of seconds')
   print('\t-w <watermark-image> # add watermark image into main video')
   print('\t-r <angle> # rotate main video by given angle')
   print('\t-m # mirror main video')
   print('\n## word specified arguments:')
   print('\t--help # show this help')
   print('\t--copy-codec <file_suffix> # copy codecs and save file in specified format (eq. avi)')
   print('\t--suffix <file_suffix> # set file suffix to given value, can be used to override codec output (eq. avi)')
   print('\t--folder=<folder> # folder with video files to be edited')
   print('\t--output=<output-folder> # output folder to store results')
   print('\t--video=<video> # video to be added at the begining')
   print('\t--video-end=<video> # video to be added at the end')
   print('\t--image=<image> # image to be added at the begining')
   print('\t--image-end=<image> # image to be added at the end')
   print('\t--image-time=<image-time> # time for image to be displayed if image is set (default N=3)')
   print('\t--cut-start=<cut-start> # cut N seconds from begining of all video files (default N=0)')
   print('\t--cut-end=<cut-end> # cut N seconds from end of all video files (default N=0)')
   print('\t--cut-percent # cut units are in percents instead of seconds')
   print('\t--cut-percent-start # cut units from start are in percents instead of seconds')
   print('\t--cut-percent-end # cut units from end are in percents instead of seconds')
   print('\t--watermark=<watermark-image> # add watermark image into main video')
   print('\t--watermark-width=<watermark-width> # set watermark width in percent relative to main video')
   print('\t--watermark-to-left # set watermark anchor to left')
   print('\t--watermark-to-bottom # set watermark anchor to bottom')
   print('\t--watermark-to-center # set watermark anchor to center')
   print('\t--watermark-width=<watermark-width> # set watermark width in percent relative to main video')
   print('\t--watermark-duration=<duration> # set watermark duration in seconds')
   print('\t--watermark-show-at=<percent marks divided by ,> # set watermark start positions separated by comma')
   print('\t--watermark-fade-duration=<duration> # set watermark fade in and out duration in seconds')
   print('\t--black-top=<height> # add black rectangle from top of video of length N% (default N=0)')
   print('\t--black-bottom=<height> # add black rectangle from bottom of video of length N% (default N=0)')
   print('\t--ffmpeg=<params> # additional params passed to ffmpeg')
   print('\t--resize-by-intro # resize main video by intro')
   print('\t--resize-by-outro # resize main video by outro')
   print('\t--rotate=<angle> # rotate main video by given angle')
   print('\t--mirror # mirror main video')
   print('\n## available codecs:')
   for c in codecs:
      print('\t' + c + ' results in ' + codecs[c])

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
   codec = None
   fixedLength = None
   watermarkImage = None
   watermarkWidth = 100
   watermarkDuration = None
   fadeDuration = 1
   blackTop = 0
   blackBottom = 0
   cutUnitsPx = True
   cutUnitsStartPx = True
   cutUnitsEndPx = True
   watermarkX = "right"
   watermarkY = "top"
   watermarkStarts = None
   codecSuffix = None
   params = None
   resizeWithIntro = False
   resizeWithOutro = False
   mirrorVideo = False
   rotateVideo = None

   print_short_licence()

   try:
      opts, args = getopt.getopt(
         argv,
         "humf:v:i:t:s:e:o:c:l:w:r:",
         ["help", "folder=", "output=", "video=", "video-end=", "image=",
          "image-end=", "image-time=", "cut-start=", "cut-end=", "licence",
          "watermark=", "black-top=", "black-bottom=", "cut-percent", "watermark-width=",
          "cut-percent-start", "cut-percent-end", "watermark-to-left", "watermark-to-bottom",
          "watermark-to-center", "watermark-duration=", "watermark-fade-duration=", "watermark-show-at=",
          "copy-codec=", "ffmpeg=", "suffix=", "resize-by-intro", "resize-by-outro", "mirror", "rotate="]
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
      elif opt in ("--watermark-to-left"):
         watermarkX = "left"
      elif opt in ("--watermark-to-center"):
         watermarkX = "center"
         watermarkY = "center"
      elif opt in ("--watermark-to-bottom"):
         watermarkY = "bottom"
      elif opt in ("--watermark-duration"):
         watermarkDuration = int(arg)
      elif opt in ("--watermark-fade-duration"):
         fadeDuration = int(arg)
      elif opt in ("--watermark-show-at"):
         watermarkStarts = [int(a) for a in arg.split(',')]
      elif opt in ("--black-top"):
         blackTop = int(arg)
      elif opt in ("--black-bottom"):
         blackBottom = int(arg)
      elif opt in ("-u", "--cut-percent"):
         cutUnitsPx = False
      elif opt in ("--watermark-width"):
         watermarkWidth = max(0, int(arg))
      elif opt in ("--cut-percent-start"):
         cutUnitsStartPx = False
      elif opt in ("--cut-percent-end"):
         cutUnitsEndPx = False
      elif opt in ("--copy-codec"):
         codec = 'copy'
         codecSuffix = arg
      elif opt in ("--suffix"):
         codecSuffix = arg
      elif opt in ("--ffmpeg"):
         params = arg.split(' ')
      elif opt in ("--resize-by-intro"):
         resizeWithIntro = True
      elif opt in ("--resize-by-outro"):
         resizeWithOutro = True
      elif opt in ("-m", "--mirror"):
         mirrorVideo = True
      elif opt in ("-r", "--rotate"):
         rotateVideo = int(arg)

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
   elif codec is not None and codecSuffix is None:
      codecSuffix = codecs[codec]

   if resizeWithIntro and not videoFile:
      print('No intro for resize found, use -h or --help to show help message.')
      sys.exit(2)

   if resizeWithIntro and not videoEndFile:
      print('No outro for resize found, use -h or --help to show help message.')
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

            if (resizeWithIntro and ffvideoFile):
               video = video.resize(ffvideoFile.size)

            if (resizeWithOutro and ffvideoEndFile):
               video = video.resize(ffvideoEndFile.size)

            beginingCut = cutFromBegining
            endingCut = -cutFromEnd if cutFromEnd > 0 else None

            if (not cutUnitsPx or not cutUnitsStartPx):
               beginingCut = (cutFromBegining * video.duration) / 100

            if (not cutUnitsPx or not cutUnitsEndPx):
               endingCut = -(cutFromEnd * video.duration) / 100 if cutFromEnd > 0 else None

            video = video.subclip(beginingCut, endingCut)
            width, height = video.size

            if (mirrorVideo):
               video = video.fx(vfx.mirror_x)

            if (rotateVideo is not None):
               video = video.rotate(rotateVideo)

            # video = (video
            #    # .fx(vfx.mirror_x)
            #    # .rotate(1)
            #    # .fx(vfx.colorx, factor=1.4)
            #    # .fx(vfx.painting, saturation=1.6, black=0.01)
            # )

            if (fixedLength is not None):
               video = video.subclip(0, fixedLength)

            if (blackTop > 0):
               blackHeight = (blackTop * height) / 100

               def top_filter(frame):
                  frame[0: blackHeight, 0: width] = 0
                  return frame

               video = video.fl_image(top_filter)

            if (blackBottom > 0):
               blackHeight = (blackBottom * height) / 100

               def bottom_filter(frame):
                  frame[(height - blackHeight): height, 0: width] = 0
                  return frame

               video = video.fl_image(bottom_filter)

            if (ffwatermark is not None):
               wWidth = (watermarkWidth * width) / 100
               duration = (watermarkDuration if watermarkDuration is not None else video.duration)
               logo = (ffwatermark
                        .set_duration(duration)
                        .margin(left=0, right=0, bottom=0, top=0, opacity=0.6)
                        .resize(width=wWidth)
                        .set_pos((watermarkX, watermarkY))
                        .crossfadein(fadeDuration)
                        .crossfadeout(fadeDuration))

               if (watermarkStarts is None):
                  video = CompositeVideoClip([video, logo])
               else:
                  logos = []
                  for w in watermarkStarts:
                     w_start = int(w * video.duration / 100)
                     logos.append(
                        logo
                           .set_start(w_start)
                           .set_duration(min(video.duration - w_start, duration)))

                  video = CompositeVideoClip([video] + logos)

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

            translated_filename = filename if codecSuffix is None else os.path.splitext(filename)[0] + "." + codecSuffix
            result.write_videofile(
               os.path.join(outputFolder, translated_filename),
               codec=codec,
               ffmpeg_params=params
            )
      except Exception as e:
         print('Error while transfering file: ', filename)
         print('Original Error: ', str(e))

if __name__ == "__main__":
   main(sys.argv[1:])