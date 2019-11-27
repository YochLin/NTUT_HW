//
//  hw2_4.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/31.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw2_4()
{
    char fingerPath[] = "finger.bmp";
    char detectPath[] = "fingerDetect.bmp";
    char colorLabePath[] = "fingerLabelColor.bmp";
    RGB *fingerPixel = new RGB[926 * 486];
    Header header;
    
    readBmp(fingerPixel, fingerPath, &header);
    RGB *labelPixel = connectedComponent(fingerPixel, header);
    RGB *colorLabelImg = labelColorSet(labelPixel, header);
    boundingBox(fingerPixel, labelPixel, header);
    findCentralPoint(fingerPixel, labelPixel, header);
    writeBmp(colorLabelImg, colorLabePath, &header);
    writeBmp(fingerPixel, detectPath, &header);
    
    delete [] fingerPixel;
    delete [] labelPixel;
    delete [] colorLabelImg;
    return 0;
}
