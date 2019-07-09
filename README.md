# Long exposure with OpenCV and Python

[![Build Status](https://travis-ci.org/kelvins/long-exposure.svg?branch=master)](https://travis-ci.org/kelvins/long-exposure)

This project creates long exposure-like images from an input video using Python and OpenCV. It computationally simulates the long exposure photography effect.

[Long-exposure photography][1]:

> Long-exposure, time-exposure, or slow-shutter photography involves using a long-duration shutter speed to sharply capture the stationary elements of images while blurring, smearing, or obscuring the moving elements. Long-exposure photography captures one element that conventional photography does not: an extended period of time. The paths of bright moving objects become clearly visible. Clouds form broad bands, head and tail lights of cars draw bright streaks, stars leave trails in the sky, and water waves appear smoothened. Only bright objects will leave visible trails, whereas dark objects usually disappear. Boats in long exposures will disappear during daytime, but will draw bright trails from their lights at night.

## Usage

The usage is very simple, we just need to call the script passing a desired operation (e.g. `local-video`), the video path, the output image path and the step (optional), for example:

```bash
$ python src/long_exposure.py local-video /home/user/videos/video.mp4 /home/user/images/long_exp.png -s 5
```

If you have doubts you can call for help:

```bash
python src/long_exposure.py --help
```

## Environment

This project uses `pipenv` so to set up the environment you need to make sure you have `pipenv` installed and run the following commands to install the dependencies and activate the virtual environment:

```bash
pipenv install --dev
pipenv shell
```

## Tests

We can run the tests using `pytest` directly or using the `Makefile`, for example:

```bash
make runtests
```

## Input/Output

| **Input (video)** | **Output (image)** |
|:---------:|:----------:|
| ![Input](http://i.imgur.com/ji8h6FK.jpg) | ![Output](http://i.imgur.com/UXVCLIE.jpg) |
| ![Input](http://i.imgur.com/l97V6Cm.jpg) | ![Output](http://i.imgur.com/oPedXbB.jpg) |

## References

- **Long exposure with OpenCV and Python**. Adrian Rosebrock.
http://www.pyimagesearch.com/2017/08/14/long-exposure-with-opencv-and-python/

- **Long-exposure photography**. https://en.wikipedia.org/wiki/Long-exposure_photography

  [1]: https://en.wikipedia.org/wiki/Long-exposure_photography
