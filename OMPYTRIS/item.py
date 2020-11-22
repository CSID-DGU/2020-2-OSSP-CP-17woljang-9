import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
import random
import threading


# 이미지 불러오기, 아이템 리스트, 인벤토리 전역변수 선언
item_list, inven=[],[]

squid=pygame.transform.scale(pygame.image.load("assets/images/squid.png"),(25,25))

squid_ink=pygame.transform.scale(pygame.image.load("assets/images/real-ink.png"),(250,250))

item_list.append(squid)

class Board:
   
    def __init__(self, screen):
        self.screen = screen
        self.width = 10
        self.height = 20
        self.block_size = 25
        self.init_board()
        self.generate_piece()
        # for timer
        self.start_time=0
        self.total_seconds=0
        self.minutes=0
        self.seconds=0
        
    def init_board(self):
        self.board = []
        self.score = 0
        self.round = 1
        for _ in range(self.height):
            self.board.append([0]*self.width)

    def init(self): # timer 초기화
        self.frame_count=0
        self.start_time=120
        self.piece_x=3
        self.piece_y=0

    def timer(self):
        self.total_seconds=self.start_time-(self.frame_count//30)
        if self.total_seconds<0:
            self.total_seconds=0

        self.minutes=self.total_seconds//60
        self.seconds=self.total_seconds%60

        output='{0:02}:{1:02}'.format(self.minutes,self.seconds)
        time_value=pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(output, True, BLACK)
        self.screen.blit(time_value,(275,430))
        self.frame_count+=1
 
    def delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_under(self):     # 맨 밑줄 없애는 아이템
        self.delete_line(19)
    
    def delete_vertical(self,x): # 세로로 없애는 아이템
        for i in range(len(self.board)):
            self.board[i][x]=0
    
    def delete_lines(self):
        count,line=[],[]
        for y,row in enumerate(self.board):
            if all(row):
                count.append(y)
                flag=False
                for x, block in enumerate(row): # 물음표가 존재하는 블럭이 사라지면 get_item()
                    num=self.col_num(block)
                    if num==8:
                        self.get_item()
                    elif num==15 and y!=19: # 라인에 맨 밑줄 사라지는 아이템이 있으면 그리고 그 라인이 맨 밑줄이 아니면 
                        flag=True
                    elif num==22 : # 라인에 세로로 사라지는 아이템이 있으면
                        line.append(x)
                    
                line_sound=pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
                line_sound.play()

                self.delete_line(y)

                if flag==True: # flag가 True이면 맨 밑줄 사라지는 아이템이 있으면 맨 밑줄을 없앰
                    self.delete_under()

                self.score+=10*self.round

        for x in line:
            self.delete_vertical(x)

    def get_item(self):     #인벤토리에 아이템 생성
        if len(inven)<3:
            inven.append(item_list[random.randrange(0,4)])
        return inven
    
    def use_item(self):     #인벤토리의 아이템 사용
        if len(inven)>0:
            item=inven[0]
            inven.pop(0)
            if item==item_list[0]:
                self.slow()
                t=threading.Timer(3,self.back_to_origin,args=None,kwargs=None)
                t.start()
            elif item==item_list[1]:
                self.fast()
                t=threading.Timer(3,self.back_to_origin,args=None,kwargs=None)
                t.start()
            elif item==item_list[2]:
                self.change()
            else:
                t=threading.Thread(target=self.squid_ink,args=(0,100))
                t.start()
        
    def show_item(self):    #인벤토리의 아이템들을 보여줌
            if len(inven)>=1:
                self.screen.blit(inven[0],(260,145))
                if len(inven)>=2:
                    self.screen.blit(inven[1],(288,145))
                    if len(inven)==3:
                        self.screen.blit(inven[2],(316,145))
                
    def back_to_origin(self): # 원래 속도로 돌아옴
        if self.round<=9:
            pygame.time.set_timer(pygame.USEREVENT,(500 - 50 * (self.round-1)))
        else :
            pygame.time.set_timer(pygame.USEREVENT,100)
        
    def slow(self): # 달팽이 아이템 기능
        pygame.time.set_timer(pygame.USEREVENT,1000)

    def fast(self): # 번개 아이템 기능
        pygame.time.set_timer(pygame.USEREVENT,100)

    def squid_ink(self,a,b): # 오징어 먹물 아이템 기능
        ink_sound=pygame.mixer.Sound('assets/sounds/squid_ink.wav')
        ink_sound.play()
        for i in range(3000):
            ink=self.screen.blit(squid_ink,(a, b))
            if self.minutes==0 and self.seconds==0 :
                break
