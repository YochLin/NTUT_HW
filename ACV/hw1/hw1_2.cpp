//
//  hw1_2.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/2.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw1_2()
{
    /************************** Declare Variable **************************/
    char path[] = "InputImage1.bmp";
    char outPath[] = "RotateImage.bmp";
    RGB *pixel = new RGB[512*512];
    HEADER header;
    
    /******************** Process: Read -> Rotation -> Write ****************/
    readBmp(pixel, path, &header);
    RGB *outputPixel = rotationImg(pixel, 90, &header);
    writeBmp(outputPixel, outPath, &header);
    
    delete [] pixel;
    delete [] outputPixel;
    return 0;
}
