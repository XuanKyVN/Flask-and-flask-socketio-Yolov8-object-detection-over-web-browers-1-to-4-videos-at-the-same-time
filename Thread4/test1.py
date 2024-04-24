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

#cap=cv2.VideoCapture(0)  ##when removing debug=True or using gevent or eventlet uncomment this line and comment the cap=cv2.VideoCapture(0) in gen(json)
app = Flask(__name__)
app.config['SECRET_KEY'] = '78581099#lkjh'
socketio = SocketIO(app)
#socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()
thread_event = Event()

thread1 = None
thread_lock1 = Lock()
thread_event1 = Event()

thread2 = None
thread_lock2 = Lock()
thread_event2 = Event()

thread3 = None
thread_lock3 = Lock()
thread_event3 = Event()



@app.route('/')
def index():
	return render_template('index.html')

def background_thread(event):
	#cap=cv2.VideoCapture(1)
	cap=cv2.VideoCapture(r"C:\Users\Admin\PythonLession\pic\carplate8.mp4")
	global thread

	try:
		while(cap.isOpened() and event.is_set()):
			ret,img=cap.read()
			if ret:
				#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
				img = cv2.resize(img,(600,480))
				cv2.rectangle(img,(50,30),(300,250),(255,0,0),2)


				frame = cv2.imencode('.jpg', img)[1].tobytes()
				frame= base64.encodebytes(frame).decode("utf-8")
				message(frame)
				socketio.sleep(0.01)
			else:
				break
	finally:
		event.clear()
		thread = None


def background_thread1(event):

	#cap=cv2.VideoCapture(1)
	cap=cv2.VideoCapture(r"C:\Users\Admin\PythonLession\pic\people1.mp4")
	global thread1

	try:
		while(cap.isOpened() and event.is_set()):
			ret,img=cap.read()
			if ret:
				#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
				img = cv2.resize(img,(600,480))
				cv2.rectangle(img,(50,30),(300,250),(255,0,0),2)


				frame = cv2.imencode('.jpg', img)[1].tobytes()
				frame= base64.encodebytes(frame).decode("utf-8")
				message2(frame)
				socketio.sleep(0.01)
			else:
				break
	finally:
		event.clear()
		thread1 = None

#-----------------------------------------------------
def background_thread2(event):
	#cap=cv2.VideoCapture(1)
	cap=cv2.VideoCapture(r"C:\Users\Admin\PythonLession\pic\road.mp4")
	global thread2

	try:
		while(cap.isOpened() and event.is_set()):
			ret,img=cap.read()
			if ret:
				#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
				img = cv2.resize(img,(600,480))
				cv2.rectangle(img,(50,30),(300,250),(255,0,0),2)


				frame = cv2.imencode('.jpg', img)[1].tobytes()
				frame= base64.encodebytes(frame).decode("utf-8")
				message3(frame)
				socketio.sleep(0.01)
			else:
				break
	finally:
		event.clear()
		thread2 = None


def background_thread3(event):
	#cap=cv2.VideoCapture(1)
	cap=cv2.VideoCapture(r"C:\Users\Admin\PythonLession\pic\traffic-4ways.mp4")
	global thread3

	try:
		while(cap.isOpened() and event.is_set()):
			ret,img=cap.read()
			if ret:
				#img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
				img = cv2.resize(img,(600,480))
				cv2.rectangle(img,(50,30),(300,250),(255,0,0),2)


				frame = cv2.imencode('.jpg', img)[1].tobytes()
				frame= base64.encodebytes(frame).decode("utf-8")
				message4(frame)
				socketio.sleep(0.01)
			else:
				break
	finally:
		event.clear()
		thread3 = None


@socketio.on('send_message')
def message(json, methods=['GET','POST']):
	#print("Recieved message")
	socketio.emit('image', json )
@socketio.on('send_message2')
def message2(json, methods=['GET','POST']):
	#print("Recieved message")
	socketio.emit('image2', json )

#------------------------------
@socketio.on('send_message3')
def message3(json, methods=['GET','POST']):
	#print("Recieved message")
	socketio.emit('image3', json )
@socketio.on('send_message4')
def message4(json, methods=['GET','POST']):
	#print("Recieved message")
	socketio.emit('image4', json )



@socketio.on('connect')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')

#---------------------------------
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



@socketio.on("start1")
def start1():
    global thread1
    with thread_lock1:
        if thread1 is None:
            thread_event1.set()
            thread1 = socketio.start_background_task(background_thread1, thread_event1)


@socketio.on("stop1")
def stop1():
	global thread1
	thread_event1.clear()
	with thread_lock1:
		if thread1 is not None:
			thread1.join()
			thread1 = None


#---------------------------------
@socketio.on("start2")
def start2():
    global thread2
    with thread_lock2:
        if thread2 is None:
            thread_event2.set()
            thread2 = socketio.start_background_task(background_thread2, thread_event2)


@socketio.on("stop2")
def stop():
	global thread2
	thread_event2.clear()
	with thread_lock2:
		if thread2 is not None:
			thread2.join()
			thread2 = None



@socketio.on("start3")
def start3():
    global thread3
    with thread_lock3:
        if thread3 is None:
            thread_event3.set()
            thread3 = socketio.start_background_task(background_thread3, thread_event3)


@socketio.on("stop3")
def stop3():
	global thread3
	thread_event3.clear()
	with thread_lock3:
		if thread3 is not None:
			thread3.join()
			thread3 = None




if __name__== "__main__":
	#socketio.run(app,debug=True, host='127.0.0.1', port=5000)
	socketio.run(app, port=8000, debug=True,  host='0.0.0.0')
