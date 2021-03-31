
import pygame

from game.utils import *

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

