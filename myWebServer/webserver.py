
import sys
import cgi
import urlparse
import commands
import shlex,subprocess
import BaseHTTPServer

from pykondo import *
import cv

DEBUG = True
CMD_PLAY_MOTION = 1
CMD_READ_BATTERY = 0
CMD_SET_VIDEO = 2

class KondoCommand:
    """
    Kondo command
    """

    def Init(self):
        self.max_wait = 50 * 1000000
        self.ki = KondoInstance()
        ret = kondo_init(self.ki)
        print(self.ki.error)

    def ReadBatteryLevel(self):
        print("reading battery level")
        level=0
        ret = kondo_read_analog(self.ki,level, 0)
        if ret < 0:
            sys.exit(self.ki.error)
        return ret[1]

    def PlayMotion(self, motion_id):
        print ("Playing Kondo Motion %", motion_id)
        ret = kondo_play_motion(self.ki, motion_id, self.max_wait)
        if ret < 0:
            sys.exit(self.ki.error)

    def Close(self):
        ret = kondo_close(self.ki)
        if ret < 0:
            sys.exit(self.ki.error)

class KondoVision:
    """
    OpenCV vision
    """

    def Init(self):
        self.frame = 'none'
        self.videoCapture = 'none'
        self.cascade = 'none'
        self.storage = 'none'

        cv.NamedWindow("Ex", cv.CV_WINDOW_FULLSCREEN)
        self.videoCapture = cv.CreateCameraCapture(0)
        cv.SetCaptureProperty(self.videoCapture,cv.CV_CAP_PROP_FRAME_WIDTH,80)
        cv.SetCaptureProperty(self.videoCapture,cv.CV_CAP_PROP_FRAME_HEIGHT,60)
        cv.SetCaptureProperty(self.videoCapture,cv.CV_CAP_PROP_FPS,10)

        if( self.videoCapture == 'none' ):
            print("OpenCV error: Could not create cam capture")
            return

        self.cascade = cv.Load("./haarcascade_frontalface_alt.xml")
        self.storage = cv.CreateMemStorage( 0 )

        assert(self.cascade and self.storage and self.videoCapture)

        key = cv.WaitKey(10)
        while(( key != 'none') and (key != 'q')):
            self.frame = cv.QueryFrame(self.videoCapture)
 #           if( frame == 'none'):
 #               break
           # cvFlip(self.frame, self.frame, -1)
           # self.DetectFaces()
            cv.ShowImage("videoCapture", self.frame)
            key = cv.WaitKey(10)

        return

    def DetectFaces(self):
        faces = cv.HaarDetectObjects(self.frame, self.cascade, self.storage, 1.1, 3, cv.CV_HAAR_DO_CANNY_PRUNING, (100, 100))
        if faces.total > 0:
            for f in faces:
                cv.Rectangle(self.frame, cv.Point(f.x, f.y), cv.Point(f.x+f.width, f.y+f.height), cv.CV_RGB(255,0,0), 1, 4, 0)
        return

    def Close(self):
        cv.DestroyAllWindows()
        cv.ReleaseImage(videoImage)
        cv.ReleaseCapture(videoCapture)
        return

class VideoFeedback:
    """
    Web Video Feedback / streaming based on mjpeg streamer
    """

    def Init(self, dev, resolution, fps):
        self.url = None
        command_line = '/usr/bin/mjpg_streamer  -i "input_uvc.so -y -d ' + dev + ' --resolution ' + resolution + ' --fps "' + fps + '  -o "output_http.so -w ./"'
        args = shlex.split(command_line)
        print (args)
        res = subprocess.Popen(args)
        print(res)
        return

    def Close(self):
        return


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    HTTP handler performing custom GET and POST management
    """

    cgi_directories = ["./"]

    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.kc = None
        self.videoStream = None

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        f = open('.' + parsed_path.geturl())
        self.send_response(200)

#        if parsed_path.endswith('.html'):
        self.send_header('Content-type', 'text/html')
#        elif parsed_path.endswith('.js'):
#            self.send_header('Content-type', 'text/javascript')
#        elif parsed_path.endswith('.css'):
#            self.send_header('Content-type', 'text/css')

        self.end_headers()
        self.wfile.write(f.read())
        f.close()

        return

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()

        cmd = int(form['command'].value)
        arg = int(form['arg'].value)

        # Send Battery Level
        if cmd == CMD_READ_BATTERY:
            self.wfile.write('Battery: %.2f V' % (self.kc.ReadBatteryLevel() / 42.07))
        # Play Kondo Motion
        elif cmd == CMD_PLAY_MOTION:
            self.kc.PlayMotion(arg)
        # Send server IP address
        elif cmd == CMD_SET_VIDEO:
            ip = commands.getoutput("ifconfig").split("\n")[1].split()[1][5:]
            self.wfile.write('http://' + ip + ':8080/?action=stream')
        return

class myHTTPServer(BaseHTTPServer.HTTPServer):
    """
    Custom HTTPServer
    """

    def __init__(self, server_address, RequestHandlerClass, kc, videoStream):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.RequestHandlerClass.kc = kc
        self.RequestHandlerClass.videoStream = videoStream

def main():
    try:
        # Start Kondo vision
        #kv = KondoVision()
        #kv.Init()

        # Start Kondo command
        kc = KondoCommand()
        kc.Init()

        # Start Web video stream
        videoStream = 'none'
        videoStream = VideoFeedback()
        videoStream.Init('/dev/video0', '160x120', '10')

        # Start Web Server
        server = myHTTPServer(('', 8000), MyHandler, kc, videoStream)
        print 'Httpserver started, press <CTRL+C> to quit'
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
        #kv.Close()
        videoStream.Close()

if __name__ == '__main__':
    main()

