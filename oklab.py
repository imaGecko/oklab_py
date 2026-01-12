from typing import Tuple

def str_hex_to_rgb(c:str) -> Tuple[int, int, int]:
    if not c.startswith('#'):
        raise Exception(f'Hex code must start with #\nGot {c}')
    if len(c) != 7:
        raise Exception(f'Hex string must have 7 characters #\nGot {len(c)} characters\n{c}')
    
    c_out = []
    for i in range(3):
        idx = 2*i+1
        c_out.append(int(c[idx:idx+2],16))

    return tuple(c_out)

def rgb_to_srgb(c:Tuple[int, int, int]) -> Tuple[float,float,float]:
    return (
        c[0]/255,
        c[1]/255,
        c[2]/255,
    )

def srgb_to_rgb(c:Tuple[float,float,float]) -> Tuple[int, int, int]:
    return (
        snap_float_to_rgb(c[0]*255),
        snap_float_to_rgb(c[1]*255),
        snap_float_to_rgb(c[2]*255)
    )

def snap_float_to_rgb(x:float) -> int:
    x = max(x, 0)
    x = min(x, 255)
    return int(x)

# rgb to linear rgb
# https://bottosson.github.io/posts/colorwrong/

def srgb_to_linear(c:Tuple[float,float,float]) -> Tuple[float,float,float]:
    return (
        f_inv(c[0]),
        f_inv(c[1]),
        f_inv(c[2])
    )

def linear_to_srgb(c:Tuple[float,float,float]) -> Tuple[float,float,float]:
    return (
        f(c[0]),
        f(c[1]),
        f(c[2])
    )

def f(x:float) -> float:
    if x >= 0.0031308:
        return 1.055 * x**(1.0/2.4) - 0.055
    return 12.92 * x

def f_inv(x:float) -> float:
    if x >= 0.04045:
        return ((x + 0.055)/(1 + 0.055))**2.4
    return x / 12.92 


# linear rgb to oklab
# https://bottosson.github.io/posts/oklab/

def linear_to_oklab(c:Tuple[float,float,float]) -> Tuple[float,float,float]:
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

def oklab_to_linear(c:Tuple[float,float,float]) -> Tuple[float,float,float]:
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


if __name__ == "__main__":
    print("Going from Hex Code to OKLab")
    c_hex = "#405060"
    print(f"Hex: {c_hex}")
    rgb = str_hex_to_rgb(c_hex)
    print(f"RGB: {rgb}")
    srgb = rgb_to_srgb(rgb)
    print(f"sRGB: {srgb}")
    lin_rgb = srgb_to_linear(srgb)
    print(f"Linear RGB: {lin_rgb}")
    oklab = linear_to_oklab(lin_rgb)
    print(f"Oklab: {oklab}")
    
    print("Reverting from Oklab to RGB")
    print(f"Oklab:\t\t{oklab}")
    lin_rgb_inv = oklab_to_linear(oklab)
    print(f"Linear RGB:\t{lin_rgb_inv}\nPrevious:\t{lin_rgb}")
    srgb_inv = linear_to_srgb(lin_rgb_inv)
    print(f"sRGB:\t\t{srgb_inv}\nPrevious:\t{srgb}")
    rgb_inv = srgb_to_rgb(srgb)
    print(f"RGB:\t\t{rgb_inv}\nPrevious:\t{rgb}")