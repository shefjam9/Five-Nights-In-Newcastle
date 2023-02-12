from enum import IntFlag
import pygame
import globals
from anim import Animation

class ObstacleID(IntFlag):
  """ Flag so can be used for efficient sending of multiple obstacles"""
  OBJ_NONE = (1<<0),
  OBJ_BOTTLE = (1<<1),
  OBJ_DRUNK = (1<<2),
  OBJ_SPOONS = (1<<3),
  OBJ_THUG = (1<<4),
  OBJ_POLICE = (1<<5),
  OBJ_PIGEON  =(1<<6)

_TILE_MAP = {}
_DYNAMIC_TILE_MAP = {}

class DynamicObstacle:
    
    def __init__(self, obj_id: ObstacleID, init_pos: tuple, timestamp: float, lifespan: float):
        self._id = obj_id
        self._x = init_pos[0]
        self._y = init_pos[1]
        self._willdie = lifespan + timestamp
        self._marked_for_deletion = False
        print("Created dynamic obstacle")
    
    def render(self, surface):
        _DYNAMIC_TILE_MAP[self._id].render(surface, self._x, self._y)
      
    def should_delete(self):
        return self._marked_for_deletion
      
    def update(self, time):
        if time >= self._willdie:
            self._marked_for_deletion = True
        _DYNAMIC_TILE_MAP[self._id].update(time)

class Obstacle:
  def __init__(self, id: ObstacleID, timeout: int, lifespan: int, _client):
    """ Instance of a placable obstacle 
    id: ObstacleID of obstacle
    timeout: ms before obstacle can be used again by player"""
    self._id = id
    self._isavailable = False
    self._timeout = timeout
    self._perc = 0
    self._last_used = 0
    self._x, self._y = 0, 0
    self._current_time = 0
    self._dynamic_lifespan = lifespan
    self._client = _client
  
  def set_last_used(self, time):
    """ Last used time in ms"""
    self._last_used = time
    
  def is_available(self):
    """ Can the player use the obstacle? """
    return self._isavailable
  
  def get_percentage(self):
    """ return percentage progress to being available"""
    return self._perc
  
  def get_id(self):
    """ return id of obstacle"""
    return self._id
  
  def update(self, current_time: float):
    self._current_time = current_time
    """ Update obstacle """
    # set available if it is
    if not self._isavailable and (current_time - self._last_used) > self._timeout:
      self._isavailable = True
    # update percentage
    self._perc = min((current_time - self._last_used) / self._timeout, 1.0)
  
  def set_pos(self, x, y):
    """ Set position of obstacle """
    self._x = x
    self._y = y
  
  def render(self, surface: pygame.Surface, alpha_surface: pygame.Surface):
    """ Render obstacle tile """
    surface.blit(_TILE_MAP[self.get_id()], (self._x, self._y))
    pygame.draw.rect(surface, (0, 0, 0), (self._x, self._y, globals.TILE_SIZE, globals.TILE_SIZE), 1)
    # draw progress bar
    if not self._isavailable:
      pygame.draw.rect(alpha_surface, (0, 0, 0, 128), (self._x, self._y, 
                                                       globals.TILE_SIZE - globals.TILE_SIZE*self.get_percentage(), 
                                                       globals.TILE_SIZE))
    else:
      pygame.draw.rect(alpha_surface, (255, 255, 255, 10), (self._x, self._y, globals.TILE_SIZE, globals.TILE_SIZE))

  def does_collide(self, pos):
    """ Is pos within the bounds of this obstacle? """
    if pos[0] >= self._x and pos[0] <= self._x + globals.TILE_SIZE \
      and pos[1] >= self._y and pos[1] <= self._y + globals.TILE_SIZE:
      return True
    return False

  def place(self, pos):
    """ Plcae objecte at place"""
    add_dynamic(self.get_id(), (pos[0] - globals.TILE_SIZE/2, pos[1] - globals.TILE_SIZE/2), 
                self._current_time, self._dynamic_lifespan)
    self._last_used = self._current_time
    self._isavailable = False
    self._client.send_obstacle(self._id, pos[0], pos[1])

def load_tilemap():
  """ Load assets for obstacle tiles"""
  global _TILE_MAP
  global _DYNAMIC_TILE_MAP
  _TILE_MAP = {ObstacleID.OBJ_BOTTLE: pygame.image.load("res\\Bottle.png").convert_alpha(),
                ObstacleID.OBJ_DRUNK: pygame.image.load("res\\Drunk.png").convert_alpha(),
                ObstacleID.OBJ_SPOONS: pygame.image.load("res\\Knife.png").convert(),
                ObstacleID.OBJ_THUG: pygame.image.load("res\\Thug.png").convert_alpha(),
                ObstacleID.OBJ_POLICE: pygame.image.load("res\\Police.png").convert_alpha(),
                ObstacleID.OBJ_PIGEON: pygame.image.load("res\\Pigeon.png").convert_alpha()}
  _DYNAMIC_TILE_MAP = {ObstacleID.OBJ_BOTTLE: Animation("res\\Bottle_Animation.png", 8, 8),
                       ObstacleID.OBJ_DRUNK: pygame.image.load("res\\Drunk_Dynamic.png").convert(),
                       ObstacleID.OBJ_THUG: pygame.image.load("res\\Thug_Dynamic.png").convert(),
                       ObstacleID.OBJ_SPOONS: pygame.image.load("res\\Knife_Dynamic.png").convert_alpha(),
                       ObstacleID.OBJ_POLICE: Animation("res\\Police_Animation.png", 2, 4),
                       ObstacleID.OBJ_PIGEON: Animation("res\\Bottle_Animation.png", 8, 8)}
  if globals.TILE_SIZE != 128:
    _TILE_MAP = {id: pygame.transform.scale(_TILE_MAP[id], (globals.TILE_SIZE, globals.TILE_SIZE)) for id in _TILE_MAP}
    _DYNAMIC_TILE_MAP = {id: pygame.transform.scale(_DYNAMIC_TILE_MAP[id], (globals.TILE_SIZE, globals.TILE_SIZE)) for id in _DYNAMIC_TILE_MAP}


