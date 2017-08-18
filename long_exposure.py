#!/usr/bin/env python

import argparse
import cv2
import sys


class ProgressBar(object):

    def __init__(self, total, prefix='Progress:', suffix='Complete', decimals=2, bar_length=50):
        """
        It is used to show a progress bar.
        :param total: the total value of the progress bar (100%)
        :param prefix: the prefix show before the progress bar (default is 'Progress:')
        :param suffix: the suffix show after the progress bar (default is 'Complete')
        :param decimals: the number of decimal places
        :param bar_length: the length/width of the progress bar
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.bar_length = bar_length

    def update(self, progress):
        """
        Function used to update the progress bar.
        :param progress: the current progress (should be lower than the total)
        """
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
    def run(video, output, step=1):
        """
        The function used to run the long-exposure effect based on the video.
        :param video: the path to the video file
        :param output: the path to the output image file
        :param step: the step used to ignore some frames (optional)
        """

        # Initialize the RGB channel averages
        (r_avg, g_avg, b_avg) = (None, None, None)

        # Used to count the total number of selected frames
        selected_frames = 0

        print("[INFO] Opening video file pointer...")

        # Open a pointer to the video file
        stream = cv2.VideoCapture(video)

        print("[INFO] Computing frame averages...")

        # Get the total number of frames to show the progress bar
        total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

        # Initialize the progress bar
        progress_bar = ProgressBar(total_frames)
        progress_bar.update(0)

        # Used to count the number of frames to update the progress bar
        frame_count = 0

        # Loop over all frames from the video file stream
        while True:
            # Grab the frame from the file stream
            grabbed, frame = stream.read()

            # If the frame was not grabbed, then we have reached the end of the file
            if not grabbed:
                break

            if frame_count % step == 0:
                # Split the frame into its respective channels
                # We need to convert it to float
                (B, G, R) = cv2.split(frame.astype("float"))

                # If the frame averages are None, initialize them
                if r_avg is None:
                    r_avg = R
                    b_avg = B
                    g_avg = G
                # Otherwise, compute the weighted average between the history
                # of frames and the current frames
                else:
                    r_avg = ((selected_frames * r_avg) + (1 * R)) / (selected_frames + 1.0)
                    g_avg = ((selected_frames * g_avg) + (1 * G)) / (selected_frames + 1.0)
                    b_avg = ((selected_frames * b_avg) + (1 * B)) / (selected_frames + 1.0)

                # Increment the total number of selected frames
                selected_frames += 1

            # Update the progress bar
            frame_count += 1
            progress_bar.update(frame_count)

        # Make sure that the progress bar state is 100%
        progress_bar.update(total_frames)

        # If we got at least one frame
        if selected_frames > 0:
            # Merge the RGB averages together and write the output image to disk
            # Here, we need to convert the value to uint8 to create the new image
            avg = cv2.merge([b_avg, g_avg, r_avg]).astype("uint8")
            cv2.imwrite(output, avg)
        else:
            print("[ERRO] No frames found...")

        # Release the stream pointer
        stream.release()

if __name__ == "__main__":
    # Construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True, help="Path to input video file")
    ap.add_argument("-o", "--output", required=True, help="Path to output 'long exposure' image")
    ap.add_argument("-s", "--step", type=int, default=1, help="Step used to get the frames")
    args = vars(ap.parse_args())

    # Run the long exposure algorithm passing the required parameters
    LongExposure.run(args["video"], args["output"], args["step"])
