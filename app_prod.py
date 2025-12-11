import turtle as trtl
import os
import datetime as dt
import glob
import random
import typing
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' 
import pygame

class EnemyData_Types(typing.TypedDict):
  x: int
  y: int
  sprite: trtl.Turtle

def get_gif_files(directory_path):
    search_pattern = os.path.join(directory_path, '*.gif')
    gif_files = glob.glob(search_pattern)
    
    return gif_files

Sprite_AllSpritesPath        = os.path.join('Sprites', 'Invaders')
Sprite_Invaders_list         = get_gif_files(Sprite_AllSpritesPath)
Invaders_List                = []

pygame.mixer.init() 

Level_StartSFX  = pygame.mixer.Sound(os.path.join('Sounds', 'level-start-sfx.wav'))
Enemy_MoveSFX   = pygame.mixer.Sound(os.path.join('Sounds', 'alien-move-sfx.wav'))
Enemy_DiedSFX   = pygame.mixer.Sound(os.path.join('Sounds', 'alien-explosion-sfx.wav'))
Game_OverSFX    = pygame.mixer.Sound(os.path.join('Sounds', 'game-over-sfx.wav'))
Player_ShootSFX = pygame.mixer.Sound(os.path.join('Sounds', 'player-bullet-sfx.wav')) 
Player_DiedSFX  = pygame.mixer.Sound(os.path.join('Sounds', 'player-explosion-sfx.wav'))



for file_path in Sprite_Invaders_list:
    if (file_path.find("E_") != -1):
      Invaders_List.append(file_path)

Sprite_ProjectilePath                  = os.path.join('Sprites', 'Projectiles')
Sprite_Projectile_list                 = get_gif_files(Sprite_ProjectilePath)
Program_CreationDate                   = dt.datetime(2025, 12, 4)
Top_Height                             = 230
Screen_Width                           = 300
Screen_Height                          = 100
Shoot_Cooldown                         = False
Current_Enemies: list[EnemyData_Types] = []
Hit_Score                              = 0
Start_Time                             = 120 
Gun_Ammo                               = 55
Game_OverB                             = False
Title_Colors                           = [
    "red",
    "orange",
    "yellow",
    "lime", 
    "greenyellow",
    "chartreuse",
    "aqua",
    "cyan",
    "skyblue",
    "deepskyblue",
    "blue",
    "magenta",
    "fuchsia",
    "hotpink",
    "deeppink",
    "gold",
    "lightyellow",
    "palegreen",
    "springgreen",
    "turquoise",
    "lightskyblue",
    "lavender",
    "violet",
    "orchid",
    "coral",
    "tomato"
]

Intro_Questions = [
  "What's your name?:",
  "What day is it today? (mm/dd/yy):",
  "Are You good with games?:",
  "No matter the reply you just said, you up for a challenge? (yes, no):"
]

Title_Shower = trtl.Turtle()
Title_Screen = Title_Shower.getscreen()
Title_Shower.hideturtle()
Title_Shower.penup()
Title_Shower.goto(-230, 180)
Title_font_setup = ("Arial", 18, "normal")
Title_Shower.write("Loading...", font=Title_font_setup)

SpaceShip_Char = trtl.Turtle()
SpaceShip_Char.penup()
SpaceShip_Char_Screen = SpaceShip_Char.getscreen()
SpaceShip_Char_Screen.setup(500, 550) 
SpaceShip_Char_Screen.bgcolor("gray")

for file_path in Sprite_Invaders_list:
    SpaceShip_Char_Screen.addshape(file_path)
    
SpaceShip_Char_Screen.tracer(False)

def Create_MissileTurtle():
  Missile_Char = trtl.Turtle()
  Missile_Char.penup()
  Missile_Char_Screen = Missile_Char.getscreen()
  Missile_Char.shapesize(2,4)
  Missile_Char.goto(SpaceShip_Char.xcor(), SpaceShip_Char.ycor())
  Missile_Char_Screen.tracer(False)
  return Missile_Char

Main_PointSpawn = trtl.Turtle()
Main_PointSpawn.shapesize(.5)
Main_PointSpawn.color('orange')
Main_PointSpawn.penup()
Main_PointSpawn.shape('square')
Main_PointSpawn_Screen = Main_PointSpawn.getscreen()
Main_PointSpawn_Screen.tracer(True)

