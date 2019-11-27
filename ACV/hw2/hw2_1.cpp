//
//  hw2_1.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/21.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//
//  Topic: Generate a binarized image with threshold 200

#include "Header.hpp"



int hw2_1()
{
    char path[] = "hand.bmp";
    char grayPath[] = "grayHand.bmp";
    char threshPath[] = "threshHand.bmp";
    RGB *pixel = new RGB[926*486];
    Header header;

    readBmp(pixel, path, &header);
    RGB *grayPixel = RGB2Gray(pixel, header);
    RGB *threshImg = thresHoldGrayBmp(grayPixel, header, 200);

    
    writeBmp(grayPixel, grayPath, &header);
    writeBmp(threshImg, threshPath, &header);
    
    delete [] pixel;
    delete [] grayPixel;
    delete [] threshImg;
    return 0;
}
