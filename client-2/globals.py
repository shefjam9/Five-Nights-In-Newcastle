import ctypes

_DEFAULT_DIMENSIONS: tuple = (1920, 1080)
SCREEN_DIMENSIONS: tuple = None
TILE_SIZE: int = 128


def setup_scaling():
  global SCREEN_DIMENSIONS, TILE_SIZE
  user32 = ctypes.windll.user32
  SCREEN_DIMENSIONS = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
  print(SCREEN_DIMENSIONS)
  scale = SCREEN_DIMENSIONS[0] / _DEFAULT_DIMENSIONS[0]
  if scale != 1:
    TILE_SIZE *= scale
    print(f"Scaled tile size by: {scale}")