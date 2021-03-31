
import pygame
##########################################################################
############################# Music Class #################################
##########################################################################

        

class MusicPlayer:
	def __init__(self):
		self.loadBgMusic()
		self.loadGameSounds()
		self.SFX= True
		self.music= True


	def loadBgMusic(self):
		pygame.mixer.init()
		pygame.mixer.music.load("assets/sound/bgMusic.mp3")
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.play(-1,0,10)

	def loadGameSounds(self):
		self.completedTube=pygame.mixer.Sound("assets/sound/completedTubeSound.mp3")
		self.selectLevel=pygame.mixer.Sound("assets/sound/selectLevelSound.mp3")
		self.hint=pygame.mixer.Sound("assets/sound/hintSound.mp3")
		self.button=pygame.mixer.Sound("assets/sound/buttonSound.mp3")
		self.selectLevel.set_volume(0.05)
		self.completedTube.set_volume(0.1)
		self.hint.set_volume(0.1)
		self.button.set_volume(0.1)

	def inMenu(self):
		pygame.mixer.music.set_volume(0.3)
		pygame.mixer.music.rewind()

	def enterLevel(self):
		pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.rewind()
		if self.SFX:
			self.selectLevel.play()

	def clickHint(self):
		if self.SFX:
			self.hint.play()

	def completeTube(self):
		if self.SFX:
			self.completedTube.play()

	def clickedButton(self):
		if self.SFX:
			self.button.play()

	def switchMusic(self):
		self.music=not self.music
		if self.music:
			pygame.mixer.music.unpause()
		else:
			pygame.mixer.music.pause()

	def switchSFX(self):
		self.SFX=not self.SFX