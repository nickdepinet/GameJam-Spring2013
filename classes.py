class Point :
	__slots__ = ('x', 'y')

	def __init__(self, x, y) :
		self.x = x
		self.y = y

class Level :
	__slots__ = ('map', 'start', 'goal', 'width', 'height')

	def __init__(self, map, start, goal) :
		self.map = map
		# start.x = 288
		# start.y = 272
		self.start = start
		self.goal = goal
		self.width = len(map)
		self.height = len(map[0])

class Player :
	__slots__ = ('sprite', 'rect', 'x', 'y')

	def __init__(self, sprite, rect, x = 0, y = 0) :
		self.sprite = sprite
		self.rect = rect
		self.x = x
		self.y = y
	
	def pos(self, point) :
		self.x = point.x
		self.y = point.y