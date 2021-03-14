import os
import time
import copy
import json
from pygame.locals import *

import pygame


from solver import *
from tube import *

#level box size: width-200 height-100




##########################################################################
########################### Global Variables #############################
##########################################################################

mouse_timeout=0.15


########################## Screen Dimensions #############################
screen_width = 1400
screen_height = 1000



############################ Dictionaries ################################
with open('levels.json') as f:
  	levels = json.load(f)

for level in levels:
	tubes = levels[level]['tubes']
	new_tubes = []
	for tube in tubes:
		new_tubes.append(Tube(tube))
	levels[level] = new_tubes


ball_dict = {
	1:"blueBall.png",
	2:"pinkBall.png",
	3:"darkGreenBall.png",
	4:"orangeBall.png",
	5:"redBall.png",
	6:"purpleBall.png",
	7:"darkRedBall.png",
	8:"yellowBall.png",
	9:"darkPurpleBall.png",
	10:"lightBlueBall.png",
	11:"greenBall.png",
	12:"darkBlueBall.png"
}


######################## Load Sprite functions ###########################
def loadSprite(file):
		img = pygame.image.load(file)
		sprite = pygame.sprite.Sprite()
		sprite.image=img
		sprite.rect=img.get_rect()
		return sprite

def textToSprite(text,img,color,pos,font):

	
	textSurf = font.render(text, 1, color)
	
	background = pygame.Surface((img.get_width(), img.get_height()))
	
	background.blit(img,[0,0])

	width = textSurf.get_width()
	height = textSurf.get_height()

	background.blit(textSurf, [img.get_width()/2 - width/2, img.get_height()/2 - height/2])

	sprite = pygame.sprite.Sprite()
	sprite.image=background
	sprite.rect=background.get_rect()
	sprite.rect.left, sprite.rect.top = pos


	return sprite



def onlyTextSprite(text,color,pos,font):
	textSurf = font.render(text, 1, color)
	sprite = pygame.sprite.Sprite()

	background = pygame.Surface((textSurf.get_width()*1.1, textSurf.get_height()*1.1),pygame.SRCALPHA)

	background.blit(textSurf, [textSurf.get_width()*0.05, textSurf.get_height()*0.05])
	sprite.image=background
	sprite.rect=background.get_rect()
	sprite.rect.left, sprite.rect.top = pos

	return sprite


##########################################################################
############################# Timer Class ################################
##########################################################################

class Timer:
	def __init__(self,timer):
		self.time=timer
		self.timer=time.time()

	def startTimer(self):
		self.timer=time.time()+self.time

	def checkTimer(self):
		if self.timer < time.time():
			self.timer=time.time()+self.time
			return True
		return False



##########################################################################
############################# Score Class ################################
##########################################################################

class Score:
	def __init__(self,coords):
		self.coords=coords
		self.loadNumbers()
		self.score=0

	def setScore(self,score):
		self.score=score
	
	def increaseScore(self):
		self.score+=1

	def decreaseScore(self):
		self.score-=1

	def loadNumbers(self):
		self.numbers=[]
		font = pygame.font.SysFont("Arial", 50)
		for i in range(0,10):
			num=onlyTextSprite(str(i),(0,0,0),self.coords,font)
			
			number=pygame.sprite.GroupSingle(num)
			self.numbers.append(number)

	def draw(self,screen):
		num1=self.score//100
		num2=self.score%100//10
		num3=self.score%10

		self.numbers[num1].sprite.rect.left=self.coords[0]
		self.numbers[num1].draw(screen)
		self.numbers[num2].sprite.rect.left=self.coords[0]+35
		self.numbers[num2].draw(screen)
		self.numbers[num3].sprite.rect.left=self.coords[0]+70
		self.numbers[num3].draw(screen)






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
		self.completedTube=pygame.mixer.Sound("assets/sound/completedTubeSound.wav")
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
		watch = textToSprite("Watch",img,(120,120,120),[500,500],font)
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

		img = pygame.image.load("assets/img/holders/SettingsHolders.png")
		offBg = pygame.image.load("assets/img/holders/offBg.png")
		onBg = pygame.image.load("assets/img/holders/onBg.png")
		font = pygame.font.SysFont("Arial", 60)
		font2 = pygame.font.SysFont("Arial", 50)
		off1 = textToSprite("Off",offBg,(0,0,0),[810,410],font2)
		off2 = textToSprite("Off",offBg,(0,0,0),[810,610],font2)
		on1 = textToSprite("On",onBg,(230,230,230),[810,410],font2)
		on2 = textToSprite("On",onBg,(230,230,230),[810,610],font2)
		music = textToSprite("Music",img,(230,230,230),[390,400],font)
		sfx = textToSprite("SFX",img,(230,230,230),[390,600],font)

		
		self.music = pygame.sprite.GroupSingle(music)
		self.sfx = pygame.sprite.GroupSingle(sfx)
		self.musicOff = pygame.sprite.GroupSingle(off1)
		self.musicOn = pygame.sprite.GroupSingle(on1)
		self.sfxOff = pygame.sprite.GroupSingle(off2)
		self.sfxOn = pygame.sprite.GroupSingle(on2)
		


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
		return -1








