from typing import Tuple
RGB = Tuple[int,int,int]
sRGB = Tuple[float,float,float]
LinearRGB = Tuple[float,float,float]
Oklab = Tuple[float,float,float]

def hex_code_to_rgb(c:str) -> RGB:
    if not c.startswith('#'):
        raise Exception(f'Hex code must start with #\nGot {c}')
    if len(c) != 7:
        raise Exception(f'Hex string must have 7 characters #\nGot {len(c)} characters\n{c}')
    
    return (
        int(c[1:3],16),
        int(c[3:5],16),
        int(c[5:7],16)
    )

def rgb_to_srgb(c:RGB) -> sRGB:
    return (
        c[0]/255,
        c[1]/255,
        c[2]/255,
    )

def srgb_to_rgb(c:sRGB) -> RGB:
    return (
        _snap_float_to_rgb(c[0]*255),
        _snap_float_to_rgb(c[1]*255),
        _snap_float_to_rgb(c[2]*255)
    )

def _snap_float_to_rgb(x:float) -> int:
    x = max(x, 0)
    x = min(x, 255)
    return round(x)

# srgb to linear rgb
# https://bottosson.github.io/posts/colorwrong/

def srgb_to_linear(c:sRGB) -> LinearRGB:
    return (
        _f_inv(c[0]),
        _f_inv(c[1]),
        _f_inv(c[2])
    )

def linear_to_srgb(c:LinearRGB) -> sRGB:
    return (
        _srgb_clamp(_f(c[0])),
        _srgb_clamp(_f(c[1])),
        _srgb_clamp(_f(c[2]))
    )

def _f(x:float) -> float:
    if x >= 0.0031308:
        return 1.055 * x**(1.0/2.4) - 0.055
    return 12.92 * x

def _f_inv(x:float) -> float:
    if x >= 0.04045:
        return ((x + 0.055)/(1 + 0.055))**2.4
    return x / 12.92 

#ensure srgb values within valid range [0,1]
def _srgb_clamp(x:float) -> float:
    x = max(x,0.0)
    x = min(x,1.0)
    return x

# linear rgb to oklab
# https://bottosson.github.io/posts/oklab/

def linear_to_oklab(c:LinearRGB) -> Oklab:
    l = 0.4122214708 * c[0] + 0.5363325363 * c[1] + 0.0514459929 * c[2]
    m = 0.2119034982 * c[0] + 0.6806995451 * c[1] + 0.1073969566 * c[2]
    s = 0.0883024619 * c[0] + 0.2817188376 * c[1] + 0.6299787005 * c[2] 
    l_ = l ** (1/3)
    m_ = m ** (1/3)
    s_ = s ** (1/3)

    return (
        0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
        1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
        0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_
    )

def oklab_to_linear(c:Oklab) -> LinearRGB:
    l_ = c[0] + 0.3963377774 * c[1] + 0.2158037573 * c[2]
    m_ = c[0] - 0.1055613458 * c[1] - 0.0638541728 * c[2]
    s_ = c[0] - 0.0894841775 * c[1] - 1.2914855480 * c[2]

    l = l_*l_*l_
    m = m_*m_*m_
    s = s_*s_*s_

    return (
    	+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    	-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    	-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    )

def rgb_to_oklab(c:RGB) -> Oklab:
    return linear_to_oklab(srgb_to_linear(rgb_to_srgb(c)))

def oklab_to_rgb(c:Oklab) -> RGB:
    return srgb_to_rgb(linear_to_srgb(oklab_to_linear(c)))

def delta_e(c1:Oklab, c2:Oklab) -> float:
    '''
    Delta E describes the equivalence of 2 different colours using euclidian distance in the Oklab colour space.
    Oklab is perceptually uniform making simple euclidian distance a meaningful metric.

    Rough interpretation:
    \tDelta > 0.5 minor colour difference
    \tDelta > 1 small colour difference
    \tDelta > 2 noticable colour difference
    \tDelta > 5 different colour
    '''
    return (
        (c1[0]-c2[0])**2 + 
        (c1[1]-c2[1])**2 + 
        (c1[2]-c2[2])**2
    ) ** 0.5

__all__ = [
    "RGB",
    "sRGB",
    "LinearRGB",
    "Oklab",
    "hex_code_to_rgb",
    "rgb_to_srgb",
    "srgb_to_linear",
    "linear_to_oklab",
    "oklab_to_linear",
    "linear_to_srgb",
    "srgb_to_rgb",
    "rgb_to_oklab",
    "oklab_to_rgb",
    "delta_e",
]

if __name__ == "__main__":
    print("Going from Hex Code to OKLab")
    c_hex = "#0088FF"
    print(f"Hex: {c_hex}")
    rgb = hex_code_to_rgb(c_hex)
    print(f"RGB: {rgb}")

    print("RGB to Oklab and back")
    oklab = rgb_to_oklab(rgb)
    print(f"Oklab:\t\t{oklab}")
    rgb_direct = oklab_to_rgb(oklab)
    print(f"RGB:\t\t{rgb_direct}\nShould be:\t{rgb}")
