//
//  Header.hpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/21.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#ifndef Header_hpp
#define Header_hpp

#include <iostream>
#include <fstream>
#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>
#include <time.h>

using namespace std;
using namespace cv;


struct Header{
    int width;
    int heigh;
    int rowSize;  // 存放被4整除的寬
    char information[54];
};

struct RGB{
    uchar g;
    uchar b;
    uchar r;
};

typedef struct QNode{
    int data;
    struct QNode *next;
}QNode;

typedef struct Queue{
    struct QNode* first;
    struct QNode* last;
}Queue;


// ========================= c++ functions ============================
void readBmp(RGB *pixel, char *path, Header *header);
void writeBmp(RGB *pixel, char *path, Header *header);
void showRGBPixelValue(RGB *pixel, Header header);
RGB *RGB2Gray(RGB *pixel, Header header);
RGB *thresHoldGrayBmp(RGB *pixel, Header header, int threshold);
RGB *binaryPixelLabeling(RGB *binaryPixel, Header header);
RGB *connectedComponent(RGB *src, Header header);
RGB *labelColorSet(RGB *pixel, Header header);
void boundingBox(RGB *src, RGB *labelImg, Header header);
void findCentralPoint(RGB *src, RGB *labelImg, Header header);
void dilation(RGB *src, int *mask, Header header);
void erosion(RGB *src, int *mask, Header header);
void opening(RGB *src, int *mask, Header header);
void closing(RGB *src, int *mask, Header header);
void nor(RGB *src, RGB *dst, Header header);

// ========================= openCV functions ============================
Mat matLabelColor(Mat labelImage, int nLabels);
Mat matSingleDim2threeDim(Mat imBin);
void matBoundingBox(Mat binImg, Mat labelImg, int nLabels);
Mat matNor(Mat src, Mat dst);


// ==========================  homeWork ====================================
int hw2_1();
int hw2_2();
int hw2_3();
int hw2_4();
int hw2_1_opencv();
int hw2_2_opencv();
int hw2_3_opencv();
#endif /* Header_hpp */