##########################################################################
############################# Game Menu Class #################################
##########################################################################

        

class GameMenu:
	def __init__(self):
		self.getLevels()
		self.getNextPrev()
		self.getBack()
		
		

	def getLevels(self):
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




##########################################################################
########################## End Screen Class ##############################
##########################################################################


class EndScreen:
	def __init__(self):
		self.coords=[800,450]
		self.loadNumbers()
		self.loadLevelPassed()
		self.loadHolders()
		self.loadText()
		self.loadBackToMenu()


	def loadNumbers(self):
		self.numbers=[]
		font = pygame.font.SysFont("Arial", 70)
		for i in range(0,10):
			num=onlyTextSprite(str(i),(0,0,0),self.coords,font)
			
			number=pygame.sprite.GroupSingle(num)
			self.numbers.append(number)


	def loadLevelPassed(self):
		sprite = loadSprite("assets/img/titles/levelPassed.png")
		sprite.rect.left,sprite.rect.top=[350,200]
		self.passed=pygame.sprite.GroupSingle(sprite)

	def loadHolders(self):
		sprite = loadSprite("assets/img/holders/endScoreHolder.png")
		sprite.rect.left,sprite.rect.top=[self.coords[0]-10,self.coords[1]]
		self.scoreHolder=pygame.sprite.GroupSingle(sprite)
		copy =  loadSprite("assets/img/holders/endScoreHolder.png")
		copy.rect.left,copy.rect.top=[self.coords[0]-10,self.coords[1]+190]
		self.undoHolder=pygame.sprite.GroupSingle(copy)


	def loadText(self):
		font = pygame.font.SysFont("Arial", 50)
		img = pygame.image.load("assets/img/holders/TextHolder.png")
		move=textToSprite("Move Count: ",img,(230,230,230),[350,self.coords[1]-10],font)
		undo=textToSprite("Undo Count: ",img,(230,230,230),[350,self.coords[1]+180],font)
		self.moveText=pygame.sprite.Group(move)
		self.undoText=pygame.sprite.Group(undo)

	def loadBackToMenu(self):
		back = loadSprite("assets/img/buttons/backToMenu.png")
		back.rect.left, back.rect.top=[500,800]
		self.backToMenu=pygame.sprite.GroupSingle(back)


	def draw(self, screen, score, undo):
		self.passed.draw(screen)
		self.drawBackToMenu(screen)
		self.drawHolders(screen)
		self.drawScore(screen,score)
		self.drawUndo(screen,undo)
		
	def drawHolders(self,screen):
		self.scoreHolder.draw(screen)
		self.undoHolder.draw(screen)
		self.moveText.draw(screen)
		self.undoText.draw(screen)


	def drawScore(self,screen,score):
		num1=score//100
		num2=score%100//10
		num3=score%10

		self.numbers[num1].sprite.rect.top=self.coords[1]-5
		self.numbers[num1].sprite.rect.left=self.coords[0]
		self.numbers[num1].draw(screen)

		self.numbers[num2].sprite.rect.top=self.coords[1]-5
		self.numbers[num2].sprite.rect.left=self.coords[0]+70
		self.numbers[num2].draw(screen)

		self.numbers[num3].sprite.rect.top=self.coords[1]-5
		self.numbers[num3].sprite.rect.left=self.coords[0]+140
		self.numbers[num3].draw(screen)
	
	def drawUndo(self,screen,undo):
		num1=undo//100
		num2=undo%100//10
		num3=undo%10

		self.numbers[num1].sprite.rect.top=self.coords[1]+185
		self.numbers[num1].sprite.rect.left=self.coords[0]
		self.numbers[num1].draw(screen)

		self.numbers[num2].sprite.rect.top=self.coords[1]+185
		self.numbers[num2].sprite.rect.left=self.coords[0]+70
		self.numbers[num2].draw(screen)

		self.numbers[num3].sprite.rect.top=self.coords[1]+185
		self.numbers[num3].sprite.rect.left=self.coords[0]+140
		self.numbers[num3].draw(screen)


	def drawBackToMenu(self,screen):
		self.backToMenu.draw(screen)
	
	def checkBackCol(self,mouse_pos):
		return self.backToMenu.sprite.rect.collidepoint(mouse_pos)


