# Simple image manipulator for python

A python script that can add simple filters to images, such as ```blur()```, ```tint()```, ```crop()``` and more

### Prerequisites

This script requires numpy, scipy and pillow as dependencies

```
pip install numpy scipy pillow
```

### Usage
```
python main.py <INPUT_FILE> -f "<FILTERS>" -o <OUTPUT_FILE>
```

There are a few filters to choose from, with various arguments. `*` represents arguments which are required for the filter.

```
crop(
  *crop_width: int,
  *crop_height: int,
  centre_x: int,
  centre_y: int
)

rotate(
  *n: int
)

flip(
  *direction: "x"|"xy"|"y"
)

greyscale()

tint(
  *r: int,
  *g: int,
  *b: int,
  strength: [0.0-1.0]
)
```

## Examples
```
# Greyscale an image
python main.py image.png -f "greyscale()" -o image_grey.png

# Blurs an image and rotates it by 180deg CW
python main.py image.png -f "blur(5) rotate(2)" -o output.png

# Vertically flips the image, tints it green and blurs it.
python main.py image.jpg -f "flip(y) tint(0, 255, 0) blur(8)"
```

## Contributing

All changes to this project are appreciated. This project was a simple project I made to
learn numpy and improve my python skills.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details