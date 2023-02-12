import time
import ctypes
import pygame

import gamemap as GameMap
import obstacle as ObstacleManager
import globals
from player import Player
from client import Client
import threading

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

_client = None
_client_thread = None

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

  global _client, _client_thread
  _client = Client('127.0.0.1', 6969)
  _client_thread = threading.Thread(target=_client.run)
  _client_thread.setDaemon(True)
  _client_thread.start()

def _handle_input():
  """ Handle all input"""
  global _running
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
      _running = False
    else:
      ObstacleManager.handle_input(event)

def _update():
  """ Update the client"""
  ctime = get_client_time_ms()
  GameMap.update(ctime)
  ObstacleManager.update(ctime)

def _render():
  """ Render the client """
  GameMap.render(_surface)
  ObstacleManager.render(_surface)
  pos_x, pos_y = 360 + 1200*float(_client.pos.x)/3200, 1200*float(_client.pos.y)/3200
  pygame.draw.rect(_surface, (255, 0, 0), (pos_x, pos_y, 10, 10))

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
