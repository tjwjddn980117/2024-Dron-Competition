import sys
import cv2
#import os
import threading
import traceback
import time
#from PIL import Image
import numpy as np
import pickle

#from keras.preprocessing.image import load_img
try:
    import openvino
    import openvino as ov
    #from openvino.tools.mo import convert_model
    #from openvino.inference_engine import IENetwork, IEPlugin
    #from openvino import inference_engine as ie
except Exception as e:
    exception_type = type(e).__name__
    print("The following error happened while importing Python API module:\n[ {} ] {}".format(exception_type, e))
    sys.exit(1)
class ObjectClassifier():
    def __init__(self, device, getFrameFunc):
        self.getFrameFunc = getFrameFunc
        self.originFrame = None
        self.processedFrame = None
############### 모델이름 Please write mobilenet imageclassifcation xml and bin file############## 
        model_xml = './models/mobilenetv2_class8.xml'
        model_bin = './models/mobilenetv2_class8.bin'

        cpu_extension = None# '/opt/intel/openvino/inference_engine/lib/intel64/libcpu_extension_sse4.so'
############### 레이블이름 Please write label fiel ################################################ 
        with open('./models/mobilenetv2_class8.txt', 'rt',encoding='utf-8') as f:
            lines = f.readlines()
        self.labels = list(map(lambda x: x.replace('\n', ''), lines))

        core = ov.Core()
        model = core.read_model('./models/mobilenetv2_class8.xml')

        if len(model.inputs) != 1: print('Sample supports only single input topologies')
        if len(model.outputs) != 1: print('Sample supports only single output topologies')
        #net = IENetwork(model=model_xml, weights=model_bin)
        #assert len(net.inputs.keys()) == 1
        #assert len(net.outputs) == 1

        labels = []
        with open('./models/class8.pickle', 'rb') as f:
            labels = pickle.load(f)

        self.compiled_model = core.compile_model(model, 'CPU')
        img_height = 224

        result = []

        #print(device)
        #plugin = IEPlugin(device=device)
        #print(IEPlugin)
        #if cpu_extension and 'CPU' in device:
        #    plugin.add_cpu_extension(cpu_extension)

        #self.exec_net = plugin.load(network=net)
        #del net

        #self.input_blob = next(iter(net.inputs))
        #self.out_blob = next(iter(net.outputs))
        #print("Loading IR to the plugin...")
        #n, c, self.h, self.w = net.inputs[self.input_blob].shape #?? 겠다
        #print(n, c, self.h, self.w)

        self.sortedClassifiedList = []
        self.infer_time = 0
        self.inferFPS = 15

        processThread = threading.Thread(target=self.inferenceThread)
        processThread.daemon = True
        processThread.start()

    def pre_process_image(self, org_image, img_height=224):
        # Model input format
        #n, c, h, w = [1, 3, img_height, img_height]
        #processedImg = cv2.resize(image, (h, w), interpolation=cv2.INTER_AREA)

        # Normalize to keep data between 0 - 1
        #processedImg = (np.array(processedImg) - 0) / 255.0

        # Change data layout from HWC to CHW
        #processedImg = processedImg.transpose((2, 0, 1))
        #processedImg = processedImg.reshape((n, c, h, w))

        ###############################################################################################################
        image = cv2.resize(org_image, (img_height,img_height), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
        #img = cv2.resize(img, (224,224), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.

        # Add N dimension
        nchw_tensor = np.expand_dims(image, 0)

        # NHWC -> NCHW
        input_tensor = np.transpose(nchw_tensor, (0,1,2,3))#(0,3,1,2))

        return org_image, input_tensor

    def detect(self):
        image, input_tensor = self.pre_process_image(self.originFrame)

        infer_start = time.time()
        #res = self.exec_net.infer(inputs={self.input_blob: input_tensor})
        # --------------------------- Step 6. Create infer request and do inference synchronously -----------------------------
        results = self.compiled_model.infer_new_request({0:input_tensor})

        # --------------------------- Step 7. Process output ------------------------------------------------------------------
        predictions = next(iter(results.values()))
        output_node_name = next(iter(results.keys())) #

        # Change a shape of a numpy.ndarray with results to get another one with one dimension
        probs = predictions.reshape(-1)
        probs = probs[:-1]

        # Get an array of 8 class IDs in descending order of probability
        top_8 = np.argsort(probs)[-8:][::-1]
       
        self.infer_time = time.time() - infer_start

        #output_node_name = list(res.keys())[0]
        #res = res[output_node_name]

        # Predicted class index.
        #sortedIdx = np.argsort(res[0])[::-1]

        #index_max = max(range(len(res[0])), key=res[0].__getitem__)

        self.sortedClassifiedList.clear()
        #sortedList = sorted(range(len(res[0])), key=lambda i: res[0][i], reverse=True)

        for idx in top_8:
            self.sortedClassifiedList.append((idx, probs[idx]*100))
        #[self.labels[idx], 
        #print(self.sortedClassifiedList)

    def inferenceThread(self):
        while True:
            frame = self.getFrameFunc()
            if frame is not None:
                try:
                    self.originFrame = frame.copy()
                    self.detect()
                    time.sleep(1.0/self.inferFPS)

                except Exception as error:
                    print(error)
                    traceback.print_exc()
                    print("catch error")
    def getProcessedData(self):
        return self.infer_time, self.sortedClassifiedList
    def setInferFPS(self, newFPS):
        self.inferFPS = newFPS


if __name__ == "__main__":
    
    frame = None
    complied_model = None
    def getOriginFrame():
        return frame    

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ret, frame = capture.read()

    classifier = ObjectClassifier('CPU',getOriginFrame)
    while capture.isOpened():
        ret, frame = capture.read()
        data = classifier.getProcessedData()
