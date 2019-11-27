//
//  hw1_1.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/10/1.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

using namespace std;

int hw1_1(){
    /************************** Declare Variable **************************/
    cout << "hw1:\n";
    char path[] = "InputImage1.bmp";
    char outPath[] = "OutputImage.bmp";
    RGB *pixel = new RGB[512*512];
    
    /*********************** Process: Read -> Write ************************/
    HEADER header;
    readBmp(pixel, path, &header);
    writeBmp(pixel, outPath, &header);
    delete [] pixel;
    return 0;
}
