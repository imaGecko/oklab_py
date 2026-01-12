## Lightweight Python Oklab
Implements colour conversion from RGB to sRGB to linear RGB to OkLab according to the GitHub posts from Björn Ottosson

Linear RGB
https://bottosson.github.io/posts/colorwrong/

Oklab
https://bottosson.github.io/posts/oklab/

### Features
- No Dependencies
- RGB &harr; sRGB &harr; Linear RGB &harr; Oklab
- ΔE distance for Oklab

### Example
```python
from oklablite import hex_code_to_rgb, rgb_to_oklab, delta_e

c1 = (64, 80, 96)
c2 = hex_code_to_rgb("#415161")
lab1, lab2 = rgb_to_oklab(c1), rgb_to_oklab(c2)
delta = delta_e(lab1, lab2) #1.73
```

### License
MIT License

Copyright (c) 2026 Florian Reh