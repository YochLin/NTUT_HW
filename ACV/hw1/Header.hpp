//
//  Header.hpp
//  hw1
//
//  Created by Yoch Lin on 2019/9/30.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#ifndef Header_hpp
#define Header_hpp
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <vector>
#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

struct HEADER{
    int width;
    int heigh;
    uchar header[54];
};
struct RGB{
    uchar b;
    uchar g;
    uchar r;
};

void readBmp(RGB *pixel, char *path, HEADER *header);
void writeBmp(RGB *pixel, char *path, HEADER *header);
RGB *rotationImg(RGB *pixel, int angle, HEADER *header);
void channelChange(RGB *pixel, RGB *outputPixel, char const *chageType);
int hw1_1();
int hw1_2();
int hw1_3();
int hw1_bonus();
int hw1_1_opencv();
int hw1_2_opencv();
int hw1_3_opencv();
int hw1_bonus_opencv();

#endif /* Header_hpp */
