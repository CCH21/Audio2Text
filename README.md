# 基于SpeechRecognition的音频转文字工具

## 0. 项目简介

本项目是一个基于Python SpeechRecognition模块和Google API的音频转文字工具。  
目前该项目支持`wav`格式的音频转文字，支持中文和英文两种语言。音频时长限制为2小时以内。  
本项目仍处于测试期，时长较长或声音不清晰的音频会出现转文字失败的情况，作者正在研究解决方案。  
此外，由于测试音频较少，本项目可能还会存在其他问题。  
如果你对这个项目感兴趣，想要给出意见或建议，欢迎通过[我的电子邮箱](cch_personal@163.com)联系我！  

| 更新日期            | 版本    | 更新说明                            |
|-----------------|-------|---------------------------------|
| 2023-11-23 Thu. | 1.0.0 | 初代版本，支持`wav`格式音频转文字，支持中文和英文两种语言 |
| -               | -     | Coming soon...                  |


## 1. 依赖安装

### 1.1 安装所需模块

通过下面的命令新建Conda环境。其中`ENV_NAME`为Conda环境名称，`PY_VERSION`为Python版本号，根据自己需要指定即可。  

```commandline
conda create -n ENV_NAME python=PY_VERSION
conda activate ENV_NAME
```

通过下面的命令安装所需模块。  

```commandline
pip install -r requirements.txt
```

| 模块名称              | 版本     | 说明                         |
|-------------------|--------|----------------------------|
| pydub             | 0.25.1 | 对音频文件进行拆分                  |
| SpeechRecognition | 3.10.0 | 音频转文字的核心模块，本项目使用Google API |

### 1.2 下载中文语言模型

下载链接：<https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/>  
选择`Mandarin/cmusphinx-zh-cn-5.2.tar.gz`下载到本地并解压。  
进入`speech_recognition/pocketsphinx-data`目录，新建`zh-CN`目录。将解压后的`zh_cn.cd_cont_5000`目录以及`zh_cn.dic`、`zh_cn.lm.bin`两个文件拷贝到`zh-CN`目录内。

## 2. 运行程序

通过以下命令运行程序。  

```commandline
python main.py -i INPUT -o OUTPUT -l LANG
```

以下是运行参数说明。  

| 运行参数            | 说明                                    |
|-----------------|---------------------------------------|
| `-i`或`--input`  | 必需参数，指定输入的音频文件（仅支持`wav`格式）            |
| `-o`或`--output` | 必需参数，指定输出的文本文件（仅支持`txt`格式）            |
| `-l`或`--lang`   | 必需参数，指定语言类型（目前仅支持英文`en-US`和中文`zh-CN`） |

## 3. 可能遇到的问题

- **不支持除`wav`格式的音频文件**：可以通过`ffmpeg`或其他工具将其他格式的音频文件转为`wav`格式。  
  > e.g. 使用`ffmpeg`将`m4a`格式的音频文件转为`wav`格式：
  > 
  > ```commandline
  > ffmpeg -i input.m4a -acodec pcm_s16le -ac 2 -ar 44100 output.wav
  > ```
  > 
- **不支持除`zh-CN`和`en-US`的语言类型**：后续考虑支持更多语言类型。
- **存在转文字失败的可能性**。
- **转中文文本存在断句问题**。
- **由于测试音频有限导致可能会出现其他问题**。

## 4. 后续工作

- 完善对其他格式音频文件的支持。
- 完善对其他语言类型的支持。
- 排查现有问题的出现原因，尝试给出解决方案。