# Long exposure with OpenCV and Python

An algorithm that creates long exposure-like images from an input video using Python and OpenCV. It computationally simulates the long exposure photography effect.

[Long-exposure photography][1]:

> Long-exposure, time-exposure, or slow-shutter photography involves using a long-duration shutter speed to sharply capture the stationary elements of images while blurring, smearing, or obscuring the moving elements. Long-exposure photography captures one element that conventional photography does not: an extended period of time. The paths of bright moving objects become clearly visible. Clouds form broad bands, head and tail lights of cars draw bright streaks, stars leave trails in the sky, and water waves appear smoothened. Only bright objects will leave visible trails, whereas dark objects usually disappear. Boats in long exposures will disappear during daytime, but will draw bright trails from their lights at night.

## Usage

```
$ python long_exposure.py --video C:\video.avi --output C:\output_image.png --step 1
```

### Arguments

- **video**: you must pass the file path and file name as the **video** argument. E.g.: `C:\videos\video.avi`.
- **output**: you must pass the file path and file name for the **output** file (image). E.g. `C:\output_image.png`.
- **step**: you can pass a **step** value as an argument. Its default value is 1. It is used to skip some frames and make the processing faster. Keep in mind that using higher **step** values will result in losing frames/information.

### Requirements

- Python 2.7
- OpenCV 3.1

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