# FightOfPlane

实现碰撞检测

1.此时初步创建出我方飞机，加载出背景图片和背景音乐，且能够控制飞机移动的方向，但是还存在一个问题，即飞机移动至最下方时，会出现上下抖动的情况。

2.为加强飞机的动感，采用两张图片交替显示的方法，使得飞机尾气看似在喷射。

3.创建敌机类，敌机共分为3种，大小、速度、承受攻击的能力不同。其中大飞机与中小型敌机不同，大型飞机与我方飞机类似，加入了飞行特效。

4.绘制敌机时没考虑绘制位置，将大型敌机绘制在小型机之前，会导致两者重合，若此时敌机逼近会使我方飞机被另一未被摧毁的飞机撞毁。

5.碰撞检测：两方飞机碰撞之后，双方飞机均损毁，播放损毁时的图像。
（1）出现问题：找不到图像位置，碰撞后自动闪退。
      原因：python加载和打开文件语句中，没有加入文件夹名称。
6.此时飞机能够实现被敌机撞毁时的检测，
