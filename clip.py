from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

CLIP_TIME = 600
DICT_PATH = "movies/"
OUTPUT_PATH = "output/"


def get_movies_path(dict_path):
    file_name = list()
    for i in os.listdir(dict_path):
        data_collect = ''.join(i)
        file_name.append(data_collect)
    return file_name


def print_line():
    print("----------------------------------")


def print_short_line():
    print("---------------")


def clip_video(ori, begin, end, target):
    ffmpeg_extract_subclip(ori, begin, end, target)


def clip():
    f_name_list = get_movies_path(DICT_PATH)
    print("*找到" + str(len(f_name_list)) + "个视频*")

    j = 1

    success = 0
    fail = 0
    for f_name in f_name_list:

        stem, suffix = os.path.splitext(DICT_PATH + f_name)

        print_line()
        try:
            t = 0
            video = VideoFileClip(DICT_PATH + f_name)
            duration = video.duration

            print("*(" + str(j) + "/" + str(len(f_name_list)) + ") 正在处理: " + f_name + " 视频时长" + str(duration) + "秒 *")
            i = 1

            while t < duration:
                print_short_line()
                print("正在处理该视频下第" + str(i) + "个剪辑")
                if t + CLIP_TIME > duration:
                    # clip = video.subclip(t, duration)
                    clip_video(DICT_PATH + f_name, t, duration, OUTPUT_PATH + f_name.replace(suffix, "") + "_" + str(i).rjust(3, '0') + suffix)
                else:
                    # clip = video.subclip(t, t + CLIP_TIME)
                    clip_video(DICT_PATH + f_name, t, t + CLIP_TIME, OUTPUT_PATH + f_name.replace(suffix, "") + "_" + str(i).rjust(3, '0') +suffix)
                t += CLIP_TIME
                i += 1
            j += 1
            success += 1
        except BaseException:
            print("*该视频处理失败*")
            j += 1
            fail += 1
            continue

    print_line()

    print("*处理完成*")
    print("*成功处理" + str(success) + "个视频*")
    print("*处理失败" + str(fail) + "个视频*")
    print_line()
