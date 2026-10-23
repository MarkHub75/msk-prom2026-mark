### Raw-tensor parity, max over 8 inputs per model (bus/zidane x {orig, flip, bright1.4, crop16x9}; NB: zidane crop16x9 == zidane because zidane is already 16:9, so 6 distinct inputs)

| model | comparison | box max abs, all 8400 anchors (px) | box max abs, anchors with ref cls prob>0.05 (px) | cls prob max abs | min cosine over 4 box channels | min cosine over class channels |
|---|---|---|---|---|---|---|
| yolov8n | PT fused fp32 vs ORT fp32 (same tensor) | 0.00226 | 0.000305 | 1.88e-05 | 0.99999984 | 0.99325 |
| yolov8n | PT fp16 (CPU) vs PT fp32 | 5.2 | 0.715 | 0.0101 | 0.99999726 | 0.99750 |
| yolo11n | PT fused fp32 vs ORT fp32 (same tensor) | 0.0334 | 0.000488 | 1.98e-05 | 0.99999985 | 0.99584 |
| yolo11n | PT fp16 (CPU) vs PT fp32 | 63.2 | 0.609 | 0.0484 | 0.99989310 | 0.99717 |
| yolo26n | PT fused fp32 vs ORT fp32 (same tensor) | 0.00708 | 0.000519 | 4.04e-05 | 0.99999982 | 0.98790 |
| yolo26n | PT fp16 (CPU) vs PT fp32 | 9.9 | 0.898 | 0.0631 | 0.99999176 | 0.99504 |

### Synthetic output-tensor fake quantization (NOT LinQ; calibrated on the same tensor = best case). cell: matched/n_ref, +extra, min IoU (conf=0.25 / iou=0.7)

| model | image | scenario | max box err px | max cls err | conf=0.25 | conf=0.05 |
|---|---|---|---|---|---|---|
| yolov8n | bus | S1_single_tensor_int8_symmetric(scale=5.018) | 2.51 | 0.8902 | 0/5 +0 IoUmin=None | 0/7 +0 |
| yolov8n | bus | S2_single_tensor_uint8_asym(scale=2.499) | 1.25 | 0.8902 | 0/5 +0 IoUmin=None | 0/7 +0 |
| yolov8n | bus | S3_split_box_int8(scale=5.018)_cls_uint8(scale=0.0039) | 2.51 | 0.0020 | 5/5 +0 IoUmin=0.9407 | 7/7 +0 |
| yolov8n | bus | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 1.25 | 0.0020 | 5/5 +0 IoUmin=0.9536 | 7/7 +1 |
| yolov8n | bus | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 1.25 | 0.0020 | 5/5 +0 IoUmin=0.9536 | 7/7 +1 |
| yolov8n | zidane | S1_single_tensor_int8_symmetric(scale=5.013) | 2.51 | 0.8270 | 0/3 +0 IoUmin=None | 0/16 +0 |
| yolov8n | zidane | S2_single_tensor_uint8_asym(scale=2.497) | 1.25 | 0.8270 | 0/3 +0 IoUmin=None | 0/16 +0 |
| yolov8n | zidane | S3_split_box_int8(scale=5.013)_cls_uint8(scale=0.0039) | 2.51 | 0.0020 | 3/3 +0 IoUmin=0.9411 | 16/16 +0 |
| yolov8n | zidane | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 1.25 | 0.0020 | 3/3 +0 IoUmin=0.937 | 16/16 +1 |
| yolov8n | zidane | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 1.25 | 0.0020 | 3/3 +0 IoUmin=0.937 | 16/16 +1 |
| yolo11n | bus | S1_single_tensor_int8_symmetric(scale=5.017) | 2.51 | 0.9392 | 0/5 +0 IoUmin=None | 0/8 +0 |
| yolo11n | bus | S2_single_tensor_uint8_asym(scale=2.499) | 1.25 | 0.9392 | 0/5 +0 IoUmin=None | 0/8 +0 |
| yolo11n | bus | S3_split_box_int8(scale=5.017)_cls_uint8(scale=0.0039) | 2.51 | 0.0020 | 5/5 +0 IoUmin=0.9242 | 8/8 +1 |
| yolo11n | bus | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 1.25 | 0.0020 | 5/5 +0 IoUmin=0.9556 | 8/8 +0 |
| yolo11n | bus | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 1.25 | 0.0020 | 5/5 +0 IoUmin=0.9556 | 8/8 +0 |
| yolo11n | zidane | S1_single_tensor_int8_symmetric(scale=5.016) | 2.51 | 0.8577 | 0/3 +0 IoUmin=None | 0/11 +0 |
| yolo11n | zidane | S2_single_tensor_uint8_asym(scale=2.498) | 1.25 | 0.8578 | 0/3 +0 IoUmin=None | 0/11 +0 |
| yolo11n | zidane | S3_split_box_int8(scale=5.016)_cls_uint8(scale=0.0039) | 2.51 | 0.0019 | 3/3 +0 IoUmin=0.9552 | 11/11 +2 |
| yolo11n | zidane | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 1.25 | 0.0019 | 3/3 +0 IoUmin=0.9766 | 11/11 +2 |
| yolo11n | zidane | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 1.25 | 0.0019 | 3/3 +0 IoUmin=0.9766 | 11/11 +2 |
| yolo26n | bus | S1_single_tensor_int8_symmetric(scale=5.186) | 2.59 | 0.9030 | 0/5 +0 IoUmin=None | 0/8 +0 |
| yolo26n | bus | S2_single_tensor_uint8_asym(scale=2.583) | 1.29 | 0.9030 | 0/5 +0 IoUmin=None | 0/8 +0 |
| yolo26n | bus | S3_split_box_int8(scale=5.186)_cls_uint8(scale=0.0039) | 2.59 | 0.0020 | 5/5 +0 IoUmin=0.9307 | 8/8 +1 |
| yolo26n | bus | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 18.61 | 0.0020 | 5/5 +0 IoUmin=0.9722 | 8/8 +0 |
| yolo26n | bus | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 18.61 | 0.0020 | 5/5 +0 IoUmin=0.9722 | 8/8 +0 |
| yolo26n | zidane | S1_single_tensor_int8_symmetric(scale=5.266) | 2.63 | 0.8970 | 0/3 +0 IoUmin=None | 0/9 +0 |
| yolo26n | zidane | S2_single_tensor_uint8_asym(scale=2.623) | 1.31 | 0.8970 | 0/3 +0 IoUmin=None | 0/9 +0 |
| yolo26n | zidane | S3_split_box_int8(scale=5.266)_cls_uint8(scale=0.0039) | 2.63 | 0.0020 | 3/3 +0 IoUmin=0.9203 | 9/9 +2 |
| yolo26n | zidane | S4_single_tensor_boxes_div640_uint8(scale=0.0039) | 28.76 | 0.0020 | 3/3 +0 IoUmin=0.9746 | 9/9 +1 |
| yolo26n | zidane | S5_split_box_uint8_0to640(scale=2.510)_cls_uint8 | 28.76 | 0.0020 | 3/3 +0 IoUmin=0.9746 | 9/9 +1 |
