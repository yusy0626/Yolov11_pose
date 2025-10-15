import os
from xml.dom import minidom

# 假设：每张 image 内，<box> 与 <points> 数量一致且按顺序对应
# 输出：每张图像一个 .txt，包含多个对象，每行：
# class x_center y_center w h [pts_x1 pts_y1 pts_x2 pts_y2 ...]

IN_XML = 'annotations.xml'
OUT_DIR = './out'
CLASS_ID = 0  # 固定为0，如需根据label映射，可自行添加映射表

os.makedirs(OUT_DIR, exist_ok=True)

doc = minidom.parse(IN_XML)
images = doc.getElementsByTagName('image')

for image in images:
    width = int(float(image.getAttribute('width')))
    height = int(float(image.getAttribute('height')))
    name = image.getAttribute('name')

    # 一个图像一个txt
    out_path = os.path.join(OUT_DIR, os.path.splitext(name)[0] + '.txt')

    boxes = image.getElementsByTagName('box')
    points_list = image.getElementsByTagName('points')  # 可能不存在

    lines = []

    # 遍历每个box
    for i, bbox in enumerate(boxes):
        xtl = float(bbox.getAttribute('xtl'))
        ytl = float(bbox.getAttribute('ytl'))
        xbr = float(bbox.getAttribute('xbr'))
        ybr = float(bbox.getAttribute('ybr'))

        w = xbr - xtl
        h = ybr - ytl
        xc = xtl + w / 2.0
        yc = ytl + h / 2.0

        # 归一化
        xc_n = xc / width
        yc_n = yc / height
        w_n = w / width
        h_n = h / height

        parts = [str(CLASS_ID), f"{xc_n:.6f}", f"{yc_n:.6f}", f"{w_n:.6f}", f"{h_n:.6f}"]

        # 若有points且数量不少于当前i，则顺序配对
        if i < len(points_list):
            pts_attr = points_list[i].getAttribute('points')
            if pts_attr:
                pts_pairs = []
                for pair in pts_attr.split(';'):
                    p1, p2 = pair.split(',')
                    x = float(p1.strip()) / width
                    y = float(p2.strip()) / height
                    pts_pairs.extend([f"{x:.6f}", f"{y:.6f}"])
                parts.extend(pts_pairs)

        line = ' '.join(parts)
        lines.append(line)

    # 如果没有box但有points，你可决定是否只输出points（下段可按需启用）
    # if not boxes and points_list:
    #     for pp in points_list:
    #         pts_attr = pp.getAttribute('points')
    #         parts = [str(CLASS_ID), "0", "0", "0", "0"]
    #         if pts_attr:
    #             pts_pairs = []
    #             for pair in pts_attr.split(';'):
    #                 p1, p2 = pair.split(',')
    #                 x = float(p1.strip()) / width
    #                 y = float(p2.strip()) / height
    #                 pts_pairs.extend([f"{x:.6f}", f"{y:.6f}"])
    #             parts.extend(pts_pairs)
    #         lines.append(' '.join(parts))

    # 写文件
    with open(out_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

print("完成：所有 image 的标签已生成。")