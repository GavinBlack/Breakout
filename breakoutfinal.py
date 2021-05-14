# Pizza Panic
# Player must catch falling pizzas before they hit the ground

from livewires import games, color
import random, time, math

games.init(screen_width = 640, screen_height = 480, fps = 50)

class Paddle(games.Sprite):
	"""
	A pan controlled by player to catch falling pizzas.
	"""
	image = games.load_image("paddle.png")
	bigPaddle = games.load_image("bigpaddle.png")
	smallPaddle = games.load_image("smallPaddle.png")
	extra_paddles = 0
	max_paddles = 2

	def __init__(self, whichImage = 1, y = 445):
		""" Initialize Pan object and create Text object for score. """
		if whichImage == 1:
                        super(Paddle, self).__init__(image = Paddle.image, x = games.mouse.x,y = y)
		elif whichImage == 2:
                        super(Paddle, self).__init__(image = Paddle.bigPaddle, x = games.mouse.x,y = y)
		elif whichImage == 3:
                        super(Paddle, self).__init__(image = Paddle.smallPaddle, x = games.mouse.x,y = y)  

	def update(self):
		""" Move to mouse x position. """
		self.x = games.mouse.x
		
		if self.left < 0:
			self.left = 0
			
		if self.right > games.screen.width:
			self.right = games.screen.width
			
		self.check_hit()

	def check_hit(self):
		""" Check if hits ball """
		paddleLen = (self.right - self.left) / 2

		#angular math
		for ball in self.overlapping_sprites:
                        #if paddle hits ball, perform math
                        if type(ball) == Ball:
                                if ball.x < self.left or ball.x > self.right:
                                        ball.dx = -ball.dx
                                elif ball.x < self.x:
                                        ballPos = ball.x - self.left
                                        posOfImpact = ballPos / paddleLen 
                                        angle = posOfImpact * 90
                                        ball.dy = -abs(math.sin(math.radians(angle))) * ball.speed
                                        ball.dx = -abs(math.cos(math.radians(angle))) * ball.speed
                                else:
                                        ballPos = self.right - ball.x
                                        posOfImpact = ballPos / paddleLen
                                        angle = posOfImpact * 90
                                        ball.dy = -abs(math.sin(math.radians(angle))) * ball.speed
                                        ball.dx = abs(math.cos(math.radians(angle))) * ball.speed
                        #if paddle hits star, make paddle bigger
                        elif type(ball) == Star:
                                self.destroy()
                                paddle = Paddle(2,y = self.y)
                                games.screen.add(paddle)
                                ball.destroy()
                        #if paddle hits caution drop, make paddle tiny
                        elif type(ball) == Caution:
                                self.destroy()
                                paddle = Paddle(3, y = self.y)
                                games.screen.add(paddle)
                                ball.destroy()
                        #if paddle hits doublePaddle drop, add another paddle above current paddle
                        elif type(ball) == DoublePaddle:
                                Paddle.extra_paddles += 1
                                #cannot have more than 2 total paddles at once
                                if Paddle.extra_paddles < Paddle.max_paddles:
                                        paddle = Paddle(y = self.y - 75)
                                        games.screen.add(paddle)
                                ball.destroy()
                        
class Brick(games.Sprite):
        brick_image = games.load_image("brick.png")
        brick2_image = games.load_image("brick2.png")
        brick3_image = games.load_image("brick3.png")
        brick4_image = games.load_image("brick4.png")
        brick5_image = games.load_image("brick5.png")
        rows = 1
        cols = 7
        total_bricks = rows * cols
        tot_bricks = rows * cols
        total_broken = 0
        level = 1
        max_rows = 6

        def __init__(self,world,x,y,whichImage = 1):
                #determines what image to use based on whichImage value
                if whichImage == 1:
                        super(Brick,self).__init__(image = Brick.brick_image, x = x, y = y)
                elif whichImage == 2:
                        super(Brick,self).__init__(image = Brick.brick2_image, x = x, y = y)
                elif whichImage == 3:
                        super(Brick,self).__init__(image = Brick.brick3_image, x = x, y = y)
                elif whichImage == 4:
                        super(Brick,self).__init__(image = Brick.brick4_image, x = x, y = y)
                elif whichImage == 5:
                        super(Brick,self).__init__(image = Brick.brick5_image, x = x, y = y)

                self.world = world
                self.whichImage = whichImage

        def update(self):
                self.check_hit()
                self.check_if_win()
                
        def check_hit(self):
                """ Check if ball hits brick """
                alreadyDroppedPowerup = False
                
                for ball in self.overlapping_sprites:
                        if ball.x < self.left or ball.x > self.right:
                                ball.dx = -ball.dx
                        else:
                                ball.dy = -ball.dy
                        self.destroy()
                        Brick.total_bricks -= 1
                        Brick.total_broken += 1
                        self.world.score.value += 1
                        
                        #random chance that a star powerup can spawn after breaking brick
                        ran = random.randint(0,12)
                        if ran == 0 and not alreadyDroppedPowerup:
                                star = Star(self.x,self.y)
                                games.screen.add(star)
                                alreadyDroppedPowerup = True
                        #random chance a caution powerup can spawn
                        ran = random.randint(0,10)
                        if ran == 0 and not alreadyDroppedPowerup:
                                caution = Caution(self.x,self.y)
                                games.screen.add(caution)
                                alreadyDroppedPowerup = True
                        #random chance a doublePaddle powerup can spawn
                        ran = random.randint(0,12)
                        if ran == 0 and not alreadyDroppedPowerup:
                                doublePaddle = DoublePaddle(self.x,self.y)
                                games.screen.add(doublePaddle)
                                alreadyDroppedPowerup = True

                        #ALL BRICKS ARE BROKEN
                        if Brick.total_broken == Brick.tot_bricks:
                                ball.destroy()
                                level_message = games.Message(value = "Level " + str(Brick.level+1),
                                                              size = 40,
                                                              color = color.yellow,
                                                              x = games.screen.width/2,
                                                              y = games.screen.width/10,
                                                              lifetime = 5 * games.screen.fps,
                                                              after_death = self.reset,
                                                              is_collideable = False)
                                games.screen.add(level_message)

        def reset(self):
                """
                reset, recalc variables, create new ball, add more bricks
                """
                ranX = random.randint(5,460)
                ranY = random.randint(190,230)
                ball = Ball(ranX,ranY)
                games.screen.add(ball)
                world = World()
                world.addBricks()
                Brick.level += 1
                Brick.total_broken = 0
                #do not exceed max row limit
                if Brick.level < Brick.max_rows:
                        Brick.rows += 1
                Brick.tot_bricks = Brick.cols * Brick.rows


        def check_if_win(self): #temp disabled
                if Brick.total_bricks == 0:
                        return
                        self.win()

        def win(self):
                """ Win game """
                end_message = games.Message(value = "Win!!!",size = 90,color = color.green,x = games.screen.width/2,y = games.screen.height/2,lifetime = 5 * games.screen.fps,after_death = games.screen.quit)
                games.screen.add(end_message)
                
