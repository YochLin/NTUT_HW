//
//  hw2_1_opencv.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/30.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw2_1_opencv()
{
    Mat src = imread("hand.bmp");
    Mat dst;
    cvtColor(src, dst, COLOR_BGR2GRAY);
    threshold(dst, dst, 200, 255, THRESH_BINARY_INV);
    imshow("OpenCV binary Hand", dst);
    waitKey(0);
    return 0;
}
