import logging

import cv2
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)


class LongExposure:
    def __init__(self, video, output_image_path, step=1):
        self.video = video
        self.output_image_path = output_image_path
        self.step = step

    @staticmethod
    def averager():
        """Calculate the average using a clojure."""
        count = 0
        total = 0.0
        def average(value):
            nonlocal count, total
            count += 1
            total += value
            return total/count
        return average

    def __call__(self):
        logging.info('Processing video %r with step %r', self.video, self.step)

        # Open a pointer to the video file
        stream = cv2.VideoCapture(self.video)

        # Get the total frames to be used by the progress bar
        total_frames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

        r, g, b = None, None, None
        r_avg, g_avg, b_avg = self.averager(), self.averager(), self.averager()

        for count in tqdm(range(total_frames)):
            # Split the frame into its respective channels
            _, frame = stream.read()

            if count % self.step == 0:
                # Get the current RGB
                b_curr, g_curr, r_curr = cv2.split(frame.astype('float'))
                r, g, b = r_avg(r_curr), g_avg(g_curr), b_avg(b_curr)

        # Merge the RGB averages together and write the output image to disk
        avg = cv2.merge([b, g, r]).astype('uint8')
        logging.info('Saving image as %r', self.output_image_path)
        cv2.imwrite(self.output_image_path, avg)

        # Release the stream pointer
        stream.release()