class World(object):
        bricks = []
        rows = 1
        cols = 7
        total_bricks = rows * cols
        level = 0
        max_rows = 6

        score = games.Text(value = 0,
                                size = 30,
                                color = color.white,
                                top = 5,
                                right = games.screen.width - 10,
                                is_collideable = False)
        games.screen.add(score)

        def addBricks(self):
                x = 65
                y = 40
                World.level += 1
                
                #if not the first level and level is below the max row limit, add rows
                if World.level != 1 and World.level < World.max_rows:
                        World.rows += 1

                #create rows and cols of bricks based on values
                for i in range(World.rows):
                        tempList = []
                        for j in range(World.cols):
                                if i == 0:
                                        brick = Brick(world = self,x = x+j*85,y = y+i*45)
                                        games.screen.add(brick)
                                elif i == 1:
                                        brick = Brick(world = self,x = x+j*85,y = y+i*45,whichImage = 2)
                                        games.screen.add(brick)
                                elif i == 2:
                                        brick = Brick(world = self,x = x+j*85,y = y+i*45,whichImage = 3)
                                        games.screen.add(brick)
                                elif i == 3:
                                        brick = Brick(world = self,x = x+j*85,y = y+i*45,whichImage = 4)
                                        games.screen.add(brick)
                                elif i == 4:
                                        brick = Brick(world = self,x = x+j*85,y = y+i*45,whichImage = 5)
                                        games.screen.add(brick)
                                        
                                tempList.append(brick)
                                        
                                if j % World.cols == 0:
                                        World.bricks.append(tempList)
                                        #print(World.bricks)

class Star(games.Sprite):
        star = games.load_image("star.png")

        def __init__(self,x,y):
                super(Star,self).__init__(image = Star.star,x=x,y=y,dx=0,dy=3)

class Caution(games.Sprite):
        caution = games.load_image("caution.png")

        def __init__(self,x,y):
                super(Caution,self).__init__(image = Caution.caution,x=x,y=y,dx=0,dy=2)

class DoublePaddle(games.Sprite):
        doublePaddle = games.load_image("doublePaddle.png")

        def __init__(self,x,y):
                super(DoublePaddle,self).__init__(image = DoublePaddle.doublePaddle,x=x,y=y,dx=0,dy=4)

                
class Ball(games.Sprite):
        speed = 3.5
        ball_image = games.load_image("ball.png")
        ROTATION_STEP = 2

        def __init__(self,x,y):
                dx = random.randint(0,1)
                if dx == 0:
                        dx = -3.5
                super(Ball,self).__init__(image = Ball.ball_image, x = x, y = y,dx=dx,dy=3.5)

        def update(self):
                if self.left < 0 or self.right > games.screen.width:
                        self.dx = -self.dx
                if self.top < 0:
                        self.dy = -self.dy
                if self.bottom > games.screen.height:
                        self.end_game()
                #self.angle += Ball.ROTATION_STEP

        def end_game(self):
                """ End the game. """
                end_message = games.Message(value = "You Lose!",size = 90,color = color.red,x = games.screen.width/2,y = games.screen.height/2,lifetime = 5 * games.screen.fps,after_death = games.screen.quit)
                games.screen.add(end_message)
                
def main():
	""" Play the game. """
	background_image = games.load_image("background.jpg", transparent = False)
	games.screen.background = background_image


	the_paddle = Paddle()
	games.screen.add(the_paddle)

	world = World()
	world.addBricks()
	
	ball = Ball(200,200)
	games.screen.add(ball)

	games.mouse.is_visible = False

	#games.screen.event_grab = True
	games.screen.mainloop()

# start it up!
main()
