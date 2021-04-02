
import pygame

from game.utils import *




########################## Screen Dimensions #############################
screen_width = 1400
screen_height = 1000


##########################################################################
############################# Menu Class #################################
##########################################################################

        

class Menu:
	def __init__(self):
		self.getButtons()
		self.getTitle()
		self.getQuit()
		
		
	def getTitle(self):
		sprite = loadSprite("assets/img/titles/BallSort.png")
		sprite.rect.left,sprite.rect.top=[380,50]
		self.title=pygame.sprite.GroupSingle(sprite)	

	def getButtons(self):
		img = pygame.image.load("assets/img/holders/MainMenuHolder.png")
		font = pygame.font.SysFont("Arial", 70)
		play = textToSprite("Play",img,(230,230,230),[500,300],font)
		watch = textToSprite("Watch",img,(230,230,230),[500,500],font)
		settings = textToSprite("Settings",img,(230,230,230),[500,700],font)

		self.play=pygame.sprite.GroupSingle(play)
		self.watch=pygame.sprite.GroupSingle(watch)
		self.settings=pygame.sprite.GroupSingle(settings)
		


	def getQuit(self):
		quit = loadSprite("assets/img/buttons/quit.png")
		quit.rect.left=20
		quit.rect.top=20
		self.quit=pygame.sprite.GroupSingle(quit)

	def draw(self,screen):
		self.title.draw(screen)
		self.quit.draw(screen)
		self.play.draw(screen)
		self.watch.draw(screen)
		self.settings.draw(screen)


	def checkMenuCols(self):
		mouse_pos=pygame.mouse.get_pos()
		
		
		if self.play.sprite.rect.collidepoint(mouse_pos):
			return 1
		
		if self.watch.sprite.rect.collidepoint(mouse_pos):
			return 2

		if self.settings.sprite.rect.collidepoint(mouse_pos):
			return 3

		if(self.quit.sprite.rect.collidepoint(mouse_pos)):
			return 0
		return -1


##########################################################################
########################## SettingsMenu Class ############################
##########################################################################

        

class SettingsMenu:
	def __init__(self):
		self.getButtons()
		self.getTitle()
		self.getBack()
		
		
	def getTitle(self):
		sprite = loadSprite("assets/img/titles/Settings.png")
		sprite.rect.left,sprite.rect.top=[380,50]
		self.title=pygame.sprite.GroupSingle(sprite)	

	def getButtons(self):
		self.sfxActive = True
		self.musicActive = True
		self.currHint = 0


		img = pygame.image.load("assets/img/holders/SettingsHolders.png")
		hintImg = pygame.image.load("assets/img/holders/level.png")
		offBg = pygame.image.load("assets/img/holders/offBg.png")
		onBg = pygame.image.load("assets/img/holders/onBg.png")
		font = pygame.font.SysFont("Arial", 60)
		font2 = pygame.font.SysFont("Arial", 50)
		off1 = textToSprite("Off",offBg,(0,0,0),[810,410],font2)
		off2 = textToSprite("Off",offBg,(0,0,0),[810,560],font2)
		on1 = textToSprite("On",onBg,(230,230,230),[810,410],font2)
		on2 = textToSprite("On",onBg,(230,230,230),[810,560],font2)

		music = textToSprite("Music",img,(230,230,230),[390,400],font)
		sfx = textToSprite("SFX",img,(230,230,230),[390,550],font)
		
		
		hint = textToSprite("Hint",img,(230,230,230),[390,700],font)
		greedy = textToSprite("greedy",hintImg,(230,230,230),[800,700],font2)
		astar = textToSprite("A*",hintImg,(230,230,230),[800,700],font2)
		bfs = textToSprite("BFS",hintImg,(230,230,230),[800,700],font2)
		dfs = textToSprite("DFS",hintImg,(230,230,230),[800,700],font2)
		ids = textToSprite("IDS",hintImg,(230,230,230),[800,700],font2)
	



	
		self.music = pygame.sprite.GroupSingle(music)
		self.sfx = pygame.sprite.GroupSingle(sfx)
		self.musicOff = pygame.sprite.GroupSingle(off1)
		self.musicOn = pygame.sprite.GroupSingle(on1)
		self.sfxOff = pygame.sprite.GroupSingle(off2)
		self.sfxOn = pygame.sprite.GroupSingle(on2)




		self.hint = pygame.sprite.GroupSingle(hint)
		self.algorithms = []
		self.algorithms.append(pygame.sprite.GroupSingle(astar))
		self.algorithms.append(pygame.sprite.GroupSingle(greedy))
		self.algorithms.append(pygame.sprite.GroupSingle(dfs))
		self.algorithms.append(pygame.sprite.GroupSingle(bfs))
		self.algorithms.append(pygame.sprite.GroupSingle(ids))
		
		


	def getBack(self):
		back = loadSprite("assets/img/buttons/back.png")
		back.rect.left=20
		back.rect.top=20
		self.back=pygame.sprite.GroupSingle(back)

	def draw(self,screen):
		self.title.draw(screen)
		self.back.draw(screen)
		self.music.draw(screen)
		self.sfx.draw(screen)
		if self.sfxActive:
			self.sfxOn.draw(screen)
		else:
			self.sfxOff.draw(screen)

		if self.musicActive:
			self.musicOn.draw(screen)
		else:
			self.musicOff.draw(screen)
		self.drawHint(screen)


	def drawHint(self,screen):
		self.hint.draw(screen)
		self.algorithms[self.currHint].draw(screen)


	def checkMenuCols(self):
		mouse_pos=pygame.mouse.get_pos()
		
		
		if self.sfxOn.sprite.rect.collidepoint(mouse_pos):
			self.sfxActive= not self.sfxActive
			return 1
		
		if self.musicOn.sprite.rect.collidepoint(mouse_pos):
			self.musicActive= not self.musicActive
			return 2

		if(self.back.sprite.rect.collidepoint(mouse_pos)):
			return 0

		if(self.algorithms[self.currHint].sprite.rect.collidepoint(mouse_pos)):
			self.currHint+=1
			if(self.currHint>=5):
				self.currHint=0
			return self.currHint + 3
		return -1