##########################################################################
############################# Flask Class ################################
##########################################################################

class Flask:
	def __init__(self,tube,coords):
		self.tube=tube
		self.coords=coords
		self.balls=pygame.sprite.Group()
		self.createFlask()
		self.loadBalls()
		self.selected=False
		self.completed=False
		

	def createFlask(self):
		self.loadDefaultFlask()
		self.loadSelectedFlask()
		self.loadCompletedFlask()
		
		
############################ Load functions #################################
	def loadDefaultFlask(self):
		flask = loadSprite("assets/img/flasks/flask-white.png")
		flask.rect.left=self.coords[0]
		flask.rect.top=self.coords[1]
		self.flask = pygame.sprite.GroupSingle(flask)

	def loadSelectedFlask(self):	
		selected = loadSprite("assets/img/flasks/flask-4-selected.png")
		selected.rect.left=self.coords[0]
		selected.rect.top=self.coords[1]
		self.flask_sel = pygame.sprite.GroupSingle(selected)

	def loadCompletedFlask(self):
		completed = loadSprite("assets/img/flasks/flask-4-completed.png")
		completed.rect.left=self.coords[0]
		completed.rect.top=self.coords[1]
		self.flask_comp = pygame.sprite.GroupSingle(completed)


	def loadBalls(self):
		x=self.coords[0]+12
		y=self.coords[1]+290
		for num in self.tube.get_balls():
			y-=73
			self.loadBall(num,[x,y])

	def loadBall(self,num,coords):
		ballFile=ball_dict.get(num)
		ball = loadSprite("assets/img/balls/" +ballFile)
		ball.rect.left=coords[0]
		ball.rect.top=coords[1]
		self.balls.add(ball)



############################ Draw functions #################################
	def draw(self,screen):
		self.balls.draw(screen)
		if self.selected:
			self.flask_sel.draw(screen)
		elif self.completed:
			self.flask_comp.draw(screen)
		else:
			self.flask.draw(screen)

	
############################ Game functions #################################
	def remove_ball(self):
		sprites=self.balls.sprites()
		ball=sprites[-1]
		pygame.sprite.Group.remove(self.balls,ball)
		self.completed=False
		return ball

	def add_ball(self, ball):
		ball.rect.left=self.coords[0]+12
		ball.rect.top=self.coords[1]+290-73*(len(self.balls)+1)
		self.balls.add(ball)
		if self.tube.is_completed():
			self.completed=True
			return 1
		return 0

	def select(self):
		self.selected = not self.selected
		if len(self.balls)>0:
			if self.selected:
				ball=self.balls.sprites()[-1]
				ball.rect.top=self.coords[1]-100
			if not self.selected:
				ball=self.balls.sprites()[-1]
				ball.rect.top=self.coords[1]+290-73*len(self.balls)
	
		
	def checkMouseCol(self,mouse_pos):
		return self.flask.sprite.rect.collidepoint(mouse_pos)

	def checkDone(self):
		return self.tube.is_completed() or self.tube.is_empty()
	



##########################################################################
############################# UI Class ###################################
##########################################################################

