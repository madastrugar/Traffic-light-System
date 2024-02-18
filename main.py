import pygame
import time
from random import choice,randint

pygame.init()
#screen size
X=700
Y=600
screen=pygame.display.set_mode([X,Y])
pygame.display.set_caption("Traffic Simulator")

#images
background=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\Traffic_Simulator_3.png").convert()
purple_car=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\purple_car.PNG").convert_alpha()
yellow_car=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\yellow_car.PNG").convert_alpha()
red_car=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\red_car.PNG").convert_alpha()
red_light=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\red_light.PNG").convert_alpha()
yellow_light=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\yellow_light.PNG").convert_alpha()
green_light=pygame.image.load("D:\\Facultate\\Anul 3\\SSC\\Proiect\\green_light.PNG").convert_alpha()

lights_coordinates={"light1":[X*0.3,Y*0.3],"light2":[X*0.3,Y*0.6],"light3":[X*0.6,Y*0.3],"light4":[X*0.6,Y*0.6]}
stop_light={"DOWN":[X*0.4,Y*0.3],"RIGHT":[X*0.33,Y*0.6],"LEFT":[X*0.62,Y*0.3],"UP":[X*0.5,Y*0.625]}
car_start={"UP":[[X*0.5,Y],[X*0.54,Y]],"DOWN":[[X*0.41,0],[X*0.46,0]],"RIGHT":[[0,Y*0.55],[0,Y*0.5]],"LEFT":[[X,Y*0.41],[X,Y*0.45]]}
car_colors={"red":red_car,"yellow":yellow_car,"purple":purple_car}
directions=["UP","DOWN","RIGHT","LEFT"]
cars = {"UP":[],"DOWN":[],"RIGHT":[],"LEFT":[],"CROSSED":[]}

gap=25 #distance between cars when they stop at a red light
currentGreen=0 #which traffic light is green
class Car():
    def __init__(self):
        image=choice(list(car_colors.items()))
        image=image[1]
        self.direction=choice(directions)
        self.lane = randint(0,1)
        self.speed = 20
        self.crossed = False
        self.stop = 0
        self.x = car_start[self.direction][self.lane][0]
        self.y = car_start[self.direction][self.lane][1]
        if self.direction=="UP" or self.direction=="DOWN":
          self.stop = stop_light[self.direction][1]
        else:
          self.stop = stop_light[self.direction][0]
        if self.direction=="DOWN":
           self.car_img=pygame.transform.rotate(image,180)
        elif self.direction=="RIGHT":
            self.car_img = pygame.transform.rotate(image, -90)
        elif self.direction=="LEFT":
           self.car_img = pygame.transform.rotate(image, 90)
        else:
            self.car_img=image

    def move(self):
        if self.direction=="UP":
            self.y -= self.speed
        elif self.direction=="DOWN":
            self.y += self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        elif self.direction=="LEFT":
            self.x -= self.speed


    def cross(self):
        new_direction = ""
        match self.direction:
            case "UP":
                if self.y < stop_light[self.direction][1] - 40:
                    if self.lane == 0:
                        new_direction = choice(["LEFT", "UP"])
                    else:
                        new_direction = choice(["RIGHT", "UP"])
                    self.direction = new_direction
                    match new_direction:
                        case "RIGHT":
                            self.car_img = pygame.transform.rotate(self.car_img, -90)
                            self.y += 7
                        case "LEFT":
                            self.car_img = pygame.transform.rotate(self.car_img, 90)
                            self.y -= 48
                    return True
            case "DOWN":
                if self.y > stop_light[self.direction][1] + 40:
                    if self.lane == 0 : new_direction=choice(["LEFT", "DOWN"])
                    else : new_direction=choice(["RIGHT", "DOWN"])
                    self.direction = new_direction
                    match new_direction:
                        case "RIGHT":
                            self.car_img = pygame.transform.rotate(self.car_img, 90)
                            self.y += 58
                        case "LEFT":
                            self.car_img = pygame.transform.rotate(self.car_img, -90)
                            self.y -= 2
                    return True
            case "LEFT":
                # if self.x < stop_light[self.direction][0]:
                if self.x < stop_light[self.direction][0] - 40:
                    if self.lane == 0 : new_direction=choice(["UP", "LEFT"])
                    else : new_direction=choice(["DOWN","LEFT"])
                    self.direction = new_direction
                    match new_direction:
                        case "DOWN":
                            self.car_img = pygame.transform.rotate(self.car_img, 90)
                            self.x -= 60
                        case "UP":
                            self.car_img = pygame.transform.rotate(self.car_img, -90)
                            self.x -= 5
                    return True
            case "RIGHT":
                # if self.x > stop_light[self.direction][0]:
                if self.x > stop_light[self.direction][0] + 40:
                    if self.lane == 0 : new_direction=choice(["DOWN", "RIGHT"])
                    else : new_direction=choice(["UP","RIGHT"])
                    self.direction = new_direction
                    match new_direction:
                        case "DOWN":
                            self.car_img = pygame.transform.rotate(self.car_img, -90)
                            self.x += 15
                        case "UP":
                            self.car_img = pygame.transform.rotate(self.car_img, 90)
                            self.x += 64
                    return True
            case _:
                return False
        return False

