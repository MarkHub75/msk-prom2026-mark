
### conf=0.25, iou=0.45 (cell: matched/n_ref, +extra detections, min IoU of matched pairs, max |dconf|, max box-corner deviation)

| model | image | PT predict (rect=True default) vs ONNX predict | PT predict rect=False vs ONNX predict | examples/YOLOv8-ONNXRuntime flow | examples/cpp flow (top-left, zero pad, batched NMS) | examples/YOLOv8-OpenCV-ONNX-Python flow |
|---|---|---|---|---|---|---|
| yolov8n | bus | 5/5, +1, IoUmin 0.8935, dconf 0.1752, dbox 18.94px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9724, dconf 0.0, dbox 1.41px | 5/5, +1, IoUmin 0.899, dconf 0.1752, dbox 19.78px | 4/5, +2, IoUmin 0.891, dconf 0.1752, dbox 5.24px |
| yolov8n | zidane | 3/3, +0, IoUmin 0.9318, dconf 0.0134, dbox 5.55px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9675, dconf 0.0, dbox 1.92px | 3/3, +0, IoUmin 0.9274, dconf 0.0759, dbox 8.23px | 2/3, +1, IoUmin 0.9731, dconf 0.0323, dbox 6.91px |
| yolo11n | bus | 5/5, +0, IoUmin 0.9394, dconf 0.2226, dbox 8.09px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9859, dconf 0.0, dbox 1.54px | 5/5, +0, IoUmin 0.953, dconf 0.2299, dbox 7.08px | 4/5, +1, IoUmin 0.9383, dconf 0.2299, dbox 5.84px |
| yolo11n | zidane | 3/3, +0, IoUmin 0.9756, dconf 0.0319, dbox 9.57px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9929, dconf 0.0, dbox 1.41px | 3/3, +0, IoUmin 0.9288, dconf 0.0421, dbox 8.16px | 2/3, +1, IoUmin 0.9839, dconf 0.0365, dbox 9.06px |
| yolo26n | bus | 5/5, +0, IoUmin 0.9764, dconf 0.0996, dbox 9.72px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9833, dconf 0.0, dbox 1.6px | 5/5, +0, IoUmin 0.9632, dconf 0.1032, dbox 9.72px | 4/5, +1, IoUmin 0.9584, dconf 0.1032, dbox 9.5px |
| yolo26n | zidane | 3/3, +0, IoUmin 0.9804, dconf 0.0607, dbox 14.62px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9763, dconf 0.0, dbox 1.56px | 3/3, +0, IoUmin 0.8866, dconf 0.09, dbox 98.44px | 2/3, +1, IoUmin 0.8845, dconf 0.0585, dbox 99.51px |

### conf=0.25, iou=0.7 (cell: matched/n_ref, +extra detections, min IoU of matched pairs, max |dconf|, max box-corner deviation)

| model | image | PT predict (rect=True default) vs ONNX predict | PT predict rect=False vs ONNX predict | examples/YOLOv8-ONNXRuntime flow | examples/cpp flow (top-left, zero pad, batched NMS) | examples/YOLOv8-OpenCV-ONNX-Python flow |
|---|---|---|---|---|---|---|
| yolov8n | bus | 5/5, +1, IoUmin 0.8935, dconf 0.1752, dbox 18.94px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9724, dconf 0.0, dbox 1.41px | 5/5, +1, IoUmin 0.899, dconf 0.1752, dbox 19.78px | 4/5, +2, IoUmin 0.891, dconf 0.1752, dbox 5.24px |
| yolov8n | zidane | 3/3, +0, IoUmin 0.9318, dconf 0.0134, dbox 5.55px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9675, dconf 0.0, dbox 1.92px | 3/3, +0, IoUmin 0.9274, dconf 0.0759, dbox 8.23px | 2/3, +1, IoUmin 0.9731, dconf 0.0323, dbox 6.91px |
| yolo11n | bus | 5/5, +0, IoUmin 0.9394, dconf 0.2226, dbox 8.09px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9859, dconf 0.0, dbox 1.54px | 5/5, +0, IoUmin 0.953, dconf 0.2299, dbox 7.08px | 4/5, +1, IoUmin 0.9383, dconf 0.2299, dbox 5.84px |
| yolo11n | zidane | 3/3, +0, IoUmin 0.9756, dconf 0.0319, dbox 9.57px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9929, dconf 0.0, dbox 1.41px | 3/3, +0, IoUmin 0.9288, dconf 0.0421, dbox 8.16px | 2/3, +1, IoUmin 0.9839, dconf 0.0365, dbox 9.06px |
| yolo26n | bus | 5/5, +0, IoUmin 0.9764, dconf 0.0996, dbox 9.72px | 5/5, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 5/5, +0, IoUmin 0.9833, dconf 0.0, dbox 1.6px | 5/5, +0, IoUmin 0.9632, dconf 0.1032, dbox 9.72px | 4/5, +1, IoUmin 0.9584, dconf 0.1032, dbox 9.5px |
| yolo26n | zidane | 3/3, +0, IoUmin 0.9804, dconf 0.0607, dbox 14.62px | 3/3, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 3/3, +0, IoUmin 0.9763, dconf 0.0, dbox 1.56px | 3/3, +0, IoUmin 0.8866, dconf 0.09, dbox 98.44px | 2/3, +1, IoUmin 0.8845, dconf 0.0585, dbox 99.51px |

