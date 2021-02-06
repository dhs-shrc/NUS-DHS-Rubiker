import pygame
import random
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
ij = 0
vertices = (    
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
)
edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
surfaces = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
colors = ((1, 0, 0), (0, 1, 0), (1, 0.5, 0), (1, 1, 0), (1, 1, 1), (0, 0, 1))
#54 colors of each side of the rubiks cube spread out.
raw_confi ="WWWWWWWWWYYYYYYYYYOOOOOOOOORRRRRRRRRGGGGGGGGGBBBBBBBBB"
raw_config = list(raw_confi)
for i in range(len(raw_config)):
    if raw_config[i] == "W":
        raw_config[i] = (1,1,1)
    if raw_config[i] == "Y":
        raw_config[i] = (1,1,0)
    if raw_config[i] == "O":
        raw_config[i] = (1,0.5,0)
    if raw_config[i] == "R":
        raw_config[i] = (1,0,0)
    if raw_config[i] == "G":
        raw_config[i] = (0,1,0)
    if raw_config[i] == "B":
        raw_config[i] = (0,0,1)
#(BACK),(LEFT),(FRONT),(ORANGE),(TOP),(BOTTOM)


class Cube():
    def __init__(self, id, N, scale):
        self.N = N
        self.scale = scale
        self.init_i = [*id]
        self.current_i = [*id]
        self.rot = [[1 if i==j else 0 for i in range(3)] for j in range(3)]
    #Figure out whichc ubes in the rubiks cube are affected
    def isAffected(self, axis, slice, dir):
        return self.current_i[axis] == slice
    #Rotation of a single cube
    def update(self, axis, slice, dir):

        if not self.isAffected(axis, slice, dir):
            return

        i, j = (axis+1) % 3, (axis+2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j]*dir, self.rot[k][i]*dir

        self.current_i[i], self.current_i[j] = (
            self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
            self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i] )

    def transformMat(self):
        scaleA = [[s*self.scale for s in a] for a in self.rot]  
        scaleT = [(p-(self.N-1)/2)*2.1*self.scale for p in self.current_i] 
        return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

    def draw(self, col, surf, vert, animate, angle, axis, slice, dir, raw_config):

        glPushMatrix()
        if animate and self.isAffected(axis, slice, dir):
            glRotatef( angle*dir, *[1 if i==axis else 0 for i in range(3)] )
        glMultMatrixf( self.transformMat() )

        glBegin(GL_QUADS)
        global ij
        #(BACK),(LEFT),(FRONT),(RIGHT),(TOP),(BOTTOM)
        #Rubiks cube logic
        if ij == 6:
            colors = (raw_config[2],raw_config[9],(1,1,1),(1,1,1),raw_config[36],(1,1,1))
        elif ij == 7:
            colors = ((1,1,1),raw_config[10],(1,1,1),(1,1,1),raw_config[39],(1,1,1))
        elif ij == 8:
            colors =((1,1,1),raw_config[11],(raw_config[18]),(1,1,1),raw_config[42],(1,1,1))
        elif ij == 3:
            colors =(raw_config[5],raw_config[12],(1,1,1),(1,1,1),(1,1,1),(1,1,1))
        elif ij == 4:
            colors =((1,1,1),raw_config[13],(1,1,1),(1,1,1),(1,1,1),(1,1,1))
        elif ij == 5:
            colors =((1,1,1),raw_config[14],raw_config[21],(1,1,1),(1,1,1),(1,1,1))
        elif ij == 0:
            colors =(raw_config[8],raw_config[15],(1,1,1),(1,1,1),(1,1,1),raw_config[51])
        elif ij == 1:
            colors =((1,1,1),raw_config[16],(1,1,1),(1,1,1),(1,1,1),raw_config[48])
        elif ij == 2:
            colors = ((1,1,1),raw_config[17],raw_config[24],(1,1,1),(1,1,1),raw_config[45])
        elif ij == 15: 
            colors = (raw_config[1],(1,1,1),(1,1,1),(1,1,1),raw_config[37],(1,1,1))
        elif ij == 16:
            colors = ((1,1,1),(1,1,1),(1,1,1),(1,1,1),raw_config[40],(1,1,1))
        elif ij == 17:
            colors = ((1,1,1),(1,1,1),raw_config[19],(1,1,1),raw_config[43],(1,1,1))
        elif ij == 12:
            colors = (raw_config[4],(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1))
        elif ij == 13:
            colors = ((1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1))
        elif ij == 14:
            colors = ((1,1,1),(1,1,1),raw_config[22],(1,1,1),(1,1,1),(1,1,1))
        elif ij == 9:
            colors = (raw_config[7],(1,1,1),(1,1,1),(1,1,1),(1,1,1),raw_config[52])
        elif ij == 10:
            colors = ((1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),raw_config[49])
        elif ij == 11:
            colors = ((1,1,1),(1,1,1),raw_config[25],(1,1,1),(1,1,1),raw_config[46])
        elif ij == 24:
            colors = (raw_config[0],(1,1,1),(1,1,1),raw_config[29],raw_config[38],(1,1,1))
        elif ij == 25:
            colors = ((1,1,1),(1,1,1),(1,1,1),raw_config[28],raw_config[41],(1,1,1))
        elif ij == 26:
            colors = ((1,1,1),(1,1,1),raw_config[20],raw_config[27],raw_config[44],(1,1,1))
        elif ij == 21:
            colors = (raw_config[3],(1,1,1),(1,1,1),raw_config[32],(1,1,1),(1,1,1))
        elif ij == 22:
            colors = ((1,1,1),(1,1,1),(1,1,1),raw_config[31],(1,1,1),(1,1,1))
        elif ij == 23:
            colors = ((1,1,1),(1,1,1),raw_config[23],raw_config[30],(1,1,1),(1,1,1))
        elif ij == 18:
            colors = (raw_config[6],(1,1,1),(1,1,1),raw_config[35],(1,1,1),raw_config[53])
        elif ij == 19:
            colors = ((1,1,1),(1,1,1),(1,1,1),raw_config[34],(1,1,1),raw_config[50])
        elif ij == 20:
            colors = ((1,1,1),(1,1,1),raw_config[26],raw_config[33],(1,1,1),raw_config[47])

        for i in range(len(surf)):
            glColor3fv(colors[i])
            for k in surf[i]:
                glVertex3fv(vertices[k])
        glEnd()

        glPopMatrix()

