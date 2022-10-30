# Image stitching

## Description
Simple example for stitching 2 images.
1. Use AKAZE to find keypoints
2. Run Flann matcher and distance
3. Calculate homography matrix
4. Calculate size, offset and translation to match the image pair
5. Stitch the image and the base image


## Stitch your images
```bash
python stitch.py [BASE_IMG] [STITCHED_IMG] [OUTPUT_IMG]
```

# Materials
A good example to start with
Adobe panorama dataset: https://sourceforge.net/adobe/adobedatasets/panoramas/home/Home/
