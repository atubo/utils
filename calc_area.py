#!/usr/bin/python
import Tkinter, tkFileDialog
from PIL import Image, ImageTk
from collections import deque

class AreaCalc:
    def __init__(self, image):
        self.image = image

    def sameColor(self, pixel, p0):
        maxDist = 25
        (r0, g0, b0) = self.image.getpixel(p0)
        (r1, g1, b1) = self.image.getpixel(pixel)
        return (abs(r0-r1) <= maxDist and abs(g0-g1) <= maxDist and
                abs(b0-b1) <= maxDist)

    def inRange(self, pixel):
        (sizeX, sizeY) = self.image.size
        return (0 <= pixel[0] and pixel[0] < sizeX and
                0 <= pixel[1] and pixel[1] < sizeY)
               
    def getNeighbors(self, pixel):
        neighbors = []
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for i in range(4):
            p = (pixel[0] + dx[i], pixel[1] + dy[i])
            if self.inRange(p):
                neighbors.append(p)
        return neighbors

    def calc(self, x, y):
        visited = set()
        p0 = (x, y)
        queue = deque()
        queue.append(p0)
        while len(queue) != 0:
            pixel = queue.pop()
            if pixel not in visited and self.sameColor(pixel, p0):
                visited.add(pixel)
                for n in self.getNeighbors(pixel):
                    queue.append(n)
        print len(visited)
        (r, g, b) = self.image.getpixel(p0)
        print r, g, b
        invertedColor = (256-r, 256-g, 256-b)
        invertedImg = self.image.copy()
        for pixel in visited:
            invertedImg.putpixel(pixel, invertedColor)
        return (invertedImg, len(visited))




class App:
    def __init__(self):
        self.root = Tkinter.Tk()
        fname = tkFileDialog.askopenfilename()
        if fname == '':
            exit(0)
        self.image = Image.open(fname)
        self.areaCalc = AreaCalc(self.image)
        self.pimage = ImageTk.PhotoImage(self.image)
        width  = self.pimage.width()
        height = self.pimage.height() 
        self.frame = Tkinter.Frame(self.root)
        self.canvas = Tkinter.Canvas(self.frame,
                                     height = height,
                                     width  = width)
        self.canvas.create_image(0, 0, anchor='nw', image=self.pimage)
        self.canvas.bind("<1>", self.click)
        self.canvas.pack()

        self.sv = Tkinter.StringVar()
        self.label = Tkinter.Label(self.frame, textvariable=self.sv)
        self.label.pack()

        self.frame.pack()
        self.root.mainloop()

    def click(self, event):
        #print("Clicked at: ", event.x, event.y)
        (newImg, size) = self.areaCalc.calc(event.x, event.y)
        self.pimage = ImageTk.PhotoImage(newImg)
        self.canvas.create_image(0, 0, anchor='nw', image=self.pimage)
        self.sv.set(str(size))

App()

