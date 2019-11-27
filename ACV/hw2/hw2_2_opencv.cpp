//
//  hw2_2_opencv.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/31.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"


int hw2_2_opencv()
{
    Mat img = imread("hand.bmp");
    Mat imBin;
    cvtColor(img, imBin, COLOR_BGR2GRAY);
    threshold(imBin,imBin, 200, 255, THRESH_BINARY_INV);
    imshow("threshImg", imBin);
    waitKey(0);
    
    Mat labelImage(img.size(), CV_32S);
    int nLabels = connectedComponents(imBin, labelImage, 8);

    Mat colorImg = matLabelColor(labelImage, nLabels);
    imshow( "Connected Components", colorImg);
    waitKey(0);
    
//    labelImage = singleDim2threeDim(labelImage);
//    imBin = singleDim2threeDim(imBin);
    cvtColor(imBin, imBin, COLOR_GRAY2BGR);
//    cvtColor(labelImage, labelImage, CV_GRAY2BGR);
    matBoundingBox(imBin, labelImage, nLabels);
    imshow("bounding box", imBin);
    waitKey(0);
    
    return 0;
}