def Create_EnemyTurtle() -> trtl.Turtle: 
  Enemy_Char = trtl.Turtle()
  Enemy_Char.penup()
  Enemy_Char_Screen = Enemy_Char.getscreen()
  for file_path in Invaders_List:
        Enemy_Char_Screen.addshape(file_path)
  Enemy_Char.shape(random.choice(Invaders_List))
  Enemy_Char.shapesize(2,4)
  Enemy_Char_Screen.tracer(False)
  return Enemy_Char

def Create_Enemies(Enemy_Count: int, Gap_LengthX, Gap_LengthY, Main_Point: trtl.Turtle):
  Main_Point.sety(Main_Point.ycor() + Gap_LengthY)
  increase = Gap_LengthX
  for i in range(Enemy_Count):
    if (len(Current_Enemies) >= 50):
      break
    Created = Create_EnemyTurtle()
    Created.goto(Main_Point.xcor() + increase, Main_Point.ycor())
    Created.setheading(0)
    Created.showturtle()
    Created.getscreen().update()
    Current_Enemies.append({
      "x": Created.xcor(),
      "y": Created.ycor(),
      "sprite": Created
    })
    increase += 35

def Init_Enemies():
  Main_PointSpawn.goto(-231, 200)
  for i in range(15):
    Create_Enemies(
      10, 
      50, 
      -35,
      Main_PointSpawn
    )
  

direction = 'right'
MoveDir_X = 5
MoveDir_Y = 0
def Update_Enemies(Move_X: int = 1, Move_Y: int = 0):
  global direction, MoveDir_X, Game_OverB
  if (Game_OverB): return

  UnDown_Enmies = []
  Reached_Side  = False
  if (len(Current_Enemies) <= 0):
    Game_OverB = True
    Game_Over("Game over! You killed all the ennemies!!")
    return
  
  for Invaders_Data in Current_Enemies:
    x, y, Enemy = Invaders_Data["x"], Invaders_Data["y"], Invaders_Data["sprite"]
    Enemy.clear()
    if (Enemy.xcor() >= 230):
      direction = 'left'
      Move_Y = 15
      Reached_Side = True
    elif (Enemy.xcor() <= -230):
      direction = 'right'
      Move_Y = -15
      Reached_Side = True
    else:
      if (Enemy not in UnDown_Enmies):
        UnDown_Enmies.append(Enemy)


    if (Enemy.ycor() <= -205):
      Game_OverB = True
      Game_Over()
      Death_SpaceShip(SpaceShip_Char)
      Game_OverSFX.play()
      return
    
    if (Is_Colliding(SpaceShip_Char, Enemy)):
      Game_OverB = True
      Game_Over("Game over! Enemy touched you!")
      Death_SpaceShip(SpaceShip_Char)
      Game_OverSFX.play()
      return


    Enemy.sety(direction == 'right' and Enemy.ycor() + Move_Y or Enemy.ycor() - Move_Y)
    Enemy.setx(direction == 'right' and Enemy.xcor() + Move_X or Enemy.xcor() - Move_X)
    
    Enemy.getscreen().update()
  if (Reached_Side):
    for Enemy in UnDown_Enmies:
      Enemy.clear()
      if (direction == 'left'):
        Move_Y = 15
      elif (direction == 'right'):
        Move_Y = -15
      Enemy.sety(direction == 'right' and Enemy.ycor() + Move_Y or Enemy.ycor() - Move_Y)
      Enemy.setx(direction == 'right' and Enemy.xcor() + Move_X or Enemy.xcor() - Move_X)
      Enemy.getscreen().update()

  Enemy_MoveSFX.play()
  Move_X = MoveDir_X
  Move_Y = MoveDir_Y
  Main_PointSpawn_Screen.ontimer(lambda: Update_Enemies(Move_X, Move_Y), 60)

def Check_Variable(String, Default):
  Failed = String
  try: 
    if len(String) == 0: 
      raise """failure"""; pass
  except: 
    print(f"[❌] - [Blank or spaces] is not a vaild response. Using defaults ({Default})...")
    Failed = Default
  return Failed

def Check_Date(String, Default):
  Failed = String
  try:
    dt.datetime.strptime(String, "%m/%d/%y")
    pass
  except:
    print(f"[❌] - [{String}] is not a vaild date. Using defaults ({Default})...")
    Failed = Default
  return Failed

