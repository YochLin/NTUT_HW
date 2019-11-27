//
//  hw2_3_opencv.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/31.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"


int hw2_3_opencv()
{
    Mat img = imread("hand.bmp");
    Mat imBin;
    cvtColor(img, imBin, COLOR_BGR2GRAY);
    threshold(imBin,imBin, 200, 255, THRESH_BINARY_INV);
    imshow("threshImg", imBin);
//    waitKey(0);
    
    Mat finger;
    Mat closeStruct = getStructuringElement(MORPH_RECT,Size(5,5));
    morphologyEx(imBin, finger, MORPH_CLOSE, closeStruct);
    imshow("closing", finger);
    waitKey(0);
    
    Mat openStruct = getStructuringElement(MORPH_RECT,Size(30,50));
    morphologyEx(finger, finger, MORPH_OPEN, openStruct);
    imshow("opening", finger);
    waitKey(0);
    
    Mat dilateStruct = getStructuringElement(MORPH_RECT,Size(50,45));
    morphologyEx(finger, finger, MORPH_DILATE, dilateStruct);
    imshow("dilate", finger);
    waitKey(0);
    
    Mat lfinger = matNor(imBin, finger);
    imshow("finger", lfinger);
    waitKey(0);
    
    Mat labelImage(img.size(), CV_32S);
    int nLabels = connectedComponents(lfinger, labelImage, 8);
    
    Mat colorImg = matLabelColor(labelImage, nLabels);
    imshow( "Finger Connected Components", colorImg);
    waitKey(0);
    
    //    labelImage = singleDim2threeDim(labelImage);
    //    imBin = singleDim2threeDim(imBin);
    cvtColor(lfinger, lfinger, COLOR_GRAY2BGR);
    //    cvtColor(labelImage, labelImage, CV_GRAY2BGR);
    matBoundingBox(lfinger, labelImage, nLabels);
    imshow("Finger bounding box", lfinger);
    waitKey(0);
    return 0;
}