class UI:
	def __init__(self):
		self.state="MAINMENU"
		self.init_screen()
		self.loadOther()
		self.buildMenu()
		self.buildMainMenu()
		self.buildSettingMenu()
		self.buildMusicPlayer()
		self.buildEndScreen()
		self.timer=Timer(mouse_timeout)
		self.active=True


############################ Init functions #################################
	def init_screen(self):
		self.screen = pygame.display.set_mode((screen_width, screen_height))


	def buildMenu(self):
		self.menu=GameMenu()

	def buildMusicPlayer(self):
		self.dj=MusicPlayer()

	def buildMainMenu(self):
		self.mainMenu=Menu()

	def buildSettingMenu(self):
		self.settings=SettingsMenu()

	def buildEndScreen(self):
		self.endScreen=EndScreen()




############################ Load functions #################################
	def loadBG(self):
		self.bg = pygame.image.load('assets/img/lab.jpg')

	def loadLevel(self,num):
		if hasattr(self,'curGame'):
			del self.curGame
		level=copy.deepcopy(levels[str(num)])
		self.curGame = Game(level)
		self.createGame()

	def loadTubes(self,num):
		self.flasks=pygame.sprite.Group()

	def loadOther(self):
		self.loadBG()
		self.loadQuit()
		self.loadUndo()
		self.loadMoveCount()
		self.loadUndoCount()
		self.loadHint()


		
		


	def loadUndo(self):
		undoImg=loadSprite("assets/img/buttons/undo.png")
		undoImg.rect.left=1250
		undoImg.rect.top=200
		self.undoB=pygame.sprite.GroupSingle(undoImg)

	def loadQuit(self):
		quitImg=loadSprite("assets/img/buttons/menu.png")
		quitImg.rect.left=20
		quitImg.rect.top=20
		self.quit=pygame.sprite.GroupSingle(quitImg)

	def loadMoveCount(self):
		moveHolder=loadSprite("assets/img/holders/numberBox.png")
		moveHolder.rect.left,moveHolder.rect.top=[1250,50]
		self.moveHolder=pygame.sprite.GroupSingle(moveHolder)
		moveCount=loadSprite("assets/img/holders/moveCount.png")
		moveCount.rect.left,moveCount.rect.top=[1000,45]	
		self.moveCount=pygame.sprite.GroupSingle(moveCount)
		

	def loadUndoCount(self):
		undoHolder=loadSprite("assets/img/holders/numberBox.png")
		undoHolder.rect.left,undoHolder.rect.top=[1250,120]	
		self.undoHolder=pygame.sprite.GroupSingle(undoHolder)
		undoCount=loadSprite("assets/img/holders/undoCount.png")
		undoCount.rect.left,undoCount.rect.top=[1000,115]	
		self.undoCount=pygame.sprite.GroupSingle(undoCount)

	def loadHint(self):
		hintUp=loadSprite("assets/img/arrow_up.png")
		self.hintUp=pygame.sprite.GroupSingle(hintUp)
		hintDown=loadSprite("assets/img/arrow_down.png")
		self.hintDown=pygame.sprite.GroupSingle(hintDown)

		hintB=loadSprite("assets/img/buttons/hint.png")
		hintB.rect.left,hintB.rect.top=[1250,280]	
		self.hintB=pygame.sprite.GroupSingle(hintB)

		hintNo=loadSprite("assets/img/buttons/no-hint.png")
		hintNo.rect.left,hintNo.rect.top=[1250,280]	
		self.hintNo=pygame.sprite.GroupSingle(hintNo)


		

