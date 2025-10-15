import cv2
import os

def extract_frames(
    video_path: str,
    output_dir: str = "frames",
    prefix: str = "frame",
    start_index: int = 0,
    zero_padding: int = 6,
    jpg_quality: int = 95
):
    """
    从视频中逐帧提取并保存为jpg图片。
    
    参数:
        video_path: 视频文件路径
        output_dir: 图片输出目录
        prefix: 文件名前缀，例如 'frame'
        start_index: 起始编号
        zero_padding: 序号零填充宽度，例如6 => frame_000001.jpg
        jpg_quality: JPG保存质量(0-100)
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频：{video_path}")

    frame_idx = start_index
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or None

    print(f"开始提取: {video_path}")
    if total:
        print(f"预计总帧数: {total}")
    print(f"输出目录: {os.path.abspath(output_dir)}")

    success, frame = cap.read()
    saved = 0

    # 配置JPG编码参数
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality]

    while success:
        filename = f"{prefix}_{frame_idx:0{zero_padding}d}.jpg"
        save_path = os.path.join(output_dir, filename)

        # 保存为jpg
        ok = cv2.imwrite(save_path, frame, encode_params)
        if not ok:
            print(f"警告：保存失败 -> {save_path}")
        else:
            saved += 1
            if saved % 100 == 0:
                print(f"已保存 {saved} 张... 最新: {filename}")

        frame_idx += 1
        success, frame = cap.read()

    cap.release()
    print(f"完成！共保存 {saved} 张图片。")
    

if __name__ == "__main__":
    # 使用示例：修改为你的实际视频路径
    video_path = "input.mp4"
    extract_frames(
        video_path="./new1.mp4",
        output_dir="./frames",
        prefix="frame",
        start_index=0,
        zero_padding=6,
        jpg_quality=95
    )