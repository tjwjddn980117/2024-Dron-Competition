# ver 2019.07.16 20:30
# latest update : [Time out]

import socket
import threading
import traceback
import time
import cv2

class Tello():
    def __init__(self, loggingFunc, stateReceiveFunc):
        self.stateReceiveFunc = stateReceiveFunc #GUI쪽에 Tello의 state를 업데이트하라는 함수
        self.loggingFunc = loggingFunc #GUI쪽에서 logging을 위한 함수
        # 컨트롤러프로그램에서 Tello로 명령을 내리기위해 바인딩할  ip와 port, 소켓
        self.local_main_ip = '192.168.10.2'
        self.local_main_port = 8889
        self.socket = None
        # Tello로부터 state값을 받기위한 ip와 port, 소켓
        self.local_state_ip = "0.0.0.0"
        self.local_state_port = 8890
        self.socket_state = None
        # Tello와 직접연결했을 때 Tello의 고유주소와 포트
        self.tello_address = ('192.168.10.1', 8889)
        # Tello로부터 영상스트리밍을 받기위한 ip,port,opencv의 VideoCapture
        self.videoInput = 'udp://0.0.0.0:11111' #Tello Cam
        self.cap = None
        self.binitialized = False
        # Tello에게 지속적으로 ‘command’명령을 내려주는 스레드를 멈추기위한 플래그
        self.DoNotLandThreadStopFlag = False

    def send_command(self, command):
        if self.socket is None:
            self.loggingFunc('Not connected')
            return False
        else:
            try:
                self.socket.sendto(command.encode('utf-8'), self.tello_address)
                self.loggingFunc('sending command: %s to %s' % (command, self.tello_address[0]))
                return True
            except Exception as error:
                traceback.print_exc()
                print("catch error")


    def receive_process(self):
        while True:
            if self.socket is not None:
                try:
                    response, ip = self.socket.recvfrom(1024)
                    self.response = response.decode('utf-8')
                    self.loggingFunc('응답 : %s' % self.response)
                except Exception as exc:
                    traceback.print_exc()
                    print("catch error")

    def receive_state_process(self):
        while True:
            if self.socket_state is not None:
                try:
                    response, ip = self.socket_state.recvfrom(2048)
                    stateDict = self.stateReceiveFunc(response)
                except socket.error as exc:
                    print("Caught exception socket.error : %s" % exc)
                    return

    def readFrame(self):
        if self.cap is None:
            return None
        else:
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                return None

    def tryConnect(self):
        try:
            if self.videoInput == 'udp://0.0.0.0:11111':
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                self.socket.bind((self.local_main_ip, self.local_main_port))
                self.loggingFunc("Main socket binding ip : " + self.local_main_ip + ":" + self.local_main_port.__str__())
                print(("Main socket binding ip : " + self.local_main_ip + ":" + self.local_main_port.__str__()))
                self.receive_thread = threading.Thread(target=self.receive_process)
                self.receive_thread.daemon = True
                self.receive_thread.start()

                self.socket_state = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socket_state.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                self.socket_state.bind((self.local_state_ip, self.local_state_port))
                self.loggingFunc("State socket binding ip : " + self.local_state_ip + ":" + self.local_state_port.__str__())
                print("State socket binding ip : " + self.local_state_ip + ":" + self.local_state_port.__str__())
                self.receive_state_thread = threading.Thread(target=self.receive_state_process)
                self.receive_state_thread.daemon = True
                self.receive_state_thread.start()

                self.send_command("command")
                self.send_command("streamon")
                self.send_command("battery?")

                self.doNotLand = threading.Thread(target=self.DoNotLand)
                self.doNotLand.daemon = True
                self.doNotLand.start()

            self.binitialized = False
            th = threading.Thread(target=self.initVideoCapture)
            th.daemon = True
            th.start()
            th2 = threading.Thread(target=self.videoCaptureCheck)
            th2.daemon = True
            th2.start()

            return True
        except Exception as error:
            traceback.print_exc()
            self.DoNotLandThreadStopFlag = True
            self.socket = None
            self.socket_state = None
            self.cap = None
            self.loggingFunc(error.__str__())
            print("catch error")
            return False

    def disconnect(self):
        if self.videoInput == 'udp://0.0.0.0:11111':
            self.DoNotLandThreadStopFlag = True
            if self.socket is not None:
                self.send_command('streamoff')
                time.sleep(0.1)
                self.socket.close()
            self.socket = None
            if self.socket_state is not None:
                self.socket_state.close()
            self.socket_state = None
        if self.cap is not None:
            self.cap.release()
        self.cap = None

    #Tello 펌웨어가 업데이트되면서 15초동안 아무 command도 들어오지않으면 자동으로 착륙해버리기 때문에 이 함수를 쓰레드로 돌려야한다.
    def DoNotLand(self):
        self.DoNotLandThreadStopFlag = False
        while True:
            if self.DoNotLandThreadStopFlag:
                self.DoNotLandThreadStopFlag = False
                self.loggingFunc("자동착륙방지시스템 종료")
                break
            if not self.send_command('command'):
                self.loggingFunc("드론과 연결이 끊어진 것 같습니다. 자동착륙방지시스템을 종료합니다.")
                break
            time.sleep(10)
    def initVideoCapture(self):
        self.loggingFunc('initVideoCapturing...')
        self.cap = cv2.VideoCapture(self.videoInput)
        self.binitialized = True
    def videoCaptureCheck(self):
        initStartTime = time.time()
        while not self.binitialized:
            dt = time.time() - initStartTime
            if dt >= 10.0:
                self.loggingFunc("[Timeout] 영상스트리밍 수신을 실패했습니다. - 시간초과")
                break