############################ Draw functions #################################

	def drawScreen(self):
		self.screen.blit(self.bg, (0, 0))

	
	
	def drawMainMenu(self):
		self.mainMenu.draw(self.screen)
	
	def drawGameMenu(self):
		self.menu.draw(self.screen)

	def drawSettingsMenu(self):
		self.settings.draw(self.screen)
		
	def drawQuit(self):
		self.quit.draw(self.screen)

	def drawUndo(self):
		self.undoB.draw(self.screen)

	def drawFlasks(self):
		for flask in self.tubes:
			flask.draw(self.screen)

	def drawHint(self):
		if self.hintAvailable:
			self.hintB.draw(self.screen)
		else:
			self.hintNo.draw(self.screen)
		if self.displayHint:
			self.hintUp.draw(self.screen)
			self.hintDown.draw(self.screen)

	def drawMoveCount(self):
		self.moveCount.draw(self.screen)
		self.moveHolder.draw(self.screen)
		self.moveNum.draw(self.screen)
	
	def drawUndoCount(self):
		self.undoCount.draw(self.screen)
		self.undoHolder.draw(self.screen)
		self.undoNum.draw(self.screen)

	def drawRun(self):
		self.drawHint()
		self.drawFlasks()
		self.drawQuit()
		self.drawUndo()
		self.drawMoveCount()
		self.drawUndoCount()
		

	
	def drawEnd(self):
		self.endScreen.draw(self.screen,self.moveNum.score,self.undoNum.score)
	
	
		
	
	


############################ Collision functions #################################
	

	def checkFlasksCols(self,mouse_pos):
		i=0
		for tube in self.tubes:
			if tube.checkMouseCol(mouse_pos):
				return i
			i+=1
		return -1


	def checkQuit(self,mouse_pos):
		return self.quit.sprite.rect.collidepoint(mouse_pos)

	def checkUndo(self,mouse_pos):
		return self.undoB.sprite.rect.collidepoint(mouse_pos)

	def checkHint(self,mouse_pos):
		return self.hintB.sprite.rect.collidepoint(mouse_pos)


	def checkRunCols(self,mouse_pos):
		select=self.checkFlasksCols(mouse_pos)
		if select > -1:
			self.makeMove(select)
			if self.checkCompleted():
				self.endGame()
		elif self.checkUndo(mouse_pos):
			self.undo()
		elif self.checkQuit(mouse_pos):
			self.returnToMenu()
		elif self.checkHint(mouse_pos):
			self.displayHint=True
			self.dj.clickHint()
	
	def checkBackToMenu(self,mouse_pos):

		if self.endScreen.checkBackCol(mouse_pos):
			self.returnToMenu()






########################### Checking functions ################################
	def checkCompleted(self):
		for tube in self.tubes:
			if not tube.checkDone():
				return False
		return True


	def checkMouseTimeout(self,mouse):
		if(mouse):
			if(self.timer.checkTimer()):
				self.timer.startTimer()
				return True
		return False




############################ Run functions #################################

	def run(self):
		self.drawScreen()
		if self.state=="MAINMENU":
			self.runMainMenu()
		elif self.state=="SETTINGS":
			self.runSettingsMenu()
		elif self.state=="GAMEMENU":
			self.runGameMenu()
		elif self.state=="RUNNING":
			self.runLevel()
		elif self.state=="END":
			self.runEnd()


	def runMainMenu(self):
		self.drawMainMenu()
		mouse=pygame.mouse.get_pressed()[0]
		if self.checkMouseTimeout(mouse):
			select=self.mainMenu.checkMenuCols()
			if select == 0:
				self.active=False
			elif select ==1:
				self.levelSelection()
			elif select ==3:
				self.settingsMenu()




	def runGameMenu(self):
		self.drawGameMenu()
		mouse=pygame.mouse.get_pressed()[0]
		if self.checkMouseTimeout(mouse):
			select=self.menu.checkMenuCols()
			if select == 0:
				self.returnToMainMenu()
			elif select > 0:
				self.startGame(select)
			elif select==-2:
				self.dj.clickedButton()


	def runSettingsMenu(self):
		self.drawSettingsMenu()
		mouse=pygame.mouse.get_pressed()[0]
		if self.checkMouseTimeout(mouse):
			select=self.settings.checkMenuCols()
			if select == 0:
				self.returnToMainMenu()
			elif select ==1:
				self.dj.switchSFX()
			elif select==2:
				self.dj.switchMusic()
	

	def runLevel(self):
		self.drawRun()
		
		mouse=pygame.mouse.get_pressed()[0]
		if self.checkMouseTimeout(mouse):
			mouse_pos=pygame.mouse.get_pos()
			self.checkRunCols(mouse_pos)
			

	def runEnd(self):
		self.drawEnd()
		mouse=pygame.mouse.get_pressed()[0]
		if self.checkMouseTimeout(mouse):
			mouse_pos=pygame.mouse.get_pos()
			self.checkBackToMenu(mouse_pos)




	

