#!/usr/bin/env python3

import sys
import argparse


parser = argparse.ArgumentParser(description='Process introduction.')
parser.add_argument('finame', type=str,
                    help='输入制表的tsv列表文件')
parser.add_argument('-o', '--foname', type=str, default=None,
                    help='输出的html')
parser.add_argument('-s', '--sep', type=str, default=None,
                    help='sep')
parser.add_argument('-w', '--width', type=str, default=400,
                    help='width images')
parser.add_argument('-f', '--force', action='store_true',
                    help='是否强制所有行使用表格，不判断只有第一列的行。')
args = parser.parse_args()


# finame, foname = sys.argv[1:3]
finame, foname = args.finame, args.foname
force = args.force
sep = args.sep
width = args.width

with open(finame) as fi:
    Llines = [line.strip().split(sep) for line in fi.readlines()]

header = """<!DOCTYPE html>
<html>

<head>
    <title>PNG Table Viewer</title>
    <style>
        /* --- 基础表格样式 --- */
        p { margin: 0 0 10.5px; display: block; margin-block-start: 0.3em; margin-block-end: 1em; }
        table { border-collapse: collapse; min-width: 450px; font-size: 12px; border-spacing: 0; text-align: left; border-width: 1px; border-style: double; }
        td { padding: 5px 10px; font-family: 'Trebuchet MS', Arial, sans-serif; vertical-align: top; width: 700px; border-width: 1px; word-wrap: break-word; word-break: break-all; font-size: 14px; color: #434242; }
        
        /* 表格内图片样式 */
        table img {
            width: IMG_WIDTHpx;
            cursor: zoom-in;
            transition: opacity 0.2s;
            border: 2px solid transparent;
        }
        table img:hover { opacity: 0.8; border-color: #aaa; }

        /* SVG和PDF对象样式 */
        object {
            width: IMG_WIDTHpx;
        }

        /* --- Lightbox (图片查看器) 样式 --- */
        #lightbox-overlay {
            display: none;
            position: fixed;
            z-index: 10000;
            left: 0; top: 0;
            width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            justify-content: center;
            align-items: center;
            flex-direction: column;
            user-select: none;
            overflow: hidden;
        }

        #img-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%; height: 100%;
            pointer-events: none;
        }

        #lightbox-image {
            max-width: 90%;
            max-height: 80vh;
            object-fit: contain;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
            cursor: zoom-in;
            pointer-events: auto;
            transform-origin: center center;
            will-change: transform;
            transition: transform 0.1s linear;
            animation: zoomIn 0.3s;
        }

        /* 放大时的鼠标样式 */
        #lightbox-image.zoomed {
            cursor: grab;
        }

        @keyframes zoomIn { from {transform:scale(0.95); opacity:0} to {transform:scale(1); opacity:1} }

        /* 关闭按钮 */
        .lb-close {
            position: absolute; top: 20px; right: 35px;
            color: #f1f1f1; font-size: 40px; font-weight: bold;
            cursor: pointer; z-index: 10005;
        }

        /* 导航按钮 */
        .lb-btn {
            cursor: pointer; position: absolute; top: 50%;
            padding: 16px; margin-top: -50px;
            color: white; font-weight: bold; font-size: 30px;
            transition: 0.3s; border-radius: 3px;
            background-color: rgba(255, 255, 255, 0.1);
            z-index: 10005;
        }
        .lb-btn:hover { background-color: rgba(255, 255, 255, 0.3); }
        .lb-prev { left: 20px; }
        .lb-next { right: 20px; }

        /* 顶部位置导航栏 */
        #lb-counter {
            position: absolute; top: 20px; left: 35px;
            color: #fff; font-size: 16px; font-family: monospace;
            background: rgba(255, 255, 255, 0.2);
            padding: 5px 10px; border-radius: 4px;
            z-index: 10005;
        }

        /* 底部描述文字 */
        #lb-caption {
            position: absolute; bottom: 20px;
            color: #ccc; font-size: 16px;
            text-align: center; max-width: 80%;
            z-index: 10005;
            background-color: rgba(0,0,0,0.5);
            padding: 5px 10px;
            border-radius: 5px;
        }
    </style>
</head>
"""

# 使用字符串替换而不是格式化，避免%字符的冲突
header = header.replace('IMG_WIDTH', str(width))

