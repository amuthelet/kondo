'''
Created on 22 janv. 2011

@author: arnaud
'''


import cv
import sys
from PyQt4 import QtCore, QtGui, uic
from pykondo import *

from opencv.cv import *
from opencv.highgui import *

#def flatten():
#    cvCvtColor(img, img, CV_RGB2HSV);
#    for( int y=0; y<img->height; y++ ) {
#        uchar* ptr = (uchar*) (
#            img->imageData + y * img->widthStep
#        );
#        for( int x=0; x<img->width; x++ ) {
#            ptr[3*x+2] = 255; // maxes the value,
#            // use +1 for saturation, +0 for hue
#        }
#    }

#    cvCvtColor(img, img, CV_HSV2RGB);

        
# 77,28,60
# 83,44,70     

#    ki = KondoInstance()
#    ret = kondo_init(ki)
# kondo_set_servo_pos(ki,servo_id,servo_value)
   
        
class qt_win(QtGui.QWidget):
    capture = 0
    contrast = 0
    brightness = 0
    color_picker_min = 0
    color_picker_max = 0
    color_min = (0,0,0)
    color_max = (0,0,0)
    def __init__(self, cv_capture, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0,600,60,150)

        self.capture = cv_capture

        self.contrast = QtGui.QSlider(self)
        self.contrast.setRange(0,128)
        self.contrast.setGeometry(0,0,20,100)
        self.contrast.show()
        self.contrast.connect(self.contrast, QtCore.SIGNAL('valueChanged(int)'), self, QtCore.SLOT('udpateContrast(int)'))
        
        self.brightness = QtGui.QSlider(self)
        self.brightness.setRange(0,128)
        self.brightness.setGeometry(30,0,20,100)
        self.brightness.show()
        self.brightness.connect(self.brightness, QtCore.SIGNAL('valueChanged(int)'), self, QtCore.SLOT('udpateBrightness(int)'))
 
        self.color_picker_min = QtGui.QColorDialog(self)
        self.color_picker_min.setParent(self)
        self.color_picker_min.show()
        self.color_picker_min.setWindowTitle("Min")
        self.color_picker_min.setGeometry(300,600,10,10)
        self.connect(self.color_picker_min, QtCore.SIGNAL('currentColorChanged(QColor)'), self, QtCore.SLOT('colorMinSelected(QColor)'))
        
        self.color_picker_max = QtGui.QColorDialog(self)
        self.color_picker_max.setParent(self)
        self.color_picker_max.show()
        self.color_picker_max.setWindowTitle("Max")
        self.color_picker_max.setGeometry(800,600,10,10)
        self.connect(self.color_picker_max, QtCore.SIGNAL('currentColorChanged(QColor)'), self, QtCore.SLOT('colorMaxSelected(QColor)'))
    
    @QtCore.pyqtSlot(int)    
    def udpateContrast(self, val):
        cvSetCaptureProperty(self.capture, CV_CAP_PROP_CONTRAST, val/128.0)
 
    @QtCore.pyqtSlot(int)    
    def udpateBrightness(self, val):
        cvSetCaptureProperty(self.capture, CV_CAP_PROP_BRIGHTNESS, val/128.0)
 
    @QtCore.pyqtSlot("QColor")    
    def colorMinSelected(self, color):
        self.color_min = (color.blue(), color.green(), color.red())

    @QtCore.pyqtSlot("QColor")    
    def colorMaxSelected(self, color):
        self.color_max = (color.blue(), color.green(), color.red())
        
def on_mouse_cb(event, x, y, flags, vars):
    if event == CV_EVENT_LBUTTONDOWN:
        frame = cvQueryFrame(capture)
        height = frame.height
        width = frame.width
        color = cvGet2D(frame, y, x)
        offset = 30
        qt_gui.color_picker_max.setCurrentColor(QtGui.QColor(color[2]+offset,color[1]+offset,color[0]+offset))
        qt_gui.color_picker_min.setCurrentColor(QtGui.QColor(color[2],color[1],color[0]))
        print x,y,color,height,width
       
win_width = 640
win_height = 480
         
cvNamedWindow("CamView", 1)
cvMoveWindow("CamView", 0, 0)
cvNamedWindow("Contours", 1)
cvMoveWindow("Contours", win_width, 0)

# Connect to the camera
capture = cvCreateCameraCapture(0)
cvSetCaptureProperty(capture, CV_CAP_PROP_BRIGHTNESS, 0.8) #10
cvSetCaptureProperty(capture, CV_CAP_PROP_CONTRAST, 0.1) #20
cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, win_width)
cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, win_height)

qt_app = QtGui.QApplication(sys.argv)

frame = 0
qt_gui = qt_win(capture)
qt_gui.show()

cvSetMouseCallback("CamView", on_mouse_cb, 0)

ki = KondoInstance()
ret = kondo_init(ki)


    
while 1:
    frame = cvQueryFrame(capture)
    cvShowImage("CamView", frame)
    
    color_mask = cvCreateImage(cvGetSize(frame), 8, 1)
    cvShowImage("Contours", color_mask)
    
    qt_gui.color_picker_min
    cvInRangeS(frame, cvScalar(*qt_gui.color_min), cvScalar(*qt_gui.color_max), color_mask)
    
    storage = cvCreateMemStorage(0)
    c_count, contours = cvFindContours(color_mask, storage)
    
    if c_count != 0:
        for contour in contours.hrange():
            # Do some filtering
            # Get the size of the contour
            size = abs(cvContourArea(contour))
            # Is convex
            is_convex = cvCheckContourConvexity(contour)
        
            # Find the bounding-box of the contour
            bbox = cvBoundingRect( contour, 0 )
        
            # Calculate the x and y coordinate of center
            x, y = bbox.x+bbox.width*0.5, bbox.y+bbox.height*0.5
            point = cvPoint(int(x),int(y))
            
            if size > 90:
                cvCircle(color_mask, point, 10, cvScalar(200,200,10))

    kondo_set_servo_pos(ki,0,7650)
    print("GO")
    if cvWaitKey(10) == 27:
        break

sys.exit(qt_app.exec_())
