from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from threading import Event
from time import sleep
import cv2
import json
import base64
from threading import Lock
from ultralytics import YOLO

#cap=cv2.VideoCapture(0)  ##when removing debug=True or using gevent or eventlet uncomment this line and comment the cap=cv2.VideoCapture(0) in gen(json)
app = Flask(__name__)
app.config['SECRET_KEY'] = '78581099#lkjh'
socketio = SocketIO(app)
#socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
thread_event = Event()


@app.route('/')
def index():
	return render_template('index.html')

def background_thread(event):

	cap=cv2.VideoCapture(1)
	#cap=cv2.VideoCapture(r"C:\Users\Admin\PythonLession\pic\carplate8.mp4")
	global thread

	try:
		while(cap.isOpened() and event.is_set()):
			ret,img=cap.read()
			if ret:
				#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

				model = YOLO(r"C:\Users\Admin\PythonLession\YoloModel\yolov8n.pt")
				result = model.predict(img, device=[0])

				img = result[0].plot()

				img = cv2.resize(img,(600,480))
				cv2.rectangle(img,(50,30),(300,250),(255,0,0),2)


				frame = cv2.imencode('.jpg', img)[1].tobytes()
				frame= base64.encodebytes(frame).decode("utf-8")
				message(frame)
				socketio.sleep(0.0)
			else:
				break
	finally:
		event.clear()
		thread = None

@socketio.on('send_message')
def message(json, methods=['GET','POST']):
	#print("Recieved message")
	socketio.emit('image', json )


@socketio.on('connect')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')


@socketio.on("start")
def start():
    global thread
    with thread_lock:
        if thread is None:
            thread_event.set()
            thread = socketio.start_background_task(background_thread, thread_event)

@socketio.on("stop")
def stop():
	global thread
	thread_event.clear()
	with thread_lock:
		if thread is not None:
			thread.join()
			thread = None


if __name__== "__main__":
	#socketio.run(app,debug=True, host='127.0.0.1', port=5000)
	socketio.run(app, port=8000, debug=True,  host='0.0.0.0')
