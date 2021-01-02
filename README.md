# rune_detection

媒婆斯多利符文识别工具



### 目录说明

```sh
backup 模型训练结果
cfg 模型配置文件
data 数据集设置
dataset_tools 数据集工具
utils 项目使用过的小工具
weights yolov4的Pre-trained weights
```

### 特点

- 响应速度极快[^1]
- 识别率高达99%[^2][^3]
- 提供http api接入,方便多平台多语言调用

[^1]: NVIDIA GeForce 750Ti级别显卡能做到5fps,即1秒识别5张图片
[^2]: 识别率为当前数据集训练8000step后的结果
[^3]: 该识别率并未包含矿,花的数据,即矿,花的数据集需自行采集并重新训练



### 安装说明

#### 硬件部分

显卡必须N卡,至少Compute capability 5.0以上 或 NVIDIA Jetson Nano以上, 具体看[wikipedia的表](https://en.wikipedia.org/wiki/CUDA)

如果没有N卡,请确保你有足够的时间跟强爆炸的CPU来跑训练

#### 系统环境部分

Windows/Linux都必须安装CUDA 10.1,暂未测试CUDA 11兼容性,若无N卡无视该要求

具体参考 [yolo环境需求](https://github.com/AlexeyAB/darknet#requirements)

#### Python部分

代码仅支持Python3

**Linux发行版下注意pip对应的版本**

1. 安装opencv

   ```sh
   # 本机使用
   pip install opencv-python
   # 服务器使用
   pip install opencv-python-headless
   ```
   
2. 安装sklearn

   ```sh
   # 仅本机
   pip install scikit-learn==0.19.2
   ```

3. 安装http api依赖

   ```sh
   # web核心
   pip install sanic
   # mysql
   pip install PyMySQL aiomysql
   ```
4. 安装标记工具
    ```sh
    pip install labelImg
    ```
#### 注意事项

- 如需http api启用CUDA,请自行编译opencv with cuda, 参考该[链接](https://jamesbowley.co.uk/accelerate-opencv-4-5-0-on-windows-build-with-cuda-and-python-bindings/),重新编译后,手动指定python使用编译后的opencv或不使用上面的命令安装opencv
- 服务器需要**MySQL 5.5**以上,动手能力强的可以手动修改成**SQLite**数据库
- NVIDIA 20系列显卡以上可以开启cudnn_half加速训练
- 有其他问题请发issue

### 原理

先使用[Labelmg](https://github.com/tzutalin/labelImg)手动标记数据集,接着AlexeyAB的[yolov4](https://github.com/AlexeyAB/darknet)训练模型,最后使用opencv调用模型并返回结果

### 使用

1. 先自行编译darknet,Linux参考[该链接](https://github.com/AlexeyAB/darknet#how-to-compile-on-linuxmacos-using-cmake) Windows参考[该链接](https://github.com/AlexeyAB/darknet#how-to-compile-on-windows-using-cmake),并且把**darknet.exe**放入项目根目录

2. 采集符文图像,放入**utils/runes_orig**,并使用**utils/cut_img.py**进行裁剪

3. 使用**LabelImg**标记裁剪后的数据集

   1. 这里注意类别**名字**为up down left right
   2. 顺序必须跟上面的顺序一致

4. 把标记完成的数据集文件夹放到**`dataset_tools`**里,并改名为**final**

5. 生成的**train-runes.txt**和**test-runes.txt**放入项目根目录的**data**下

6. 把标记完成的数据集内容全部移动到**data/runes**

7. 下载[pre trained](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29)文件到项目根目录的**weights**目录下

8. 使用命令`darknet.exe detector train data\runes.data cfg\yolov4-tiny-runes.cfg weights\yolov4-tiny.conv.29`开始训练

   1. 20系列显卡大概需要2-3小时,取决于显卡

   2. 10系列显卡大概需要4-6小时

   3. CPU没试过,建议慢慢等

      如果训练时间超过我说的时间,建议检查第一步是否正确执行完成

9. 从**backup**文件夹拿出best后缀的文件,放入**server/darknet/weights**中

10. 从**cfg**文件夹拿出**yolov4-tiny-runes-test.cfg**,放入**server/darknet/cfg**中

11. 进入**server**目录执行`python app.py`,到此完成

