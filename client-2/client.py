import time
import ctypes
import pygame

import gamemap as GameMap
import obstacle as ObstacleManager
import globals
from player import Player

""" -------- Client functions -----------"""

_running: bool = False
_player_instance: Player = None

def get_client_time_ms() -> float:
  """ Return client time in ms"""
  return time.perf_counter() * 1e3

_global_tickbase: int = 0                       # number of ticks elapsed on this client (help sync with other client)
_ticks_per_second: int = 60                     # number of ticks per second
_ms_per_tick: float = 1e3 / _ticks_per_second   # ms per tick

def get_client_time() -> int:
  """ get total client ticks elapsed"""
  return _global_tickbase

_surface: pygame.Surface = None

""" ------------------------------ """

def _init():
  """ Initialise the client"""
  # prevent windows scaling from being an issue #fuckwindows
  ctypes.windll.user32.SetProcessDPIAware()
  globals.setup_scaling()
  # pygame stuff
  pygame.init()
  global _surface, _running
  _surface = pygame.display.set_mode(globals.SCREEN_DIMENSIONS, pygame.DOUBLEBUF | pygame.NOFRAME)
  _running = True
  # initialise client objects
  GameMap.init_map()
  ObstacleManager.init_obstacles(200, 1000, get_client_time_ms())
  global _player_instance
  _player_instance = Player("hello")

def _handle_input():
  """ Handle all input"""
  global _running
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      _running = False
    else:
      ObstacleManager.handle_input(event)

def _update():
  """ Update the client"""
  ctime = get_client_time_ms()
  GameMap.update(ctime)
  ObstacleManager.update(ctime)
  _player_instance.update(ctime)

def _render():
  """ Render the client """
  GameMap.render(_surface)
  ObstacleManager.render(_surface)
  _player_instance.render(_surface)
  pygame.display.update()

def run():
  _init()
  global _running, _global_tickbase
  # variables to ensure desired tick rate
  pTime = get_client_time_ms()
  lag = 0
  timer = 0
  updates, frames = 0, 0
  while(_running):
    cTime = get_client_time_ms()
    eTime = cTime - pTime
    lag += eTime
    timer += eTime
    # every second do this
    if timer >= 1e3:
      print(f"Frames: {frames}")
      print(f"Updates: {updates}")
      frames, updates = 0, 0
      timer -= 1e3
    _handle_input()
    # update as many times as needed to catch up
    while lag >= _ms_per_tick:
      _update()
      _global_tickbase += 1
      updates += 1
      lag -= _ms_per_tick
    _render()
    frames += 1
    pTime = cTime


if __name__ == "__main__":
  run()
