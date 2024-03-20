import cv2
import cvzone
import time
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands = 1)

timer = 0
stateResults = False
startGame = False
scores = [0,0] 

wonText = "You Won!!"
loseText = "AI Won!"
drawText = "Draw"

while True:
  imgBG = cv2.imread("Resources/BG.png")
  success, img = cap.read()
  img = cv2.flip(img,1)

  imgScaled = cv2.resize(img,(0,0), None,0.875,0.875)
  imgScaled = imgScaled[:,80:480]
#Find Hand
  hands, img = detector.findHands(imgScaled)
  imgBG[233:653,796:1196] = imgScaled 

  wonFlag = False
  loseFlag = False

  if startGame: 
    if stateResults is False:
      timer = time.time() - initialTime
      cv2.putText(imgBG, str(int(timer)),(605,435), cv2.FONT_HERSHEY_PLAIN,6,(255,0,255),4)
      if timer>3:
        stateResults = True
        timer = 0
        if hands:
          hand = hands[0]
          fingers = detector.fingersUp(hand)
          if fingers == [0,0,0,0,0]:
            playerMove = 1
          if fingers == [1,1,1,1,1]:
            playerMove = 2
          if fingers == [0,1,1,0,0]:
            playerMove = 3

          randNum = random.randint(1,3)
          imgAI = cv2.imread(f'Resources/{randNum}.png',cv2.IMREAD_UNCHANGED)
          imgBG = cvzone.overlayPNG(imgBG,imgAI,(149,310))

          #Player
          if(playerMove == 1 and randNum == 3) or \
            (playerMove == 2 and randNum == 1) or \
            (playerMove == 3 and randNum == 2):
            scores[1] += 1
            wonFlag = True
            

          #AI 
          if(playerMove == 3 and randNum == 1) or \
            (playerMove == 1 and randNum == 2) or \
            (playerMove == 2 and randNum == 3):
            scores[0] += 1
            loseFlag = True 
            
          print(playerMove)

  if stateResults:
    imgBG = cvzone.overlayPNG(imgBG,imgAI,(149,310))
    if wonFlag == True:
      cv2.putText(imgBG, wonText,(605,215), cv2.FONT_HERSHEY_PLAIN,6,(0,190,10),4)
    elif loseFlag == True:
      cv2.putText(imgBG, loseText,(605,215), cv2.FONT_HERSHEY_PLAIN,6,(190,0,10),4)
    else:
      cv2.putText(imgBG, drawText,(605,435), cv2.FONT_HERSHEY_PLAIN,6,(190,0,10),4)

  cv2.putText(imgBG, str(int(scores[0])),(410,215), cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
  cv2.putText(imgBG, str(int(scores[1])),(1112,215), cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)



  cv2.imshow("Image", imgBG)

  key = cv2.waitKey(1)
  if key == ord('s'):
    startGame = True
    initialTime = time.time()
    stateResults = False
    wonFlag = False
    loseFlag = False
  if key == ord('q'):
    break