##########################################################################
############################# Game Menu Class #################################
##########################################################################

        

class GameMenu:
	def __init__(self,levels):
		self.getLevels(levels)
		self.getNextPrev()
		self.getBack()
		
		

	def getLevels(self,levels):
		self.levels=[]
		self.currPage=0
		self.totalPages=0
		levelsPage=pygame.sprite.Group()
		img = pygame.image.load("assets/img/holders/level.png")
		font = pygame.font.SysFont("Arial", 70)
		
		x=200
		y=150
		rows = 3
		x_inc = (screen_width-x)//3
		y_inc = (screen_height-y)//rows
		
		for i in range(1,len(levels)+1):
			if i%9==1 and i>1:
				copy=levelsPage.copy()
				self.levels.append(copy)
				pygame.sprite.Group.empty(levelsPage)
				self.totalPages+=1
				x=200
				y=150
			
			sprite = textToSprite(str(i),img,(230,230,230),[x,y],font)
			levelsPage.add(sprite)

			if i%3==0 and i>0:
				x=200
				y+=y_inc
			else:
				x+=x_inc

		if len(levels)%9!=0:
			self.levels.append(levelsPage)
			

	def getNextPrev(self):
		img = pygame.image.load("assets/img/holders/prevNext.png")
		font = pygame.font.SysFont("Arial", 35)
		nextSprite = textToSprite("Next",img,(230,230,230),[1200,900],font)
		prevSprite = textToSprite("Prev",img,(230,230,230),[1050,900],font)
		self.next=pygame.sprite.GroupSingle(nextSprite)
		self.prev=pygame.sprite.GroupSingle(prevSprite)
		


	def getBack(self):
		back = loadSprite("assets/img/buttons/back.png")
		back.rect.left=20
		back.rect.top=20
		self.back=pygame.sprite.GroupSingle(back)

	def draw(self,screen):
		self.back.draw(screen)
		self.levels[self.currPage].draw(screen)
		if self.currPage>0:
			self.prev.draw(screen)
		if self.currPage<self.totalPages:
			self.next.draw(screen)


	def checkMenuCols(self):
		mouse_pos=pygame.mouse.get_pos()
		
		if self.currPage>0:
			if self.prev.sprite.rect.collidepoint(mouse_pos):
				self.currPage-=1
				return -2
		if self.currPage<self.totalPages:
			if self.next.sprite.rect.collidepoint(mouse_pos):
				self.currPage+=1
				return -2
		i=0
		for k in self.levels[self.currPage]:
			i+=1
			if k.rect.collidepoint(mouse_pos):
				return 9*self.currPage+i
		if(self.back.sprite.rect.collidepoint(mouse_pos)):
			return 0

		
		

		return -1