class EntireCube():
    def __init__(self, N, scale):
        self.N = N
        cr = range(self.N)
        self.cubes = []
        #Creating a 3x3x3 cube
        for x in cr:
            for y in cr:
                for z in cr:
                    self.cubes.append(Cube((x,y,z), self.N, scale))

    def mainloop(self):
        #view rotation dictionary
        rot_cube_map  = { K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)}
        #slice rotation dictionary
        rot_slice_map = {
            K_1: (0, 0, 1), K_2: (0, 1, 1), K_3: (0, 2, 1), K_4: (1, 0, 1), K_5: (1, 1, 1),
            K_6: (1, 2, 1), K_7: (2, 0, 1), K_8: (2, 1, 1), K_9: (2, 2, 1),
            K_F1: (0, 0, -1), K_F2: (0, 1, -1), K_F3: (0, 2, -1), K_F4: (1, 0, -1), K_F5: (1, 1, -1),
            K_F6: (1, 2, -1), K_F7: (2, 0, -1), K_F8: (2, 1, -1), K_F9: (2, 2, -1),
        }  

        ang_x, ang_y, rot_cube = 0, 0, (0, 0)
        animate, animate_ang, animate_speed = False, 0, 5
        action = (0, 0, 0)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    #view rotation + actual rotation
                if event.type == KEYDOWN:
                    if event.key in rot_cube_map:
                        rot_cube = rot_cube_map[event.key]
                    if not animate and event.key in rot_slice_map:
                        animate, action = True, rot_slice_map[event.key]
                if event.type == KEYUP:
                    if event.key in rot_cube_map:
                        rot_cube = (0, 0)
            #Final calculations to rotation matrix
            ang_x += rot_cube[0]*2
            ang_y += rot_cube[1]*2

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -40)
            #Applying multiplication matrix for axis
            glRotatef(ang_y, 0, 1, 0)
            glRotatef(ang_x, 1, 0, 0)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            #Animation
            if animate:
                if animate_ang >= 90:
                    for cube in self.cubes:
                        cube.update(*action)
                    animate, animate_ang = False, 0

            for cube in self.cubes:
                cube.draw(colors, surfaces, vertices, animate, animate_ang, *action, raw_config)
                global ij
                ij += 1
                if ij > 26:
                    ij = 0

            if animate:
                animate_ang += animate_speed

            pygame.display.flip()
            pygame.time.wait(10)

def main():

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST) 

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)  

    NewEntireCube = EntireCube(3, 1.5) 
    NewEntireCube.mainloop()

if __name__ == '__main__':
    main()
    pygame.quit()
    quit()

