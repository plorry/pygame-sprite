import pygame, sys
from pygame.locals import *

SMALL = (16,16)
MEDIUM = (32,32)
LARGE = (64,64)

TRANS = (255,0,255)

ANIM_STOPPED = 0
ANIM_WALKING = 1
ANIM_JUMPING = 2
ANIM_FALLING = 3

FPS = 50

class Animation():
	def __init__(self, name, no_frames = 1, frame_duration = 10):
		self.name        = name
		self.no_frames   = no_frames - 1
		self.frame_duration= frame_duration

class Sprite():
	def __init__(self, screen, image_file, pos, res):
		self.screen      = screen
		self.image_file  = image_file
		self.pos         = pos
		self.res         = res
		self.rect        = pygame.Rect((1,1),(self.res))
		self.image       = pygame.image.load(self.image_file).convert()
		self.animation_no= 0
		self.frame_no    = 0
		self.animation   = [Animation('stopped', 2)]
		
		self.frames_passed = 0

		self.image.set_colorkey(TRANS)
		
	def new_anim(self, name, no_frames = 1, fps = 0):
		self.animation.append(Animation(name,no_frames,fps))
	
	def set_anim(self, animation):
		self.animation_no = animation
	
	def update(self):
		self.rect = pygame.Rect(((self.frame_no) * (self.res[0]+1) + 1, (self.animation_no) * (self.res[1]+1) + 1),(self.res))
		self.screen.blit(self.image, self.pos, self.rect)
		self.frames_passed += 1
		if self.frames_passed >= self.animation[self.animation_no].frame_duration:
			self.frame_no += 1
			self.frames_passed = 0
		if self.frame_no > self.animation[self.animation_no].no_frames:
			self.frame_no = 0


class Platformer(Sprite):

	def __init__(self, screen, image_file, pos, res, max_speed = 2, grav = 0.2):
		self.screen      = screen
		self.image_file  = image_file
		self.pos         = pos
		self.res         = res
		self.max_speed   = max_speed
		self.grav        = grav
		self.rect        = pygame.Rect((1,1),(self.res))
		self.image       = pygame.image.load(self.image_file).convert()
		self.animation_no= 0
		self.frame_no    = 0
		self.animation   = [Animation('stopped', 2)]
		self.fall_speed  = 0
		self.falling     = False
		self.jumping     = False
		self.running     = False
		self.term_fall_speed = 7
		self.accel       = 0.3
		self.decel       = 0.5
		self.speed       = 0
		self.dir         = 'right'
		self.col_rect    = pygame.Rect((self.pos),(self.res))
		self.below_rect  = pygame.Rect((self.pos[0],self.pos[1]+self.res[1]),(self.res[0],10))
		
		self.frames_passed = 0

		self.image.set_colorkey(TRANS)
		
	def set_gravity(self, grav):
		self.grav = grav
	
	def set_speed(self, speed):
		self.speed = speed
	
	def _is_falling(self):
		return self.falling
	
	def _is_running(self):
		return self.running
		
	def check_BG_collisions(self,level):
		for i in level.map:
			for j in i:
				if self.col_rect.colliderect(j.get_rect()):
					if j._is_obstacle() and self.jumping == False and self._is_falling():
						self.falling = False
						self.fall_speed = 0
						new_y_pos = j.get_ypos() - self.res[1]
						self.pos = (self.pos[0],new_y_pos)
						break
					if self.below_rect.colliderect(j.get_rect()):
						if j.obstacle != 1:
							self.falling = True
	
	def update(self, level):

		self.col_rect = pygame.Rect((self.pos),(self.res))
		self.check_BG_collisions(level)	
		self.rect = pygame.Rect(((self.frame_no) * (self.res[0]+1) + 1, (self.animation_no) * (self.res[1]+1) + 1),(self.res))
		self.screen.blit(self.image, self.pos, self.rect)
		self.frames_passed += 1
		if self.frames_passed >= self.animation[self.animation_no].frame_duration:
			self.frame_no += 1
			self.frames_passed = 0
		if self.frame_no > self.animation[self.animation_no].no_frames:
			self.frame_no = 0
			
		if self.falling == True:
			self.fall_speed += self.grav
			if self.fall_speed > self.term_fall_speed:self.fall_speed = self.term_fall_speed
			new_y_pos = self.pos[1] + self.fall_speed
			self.pos = (self.pos[0],new_y_pos)
			if self.fall_speed > 0 and self.jumping == True:self.jumping = False
			
		
		if self.running == True:self.speed += self.accel
		if self.running == False:self.speed -= self.decel
		if self.speed > self.max_speed:self.speed = self.max_speed
		if self.speed < 0:self.speed=0
		if self.dir=='right':new_x_pos = self.pos[0] + self.speed
		if self.dir=='left':new_x_pos = self.pos[0] - self.speed
		self.pos = (new_x_pos, self.pos[1])
	
	def get_input(self, input):
		if input.type == pygame.KEYDOWN:
			if input.key == pygame.K_RIGHT:
				self.running = True
				self.dir = 'right'
			if input.key == pygame.K_LEFT:
				self.running = True
				self.dir = 'left'
			if input.key == pygame.K_UP:
				self.jumping = True
				self.falling = True
				self.fall_speed = -5
		if input.type == pygame.KEYUP:
			if input.key == pygame.K_RIGHT or input.key == pygame.K_LEFT:self.running = False
		



def exit_game():
	sys.exit()
	
if __name__ == '__main__':

	BLACK = (0,0,0)
	BLUE = (0,0,255)
		
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((320,240),FULLSCREEN,32)
	man = Platformer(screen, 'sprite_test.png', (150.0, 120.0), SMALL)
	while 1:
		screen.fill(BLUE)
		man.update()
		for event in pygame.event.get():
			man.get_input(event)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit_game()

		pygame.display.flip()
		clock.tick(FPS)