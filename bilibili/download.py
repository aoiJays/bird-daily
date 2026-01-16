import yt_dlp
import os

def download_bilibili_audio(url, output_path='.', filename=None, audio_format='mp3'):
    """
    下载 Bilibili 视频的音频。
    
    :param url: Bilibili 视频链接
    :param output_path: 下载保存的文件夹路径 (默认为当前目录)
    :param filename: 保存的文件名 (不含后缀，默认为视频标题)
    :param audio_format: 音频格式，如 'mp3', 'm4a', 'wav', 'flac' (默认为 'mp3')
    """
    
    if filename:
        outtmpl = os.path.join(output_path, f'{filename}.%(ext)s')
    else:
        outtmpl = os.path.join(output_path, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'outtmpl': outtmpl,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio', # 使用 FFmpeg 提取音频
            'preferredcodec': audio_format, # 目标音频编码格式 (mp3, m4a, wav 等)
            'preferredquality': '192',      # 音频比特率，192k 为常用高质量标准 (0-9 for VBR, 128k, 192k, 320k)
        }],
    
    }

    try:
        # 确保输出目录存在
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"yt-dlp音频下载发生错误: {e}")


def download_danmu(video_url, output_dir="danmaku_downloads", filename=None):
    """
    使用 yt-dlp 下载 B站视频的弹幕（不下载视频）。
    
    :param video_url: B站视频链接 (例如: https://www.bilibili.com/video/BV1xx...)
    :param output_dir: 结果保存的文件夹路径
    """
    
    # 如果输出目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 已创建目录: {output_dir}")

    # 配置 yt-dlp 选项
    ydl_opts = {
        'skip_download': True,       # 关键：跳过视频下载，只下元数据和字幕
        'writesubtitles': True,      # 开启字幕下载
        'writeautomaticsub': True,   # B站弹幕有时被视为自动生成的字幕
        'subtitleslangs': ['all'],   # 下载所有可用的语言/格式
        # 输出模板：路径/视频标题.扩展名
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s') if filename is None else os.path.join(output_dir, f'{filename}.%(ext)s'),
        'ignoreerrors': True,        # 遇到错误继续（比如某个分P下载失败）
        'quiet': False,              # 显示下载日志（设为 True 则静默）
    }

    print(f"🚀 开始获取弹幕: {video_url}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown Title')
            print(f"✅ 下载完成: {title}")
            print(f"📁 文件保存在: {os.path.abspath(output_dir)}")
            
    except Exception as e:
        print(f"❌ 发生错误: {e}")



if __name__ == "__main__":
    # 示例用法：
    # 替换 BV 号, 指定下载目录为 'downloads', 文件名为 'custom_name', 格式为 'mp3'

    target_url = "https://www.bilibili.com/video/BV1pdroBiEMg"
    download_bilibili_audio(target_url, 
                            output_path="downloads", 
                            filename="custom_name", 
                            audio_format="mp3")
    download_danmu(target_url)