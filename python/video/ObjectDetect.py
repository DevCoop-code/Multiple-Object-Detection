import numpy as np
import imutils
import time
import cv2
import os

# YOLO 모델이 훈련한 라벨 클래스들을 가져옴
labelsPath = "drive/MyDrive/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

# 각 클래스 라벨에 대한 색상 값을 초기화
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# YOLO weight 파일과 config 파일 경로
weightsPath = "drive/MyDrive/yolov3.weights"
configPath = "drive/MyDrive/yolov3.cfg"

# config파일과 weight 파일을 이용하여 yolo inference network 모델을 로드
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# 전체 darknet layer에서 13x13, 26x26, 52x52 grid에서 detect된 output layer만 필터링
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 입력될 video file을 읽어온다
vs = cv2.VideoCapture("drive/MyDrive/yolo_vehicle/vehicle_test.mp4")
writer = None
(W, H) = (None, None)

# try to determine the total number of frames in the video file
try:
  prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() else cv2.CAP_PROP_FRAME_COUNT
  total = int(vs.get(prop))
  print("[INFO] {} total frames in video".format(total))

# an error occured while trying to determine the total
# number of frames in the video file
except:
  print("[INFO] could not determine of frames in video")
  print("[INFO] no approx. completion time can be provided")
  total = -1

# 비디오 상 전체 자동차 카운트 변수
counting = 0;

# detecting된 객체들 중 가장 작은 x, y 좌표
smallYCoord = -1;
smallXCoord = -1;

# detecting된 객체들 중 가장 큰 x, y 좌표
bigYCoord = -1;
bigXCoord = -1;

# 한 프레임당 detecting 된 객체의 갯수
detectionPerFrame = 0;

# loop over frames from the video file stream
while True:
  # Read the Next frame from the file
  (grabbed, frame) = vs.read()

  # if the frame was not grabbed, Then we have reached the end
  # of the stream
  if not grabbed:
    break

  # if the frame dimensions are empty, grab them
  if W is None or H is None:
    (H, W) = frame.shape[:2]

  # Yolov3 416은 416x416 input을 받음. 원본 이미지 배열을 사이즈 416x416으로 변환
  # blobFromImage를 사용하여 CNN에 넣어야 할 이미지 전처리를 해야함
  blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
  net.setInput(blob)
  start = time.time()
  layerOutputs = net.forward(ln)
  end = time.time()

  # initialize our lists of detected bounding boxes, confidences, and class IDs respectively
  boxes = []
  confidences = []
  classIDs = []

  detectionPerFrame = 0;
  lastDetectionPerFrame = 0;

  # loop over each of the layer outputs
  for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
      # extract the class ID and confidence (i.e., probability)
      # of the current object detection
      scores = detection[5:]
      classID = np.argmax(scores)
      confidence = scores[classID]
      
      # filter out weak predictions by ensuring the detected
      # probability is greater than the minimum probability
      if confidence > 0.5:
        detectionPerFrame += 1

        # scale the bounding box coordinates back relative to
        # the size of the image, keeping in mind that YOLO
        # actually returns the center (x, y)-coordinates of
        # the bounding box followed by the boxes width & height
        box = detection[0:4] * np.array([W, H, W, H])
        (centerX, centerY, width, height) = box.astype("int")

        # use the center (x, y)-coordinates to derive the top
        # and the left corner of the bounding box
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))

        # classID 2가 자동차로 인지한 객체로 자동차로 인지한 것만 카운트 한다
        if classID == 2:
          if smallYCoord == -1:
            bigYCoord = y
            bigXCoord = x

            smallYCoord = y
            smallXCoord = x
          else:
            if smallYCoord >= y:
              if smallYCoord == y:
                if detectionPerFrame != lastDetectionPerFrame:
                  print("Count the vehicle")
                  counting+=1
              else:
                print("Count the vehicle")
                smallYCoord = y
                counting+=1

        # Update our list of bounding box coordinates, confidences, and class IDs
        boxes.append([x, y, int(width), int(height)])
        confidences.append(float(confidence))
        classIDs.append(classID)
        print("class ID {} {:.4f}, {:.4f}".format(classID, x, y))

  print("detection Per Frame {}".format(detectionPerFrame))
  lastDetectionPerFrame = detectionPerFrame

  # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
  idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

  # Ensure at least one detection exists
  if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
      # extract the bounding box coordinates
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])

      # draw a bounding box rectangle and label on the frame
      color = [int(c) for c in COLORS[classIDs[i]]]
      cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
      text = "{}: {:.4f} {:.4f}, {:.4f}".format(LABELS[classIDs[i]], confidences[i], x, y)
      cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

  # check if the video writer is None
  if writer is None:
    # initialize our video writer
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter("drive/MyDrive/yolo_vehicle/carCounting.avi", fourcc, 30, (frame.shape[1], frame.shape[0]), True)

    # some information on processing single frame
    if total > 0:
      elap = (end - start)
      
  # write the output frame to disk
  writer.write(frame)

# release the file pointers
print("[INFO] cleaning up...")
print("Count : {}".format(counting))
writer.release()
vs.release()