class Object:
	pass

class hitsoundData:
	pass

class BeatmapData:
	def __init__():
		self.objects = []
		self.mode = 0
	def mp3(mp3):
		self.mp3 = mp3
	def general(stackLeniency, mode):
		self.stackLeniency = stackLeniency
		self.mode = mode
	def difficulty(hp,cs,od,ar,sm,st):
		#sm = SliderMultiplier, st = SliderTickRate
		self.hp = hp
		self.cs = cs
		self.od = od
		self.ar = ar
		self.sm = sm
		self.st = st
	def metadata(title, id):
		self.title = title
		self.id = id
	def addobjects(object):
		self.objects.append(object)
	def sortobjectTime():
		self.objects.sort()