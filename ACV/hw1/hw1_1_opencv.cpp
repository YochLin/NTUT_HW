//
//  hw1_1_opencv.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/3.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw1_1_opencv()
{
    Mat pixel = imread("InputImage1.bmp");
    imshow("lena", pixel);
    waitKey(0);
    imwrite("OutputImageOpenCV.bmp", pixel);
    return 0;
}
