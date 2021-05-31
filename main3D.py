import pygame
import os
import sys
import math
import numpy as np
import time
import uuid
# from matrix import matrix_multiplication
from time import sleep, process_time
from numpy.linalg import multi_dot
from csv import writer
from TestPage import *



class Object3D:
    def __init__(self, angle, screen, clock, fps, cube_position, scale, speed, live_mode=False):
        self.angle = angle
        self.screen = screen
        self.clock = clock
        self.fps = fps
        self.cube_position = cube_position
        self.scale = scale
        self.speed = speed
        self.black, self.white, self.blue, self.red = (20, 20, 20), (230, 230, 230), (0, 154, 255), (255, 66, 0)
        self.MarkerList = dict()
        self.points = [n for n in range(8)]
        self.counter = 0
        self.marker_csv = []

        if live_mode:
            self._pos_live()


    def connect_point(self, i, j, k):
        a = k[i]
        b = k[j]
        pygame.draw.line(self.screen, self.black, (a[0], a[1]), (b[0], b[1]), 3)

    # Due to problems with Emotiv we used an own implementation for the markers
    def marker_inject(self, direction_dict):
        Timestamp = time.time()
        Endtime = 0
        Label = direction_dict['Label']
        Value = direction_dict['Value']
        self.Current_Marker = uuid.uuid1().hex

        self.MarkerList[str(self.Current_Marker)] = [Timestamp, Endtime, Label, Value]
        print(self.MarkerList)

    def update_marker(self):
        End_Timestamp = time.time()
        self.MarkerList[self.Current_Marker][1] = End_Timestamp
        
        ######
        self.marker_csv.append(self.MarkerList[self.Current_Marker])

    def export_Marker(self, file):
        row = ['Marker_ID', 'Start', 'End', 'Label', 'Value']
        self.build_marker_csv(file, row)

        for key in self.MarkerList:
            csv_row = self.MarkerList[key][:]
            csv_row.insert(0, key)
            self.build_marker_csv(file, csv_row)

    def build_marker_csv(self, file, row):
        with open(file, "a+", newline='') as csv_file:
            print(row)
            print(file)
            csv_writer = writer(csv_file)
            csv_writer.writerow(row)

    # Very basic way of visualizing text on screen
    def _pre_run_text(self, label):
        self.screen.fill(self.white)
        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        mode = 'Training: ' + label
        dialog = text.render(mode, True, self.black, self.white)
        new_x = 583
        new_y = 400
        self.screen.blit(dialog, [new_x, new_y])
        pygame.display.update()
        time.sleep(2)


        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        dialog = text.render('Please relax..', True, self.black, self.white)
        new_x = 595
        new_y = 450
        self.screen.blit(dialog, [new_x, new_y])

        dialog = text.render('Sequence starting in:', True, self.black , self.white)
        new_x = 520
        new_y = 500

        self.screen.blit(dialog, [new_x, new_y])
        pygame.display.update()
        time.sleep(4)

        self.screen.fill(self.white)
        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        dialog = text.render('3..', True, self.black, self.white)
        new_x = 720
        new_y = 500
        self.screen.blit(dialog,  [new_x, new_y])

        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        mode = 'Training: ' + label
        dialog = text.render(mode, True, self.black, self.white)
        new_x = 610
        new_y = 450
        self.screen.blit(dialog, [new_x, new_y])

        pygame.display.update()
        time.sleep(1)

        self.screen.fill(self.white)
        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        dialog = text.render('2..', True, self.black, self.white)
        new_x = 720
        new_y = 500
        self.screen.blit(dialog,  [new_x, new_y])

        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        mode = 'Training: ' + label
        dialog = text.render(mode, True, self.black, self.white)
        new_x = 610
        new_y = 450
        self.screen.blit(dialog, [new_x, new_y])

        pygame.display.update()
        time.sleep(1)

        self.screen.fill(self.white)
        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        dialog = text.render('1..', True, self.black, self.white)
        new_x = 720
        new_y = 500
        self.screen.blit(dialog,  [new_x, new_y])

        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        mode = 'Training: ' + label
        dialog = text.render(mode, True, self.black, self.white)
        new_x = 610
        new_y = 450
        self.screen.blit(dialog, [new_x, new_y])

        pygame.display.update()
        time.sleep(1)

    # Initialization of positions for different cubes and modes
    def _pos_init(self, direction, live_mode=False):
        if direction == 'Forward':
            self.points[0] = [[-1], [0], [1]]
            self.points[1] = [[1], [0], [1]]
            self.points[2] = [[1], [2], [1]]
            self.points[3] = [[-1], [2], [1]]
            self.points[4] = [[-1], [0], [-1]]
            self.points[5] = [[1], [0], [-1]]
            self.points[6] = [[1], [2], [-1]]
            self.points[7] = [[-1], [2], [-1]]


        else:
            self.points[0] = [[-1], [-1], [1]]
            self.points[1] = [[1], [-1], [1]]
            self.points[2] = [[1], [1], [1]]
            self.points[3] = [[-1], [1], [1]]
            self.points[4] = [[-1], [-1], [-1]]
            self.points[5] = [[1], [-1], [-1]]
            self.points[6] = [[1], [1], [-1]]
            self.points[7] = [[-1], [1], [-1]]


    def _pos_live(self):
        self.points[0] = [[-1], [0], [1]]
        self.points[1] = [[1], [0], [1]]
        self.points[2] = [[1], [2], [1]]
        self.points[3] = [[-1], [2], [1]]
        self.points[4] = [[-1], [0], [-1]]
        self.points[5] = [[1], [0], [-1]]
        self.points[6] = [[1], [2], [-1]]
        self.points[7] = [[-1], [2], [-1]]

    # Function for the Test Mode
    def run_test(self, run=False, direction_dict={'default': -1}):
        self._pre_run_text(direction_dict['Label'])
        self._pos_init(direction_dict['Label'])
        self.marker_inject(direction_dict)

        self.counter = 0

        text = pygame.font.SysFont('Proxima Nova', 50, bold=False)
        dialog = text.render(direction_dict['Label'], True, self.black, self.white)
        if direction_dict['Label'] == 'Stop':
            new_x = self.cube_position[0] - 60
            new_y = 20

        else:
            new_x = self.cube_position[0] - 100
            new_y = 20

        training_start_time = time.time()
        while run:
            self.clock.tick(self.fps)
            self.screen.fill(self.white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            index = 0
            projected_points = [j for j in range(len(self.points))]

            if direction_dict['Label'] == "Rotate":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[math.cos(self.angle), 0,-math.sin(self.angle)],
                                       [0, 1, 0],
                                       [math.sin(self.angle), 0, math.cos(self.angle)]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

            elif direction_dict['Label'] == "Neutral":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                # fluctu means fluctuations because it was wanted to have still some
                # 3D movement in the neural position
                for i in self.points:
                    fluctu = math.radians(self.counter)
                    i[1][0] -= 0.003 * math.sin(fluctu)
                    i[2][0] -= 0.002 * math.cos(fluctu)
                    i[0][0] += 0.001 * math.cos(fluctu)

            elif direction_dict['Label'] == "Stop":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])


            elif direction_dict['Label'] == "Forward":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                for i in self.points:
                    if i[1][0] <= -7.0:
                        self.points[0] = [[-1], [1], [1]]
                        self.points[1] = [[1], [1], [1]]
                        self.points[2] = [[1], [3], [1]]
                        self.points[3] = [[-1], [3], [1]]
                        self.points[4] = [[-1], [1], [-1]]
                        self.points[5] = [[1], [1], [-1]]
                        self.points[6] = [[1], [3], [-1]]
                        self.points[7] = [[-1], [3], [-1]]
                    i[1][0] -= 0.0038



            for point in self.points:
                rotated_2d = multi_dot([rotation_y, point])
                rotated_2d = multi_dot([rotation_x, rotated_2d])
                rotated_2d = multi_dot([rotation_z, rotated_2d])
                self.distance = 4
                z = 1 / (self.distance - rotated_2d[2][0])
                projection_matrix = np.array([[z, 0, 0],[0, z, 0]])
                projected_2d = multi_dot([projection_matrix, rotated_2d])

                x = int(projected_2d[0][0] * self.scale) + self.cube_position[0]
                y = int(projected_2d[1][0] * self.scale) + self.cube_position[1]
                projected_points[index] = [x, y]
                pygame.draw.circle(self.screen, self.blue, (x, y), 8)
                index += 1

            for m in range(4):
                self.connect_point(m, (m + 1) % 4, projected_points)
                self.connect_point(m + 4, (m + 1) % 4 + 4, projected_points)
                self.connect_point(m, m + 4, projected_points)

            self.angle += self.speed**0.7
            self.screen.blit(dialog, [new_x, new_y])
            pygame.display.update()
            sleep(0.01)
            self.counter += 1
            elapsed_time = time.time() - training_start_time

            if elapsed_time >= 7 :
                self.update_marker()
                print(self.MarkerList)
                break

    # Function for the Live Mode
    def run_live(self, run=False, direction='default'):
        text_1 = pygame.font.SysFont('Arial', 50, bold=True)
        dialog = text_1.render('Live Mode', True, self.blue, self.white)
        text_2 = pygame.font.SysFont('Arial', 20, bold=True)
        quit_msg = text_2.render('Press Q in GUI to exit', True, self.red, self.white)
        new_x = self.cube_position[0] - 150
        new_y = 20

        training_start_time = time.time()
        while run:
            self.clock.tick(self.fps)
            self.screen.fill(self.white)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            index = 0
            projected_points = [j for j in range(len(self.points))]

            if direction == "Rotate":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[math.cos(self.angle), 0, -math.sin(self.angle)],
                                       [0, 1, 0],
                                       [math.sin(self.angle), 0, math.cos(self.angle)]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

            elif direction == "Stop":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

            elif direction == "Neutral":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                for i in self.points:
                    fluctu = math.radians(self.counter)
                    i[1][0] -= 0.003*math.sin(fluctu)
                    i[2][0] -= 0.002 * math.cos(fluctu)
                    i[0][0] += 0.001 * math.cos(fluctu)


            elif direction == "Forward":
                rotation_x = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_y = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                rotation_z = np.array([[1, 0, 0],
                                       [0, 1, 0],
                                       [0, 0, 1]])

                for i in self.points:
                    if i[1][0] <= -5.0:
                        self._pos_live()

                    i[1][0] -= 0.01



            for point in self.points:
                rotated_2d = multi_dot([rotation_y, point])
                rotated_2d = multi_dot([rotation_x, rotated_2d])
                rotated_2d = multi_dot([rotation_z, rotated_2d])
                distance = 4
                z = 1 / (distance - rotated_2d[2][0])
                projection_matrix = np.array([[z, 0, 0],[0, z, 0]])
                projected_2d = multi_dot([projection_matrix, rotated_2d])

                x = int(projected_2d[0][0] * self.scale) + self.cube_position[0]
                y = int(projected_2d[1][0] * self.scale) + self.cube_position[1]
                projected_points[index] = [x, y]
                pygame.draw.circle(self.screen, self.blue, (x, y), 8)
                index += 1

            for m in range(4):
                self.connect_point(m, (m + 1) % 4, projected_points)
                self.connect_point(m + 4, (m + 1) % 4 + 4, projected_points)
                self.connect_point(m, m + 4, projected_points)

            self.angle += self.speed
            self.counter += 1
            self.screen.blit(dialog, [new_x, new_y])
            self.screen.blit(quit_msg, [20, 20])
            pygame.display.update()
            sleep(0.01)

            elapsed_time = time.time() - training_start_time

            if elapsed_time >= 0.5:  # From Testapage imported overlap value
                break



# change start position

def start_3Danimation(speed, live_mode=False):
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    angle = 0
    width = 1466
    height = 1100

    pygame.init()
    pygame.display.set_caption("BCI - Live Mode")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    fps = 100

    #angle = 0
    cube_position = [width // 2, height // 2]
    scale = 600

    return Object3D(angle, screen, clock, fps, cube_position, scale, speed, live_mode)


def quit_3Danimation():
    pygame.quit()

# Some testings where done here. To get a grasp of 
# how this is working, you can use this.
if False:

    neutral_marker = {"Label": "Neutral", "Value": 0}
    forward_marker = {"Label": "Forward", "Value": 1}
    rotate_marker = {"Label": "Rotate", "Value": 2}

    Obj = start_3Danimation(0.005)
    Obj.run_test(True, neutral_marker)
    time.sleep(0.5)
    Obj.run_test(True, forward_marker)
    time.sleep(0.5)
    Obj.run_test(True, rotate_marker)
    time.sleep(0.5)
    Obj.export_Marker('marker_info.csv')
    quit_3Danimation()