_obstacles = []
_dynamic_obstacles = []
_obj_selected = ObstacleID.OBJ_NONE
_x, _y = 0, 0
_width, _height = 0, 0
_tray  = None

_showing = False

def add_obstacle(id: ObstacleID, timeout: float, lifespan: int, client):
  """ Add obstacle to obstacles"""
  _obstacles.append(Obstacle(id, timeout, lifespan, client))

def add_dynamic(id: ObstacleID, pos: tuple, time: float, lifespan: float):
  _dynamic_obstacles.append(DynamicObstacle(id, pos, time, lifespan))

def clear_dynamics(time):
  to_remove = []
  for obj in _dynamic_obstacles:
    obj.update(time)
    if obj.should_delete():
      to_remove.append(obj)
  for obj in to_remove:
    _dynamic_obstacles.remove(obj)
    print("Removed dynamic object!")

def calc_bounds():
  """ Calculate the positions of all of the obstacles
  Might as well only do it once
  """
  y_offset = 70
  x_offset = 20
  global _width, _height
  for i,obj in enumerate(_obstacles):
    x_pos = i%6
    y_pos = i//6
    x = _x + x_offset + (globals.TILE_SIZE + 20)*x_pos
    y = _y + y_offset + (globals.TILE_SIZE + 20)*y_pos
    obj.set_pos(x, y)
  _width = _tray.get_width()
  _height = _tray.get_height()


    

def init_obstacles(x: float, y: float, time: float, client):
  """ Initialise obstacles"""
  # load assets
  load_tilemap()
  global _x, _y, _tray
  _x, _y = x, y
  # -------------- ADD OBSTACLES HERE!!! --------------
  add_obstacle(ObstacleID.OBJ_PIGEON, 1000, 10e3, client)
  add_obstacle(ObstacleID.OBJ_BOTTLE, 2e3, 1000, client)
  add_obstacle(ObstacleID.OBJ_DRUNK, 10000, 5e3, client)
  add_obstacle(ObstacleID.OBJ_SPOONS, 5000, 2e3, client)
  add_obstacle(ObstacleID.OBJ_THUG, 7500, 5e3, client)
  add_obstacle(ObstacleID.OBJ_POLICE, 11000, 20e3, client)
  _tray = pygame.image.load("res\\Tray.png").convert_alpha()
  _x = (globals.SCREEN_DIMENSIONS[0] - _tray.get_width())/2
  _y = globals.SCREEN_DIMENSIONS[1] - 50
  # calculate obstacle bounds
  calc_bounds()
  # set their last used time
  for obj in _obstacles:
    obj.set_last_used(time)

def get_obstacle_by_id(id: ObstacleID):
  """ Gets the first static object of the given id"""
  for obj in _obstacles:
    if obj.get_id() == id:
      return obj

def update(time: float):
  """ Update all obstacles"""
  for _ob in _obstacles:
    _ob.update(time)
  clear_dynamics(time)

def render(surface: pygame.Surface) -> None:
  """ Render all obstacles"""
  surface.blit(_tray, (_x, _y))
  if not _showing:
    return
  alpha_surface = pygame.Surface(globals.SCREEN_DIMENSIONS, pygame.SRCALPHA)
  for _ob in _obstacles:
    _ob.render(surface, alpha_surface)
  surface.blit(alpha_surface, (0, 0))
  for _ob in _dynamic_obstacles:
    _ob.render(surface)

def handle_input(event: pygame.event.Event):
  """ Handle events sent to the obstacle manager"""
  global _obj_selected, _showing, _y
  # we only care about mouse pressses
  if event.type == pygame.MOUSEBUTTONUP:
    pos = pygame.mouse.get_pos()
    if not _showing:
      if pos[1] >= globals.SCREEN_DIMENSIONS[1] - 50:
        _showing = True
        _y = globals.SCREEN_DIMENSIONS[1] - _tray.get_height()
        calc_bounds()
        print("Shown!!")
        return
    found = False
    # if the mouse collides with any of the obstacles then set it to the currently selected
    for obj in _obstacles:
        if obj.does_collide(pos) and obj.is_available():
          found = True
          print(f"Changed object selected to {_obj_selected}")
          _obj_selected = obj.get_id()
    # if the mouse does not collide, place the obstacle selected if applicable
    if not found:
      if _obj_selected != ObstacleID.OBJ_NONE:
        get_obstacle_by_id(_obj_selected).place(pos)
      print("Reset object selected!")
      _obj_selected = ObstacleID.OBJ_NONE