### conf=0.05, iou=0.7 (cell: matched/n_ref, +extra detections, min IoU of matched pairs, max |dconf|, max box-corner deviation)

| model | image | PT predict (rect=True default) vs ONNX predict | PT predict rect=False vs ONNX predict | examples/YOLOv8-ONNXRuntime flow | examples/cpp flow (top-left, zero pad, batched NMS) | examples/YOLOv8-OpenCV-ONNX-Python flow |
|---|---|---|---|---|---|---|
| yolov8n | bus | 7/7, +7, IoUmin 0.8774, dconf 0.1752, dbox 18.94px | 7/7, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 7/7, +0, IoUmin 0.9404, dconf 0.0, dbox 1.41px | 7/7, +6, IoUmin 0.899, dconf 0.1752, dbox 19.78px | 5/7, +5, IoUmin 0.891, dconf 0.1752, dbox 5.24px |
| yolov8n | zidane | 16/16, +2, IoUmin 0.8946, dconf 0.0575, dbox 11.95px | 16/16, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 15/16, +0, IoUmin 0.9137, dconf 0.0, dbox 1.92px | 11/16, +3, IoUmin 0.8124, dconf 0.0783, dbox 15.31px | 3/16, +7, IoUmin 0.9243, dconf 0.0323, dbox 7.94px |
| yolo11n | bus | 7/8, +4, IoUmin 0.9394, dconf 0.2226, dbox 8.09px | 8/8, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 8/8, +0, IoUmin 0.91, dconf 0.0, dbox 1.9px | 7/8, +3, IoUmin 0.9138, dconf 0.2299, dbox 7.08px | 4/8, +5, IoUmin 0.9383, dconf 0.2299, dbox 5.84px |
| yolo11n | zidane | 11/11, +0, IoUmin 0.8134, dconf 0.0381, dbox 44.38px | 11/11, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 11/11, +0, IoUmin 0.9059, dconf 0.0, dbox 1.64px | 7/11, +3, IoUmin 0.6646, dconf 0.1198, dbox 15.29px | 2/11, +5, IoUmin 0.9839, dconf 0.0365, dbox 9.06px |
| yolo26n | bus | 7/8, +3, IoUmin 0.9534, dconf 0.125, dbox 9.72px | 8/8, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 8/8, +0, IoUmin 0.9532, dconf 0.0, dbox 1.87px | 6/8, +2, IoUmin 0.9302, dconf 0.1183, dbox 9.72px | 4/8, +3, IoUmin 0.9584, dconf 0.1032, dbox 9.5px |
| yolo26n | zidane | 9/9, +0, IoUmin 0.9768, dconf 0.0607, dbox 14.62px | 9/9, +0, IoUmin 1.0, dconf 0.0, dbox 0.0px | 9/9, +0, IoUmin 0.8946, dconf 0.0, dbox 1.58px | 8/9, +4, IoUmin 0.5946, dconf 0.09, dbox 98.44px | 2/9, +6, IoUmin 0.8845, dconf 0.0585, dbox 99.51px |