class TrafficLight():
    def __init__(self, x, y, status,image,lane):
        self.x = x
        self.y = y
        self.color = status
        self.image=image
        self.time=0
        self.lane=lane


text_font = pygame.font.SysFont(None,20)

def show_text(text,font,x,y):
    img = font.render(text,True,(0,0,0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+5, y-20, 21, 15))
    screen.blit(img,(x+10,y-20))

vehicles=[]
for i in range(10):
    new_car=Car()
    cars[new_car.direction].append(new_car)

traffic_lights=[]

def createTrafficLights(list:[]):
    list.append(TrafficLight(X*0.32,Y*0.27,"red",red_light,"DOWN"))
    list.append(TrafficLight(X*0.32,Y*0.65,"red",red_light,"RIGHT"))
    list.append(TrafficLight(X*0.62,Y*0.27,"red",red_light,"LEFT"))
    list.append(TrafficLight(X*0.62,Y*0.65,"red",red_light,"UP"))
    return list

traffic_lights = createTrafficLights(traffic_lights)

allRed = True

class Main:
 running=True
 while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.blit(background,(0,0))

    if allRed==True:
        if currentGreen<3 :
           currentGreen+=1
        else : currentGreen=0
        traffic_lights[currentGreen].time=10
        traffic_lights[currentGreen].image=green_light
        traffic_lights[currentGreen].color="green"
        allRed=False

    for t in traffic_lights:
        screen.blit(t.image,(t.x,t.y))
        if t.time==0 :
          show_text("-",text_font, t.x, t.y)
        else:
          show_text(str(t.time), text_font, t.x, t.y)

    if traffic_lights[currentGreen].time>0 :
          traffic_lights[currentGreen].time-=1
    elif traffic_lights[currentGreen].time==0 and traffic_lights[currentGreen].color=="green":
          traffic_lights[currentGreen].color = "yellow"
          traffic_lights[currentGreen].time = 3
          traffic_lights[currentGreen].image = yellow_light
    else :
        traffic_lights[currentGreen].color="red"
        traffic_lights[currentGreen].image=red_light
        allRed=True
        # generate new car
        new_car = Car()
        cars[new_car.direction].append(new_car)

    #verificare daca masina a trecut de semafor, daca nu atunci unde sa opreasca daca are rosu
    for key in cars.keys():
        if key != "CROSSED" and len(cars[key])!=0:
            for x in cars[key]:
                x.crossed = x.cross()
                if x.crossed:

                    cars["CROSSED"].append(x)
                    cars[key].remove(x)
                else:

                   sum0 =0
                   sum1 =0
                   for i in range(0,cars[key].index(x)):
                       if cars[key][i].lane ==0 : sum0+=1
                       else: sum1+=1

                   if x.lane == 0:
                        stop = sum0 * 35 + gap

                   else:
                        stop = sum1 * 35 + gap


                   # stop = cars[key].index(x) * 35 + gap  #
                   match x.direction:
                            case "UP":
                                 x.stop = stop_light[x.direction][1] + stop
                            case "DOWN":
                                 x.stop = stop_light[x.direction][1] - stop
                            case "RIGHT":
                                 x.stop = stop_light[x.direction][0] - stop
                            case "LEFT":
                                 x.stop = stop_light[x.direction][0] + stop

    for key in cars.keys():
        if key == "CROSSED":
            for c in cars[key]:
                c.move()
                screen.blit(c.car_img, (c.x, c.y))
        else:
          for x in cars[key]:
            if traffic_lights[currentGreen].lane != key:
              match x.direction:
                case "UP":
                    if x.y > x.stop:
                        x.move()
                case "DOWN":
                    if x.y < x.stop:
                        x.move()
                case "RIGHT":
                    if x.x < x.stop:
                        x.move()
                case "LEFT":
                    if x.x > x.stop:
                        x.move()
            else:
                x.move()
            screen.blit(x.car_img, (x.x, x.y))

    pygame.display.update()
    time.sleep(1)