L_result = []
if foname:
    L_result.append(header)
    L_result.append("<body>\n")
    # 添加图片查看器的HTML结构
    L_result.append('''
<div id="lightbox-overlay">
    <div id="lb-counter"></div>
    <span class="lb-close" onclick="closeLightbox()">&times;</span>
    <a class="lb-btn lb-prev" onclick="move('left')">&#10094;</a>
    <a class="lb-btn lb-next" onclick="move('right')">&#10095;</a>
    <div id="img-wrapper">
        <img id="lightbox-image" src="" 
             onclick="toggleZoom(event)" 
             onmousemove="panImage(event)" 
             onwheel="zoomWheel(event)">
    </div>
    <div id="lb-caption"></div>
</div>
''')
table_in = 0
for Lline in Llines:
    if len(Lline) == 1 and not force:
        if table_in == 1:
            L_result.append("</table>\n")
        L_result.append("<p>%s</p>\n" % Lline[0])
        table_in = 0
    else:
        if table_in == 0:
            L_result.append("<table>\n")
        L_result.append("<tr>")
        for x in Lline:
            if x.endswith(".png"):
                L_result.append('  <td><p>%s</p><img src="%s" /></td>' % (x, x))
            elif x.endswith(".svg"):
                L_result.append(
                    '  <td><p>%s</p><object data="%s" type="image/svg+xml"></object></td>' % (x, x))
            elif x.endswith(".pdf"):
                L_result.append(
                    '  <td><p>%s</p><object data="%s" type="application/pdf" style="width:660px;  height:680px;" ></object></td>' % (x, x))
            else:
                L_result.append(
                    '  <td><p>%s</p></td>' % (x))
        L_result.append("</tr>\n")
        table_in = 1
if table_in:
    L_result.append("</table>\n")
