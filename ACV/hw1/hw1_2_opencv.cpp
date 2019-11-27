//
//  hw1_2_opencv.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/3.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw1_2_opencv()
{
    Mat src = imread("InputImage1.bmp");
    Mat dst;
    Mat dst1;
    flip(src, dst, 1);
    transpose(dst, dst1);
    
    imshow("lena", dst1);
    waitKey(0);
    imwrite("lena_rotate_opencv.bmp", dst1);
    return 0;
}
