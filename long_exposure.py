#!/usr/bin/env python

import argparse
import cv2
import sys


class ProgressBar(object):

    def __init__(self, total, prefix='Progress:', suffix='Complete', decimals=2, bar_length=50):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length

    def update(self, progress):
        str_format = "{0:." + str(self.decimals) + "f}"
        percents = str_format.format(100 * (progress / float(self.total)))
        filled_length = int(round(self.bar_length * progress / float(self.total)))
        bar = '#' * filled_length + '-' * (self.bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.suffix))

        if progress >= self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()


class LongExposure(object):

    @staticmethod
    def run(video, output):

        # initialize the Red, Green, and Blue channel averages, along with
        # the total number of frames read from the file
        (r_avg, g_avg, b_avg) = (None, None, None)
        total = 0

        # open a pointer to the video file
        print("[INFO] Opening video file pointer...")
        stream = cv2.VideoCapture(video)
        print("[INFO] Computing frame averages (this will take awhile)...")

        # Get the total number of frames to show the progress bar
        total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

        progress_bar = ProgressBar(total_frames)
        # Start the progress bar as zero
        count = 0
        progress_bar.update(0)

        # Get the step that will be used to get the frames
        step = args["step"]

        # loop over frames from the video file stream
        while True:
            # grab the frame from the file stream
            (grabbed, frame) = stream.read()

            # if the frame was not grabbed, then we have reached the end of
            # the file
            if not grabbed:
                break

            if count % step == 0:
                # otherwise, split the frame into its respective channels
                (B, G, R) = cv2.split(frame.astype("float"))

                # if the frame averages are None, initialize them
                if r_avg is None:
                    r_avg = R
                    b_avg = B
                    g_avg = G
                # otherwise, compute the weighted average between the history of
                # frames and the current frames
                else:
                    r_avg = ((total * r_avg) + (1 * R)) / (total + 1.0)
                    g_avg = ((total * g_avg) + (1 * G)) / (total + 1.0)
                    b_avg = ((total * b_avg) + (1 * B)) / (total + 1.0)

                # increment the total number of frames read thus far
                total += 1
            count += 1

            progress_bar.update(count)

        progress_bar.update(total_frames)
        if total > 0:
            # merge the RGB averages together and write the output image to disk
            avg = cv2.merge([b_avg, g_avg, r_avg]).astype("uint8")
            cv2.imwrite(output, avg)
        else:
            print("[ERRO] No frames found...")

        # do a bit of cleanup on the file pointer
        stream.release()

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="Path to input video file")
    ap.add_argument("-o", "--output", required=True, help="Path to output 'long exposure' image")
    ap.add_argument("-s", "--step", type=int, default=1, help="Step used to get the frames")
    args = vars(ap.parse_args())
    long_exposure = LongExposure()
    long_exposure.run(args["video"], args["output"])