def Sprite_SetDirection_LEFT(Sprite: trtl.Turtle):
  if (Sprite.xcor() <= -225): return
  Sprite.setheading(0)
  Sprite.goto(Sprite.xcor() - 5, Sprite.ycor())
  SpaceShip_Char_Screen.update()

def Sprite_SetDirection_RIGHT(Sprite: trtl.Turtle):
  if (Sprite.xcor() >= 225): return
  Sprite.goto(Sprite.xcor() + 5, Sprite.ycor())
  SpaceShip_Char_Screen.update()

def draw_sprite(Active_Sprite: trtl.Turtle):
 xran  = random.randint(-100, -100)
 Active_Sprite.goto(xran, -200)
 Active_Sprite.showturtle()
 SpaceShip_Char.shape(os.path.join('Sprites', 'Invaders', 'MainPlayer.gif'))
 SpaceShip_Char_Screen.update()


def Reset_Sprite(Active_Sprite: trtl.Turtle):
  Active_Sprite.goto(SpaceShip_Char.xcor(), SpaceShip_Char.ycor())
  Active_Sprite.hideturtle()
  Active_Sprite.clear()
  Active_Sprite.getscreen().update()


def on_disspear(Active_Sprite: trtl.Turtle, Delete: bool):
    Active_Sprite.hideturtle()
    Active_Sprite.clear()
    if (Delete): del Active_Sprite


def Death_Enemy(Invaders_Data: EnemyData_Types):
  print('destroyed enemy')
  Current_Enemies.remove(Invaders_Data)
  Invaders_Data["sprite"].shape(os.path.join('Sprites', 'Invaders', 'EnemyExplosion.gif'))
  Invaders_Data["sprite"].getscreen().ontimer(lambda: on_disspear(Invaders_Data["sprite"], True), 1000)

def Death_SpaceShip(Active_Sprite: trtl.Turtle):
  print('destroyed player')
  Player_DiedSFX.play()
  Active_Sprite.shape(os.path.join('Sprites', 'Invaders', 'MainPlayer_PlayerExplosion.gif'))
  Active_Sprite.getscreen().ontimer(lambda: on_disspear(Active_Sprite, False), 5000)


def _ShootTimer(Active_Sprite: trtl.Turtle):
  global Shoot_Cooldown, Hit_Score
  if (Active_Sprite.ycor() < Top_Height):
    for Invaders_Data in Current_Enemies:
      x, y, Enemy = Invaders_Data["x"], Invaders_Data["y"], Invaders_Data["sprite"]
      if (Is_Colliding(Active_Sprite, Enemy)):
        Enemy_DiedSFX.play()
        Reset_Sprite(Active_Sprite)
        Death_Enemy(Invaders_Data)
        print('collided')
        Shoot_Cooldown = False
        Hit_Score += 1
        return
    Draw_Missile(Active_Sprite.xcor() + 5, Active_Sprite.ycor() + 0.01, Active_Sprite)
    SpaceShip_Char_Screen.ontimer(lambda: _ShootTimer(Active_Sprite), 40)
    
  else:
    Reset_Sprite(Active_Sprite)
    Shoot_Cooldown = False
  Active_Sprite.getscreen().update()

def shoot_Missile():
  global Shoot_Cooldown, Gun_Ammo
  if (Shoot_Cooldown): 
    print("cooldown")
    return
  if (Game_OverB):
    return
  Shoot_Cooldown = True
  Player_ShootSFX.play()
  Gun_Ammo -= 1
  _ShootTimer(Create_MissileTurtle())


def Is_Colliding(Main_Sprite: trtl.Turtle, Hit_Sprite: trtl.Turtle):
  if Main_Sprite.distance(Hit_Sprite) <= 20:
    return True
  return False
                 

Show = True
def Game_Over(CustomText = None):
 global Game_OverB, Show
 if (Game_OverB == False):
   return
 Title_Shower.clear()
 if (Show): 
  Title_Shower.goto(-225, 180)
  Title_Shower.color('red')
  Title_Shower.write(CustomText or "Game over! Times up!", font=Title_font_setup)

 Show = not Show
 Title_Screen.ontimer(lambda: Game_Over(CustomText), 500)

