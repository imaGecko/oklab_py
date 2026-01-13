from oklab_lite import rgb_to_oklab, oklab_to_rgb, RGB

COLOURS = [
    (0,0,0),
    (255,255,255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0), 
    (255, 0, 255), 
    (0, 255, 255)
]

GRAYS = [
    (1, 1, 1),
    (32, 32, 32),
    (128, 128, 128),
    (200, 200, 200),
]

def _test_roundtrip(c:RGB) -> None:
    assert oklab_to_rgb(rgb_to_oklab(c)) == c

def test_colours() -> None:
    for c in COLOURS: _test_roundtrip(c)
    
def test_grays() -> None:
    for c in GRAYS: _test_roundtrip(c)
