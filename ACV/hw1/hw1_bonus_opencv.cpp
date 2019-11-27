//
//  hw1_bonus_opencv.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/6.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

Mat roate_opencv(char *path, int angle, float scale)
{
    Mat src = imread(path);
    Mat dst;
    Mat dst1;
    flip(src, dst, 1);
    transpose(dst, dst1);
    
    return dst1;
}

int hw1_bonus_opencv()
{
    char lena64Path[] = "lena64.bmp";
    char lena1024Path[] = "lena1024.bmp";
    char lenaCropPath[] = "lena_cropped.bmp";
    Mat dst64 = roate_opencv(lena64Path, 90, 1.0);
    Mat dst1024 = roate_opencv(lena1024Path, 90, 1.0);
    Mat dstCrop = roate_opencv(lenaCropPath, 90, 0.6);
    imshow("lena64", dst64);
    imshow("lena1024", dst1024);
    imshow("lenaCrop", dstCrop);
    waitKey(0);
    imwrite("lena64_rotate_opencv.bmp", dst64);
    imwrite("lena1024_rotate_opencv.bmp", dst1024);
    imwrite("lenaCrop_rotate_opencv.bmp", dstCrop);
    return 0;
}
