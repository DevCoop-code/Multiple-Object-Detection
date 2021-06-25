import cv2
import numpy as np

# Check the opencv version
print(cv2.__version__)

# What we need is 3 files using YOLO
# 1. Weight File: Trained Model
# 2. Cfg File: Configuration file, these file has setting of algorithm
# 3. Name File: Include Object Name Label

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg");
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Get an Image
img = cv2.imread("vehicles.png");
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Convert Blob, Blob is the specialized extract image characteristics and Resizing

# 3 Sizes that YOLO allows
# 320 x 320: Low Accurate but very speed, 609 x 609: High Accuate but low speed, 416 x 416: Middle
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False);
net.setInput(blob)
outs = net.forward(output_layers)

# Display a information on screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # Coordinate
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Remove the Noise
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Displaying
font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x,y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()