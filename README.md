## README

### Bilibili
- 爬取指定up的视频主页，获取视频列表
- 通过ytplp下载音频


## 本地测试

### 本地环境

#### 配置Google Chrome
```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt install -y ./google-chrome-stable_current_amd64.deb
google-chrome --version  
```
如果最后能输出版本号说明成功

#### FFmepeg
如果你需要提取B站音视频的话
```
sudo apt update
sudo apt install ffmpeg
ffmpeg -version
```

#### Python
建议使用虚拟环境（推荐版本3.10）
```python
python -m pip install --upgrade pip
pip install -r requirements.txt
```