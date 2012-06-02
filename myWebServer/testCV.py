__author__ = 'amuthelet'

import cv
import time

cv.NamedWindow("cam", 1)
capture = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,200)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,150)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FPS,20)
while True:
    img = cv.QueryFrame(capture)
    if (not img):
        break
    cv.ShowImage("cam", img)
    if cv.WaitKey(10) == 27:
        break;