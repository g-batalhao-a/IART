import json

import pygame






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
