import pygame, random, sys, math

# Variables
pygame.init()
SIZE = (924, 784)
clock = pygame.time.Clock()
FPS = 30
pygame.display.set_caption("Memory Game")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
screen = pygame.display.set_mode(SIZE)
RED = (233, 150, 122)
cardback = pygame.image.load("images/cardback.png")
CARDW = cardback.get_width()
CARDH = cardback.get_height()

def set_deck():
	cards = []
	for i in range(1,15):
		card = "images/card-%s.png" % i
		card_load = pygame.image.load(card) 
		cards.append(card_load)
	cards = cards * 2
	random.shuffle(cards)
	return [cards[i:i+7] for i in range(0, len(cards), 7)] # Returns a 2D List

def cover_board(deck):
	screen.fill(RED)
	xpos = 0 
	ypos = 0
	for i in range(4):
		for j in range(7):
			if deck[i][j]:
				screen.blit(cardback, (xpos,ypos))
			xpos = xpos + CARDW
		ypos = ypos + CARDH
		xpos = 0

def get_card_position(mousepos):
	cardx = mousepos[0] / CARDW
	cardy = mousepos[1] / CARDH
	i = math.floor(cardy)
	j = math.floor(cardx)
	return i, j

def uncover_card(i,j):
	x = j * CARDW
	y = i * CARDH
	if deck[i][j]:
		screen.blit(deck[i][j],(x,y))
		pygame.display.update()
	return deck[i][j]

def is_over(deck):
	for i in range(4):
		for j in range(7):
			if deck[i][j]:
				return False
	return True
	
init = True
while True:
	while init:
		deck = set_deck()
		cover_board(deck)
		flipped = []
		flipped_pos = []
		tries = 0
		init = False
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseposition =	pygame.mouse.get_pos()
			i, j = get_card_position(mouseposition)
			if deck[i][j]:
				uncover_card(i,j)
				flipped.append(uncover_card(i,j))
				flipped_pos.append(get_card_position(mouseposition))
			if len(flipped) >= 2:
				clock.tick(1)
				if flipped[0] == flipped[1] and flipped_pos[0] != flipped_pos[1]:
					deck[flipped_pos[0][0]][flipped_pos[0][1]] = 0
					deck[flipped_pos[1][0]][flipped_pos[1][1]] = 0
				cover_board(deck)
				flipped = []
				flipped_pos = []
				tries += 1
				if is_over(deck):
					screen.fill((74, 44, 97))
					font = pygame.font.SysFont('bahnschrift',50)
					label = font.render("You won!",1,(255,255,255))
					label2 = font.render(f"It took {tries} tries to win!",1,(255,255,255))
					label3 = font.render("(Press a key to play again)",1,(255,255,255))
					screen.blit(label,(350,250))
					screen.blit(label2,(250,300))
					screen.blit(label3,(150,350))
					pygame.display.update()
					final_screen = True
					while final_screen:
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								pygame.quit()
								sys.exit()
							if event.type == pygame.KEYDOWN:
								print("yes")
								init = True
								final_screen = False
	pygame.display.update()
	