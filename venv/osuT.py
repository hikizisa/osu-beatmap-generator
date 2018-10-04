class Object:
	pass

class BeatmapData:
	def __init__():
		self.objects = []
	def general(stackLeniency, mode):
		self.stackLeniency = 0
		self.mode = mode
	def difficulty(hp,cs,od,ar,sm,st):
		#sm = SliderMultiplier, st = SliderTickRate
		self.hp = hp
		self.cs = cs
		self.od = od
		self.ar = ar
		self.sm = sm
		self.st = st
	def addobjects(object):
		self.objects.append(object)
	def sortobjectTime():
		self.objects.sort()

class SongData:
	def __init__():
		self.fft = []