//
//  Header.cpp
//  hw1
//
//  Created by Yoch Lin on 2019/9/30.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"



void readBmp(RGB *pixel, char *path, HEADER *header){
    ifstream fin;
    cout << "Read Bmp file: " << path << endl;
    fin.open(path, ios::in|ios::binary);
    if(!fin){
        cout << "can't open file." << endl;
        system("pasue");
        exit(0);
    }
    else{
        fin.read((char*)header->header, 54*sizeof(uchar));
        header->width = *(int*)&header->header[18];
        header->heigh = *(int*)&header->header[22];
        fin.read((char*)pixel, header->width * header->heigh * sizeof(RGB));
    }
    fin.close();
}

void writeBmp(RGB *pixel, char *path, HEADER *header){
    ofstream fout;
    cout << "Write Bmp file: " << path << endl;
    fout.open(path, ios::out|ios::binary);
    if(!fout){
        cout << "Can't open file" << endl;
    }
    else{
        *(int*)&header->header[18] = header->width;
        *(int*)&header->header[22] = header->heigh;
        fout.write((char*)header->header, 54*sizeof(char));
        fout.write((char*)pixel, header->width * header->heigh * sizeof(RGB));
    }
    cout << "Write out Bmp file: " << path << endl;
    fout.close();
}

RGB *rotationImg(RGB *pixel, int angle, HEADER *header)
{
    int c, r, x, y, tmp, other_width, other_heigh; // x,y: coordinate  r,c, ch: row, column, channel, tmp: store size
    int x0, y0;  // x0, y0: original
    float anglePI = angle * CV_PI / 180;
    RGB *outputPixel = new RGB[header->width * header->heigh];

//    if(header->width != header->heigh)
//    {
//        other_heigh = header->width;
//        other_width = header->heigh;
//    }
//    else
//    {
//        other_heigh = header->heigh;
//        other_width = header->width;
//    }
    if(header->width != header->heigh)
    {
        tmp = header->width;
        header->width = header->heigh;
        header->heigh = tmp;
    }
    
    x0 = (header->width - 1) / 2;
    y0 = (header->heigh - 1) / 2;
    
    for(r=0; r < header->heigh; r++)
    {
        for(c=0; c < header->width; c++)
        {
            
            if(header->width == header->heigh)
            {
//                x0 = (header->width - 1) / 2;
//                y0 = (header->heigh - 1) / 2;
                x = (int)((r - y0) * cos(anglePI) - (c - x0) * sin(anglePI) + 0.5);
                y = (int)((r - y0) * sin(anglePI) + (c - x0) * cos(anglePI) + 0.5);
                x += x0;
                y += y0;
                if(x >= header->width || y > header->heigh || x < 0 || y < 0)
                {
                    (*(outputPixel + r * header->width + c)).r = 0;
                    (*(outputPixel + r * header->width + c)).g = 0;
                    (*(outputPixel + r * header->width + c)).b = 0;
                }
                else
                {
                    (*(outputPixel +  r * header->width + c)).r = (*(pixel + x * header->width + y)).r;
                    (*(outputPixel +  r * header->width + c)).g = (*(pixel + x * header->width + y)).g;
                    (*(outputPixel +  r * header->width + c)).b = (*(pixel + x * header->width + y)).b;
                }
            }
            else
            {
//                x0 = (header->heigh - 1) / 2;
//                y0 = (header->width - 1) / 2;
                x = (int)((r - y0) * cos(anglePI) - (c - x0) * sin(anglePI) + 0.5);
                y = (int)((r - y0) * sin(anglePI) + (c - x0) * cos(anglePI) + 0.5);
                x += x0;
                y += y0;
                
                if(x >= header->width || y > header->heigh || x < 0 || y < 0)
                {
                    (*(outputPixel + c * header->heigh + r)).r = 0;
                    (*(outputPixel + c * header->heigh + r)).g = 0;
                    (*(outputPixel + c * header->heigh + r)).b = 0;
                }
                else
                {
                    (*(outputPixel +  r * header->width + c)).r = (*(pixel + x * header->heigh + y)).r;
                    (*(outputPixel +  r * header->width + c)).g = (*(pixel + x * header->heigh + y)).g;
                    (*(outputPixel +  r * header->width + c)).b = (*(pixel + x * header->heigh  + y)).b;
                }
            }
        }
    }
    return outputPixel;
}

void channelChange(RGB *pixel, RGB *outputPixel, char const *chageType)
{
    if(strcmp(chageType, "GBR") == 0)
    {
        for(int i = 0; i < 512*512; i++)
        {
            outputPixel[i].r = pixel[i].g;
            outputPixel[i].g = pixel[i].b;
            outputPixel[i].b = pixel[i].r;
        }
    }
    else if(strcmp(chageType, "BGR") == 0)
    {
        for(int i = 0; i < 512*512; i++)
        {
            outputPixel[i].r = pixel[i].b;
            outputPixel[i].g = pixel[i].g;
            outputPixel[i].b = pixel[i].r;
        }
    }
    else if(strcmp(chageType, "GRB") == 0)
    {
        for(int i = 0; i < 512*512; i++)
        {
            outputPixel[i].r = pixel[i].g;
            outputPixel[i].g = pixel[i].r;
            outputPixel[i].b = pixel[i].b;
        }
    }
    else if(strcmp(chageType, "BRG") == 0)
    {
        for(int i = 0; i < 512*512; i++)
        {
            outputPixel[i].r = pixel[i].b;
            outputPixel[i].g = pixel[i].r;
            outputPixel[i].b = pixel[i].g;
        }
    }
    else if(strcmp(chageType, "RGB") == 0)
    {
        for(int i = 0; i < 512*512; i++)
        {
            outputPixel[i].r = pixel[i].r;
            outputPixel[i].g = pixel[i].g;
            outputPixel[i].b = pixel[i].b;
        }
    }
}

