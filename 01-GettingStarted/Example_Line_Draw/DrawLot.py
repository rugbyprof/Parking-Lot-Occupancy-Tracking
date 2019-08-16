import numpy as np
import cv2
import json

img = None

def addText(coords,txt):
    global img
    cv2.putText(img,txt,coords, cv2.FONT_HERSHEY_SIMPLEX, .5,(255,255,255),2,cv2.LINE_AA)


def drawSpace(coords):
    global img
    x0 = int(coords[0]['x'])
    y0 = int(coords[0]['y'])
    x1 = int(coords[1]['x'])
    y1 = int(coords[1]['y'])
    x2 = int(coords[2]['x'])
    y2 = int(coords[2]['y'])
    x3 = int(coords[3]['x'])
    y3 = int(coords[3]['y'])

    cv2.line(img,(x0,y0),(x1,y1),(255,0,0),1)
    cv2.line(img,(x0,y0),(x3,y3),(255,0,0),1)
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
    cv2.line(img,(x2,y2),(x3,y3),(255,0,0),1)


def getCenter(coords):

    xt = 0
    yt = 0

    for c in coords:
        xt = xt + c['x']
        yt = yt + c['y']

    return (int(xt/4)-10,int(yt/4))


def main():
    global img

    img = cv2.imread('West-Virginia_Full.jpg')

    with open('lot_definition.json') as data_file:
        data = data_file.read()
        lot_definition = json.loads(data)

    
    id = 0
    for space_dict in lot_definition:
        coords = space_dict['space']
        center = getCenter(coords)
        drawSpace(coords)
        addText(center,str(id))
        id += 1

    cv2.imwrite('West-Virginia_Full-Lines.jpg',img)


if __name__=='__main__':
    main()