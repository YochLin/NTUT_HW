//
//  hw1_3_opencv.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/6.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

Mat BGR2GBR_changeOpenCV(Mat img)
{
    //原始 opencv讀入通道為 BGR => 0: b, 1: g, 2: r
    Mat image(img.rows, img.cols, CV_8UC3);
    for(int i = 0; i < img.rows; i++)
    {
        Vec3b *p1 = img.ptr<Vec3b>(i);
        Vec3b *p2 = image.ptr<Vec3b>(i);
        for(int j = 0; j < img.cols; j++)
        {
            p2[j][0] = p1[j][2];
            p2[j][1] = p1[j][0];
            p2[j][2] = p1[j][1];
        }
    }
    return image;
}

int hw1_3_opencv()
{
    Mat src = imread("lena_rotate_opencv.bmp");
    Mat dst = BGR2GBR_changeOpenCV(src);
    imshow("lena", dst);
    waitKey(0);
    imwrite("lena_channel_changeOpenCV.bmp", dst);
    return 0;
}
