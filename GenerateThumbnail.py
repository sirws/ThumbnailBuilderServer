from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import os
import json
import urllib, cStringIO

fontsPath = r'C:\Users\scot5141\Documents\GitHub\ThumbnailBuilderServer\fonts'
outputPath = arcpy.env.scratchFolder
CHARS_PER_LINE = 0
numLines = 0
PIXELS_BETWEEN_LINES = 3

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
fgA = foreground.copy().convert('RGBA')
fgA = fgA.resize((200,133), Image.ANTIALIAS)
background.paste(fgA, (0, 0), fgA)
background.save(os.path.join(outputPath, mergedImageName))

fits = False #assume the text doesn't fit to start
finalSize = FONT_SIZE #start with user specified fontsize and test for fit.  Shrink as necessary

while not fits:
    words = astr.split()
    img = Image.open(os.path.join(outputPath, mergedImageName))
    MAX_W, MAX_H = img.size
    MAX_W = LRX - ULX
    MAX_H = LRY - ULY
    draw1 = ImageDraw.Draw(img)
    font1 = ImageFont.truetype(os.path.join(fontsPath,selectedFont), finalSize)
    w,h=draw1.textsize(astr, font=font1)
    arcpy.AddMessage("Width of whole line: " + str(w) + ".  Width of box: " + str(MAX_W))
    arcpy.AddMessage("Line height: " + str(h))
    
    MAX_LINES = MAX_H // (h+PIXELS_BETWEEN_LINES)
    arcpy.AddMessage("Based on this font and fontsize " + str(finalSize) + ", there can be " + str(MAX_LINES) + " lines in the box specified.")
    
    sentence = []
    lines = []
    sentenceStr = ""
    sentenceTest = ""
    for idx,word in enumerate(words):
        w,h=draw1.textsize(astr, font=font1)
        sentenceTest = " ".join(sentence)
        sentence.append(word)
        sentenceStr = " ".join(sentence)
        w,h=draw1.textsize(sentenceStr, font=font1)
        arcpy.AddMessage("Width of text: '" + sentenceStr + "' is "  + str(w) + " pixels.  Width of box: " + str(MAX_W))
        if (w > MAX_W):
            lines.append(sentenceTest)
            sentence = []
            sentence.append(word)
            arcpy.AddMessage("LINE CALCULATED: '" + sentenceTest + "' and new line started")
            arcpy.AddMessage("idx: '" + str(idx) + ", " + str(len(words)-1))
            if (idx == (len(words)-1)):
                sentenceStr = " ".join(sentence)
                lines.append(sentenceStr)
                arcpy.AddMessage("FINAL LINE CALCULATED: '" + sentenceStr + "'")
        elif (idx == (len(words)-1)):
            lines.append(sentenceStr)
            arcpy.AddMessage("FINAL LINE CALCULATED: '" + sentenceStr + "'")

    if (MAX_LINES >= len(lines)):
        fits = True
    else:
        fits = False
        finalSize-=1
        FONT_SIZE=finalSize

totalHeight = (len(lines) * (h+PIXELS_BETWEEN_LINES))-PIXELS_BETWEEN_LINES

img = Image.open(os.path.join(outputPath, mergedImageName))
MAX_W, MAX_H = img.size
MAX_W = LRX - ULX
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(os.path.join(fontsPath,selectedFont), FONT_SIZE)

numLines = len(lines)

current_h = ((LRY - ULY) - totalHeight)/2 + ULY
arcpy.AddMessage("current_h: " + str(current_h))

if (ALIGN == "Right"):
    for line in lines:
        w,h=draw.textsize(line, font=font)
        draw.text((ULX + (MAX_W - w), current_h), line, font=font, fill=TEXT_COLOR)
	arcpy.AddMessage("WRITING LINE TO IMAGE: '" + line + "' at insertion x location: " + str(current_h))
        current_h+=h+PIXELS_BETWEEN_LINES
elif (ALIGN == "Center"):
    for line in lines:
        w,h=draw.textsize(line, font=font)
        draw.text((((LRX-ULX-w)/2), current_h), line, font=font, fill=TEXT_COLOR)
	arcpy.AddMessage("WRITING LINE TO IMAGE: '" + line + "' at insertion x location: " + str(current_h))
        current_h+=h+PIXELS_BETWEEN_LINES
else:
    for line in lines:
        w,h=draw.textsize(line, font=font)
        draw.text((ULX, current_h), line, font=font, fill=TEXT_COLOR)
	arcpy.AddMessage("WRITING LINE TO IMAGE: '" + line + "' at insertion x location: " + str(current_h))
        current_h+=h+PIXELS_BETWEEN_LINES
img.save(os.path.join(outputPath, "outputimage" + ".png"))
arcpy.SetParameterAsText(13, os.path.join(outputPath, "outputimage" + ".png"))
