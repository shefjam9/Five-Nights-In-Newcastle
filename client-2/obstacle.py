from enum import IntFlag
import pygame
import globals

class ObstacleID(IntFlag):
  """ Flag so can be used for efficient sending of multiple obstacles"""
  OBJ_NONE = (1<<0),
  OBJ_BOTTLE = (1<<1),
  OBJ_DRUNK = (1<<2),
  OBJ_SPOONS = (1<<3),
  OBJ_THUG = (1<<4)

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
        surface.blit(_DYNAMIC_TILE_MAP[self._id], (self._x, self._y))
      
    def should_delete(self):
        return self._marked_for_deletion
      
    def update(self, time):
        if time >= self._willdie:
            self._marked_for_deletion = True

class Obstacle:
  def __init__(self, id: ObstacleID, timeout: int, lifespan: int):
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
    #TODO networking here :)
    # eg. Network.write(obstacleID, x, y, timeout)
    # Network.send()
    pass

def load_tilemap():
  """ Load assets for obstacle tiles"""
  global _TILE_MAP
  global _DYNAMIC_TILE_MAP
  _TILE_MAP = {ObstacleID.OBJ_BOTTLE: pygame.image.load("res\\Bottle.png").convert(),
                ObstacleID.OBJ_DRUNK: pygame.image.load("res\\Drunk.png").convert_alpha(),
                ObstacleID.OBJ_SPOONS: pygame.image.load("res\\Knife.png").convert(),
                ObstacleID.OBJ_THUG: pygame.image.load("res\\Thug.png").convert_alpha()}
  _DYNAMIC_TILE_MAP = {ObstacleID.OBJ_BOTTLE: pygame.image.load("res\\Glass_Broken.png").convert(),
                       ObstacleID.OBJ_DRUNK: pygame.image.load("res\\Drunk_Dynamic.png").convert(),
                       ObstacleID.OBJ_THUG: pygame.image.load("res\\Thug_Dynamic.png").convert()}
  if globals.TILE_SIZE != 128:
    _TILE_MAP = {id: pygame.transform.scale(_TILE_MAP[id], (globals.TILE_SIZE, globals.TILE_SIZE)) for id in _TILE_MAP}
    _DYNAMIC_TILE_MAP = {id: pygame.transform.scale(_DYNAMIC_TILE_MAP[id], (globals.TILE_SIZE, globals.TILE_SIZE)) for id in _DYNAMIC_TILE_MAP}


_obstacles = []
_dynamic_obstacles = []
_obj_selected = ObstacleID.OBJ_NONE
_x, _y = 0, 0
_width, _height = 0, 0

def add_obstacle(id: ObstacleID, timeout: float, lifespan: int):
  """ Add obstacle to obstacles"""
  _obstacles.append(Obstacle(id, timeout, lifespan))

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
  global _width, _height
  # work out number of columns and rows
  num_cols = 6 if len(_obstacles) > 6 else len(_obstacles)
  num_rows = (len(_obstacles) // 6) + 1
  # total width for the obstacle menu to take up
  total_width = (1 + globals.TILE_SIZE)*6 + 1
  # total width the actual obstacle tiles will take up
  draw_width = total_width-2 if num_cols >= 6 else (len(_obstacles)*(1+globals.TILE_SIZE)-1)
  draw_offset = int((total_width - draw_width) / 2)
  # set their positions
  for i, obj in enumerate(_obstacles):
    x_ind = i % 6
    y_ind = (i//6)
    obj.set_pos(_x + draw_offset + x_ind*(globals.TILE_SIZE+1), _y + y_ind*globals.TILE_SIZE)
  _width = total_width
  _height = globals.TILE_SIZE
    

def init_obstacles(x: float, y: float, time: float):
  """ Initialise obstacles"""
  # load assets
  load_tilemap()
  global _x, _y
  _x, _y = x, y
  # -------------- ADD OBSTACLES HERE!!! --------------
  add_obstacle(ObstacleID.OBJ_BOTTLE, 1000, 10e3)
  add_obstacle(ObstacleID.OBJ_DRUNK, 10000, 5e3)
  add_obstacle(ObstacleID.OBJ_SPOONS, 5000, 2e3)
  add_obstacle(ObstacleID.OBJ_THUG, 7500, 5e3)
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
  alpha_surface = pygame.Surface(globals.SCREEN_DIMENSIONS, pygame.SRCALPHA)
  for _ob in _obstacles:
    _ob.render(surface, alpha_surface)
  # Draw rect around obstacle menu TODO all these graphics are temporary
  pygame.draw.rect(surface, (0, 0, 0), (_x, _y, _width, _height), 1)
  surface.blit(alpha_surface, (0, 0))
  for _ob in _dynamic_obstacles:
    _ob.render(surface)

def handle_input(event: pygame.event.Event):
  """ Handle events sent to the obstacle manager"""
  global _obj_selected
  # we only care about mouse pressses
  if event.type == pygame.MOUSEBUTTONUP:
    pos = pygame.mouse.get_pos()
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