if foname:
    L_result.append('''
<script>
    document.addEventListener("DOMContentLoaded", function() {
        console.log("Lightbox script initialized.");

        // ================= 配置区域 =================
        const CLICK_ZOOM_LEVEL = 2.5; // 点击时放大的倍数
        const MAX_ZOOM = 5.0;         // 滚轮最大放大倍数
        const MIN_ZOOM = 1.0;         // 滚轮最小缩小倍数
        const ZOOM_STEP = 0.2;        // 滚轮滚动一次缩放的幅度
        // ===========================================

        const overlay = document.getElementById('lightbox-overlay');
        const lightboxImg = document.getElementById('lightbox-image');
        const captionText = document.getElementById('lb-caption');
        const counterText = document.getElementById('lb-counter');

        // 存储图片的二维矩阵
        const grid = [];
        let currentR = -1;
        let currentC = -1;
        
        // 状态变量
        let currentScale = 1.0;

        // 使用 Array.from 确保兼容性
        const rows = Array.from(document.querySelectorAll('table tr'));
        
        rows.forEach((tr, rIndex) => {
            const rowImgs = []; 
            const cells = Array.from(tr.querySelectorAll('td'));
            
            cells.forEach((td, cIndex) => {
                const img = td.querySelector('img');
                if(img) {
                    // 绑定点击事件，使用闭包保存坐标
                    img.addEventListener('click', function(e) {
                        // 阻止事件冒泡，防止意外关闭或其他干扰
                        e.stopPropagation();
                        openLightbox(rIndex, cIndex);
                    });
                    rowImgs[cIndex] = img;
                } else {
                    rowImgs[cIndex] = null;
                }
            });
            grid.push(rowImgs);
        });

        console.log("Grid built with rows:", grid.length);

        // --- 核心逻辑 ---

        window.openLightbox = function(r, c) {
            currentR = r;
            currentC = c;
            updateView();
            overlay.style.display = "flex";
        };

        window.closeLightbox = function() {
            resetZoom();
            overlay.style.display = "none";
        };

        window.move = function(direction) {
            resetZoom(); // 切换图片重置缩放
            let nextR = currentR;
            let nextC = currentC;

            if (direction === 'up') nextR--;
            if (direction === 'down') nextR++;
            if (direction === 'left') nextC--;
            if (direction === 'right') nextC++;

            // 1. 检查行是否存在
            if (nextR >= 0 && nextR < grid.length) {
                // 2. 检查列是否存在
                if (nextC >= 0 && nextC < grid[nextR].length) {
                    // 3. 检查该位置是否有图片
                    if (grid[nextR][nextC]) {
                        currentR = nextR;
                        currentC = nextC;
                        updateView();
                    } else {
                        // 如果当前位置没有图片，尝试在下一个有图片的位置停止
                        findNextValidPosition(nextR, nextC, direction);
                    }
                }
            }
        };

        function findNextValidPosition(r, c, direction) {
            let nextR = r;
            let nextC = c;
            let maxSearch = 100; // 防止无限循环
            let searchCount = 0;

            // 继续沿相同方向搜索
            while (searchCount < maxSearch) {
                searchCount++;
                
                if (direction === 'up') nextR--;
                if (direction === 'down') nextR++;
                if (direction === 'left') nextC--;
                if (direction === 'right') nextC++;

                // 检查边界
                if (nextR < 0 || nextR >= grid.length) break;
                if (nextC < 0 || nextC >= grid[nextR].length) break;

                // 如果找到有效图片位置
                if (grid[nextR][nextC]) {
                    currentR = nextR;
                    currentC = nextC;
                    updateView();
                    return;
                }
            }
        }

        function updateView() {
            if (!grid[currentR] || !grid[currentR][currentC]) return;
            
            const imgObj = grid[currentR][currentC];
            lightboxImg.src = imgObj.src;
            counterText.innerText = `Row ${currentR + 1} / Col ${currentC + 1}`;

            // 尝试获取描述文字
            const prevP = imgObj.previousElementSibling;
            if(prevP && prevP.tagName === 'P') {
                captionText.innerText = prevP.innerText;
            } else {
                captionText.innerText = "";
            }
        }

        // --- 缩放逻辑 (点击 + 滚轮) ---

        function applyTransform() {
            lightboxImg.style.transform = `scale(${currentScale})`;
            
            if (currentScale > 1.05) {
                lightboxImg.classList.add('zoomed');
            } else {
                lightboxImg.classList.remove('zoomed');
                // 如果回到原大小，重置偏移中心
                lightboxImg.style.transformOrigin = "center center";
            }
        }

        // 1. 点击切换：在 1.0 和 CLICK_ZOOM_LEVEL 之间切换
        window.toggleZoom = function(e) {
            e.stopPropagation();
            
            // 如果当前已经放大了，点击则还原
            if (currentScale > 1.1) {
                currentScale = 1.0;
                lightboxImg.style.transformOrigin = "center center"; // 还原中心
            } else {
                // 如果是原图，则放大到预设值
                currentScale = CLICK_ZOOM_LEVEL;
                updateOrigin(e); // 以鼠标点击处为中心
            }
            applyTransform();
        };

        // 2. 滚轮缩放
        window.zoomWheel = function(e) {
            e.preventDefault(); // 阻止页面滚动

            // 计算新的缩放值
            const direction = e.deltaY > 0 ? -1 : 1;
            const newScale = currentScale + (direction * ZOOM_STEP);

            // 限制范围
            currentScale = Math.min(Math.max(newScale, MIN_ZOOM), MAX_ZOOM);

            // 如果在放大过程中，同时也更新中心点跟随鼠标
            if (currentScale > 1.0) {
                updateOrigin(e);
            }

            applyTransform();
        };

        // 3. 鼠标移动漫游 (仅在放大时生效)
        window.panImage = function(e) {
            if (currentScale > 1.1) {
                updateOrigin(e);
            }
        };

        // 计算鼠标在图片内的相对百分比位置
        function updateOrigin(e) {
            const rect = lightboxImg.getBoundingClientRect();
            let x = e.clientX - rect.left;
            let y = e.clientY - rect.top;
            
            // 转换为百分比 (0-100%)
            let xPercent = (x / rect.width) * 100;
            let yPercent = (y / rect.height) * 100;

            // 边界保护
            xPercent = Math.min(100, Math.max(0, xPercent));
            yPercent = Math.min(100, Math.max(0, yPercent));

            lightboxImg.style.transformOrigin = `${xPercent}% ${yPercent}%`;
        }

        function resetZoom() {
            currentScale = 1.0;
            lightboxImg.style.transformOrigin = "center center";
            applyTransform();
        }

        // --- 键盘事件 ---
        document.addEventListener('keydown', function(event) {
            if (overlay.style.display === "flex") {
                switch(event.key) {
                    case "Escape": closeLightbox(); break;
                    case "ArrowUp":    move('up'); event.preventDefault(); break;
                    case "ArrowDown":  move('down'); event.preventDefault(); break;
                    case "ArrowLeft":  move('left'); break;
                    case "ArrowRight": move('right'); break;
                }
            }
        });

        // --- 点击遮罩关闭 ---
        overlay.addEventListener('click', function(e) {
            // 只有点击黑色背景或img-wrapper才关闭
            if (e.target === overlay || e.target.id === 'img-wrapper') {
                closeLightbox();
            }
        });
    });
</script>
''')
    L_result.append("</body>")

foname = open(foname, "w") if foname else sys.stdout
print(*L_result, sep="", end="", file=foname)
