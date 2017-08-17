#!/usr/bin/env python

import argparse
import imutils
import cv2
import sys

def print_progress(iteration, total, prefix='Progress:', suffix='Complete', decimals=2, bar_length=50):
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))
    
    if iteration >= total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
    help="Path to input video file")
ap.add_argument("-o", "--output", required=True,
    help="Path to output 'long exposure' image")
ap.add_argument("-s", "--step", type=int, default=1,
    help="Step used to get the frames")
args = vars(ap.parse_args())

# initialize the Red, Green, and Blue channel averages, along with
# the total number of frames read from the file
(rAvg, gAvg, bAvg) = (None, None, None)
total = 0

# open a pointer to the video file
print("[INFO] Opening video file pointer...")
stream = cv2.VideoCapture(args["video"])
print("[INFO] Computing frame averages (this will take awhile)...")

# Get the total number of frames to show the progress bar
total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

# Start the progress bar as zero
count = 0
print_progress(total, total_frames)

# Get the step that will be used to get the frames
step = args["step"]

# loop over frames from the video file stream
while True:
    # grab the frame from the file stream
    (grabbed, frame) = stream.read()

    # if the frame was not grabbed, then we have reached the end of
    # the sfile
    if not grabbed:
        break

    if count % step == 0:
        # otherwise, split the frmae into its respective channels
        (B, G, R) = cv2.split(frame.astype("float"))

        # if the frame averages are None, initialize them
        if rAvg is None:
            rAvg = R
            bAvg = B
            gAvg = G
        # otherwise, compute the weighted average between the history of
        # frames and the current frames
        else:
            rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
            gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
            bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)

        # increment the total number of frames read thus far
        total += 1
    count += 1
    print_progress(count, total_frames)

print_progress(total_frames, total_frames)
if total > 0:
    # merge the RGB averages together and write the output image to disk
    avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
    cv2.imwrite(args["output"], avg)
else:
    print("[ERRO] No frames found...")

# do a bit of cleanup on the file pointer
stream.release()
