//
//  hw1_bonus.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/3.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

int hw1_bonus()
{
    /************************** Declare Variable **************************/
    char lena64Path[] = "lena64.bmp";
    char lena1024Path[] = "lena1024.bmp";
    char lenaCropPath[] = "lena_cropped.bmp";
    char output64Path[] = "lena64_rotate.bmp";
    char output1024Path[] = "lena1024_roate.bmp";
    char outputCropPath[] = "lenaCrop_rotate.bmp";
    RGB *lena64Pixel = new RGB[64*64];
    RGB *lena1024Pixel = new RGB[1024*1024];
    RGB *lenaCropPixel = new RGB[512*288];
    HEADER header64;
    HEADER header1024;
    HEADER headerCrop;
    
    /******************** Process: Read -> Rotation -> Write ****************/
    readBmp(lena64Pixel, lena64Path, &header64);
    readBmp(lena1024Pixel, lena1024Path, &header1024);
    readBmp(lenaCropPixel, lenaCropPath, &headerCrop);
    RGB *outputPixel64 = rotationImg(lena64Pixel, 90, &header64);
    RGB *outputPixel1024 = rotationImg(lena1024Pixel, 90, &header1024);
    RGB *outputCropPixel = rotationImg(lenaCropPixel, 90, &headerCrop);
//    for(int i = 0; i < 512; i++)
//    {
//        for(int j = 0; j < 288; j++)
//        {
//            cout << (int)(*(outputCropPixel + i * 288 + j)).r << " ";
//        }
//    }
    writeBmp(outputPixel64, output64Path, &header64);
    writeBmp(outputPixel1024, output1024Path, &header1024);
    writeBmp(outputCropPixel, outputCropPath, &headerCrop);
    
    delete [] lena64Pixel;
    delete [] lena1024Pixel;
    delete [] lenaCropPixel;
    delete [] outputPixel64;
    delete [] outputPixel1024;
    delete [] outputCropPixel;
    return 0;
}
