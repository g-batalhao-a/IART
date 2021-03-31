
import json

import pygame


from game.utils import *


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
