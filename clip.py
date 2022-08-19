import random
import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageFont
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from tkinter.filedialog import askdirectory
from shutil import copyfile
from ffmpy import FFmpeg
from PIL import Image, ImageDraw
from time import strftime
from time import gmtime

CLIP_TIME = 600
DICT_PATH = "movies/"
OUTPUT_PATH = "output/"
ERR_PATH = "error/"
FRAG_PATH = "fragments/"
fontFolder = r'C:\Windows\Fonts'



def get_movies_path(dict_path):
    file_name = list()
    for i in os.listdir(dict_path):
        data_collect = ''.join(i)
        file_name.append(data_collect)
    return file_name


def print_line():
    print("----------------------------------")
    text.insert(tk.END, "----------------------------------\n")


def print_short_line():
    print("---------------")
    text.insert(tk.END, "---------------\n")


def clip_video(ori, begin, end, target):
    ffmpeg_extract_subclip(ori, begin, end, target)


def clip():
    global isImg

    err = ""
    f_name_list = get_movies_path(DICT_PATH)
    print("*找到" + str(len(f_name_list)) + "个视频*")
    text.insert(tk.END, "*找到" + str(len(f_name_list)) + "个视频*\n")
    global CLIP_TIME
    CLIP_TIME = int(time.get())
    text.insert(tk.END, "*剪辑时长为：" + str(CLIP_TIME) + "秒*\n")
    print("*剪辑时长为：" + str(CLIP_TIME) + "秒*")

    j = 1

    success = 0
    fail = 0
    for f_name in f_name_list:

        stem, suffix = os.path.splitext(DICT_PATH + f_name)
        if suffix == "":
            j += 1
            continue
        print(stem + " " + suffix)

        print_line()
        try:
            t = 0
            video = VideoFileClip(DICT_PATH + f_name)
            duration = video.duration

            print("*(" + str(j) + "/" + str(len(f_name_list)) + ") 正在处理: " + f_name + " 视频时长" + str(duration) + "秒 *")
            text.insert(tk.END, "*(" + str(j) + "/" + str(len(f_name_list)) + ") 正在处理: " + f_name + " 视频时长" + str(duration) + "秒 *\n")
            i = 1

            while t < duration:
                print_short_line()
                ffname = OUTPUT_PATH + f_name.replace(suffix, "") + "_" + str(i).rjust(3, '0')
                fragment_path_name = FRAG_PATH + f_name.replace(suffix, "") + "_" + str(i).rjust(3, '0')
                print("正在处理该视频下第" + str(i) + "个剪辑")
                text.insert(tk.END, "正在处理该视频下第" + str(i) + "个剪辑\n")

                if t + CLIP_TIME > duration:
                    # clip = video.subclip(t, duration)
                    clip_video(DICT_PATH + f_name, t, duration, ffname + suffix)
                    dd = duration - t
                else:
                    # clip = video.subclip(t, t + CLIP_TIME)
                    clip_video(DICT_PATH + f_name, t, t + CLIP_TIME, ffname + suffix)
                    dd = CLIP_TIME

                # 截图 16次
                if isImg.get() == 1 and dd > 17:
                    frame_list = []
                    try:
                        time_list = []
                        for k in range(16):
                            ttt = random.randint(1, int(dd))
                            while ttt in time_list:
                                ttt = random.randint(1, int(dd))
                            time_list.append(ttt)
                        time_list.sort()
                        print(str(time_list))
                        for time_dd in time_list:
                            video.save_frame(fragment_path_name + "_" + str(time_dd) + ".jpg", t + time_dd)
                            frame_list.append(fragment_path_name + "_" + str(time_dd) + ".jpg")
                        images = []
                        tl = 0
                        for imgName in frame_list:
                            blackFont1 = ImageFont.truetype(os.path.join(fontFolder, 'msyh.ttc'), size=90)
                            img = Image.open(imgName)
                            draw = ImageDraw.Draw(img)
                            draw.text((img.width/2-130, img.height-160), strftime("%H:%M:%S", gmtime(time_list[tl])), fill=(255, 255, 255), font = blackFont1)
                            images.append(img)
                            tl += 1
                        w = images[0].width
                        h = images[0].height
                        target = Image.new('RGB', (w*4, h*4))
                        for idx, img in enumerate(images):
                            ll = idx % 4
                            lll = idx // 4
                            target.paste(img, (ll * w, lll * h, ll * w + w, lll * h + h))
                        # ww = target.width
                        # target.resize((ww, 3860), Image.ANTIALIAS).save(ffname + ".jpg")
                        target.save(ffname + ".jpg")
                        for img in frame_list:
                            os.remove(img)
                    except Exception as e:
                        try:
                            for img in frame_list:
                                os.remove(img)
                        except BaseException:
                            pass
                        pass

                t += CLIP_TIME
                i += 1
            j += 1
            success += 1
            1/0
        except BaseException as ee:
            print("*该视频处理失败*")
            text.insert(tk.END, "*该视频处理失败*\n")
            err += f_name + ", "
            j += 1
            fail += 1
            try:
                print("*正在复制*")
                text.insert(tk.END, "*正在复制*\n")
                copyfile(DICT_PATH + f_name, ERR_PATH + f_name)
                print("*复制成功*")
                text.insert(tk.END, "*复制成功*\n")
            except BaseException:
                print("*复制文件失败*")
                text.insert(tk.END, "*复制文件失败*\n")
            continue

    print_line()

    print("*处理完成*")
    text.insert(tk.END, "*处理完成*\n")
    print("*成功处理" + str(success) + "个视频*")
    text.insert(tk.END, "*成功处理" + str(success) + "个视频*\n")
    print("*处理失败" + str(fail) + "个视频*")
    text.insert(tk.END, "*处理失败" + str(fail) + "个视频*\n")
    print("*失败的视频为：" + err + "*")
    text.insert(tk.END, "*失败的视频为：" + err + "*\n")
    print("-CR Soulter-")
    print_line()


def input_file():
    global ERR_PATH
    global DICT_PATH
    DICT_PATH = askdirectory() + "/"
    text.insert(tk.END, "*输入视频目录为：" + DICT_PATH + "*\n")
    ERR_PATH = DICT_PATH + "error/"
    if not os.path.exists(ERR_PATH):
        os.mkdir(ERR_PATH)


def output_file():
    global OUTPUT_PATH
    OUTPUT_PATH = askdirectory() + "/"
    text.insert(tk.END, "*输出视频目录为：" + OUTPUT_PATH + "*\n")


if __name__ == '__main__':
    # argv.pop(0)
    # params = argv

    if not os.path.exists(FRAG_PATH):
        os.mkdir(FRAG_PATH)


    root = tk.Tk()
    root.geometry("500x300")

    isImg = tk.IntVar(master=root)

    input_file_btn = ttk.Button(root, text="选择输入文件夹", command=lambda: input_file())
    input_file_btn.pack()

    output_file_btn = ttk.Button(root, text="选择输出文件夹", command=lambda: output_file())
    output_file_btn.pack()

    time = ttk.Entry(root, width=10)
    time.pack()
    time.insert(tk.END, "600")

    isImgC = tk.Checkbutton(root, text="是否生成截图", variable=isImg, onvalue = 1, offvalue = 0)
    isImgC.deselect()
    isImgC.pack()
    start_btn = ttk.Button(root, text="开始处理", command=clip)
    start_btn.pack()

    text = tk.Text(root, width=470, height=200)
    text.pack()

    scroll = tk.Scrollbar()

    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)

    root.mainloop()
