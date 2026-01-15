from config import *
from bilibili import *

from tqdm import tqdm
import os

if __name__ == "__main__":

    for video in tqdm(BILIBILI_TASK):
        print(f"开始处理视频: {video}")
        try:

            video_list = get_up_video_list(video['BILIBILI_UP_ID'])

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
                
                output_path = os.path.join(BILIBILI_VIDEO_PATH, video['CATEGORY'], str(video['BILIBILI_UP_ID']))
                download_bilibili_audio(video_url, output_path, filename=video_title, audio_format='mp3')
                download_danmu(video_url, output_dir=output_path, filename=video_title)
        except Exception as e:
            print(f"处理视频 {video} 时发生错误: {e}")
            continue
        finally:
            pass

    print("所有B站音频下载任务完成！")
    time.sleep(15)
    # 删除output目录下的临时文件
    import shutil
    temp_path = 'output'
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    print("文件已清理！")
