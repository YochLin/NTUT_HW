//
//  hw1_3.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/3.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"



int hw1_3()
{
    /************************** Declare Variable **************************/
    char path[] = "RotateImage.bmp";
    char outPath[] = "channelChange.bmp";
    RGB *pixel = new RGB[512*512];
    RGB *outPixel = new RGB[512*512];
    HEADER header;
    
    /***************** Process: Read -> change channel -> Write *************/
    readBmp(pixel, path, &header);
    channelChange(pixel, outPixel, "GBR");
    writeBmp(outPixel, outPath, &header);
    
    delete [] pixel;
    delete [] outPixel;
    return 0;
}
