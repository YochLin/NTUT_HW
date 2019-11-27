//
//  hw2_3.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/30.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//


#include "Header.hpp"

int hw2_3()
{
    char threshPath[] = "threshHand.bmp";
    char dilatePath[] = "dilate.bmp";
    char closePath[] = "closing.bmp";
    char openPath[] = "opening.bmp";
    char fingerPath[] = "finger.bmp";
    
    RGB *pixel = new RGB[926 * 486];
    int maskClose[2] = {7, 7};
    int maskOpen[2] = {40, 30};
    int mask[2] = {25, 45};
    Header header;
    RGB *pixelBuffer = new RGB[926 * 486];
    
    readBmp(pixel, threshPath, &header);
//    readBmp(pixelBuffer, threshPath, &header);
    memcpy(pixelBuffer, pixel, 3 * header.heigh * header.width);
    
    closing(pixel,maskClose, header);
    writeBmp(pixel, closePath, &header);

    opening(pixel, maskOpen, header);
    writeBmp(pixel, openPath, &header);

    dilation(pixel, mask, header);
    writeBmp(pixel, dilatePath, &header);

    nor(pixel, pixelBuffer, header);
    writeBmp(pixelBuffer, fingerPath, &header);

    delete [] pixel;
    delete [] pixelBuffer;
    return 0;
}
