import cv2
from ultralytics import YOLO

# ----------------- 配置区域 -----------------
MODEL_PATH = './best.pt'  # 你的 YOLO 模型权重
VIDEO_PATH = 'new1.mp4'                    # 输入视频
OUTPUT_PATH = 'output_new1.mp4'                 # 输出视频
SHOW_WINDOW = True                               # 是否显示窗口
CONF_THRESHOLD = 0.25                             # 置信度阈值
# --------------------------------------------

# 加载模型
model = YOLO(MODEL_PATH)

# 打开视频
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"无法打开视频: {VIDEO_PATH}")
    exit()

# 视频参数
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 预测
    results = model(frame)  # 这里 results 是一个 list，包含每帧预测结果

    # 绘制结果
    for result in results:
        # 绘制边界框和类别标签
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            if conf < CONF_THRESHOLD:
                continue
            label = f"{cls}:{conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # 如果是 keypoints 模型，可绘制关键点
        if hasattr(result, 'keypoints') and result.keypoints is not None:
            kps = result.keypoints.xy.cpu().numpy()  # 获取 xy 坐标
            for kp_set in kps:
                for x, y in kp_set:
                    cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)

    # 保存输出帧
    out.write(frame)

    # 显示帧
    if SHOW_WINDOW:
        cv2.imshow('YOLO Inference', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    frame_idx += 1
    print(f"Processed frame {frame_idx}", end='\r')

# 释放资源
cap.release()
out.release()
cv2.destroyAllWindows()
print("\n处理完成，输出保存到", OUTPUT_PATH)
