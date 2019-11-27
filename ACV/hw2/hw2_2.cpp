//
//  hw2_2.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/24.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//
//  Topic: Label the five hands with 4-connected neighbor

#include "Header.hpp"


int hw2_2()
{
    char testPath[] = "threshHand.bmp";
    char colorLabePath[] = "colorHand.bmp";
    char detectPath[] = "detectHand.bmp";
    RGB *pixel = new RGB[926 * 486];
    Header header;
    readBmp(pixel, testPath, &header);

    RGB *labelPixel = connectedComponent(pixel, header);
    RGB *colorLabelImg = labelColorSet(labelPixel, header);
    boundingBox(pixel, labelPixel, header);
    findCentralPoint(pixel, labelPixel, header);
    writeBmp(colorLabelImg, colorLabePath, &header);
    writeBmp(pixel, detectPath, &header);
    delete [] pixel;
    delete [] labelPixel;
    delete [] colorLabelImg;
    return 0;
}
