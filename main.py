from config import *
from bilibili import *

from tqdm import tqdm
import os

def BILIBILI_WORKFLOW():

    print("开始执行Bilibili WORKFLOW...")
    TASK_RESULT= BILIBILI_TASK.copy()

    for i, video in enumerate(BILIBILI_TASK):
        print(f"开始处理视频: {video}")
        print('当前进度：', i+1, '/', len(BILIBILI_TASK))



        print('正在获取{}的最新视频列表...'.format(video['BILIBILI_UP_ID']))
        video_list = get_up_video_list(video['BILIBILI_UP_ID'])
        print('获取到{}个视频，开始筛选并下载符合条件的视频...'.format(len(video_list)))
        
        for video_info in video_list:
            
            video_title = video_info['title']
            video_url = video_info['link']
            video_date = video_info['date']
            # 过滤不符合关键字的标题
            if video['KEY_WORD'] not in video_title:
                continue
             
            # 只下载24h以内的视频
            if '小时' not in video_date:
                continue
            
            try:
                output_path = os.path.join(BILIBILI_VIDEO_PATH, video['CATEGORY'], str(video['BILIBILI_UP_ID']))            
                print(f"开始下载音频: {video_title}，链接: {video_url}，保存路径: {output_path}")
                download_bilibili_audio(video_url, output_path, filename=video_title, audio_format='mp3')
                print(f"音频下载完成: {video_title}")
                TASK_RESULT[i]['STATUS'] = 'ok'
            except Exception as e:
                TASK_RESULT[i]['STATUS'] = e
                print(f"下载音频时出错: {e}")



    print("所有B站音频下载任务完成！")

    print("Bilibili WORKFLOW 结束")
    print(TASK_RESULT)

if __name__ == "__main__":

    BILIBILI_WORKFLOW()

    time.sleep(15)
    # 删除output目录下的临时文件
    import shutil
    temp_path = 'output'
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    print("文件已清理！")
