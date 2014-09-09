from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import textwrap
import math
import os
import json
import urllib, cStringIO

fontsPath = r'c:\demos\thumbnailgenerator2\fonts'
outputPath = arcpy.env.scratchFolder

def roundUp(x):
    return math.ceil(x) if x > 0. else math.floor(x)

astr = arcpy.GetParameterAsText(0)
FONT_SIZE = int(arcpy.GetParameterAsText(1))
TEXT_COLOR = arcpy.GetParameterAsText(2)
ALIGN = arcpy.GetParameterAsText(3)
selectedFont = arcpy.GetParameterAsText(4)
ULX = int(arcpy.GetParameterAsText(5))
ULY = int(arcpy.GetParameterAsText(6))
LRX = int(arcpy.GetParameterAsText(7))
LRY = int(arcpy.GetParameterAsText(8))
bgi = arcpy.GetParameterAsText(9)
fgi = arcpy.GetParameterAsText(10)
bgiItem = arcpy.GetParameterAsText(11)
fgiItem = arcpy.GetParameterAsText(12)

arcpy.AddMessage("bgi: " + bgi)
arcpy.AddMessage("fgi: " + fgi)
arcpy.AddMessage("bgiItem: " + bgiItem)
arcpy.AddMessage("fgiItem: " + fgiItem)

#Determine if user is selecting a background image from a URL (AGOL) or if they are uploading it
if bgiItem != "":
	background = Image.open(bgiItem)
	arcpy.AddMessage("Using user uploaded background...")
else:
	theBGIDict = json.loads(bgi)
	backgroundFile = cStringIO.StringIO(urllib.urlopen(theBGIDict["url"]).read())
	background = Image.open(backgroundFile)
	arcpy.AddMessage("Using user selected background...")

#Determine if user is selecting a foreground image from a URL (AGOL) or if they are uploading it
if fgiItem != "":
	foreground = Image.open(fgiItem)
	arcpy.AddMessage("Using user uploaded foreground...")
else:
	theFGIDict = json.loads(fgi)
	foregroundFile = cStringIO.StringIO(urllib.urlopen(theFGIDict["url"]).read())
	foreground = Image.open(foregroundFile)
	arcpy.AddMessage("Using user selected foreground...")

mergedImageName = "fgandbg.png"

background = background.resize((200,133), Image.ANTIALIAS)
background.paste(foreground, (0, 0), foreground)
background.save(os.path.join(outputPath, mergedImageName))

CHARS_PER_LINE = 0
numLines = 0

def getFontSize(fs):
    fits = False
    finalSize = fs
    while not fits:
        img = Image.open(os.path.join(outputPath, mergedImageName))
        MAX_W, MAX_H = img.size
        MAX_W = LRX - ULX
        draw = ImageDraw.Draw(img)
	#arcpy.AddMessage(os.path.join(r"c:\demos\thumbnailgenerator2",selectedFont))
	#arcpy.AddMessage(selectedFont)
        font = ImageFont.truetype(os.path.join(r"c:\demos\thumbnailgenerator2\fonts",selectedFont), finalSize)

        #determine CHARS_PER_LINE
        line = "W"
        w,h=draw.textsize(line, font=font)
        if (w<=MAX_W):
            moreRoom = True
            while moreRoom:
                 line = line + "W"
                 w,h=draw.textsize(line, font=font)
                 if (w>MAX_W):
                    CHARS_PER_LINE = (len(line) - 1)
                    break

        print CHARS_PER_LINE

        para=textwrap.wrap(astr,width=CHARS_PER_LINE)
        numLines = len(para) 

        totalHeight = (h+4)*numLines
        if (totalHeight <= (LRY - ULY)):
            fits = True
        else:
            finalSize = finalSize - 1
    return finalSize, totalHeight
            
FONT_SIZE,th = getFontSize(FONT_SIZE)

img = Image.open(os.path.join(outputPath, mergedImageName))
MAX_W, MAX_H = img.size
MAX_W = LRX - ULX
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(os.path.join(r"c:\demos\thumbnailgenerator2\fonts",selectedFont), FONT_SIZE)

#determine CHARS_PER_LINE
line = "W"
w,h=draw.textsize(line, font=font)
if (w<=MAX_W):
    moreRoom = True
    while moreRoom:
         line = line + "W"
         w,h=draw.textsize(line, font=font)
         if (w>MAX_W):
            CHARS_PER_LINE = (len(line) - 1)
            break

print CHARS_PER_LINE

para=textwrap.wrap(astr,width=CHARS_PER_LINE)
numLines = len(para)

current_h = ((LRY - ULY) - th)/2 + ULY
print th
print current_h

if (ALIGN == "Right"):
    for line in para:
        w,h=draw.textsize(line, font=font)
        draw.text((ULX, current_h), line.rjust(CHARS_PER_LINE), font=font, fill=TEXT_COLOR)
        current_h+=h
elif (ALIGN == "Center"):
    for line in para:
        w,h=draw.textsize(line, font=font)
        draw.text((((LRX-ULX-w)/2), current_h), line, font=font, fill=TEXT_COLOR)
        current_h+=h
else:
    for line in para:
        w,h=draw.textsize(line, font=font)
        draw.text((ULX, current_h), line, font=font, fill=TEXT_COLOR)
        current_h+=h
img.save(os.path.join(outputPath, "outputimage" + ".png"))
arcpy.SetParameterAsText(13, os.path.join(outputPath, "outputimage" + ".png"))