############################ Level functions ###################################

	def createGame(self):
		if hasattr(self,'tubes'):
			del self.tubes
		self.tubes=[]
		x=50
		y=650
		
		for tube in self.curGame.tubes:
			flask = Flask(tube,[x,y])
			self.tubes.append(flask)
			x+=112
			
	def startGame(self,level):
		self.dj.enterLevel()
		self.loadLevel(level)
		self.state="RUNNING"
		self.moves=0
		self.selected=-1
		self.updateHint()
		
		self.savedMoves=[]
		self.moveNum=Score([1256,45])
		self.undoNum=Score([1256,115])

	
	def returnToMainMenu(self):
		self.state="MAINMENU"


	def levelSelection(self):
		self.state="GAMEMENU"
	
	def returnToMenu(self):
		self.dj.inMenu()
		self.state="GAMEMENU"
		self.selected=-1

	def settingsMenu(self):
		self.state="SETTINGS"

	def endGame(self):
		self.state="END"
		self.selected=-1
		

############################ Game functions ###################################

	def makeMove(self,tube):
		if tube == self.selected:
			self.deselect()
		elif self.selected >= 0:
			if self.curGame.move_ball_r(self.selected,tube):
				self.succellfulMove(tube)
		else:
			self.select(tube)

	def succellfulMove(self,tube):
		self.moveNum.increaseScore()
		ball=self.tubes[self.selected].remove_ball()
		if self.tubes[tube].add_ball(ball):
			self.dj.completeTube()
		self.savedMoves.append([self.selected, tube])
		self.updateHint()
		self.deselect()	

	def undo(self):
		if(self.savedMoves):
			self.undoNum.increaseScore()
			self.moveNum.decreaseScore()
			lastMove=self.savedMoves.pop()
			self.undoMove(lastMove)
			
	def undoMove(self,move):
		self.curGame.move_ball(move[1],move[0])

		ball=self.tubes[move[1]].remove_ball()
		self.tubes[move[0]].add_ball(ball)
		self.updateHint()

	################### Select/Deselect flasks #####################
	def deselect(self):
		self.tubes[self.selected].select()
		self.selected=-1

	def select(self,tube):
		self.tubes[tube].select()
		self.selected=tube

	
	###################### Hint functions ########################
	def updateHint(self):
		self.displayHint=False
		init_state = Node(self.curGame)
		result = greedy_np(init_state, True)
		if result is None:
			self.hintAvailable=False
			self.hideHintArrows()
			return
		path = result[0].path(result[1])
		if len(path)>1:
			self.hintAvailable=True
			hint=self.findDiferences(path[1])
			self.updateHintArrows(hint)

	def updateHintArrows(self,hint):
		self.hintUp.sprite.rect.left=self.tubes[hint[0]].coords[0]+5
		self.hintUp.sprite.rect.top=self.tubes[hint[0]].coords[1]-130

		self.hintDown.sprite.rect.left=self.tubes[hint[1]].coords[0]+5
		self.hintDown.sprite.rect.top=self.tubes[hint[1]].coords[1]-130
			

	def hideHintArrows(self):
		self.hintUp.sprite.rect.left=8000
		self.hintUp.sprite.rect.top=8000

		self.hintDown.sprite.rect.left=8000
		self.hintDown.sprite.rect.top=8000


	def findDiferences(self,node):
		tube_from=-1
		tube_to=-1
		game1=self.curGame
		game2=node.gamestate

		for i in range(0,len(game2.tubes)):
			if len(game1.tubes[i].balls)>len(game2.tubes[i].balls):
				tube_from=i
			elif len(game1.tubes[i].balls)<len(game2.tubes[i].balls):
				tube_to=i
			
			if(tube_from!=-1 and tube_to!=-1):
				return [tube_from,tube_to]
		return [tube_from,tube_to]







pygame.init()

game = UI()

pygame.display.set_caption('Ballsort')



while game.active:
	game.run()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game.active = False

	pygame.display.update()

pygame.quit()