def _CountDown(StartTime):
  global Game_OverB

  if (Gun_Ammo <= 0):
    Game_OverB = True
    Game_Over("Game over! You ran out of missiles") 
    Death_SpaceShip(SpaceShip_Char)
    Game_OverSFX.play()
    return
  
  if (Game_OverB):
    Game_Over()
    Death_SpaceShip(SpaceShip_Char)
    Game_OverSFX.play()
    return
  Mins, Secs  = divmod(StartTime, 60)
  Time_Result = 'Score: {}\nMissles: {}\nTime left: {:02d}:{:02d}'.format(Hit_Score, Gun_Ammo, Mins, Secs)
  Title_Shower.clear()
  Title_Shower.goto(-225, 180)
  Title_Shower.color(random.choice(Title_Colors))
  Title_Shower.write(Time_Result, font=Title_font_setup)
  StartTime -= 1
  Title_Screen.ontimer(lambda: _CountDown(StartTime), 1000)

def Start_SpaceInvaders():
  global Game_OverB
  Game_OverB = False
  Title_Shower.clear()

  SpaceShip_Char_Screen._root.lift()
  SpaceShip_Char_Screen._root.attributes('-topmost', True)
  SpaceShip_Char_Screen._root.attributes('-topmost', False)
  SpaceShip_Char_Screen._root.focus_force()

  Level_StartSFX.play()
  
  Init_Enemies()
  Update_Enemies(0,1)
  _CountDown(Start_Time)
  draw_sprite(SpaceShip_Char)

Title_Shower.hideturtle()
SpaceShip_Char.hideturtle()


def Draw_Missile(StartX, StartY, Active_Sprite: trtl.Turtle):
  Active_Sprite.clear()
  Active_Sprite.goto(StartX, StartY)


  Active_Sprite.color('white')
  Active_Sprite.shape('square')
  Active_Sprite.shapesize(.2)

  Active_Sprite.stamp()
  Active_Sprite.penup()
  Active_Sprite.setheading(-180)
  Active_Sprite.forward(10.3)
  Active_Sprite.stamp()

  Active_Sprite.forward(-5.5) 

  Active_Sprite.setheading(90)
  Active_Sprite.forward(5.5)

  for i in range(5):
    Active_Sprite.setheading(90)
    Active_Sprite.pendown()
    Active_Sprite.stamp()
    Active_Sprite.penup()
    Active_Sprite.forward(4.5)
    if (i == 0):
      Active_Sprite.setheading(-180)
      Active_Sprite.forward(5) 
      Active_Sprite.stamp() 
      Active_Sprite.forward(-5)

      Active_Sprite.forward(-5) 
      Active_Sprite.stamp() 
      Active_Sprite.forward(5)
    elif (i== 4):
      Active_Sprite.color('red')
      Active_Sprite.stamp()
  Active_Sprite.getscreen().update()

Title_Shower.clear()
Title_Shower.write("Please answer questions in terminal to start.", font=Title_font_setup)
for Question in Intro_Questions:
  if (Question.find("day is") != -1):
    Result = Check_Date(input(f"{Question} "), dt.datetime.today().strftime("%m/%d/%y"))
    Res_DateRes = dt.datetime.strptime(Result, "%m/%d/%y")
    Math_Math = Program_CreationDate - Res_DateRes
    print(f"Hm, the program was created {Program_CreationDate.strftime("%m/%d/%y")}, real development started 12/08/25 and chosen day is: {Result} and the difference of playing this game since its creation is: {abs(Math_Math.days)} days ago")
  else:  
    Result = Check_Variable(input(f"{Question} "), "i dont know")
    if (Question.find("up for a") != -1):
      if (Result == 'yes'):
        print("hmm, very well! win space invaders..")
      else: 
        print("aye even tho u said no or something releated to no, too bad ur playing")
      if (Question.find("No matter the reply") != -1):
        Start_SpaceInvaders()
    elif (Question.find("name") != -1):
      print(f"ok hello there {Result}")


SpaceShip_Char_Screen.onkeypress(lambda: Sprite_SetDirection_LEFT(SpaceShip_Char), "Left")
SpaceShip_Char_Screen.onkeypress(lambda: Sprite_SetDirection_RIGHT(SpaceShip_Char), "Right")
SpaceShip_Char_Screen.onkeypress(lambda: shoot_Missile(), 'space')
SpaceShip_Char_Screen.onkeypress(Start_SpaceInvaders, 'p')

SpaceShip_Char_Screen.listen()
SpaceShip_Char_Screen.mainloop()