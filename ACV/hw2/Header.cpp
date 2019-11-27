//
//  Header.cpp
//  hw2
//
//  Created by Yoch Lin on 2019/10/21.
//  Copyright © 2019 Yoch Lin. All rights reserved.
//

#include "Header.hpp"

// =====================================  RGB data process ====================================
void showRGBPixelValue(RGB *pixel, Header header)
{
    for(int i = 0; i < header.heigh; i++){
        for(int j = 0; j < header.width; j++){
            cout << "r: " << (int)(pixel + i * header.width + j)->r << " ";
            cout << "g: " << (int)(pixel + i * header.width + j)->g << " ";
            cout << "b: " << (int)(pixel + i * header.width + j)->b << endl;
            cout << "i: " << i << " j: " << j << endl;
        }
    }
}

void inRGBSameValue(RGB *pixel, int pixelIndex, int value){
    /*將 value 放入 pixel 的 pixelIndex 位置內*/
    pixel[pixelIndex].r = value;
    pixel[pixelIndex].g = value;
    pixel[pixelIndex].b = value;
}

// =====================================   Read & Write ====================================
void readBmp(RGB *pixel, char *path, Header *header)
{
    /*
     參考本篇概念：https://charlottehong.blogspot.com/2017/06/c-raw-bmp.html
     透過該篇文章了解到 BMP 由左下到右上讀取，而每個寬都需要為4的倍數
     所以才需要將寬那部分做處理成4的倍數以利存取資訊
     還有看到可以將3通道RGB轉換成單通道灰階做存取
     但目前用的方法是將三通道像素值都設為相同再存入
     */
    ifstream fin;
    fin.open(path, ios::in|ios::binary);
    if(!fin)
    {
        cout << "Can't open file" << endl;
        system("pause");
        exit(0);
    }
    else
    {
        fin.read((char*)header->information, sizeof(header->information));
        header->width = *(int*)&header->information[18];
        uint16_t bitCount = header->information[28];             // RGB 為 24 位元、 黑白為 8 位元,   uint16_t 為 2 bytes
        cout << "bitCount: " << bitCount << "位元" << endl;
        size_t realW = header->width * bitCount>>3;              // 24位元/8 為 3 通道 乘上寬
        size_t alig = (realW*3) % 4;                             // 要與4對齊，所以取 4 的餘數找出每一行讀取後需要空多少位置
        header->heigh = *(int*)&header->information[22];
        //        fin.read((char*)pixel, sizeof(RGB) * header->width * header->heigh);
        for(int i = 0; i < header->heigh; i++){
            for(int j = 0; j < header->width; j++){
                fin.read((char*)(pixel + i * header->width + j), sizeof(RGB));
                //                fin.read((char*)(pixel + i * header->width + j)->b, sizeof(uchar));
                //                fin.read((char*)(pixel + i * header->width + j)->g, sizeof(uchar));
                //                fin.read((char*)(pixel + i * header->width + j)->r, sizeof(uchar));
            }
            fin.seekg(alig, std::ios::cur);     // 跳開對齊的空格
        }
    }
    cout << "Read down: " << path << endl;
    fin.close();
}

void writeBmp(RGB *pixel, char *path, Header *header)
{
    ofstream fout;
    fout.open(path, ios::out|ios::binary);
    if(!fout)
    {
        cout << "Can't open file" << endl;
        system("pause");
        exit(0);
    }
    else
    {
        uint16_t bitCount = header->information[28];
        size_t realW = header->width * bitCount>>3;
        size_t alig = (realW*3) % 4;
        *(int*)&header->information[18] = header->width;       // 將寬放入
        *(int*)&header->information[22] = header->heigh;       // 將高放入
        fout.write((char*)header->information, sizeof(header->information));
        //        fout.write((char*)pixel, header->rowSize * header->heigh);
        for(int i = 0; i < header->heigh; i++){
            for(int j = 0; j < header->width; j++){
                fout.write((char*)(pixel+ i * header->width + j), sizeof(RGB));  // r
            }
//            fout.seekp(alig, std::ios::cur); // 跳開對齊的空格
            for(int i = 0; i < alig; ++i){  // 由於讀取要對齊 4 的倍數需跳過幾個位元，但寫入就要將讀取跳過的寫進去(補0)
                fout << uchar(0);
            }
        }
    }
    cout << "Write down: " << path << endl;
    fout.close();
}


// =====================================  Gary  &  thresholod ====================================
RGB *RGB2Gray(RGB *pixel, Header header)
{
    int index;
    RGB *grayPixel = new RGB[header.width * header.heigh];
    cout << "RGB image to Gary ..." << endl;
    for(int i = 0; i < header.heigh; i++)
    {
        for(int j = 0; j < header.width; j++)
        {
            index = i * header.width + j;
            uchar gray = (*(pixel + i * header.width + j)).r * 0.299 + (*(pixel + i * header.width + j)).g * 0.587 + (*(pixel + i * header.width + j)).b * 0.114 + 0.5;     // 根據 RGB 轉灰階公式，將每個通道乘上不同倍率
            inRGBSameValue(grayPixel, index, gray);
//            (*(grayPixel + i * header.width + j)).r = gray;
//            (*(grayPixel + i * header.width + j)).g = gray;
//            (*(grayPixel + i * header.width + j)).b = gray;
            
        }
    }
    return grayPixel;
}

uchar thrsholdDetermine(uchar pixelValue, int threshValue)
{
    /*
     判斷每個像素點是否大於設的閥值
     */
    if (pixelValue < threshValue) return 255;
    else return 0;
}

RGB *thresHoldGrayBmp(RGB *pixel, Header header, int threshold)
{
    /*
     將 bmp RGB 轉為灰階
     */
    cout << "image threshold ..." << endl;
    RGB *binaryImg = new RGB[header.heigh * header.width];
    
    for(int i = 0; i < header.heigh; i++)
    {
        for(int j = 0; j < header.width; j++)
        {
            uchar pixelValueR = (*(pixel + i * header.width + j)).r;
            uchar pixelValueG = (*(pixel + i * header.width + j)).g;
            uchar pixelValueB = (*(pixel + i * header.width + j)).b;
            (*(binaryImg + i * header.width + j)).r = thrsholdDetermine(pixelValueR, threshold);
            (*(binaryImg + i * header.width + j)).g = thrsholdDetermine(pixelValueG, threshold);
            (*(binaryImg + i * header.width + j)).b = thrsholdDetermine(pixelValueB, threshold);
        }
    }
    return binaryImg;
}



// =====================================   Conneted Component ====================================
void PushQueue(Queue *queue, int data){
    QNode *p = new QNode[sizeof(QNode)];
    p->data = data;
    if(queue->first == NULL){
        queue->first = p;
        queue->last = p;
        p->next = NULL;
    }
    else{
        p->next = NULL;
        queue->last->next = p;
        queue->last = p;
    }
}

int PopQueue(Queue *queue){
    QNode *p = NULL;
    int data;
    if(queue->first == NULL){
        return -1;
    }
    p = queue->first;
    data = p->data;
    if(queue->first->next == NULL){
        queue->first = NULL;
        queue->last = NULL;
    }
    else{
        queue->first = p->next;
    }
    delete [] p;
    return data;
}

void searchNeighborLabel(RGB *src, RGB *labelImg, int label, int pixelIndex, Header header, Queue *queue)
{
    int searchIndex;   // 搜尋的座標
    int length = header.width * header.heigh;    // 圖片總長度
    int neighborDirection[8][2] = {{0,1},{1,1},{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1}};  // 該位置附近鄰居
    inRGBSameValue(labelImg, pixelIndex, label);
    for(int i = 0; i < 8; i++){
        searchIndex = pixelIndex + header.width * neighborDirection[i][0] + neighborDirection[i][1];
        if(searchIndex > 0 && searchIndex < length && src[searchIndex].r != 0 && labelImg[searchIndex].r == 0){
            inRGBSameValue(labelImg, searchIndex, label);
            PushQueue(queue, searchIndex);
        }
    }
}

RGB *connectedComponent(RGB *src, Header header)
{
    /*參考：http://www.voidcn.com/article/p-brykzkxg-bbr.html，透過種子填充法將pixel周圍的位置給填上Label，然後再去找pixel周圍的像素其周圍，重覆找下去*/
    cout << "Conneted Component Ing..." << endl;
    clock_t start, end;
    double cpu_time_used;
    int index, popIndex, label = 0;
    RGB *labelImg = new RGB[header.heigh * header.width]{};
    Queue *queue = new Queue[sizeof(Queue)];
    queue->first = NULL;
    queue->last = NULL;
    start = clock();
    for(int i = 0; i < header.heigh; i++){
        for(int j = 0; j < header.width; j++){
            index = i * header.width + j;
            if(src[index].r != 0 && labelImg[index].r == 0){
                label++;
                searchNeighborLabel(src, labelImg, label, index, header, queue);
                cout << "目前點位置： " << "x: " << j << " y: " << i << " Connected label: " << label << endl;
                popIndex = PopQueue(queue);
                while (popIndex > -1) {
                    searchNeighborLabel(src, labelImg, label, popIndex, header, queue);
                    popIndex = PopQueue(queue);
                }
                
            }
        }
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Connected Component spend time: " << cpu_time_used << " s " << endl;
    delete [] queue;
    return labelImg;
}

uchar *colorSet()
{
    // 亂數給定 rgb 顏色
    uchar *rgb = new uchar[3]{};   // 每次呼叫，每次生成新位址
    uchar r = 255 * (rand()/(1.0 + RAND_MAX));
    uchar g = 255 * (rand()/(1.0 + RAND_MAX));
    uchar b = 255 * (rand()/(1.0 + RAND_MAX));
    rgb[0] = r;
    rgb[1] = g;
    rgb[2] = b;
    return rgb;
}

RGB *labelColorSet(RGB *pixel, Header header)
{
    cout << "label color set: " << endl;
    // 將每個 Label 上不同顏色
    int i, j, index, pixelValue, num = 0;
    map<int, uchar*> colors;        // 透過 map 的 key, value 特性來做後續的判斷
    RGB *colorLabelPixel = new RGB[header.width * header.heigh]{};
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            index = i * header.width + j;
            pixelValue = pixel[index].r;
            if(pixelValue > 0){
                if(!colors.count(pixelValue)){      // 判斷該 pixel 的值是否有在 key 上
                    colors[pixelValue] = colorSet();  /* 這邊卡了很久，原因是之前的寫法會將每個key指向相同位址，導致不同個key，value會相同，所以 function 那邊要新增一個動態記憶體，每次呼叫每次給新的位址*/
                    num++;
                }
                colorLabelPixel[index].r = colors[pixelValue][0];
                colorLabelPixel[index].g = colors[pixelValue][1];
                colorLabelPixel[index].b = colors[pixelValue][2];
            }
        }
    }
    cout << "總類別顏色數： " << num << endl;
    return colorLabelPixel;
}

// =====================================   Bounding Box ====================================
void compareIndex(int x, int y, int *indexXY)
{
    /*比較每個點的大小*/
    if(x > indexXY[0]) indexXY[0] = x;
    if(y > indexXY[1]) indexXY[1] = y;
    if(x < indexXY[2]) indexXY[2] = x;
    if(y < indexXY[3]) indexXY[3] = y;
}

void drawBounding(RGB *src, map<int, int*> area, Header header)
{
    int i, j, k;
    for(i = 1; i < area.size(); i++){
        for(j = area[i][3]; j < area[i][1]; j++){   // 畫橫條
            int xMax = j * header.width + area[i][0];
            int xMin = j * header.width + area[i][2];
            src[xMax].r = 255;
            src[xMin].r = 255;
        }
        for(k = area[i][2]; k < area[i][0]; k++){ // 畫直條
            int yMax = area[i][1] * header.width + k;
            int yMin = area[i][3] * header.width + k;
            src[yMax].r = 255;
            src[yMin].r = 255;
        }
    }
}

map<int, int*> findAreaMaxIndex(RGB *labelImg, Header header)
{
    int i, j, index, pixelValue;
    map<int, int*> area;
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            index = i * header.width + j;
            pixelValue = labelImg[index].r;
            if(pixelValue > 0){
                if(!area.count(pixelValue)){
                    int maxX = INT_MIN, maxY = INT_MIN, minX = INT_MAX, minY = INT_MAX;
                    int *indexXY = new int[4]{maxX, maxY, minX, minY};   // 生成新的位址做存放
                    compareIndex(j, i, indexXY);
                    area[pixelValue] = indexXY;
                    cout << "生成 Label: " << pixelValue << " 最大座標 " << endl;
                }
                compareIndex(j, i, area[pixelValue]);
            }
        }
    }
    return area;
}

void boundingBox(RGB *src, RGB *labelImg, Header header)
{
    cout << "Bounding Box Ing..." << endl;
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    map<int, int*> area = findAreaMaxIndex(labelImg, header);
    for(int k = 1; k < area.size(); k++){
        cout << "Bounding Box: " << k << " ";
        cout << " x max: " << area[k][0] << " y max: " << area[k][1] << " x min: " << area[k][2] << " y min: " << area[k][3] << endl;
    }
    drawBounding(src, area, header);
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Bounding Box spend time: " << cpu_time_used << " s " << endl;
}

//void findCentralPoint(RGB *src, RGB *labelImg, Header header){
//    int i, j, index, width, heigh, newX, newY, area;
//    int neighborDirection[8][2] = {{0,1},{1,1},{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1}};  // 該位置附近鄰居
//    map<int, int*> region = findAreaMaxIndex(labelImg, header);
//    for(i = 1; i < region.size(); i++){
//        heigh = region[i][1] - region[i][3];
//        width = region[i][0] - region[i][2];
//        area = heigh * width;
//        newX = width / 2 + region[i][2];
//        newY = heigh / 2 + region[i][3];
//        index = newY * header.width + newX;
//        src[index].r = 255;
//        src[index].g = 0;
//        src[index].b = 0;
////        for(j = 0; j < 8; j++){
//////            src[index + j].r = 255;
//////            src[index + j].g = 0;
//////            src[index + j].b = 0;
////            src[index + neighborDirection[i][0] * header.width + neighborDirection[i][1]].r = 255;
////            src[index + neighborDirection[i][0] * header.width + neighborDirection[i][1]].g = 0;
////            src[index + neighborDirection[i][0] * header.width + neighborDirection[i][1]].b = 0;
////        }
//        cout << "Label: " << i << " Area compute: " << area << endl;
//    }
//}

void findCentralPoint(RGB *src, RGB *labelImg, Header header)
{
    int l, i, j, k, index, newX, newY;
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    map<int, int*> region = findAreaMaxIndex(labelImg, header);
    int neighborDirection[8][2] = {{0,1},{1,1},{1,0},{1,-1},{0,-1},{-1,-1},{-1,0},{-1,1}};  // 該位置附近鄰居
    for(l = 1; l < region.size(); l++){
        int x = 0, y = 0, area = 0;
        for(i = region[l][3]; i < region[l][1]; i++){
            for(j = region[l][2]; j < region[l][0]; j++){
                index = i * header.width + j;
                if(labelImg[index].r == l){
                    area += 1;
                    x += j;
                    y += i;
                }
            }
        }
        if(area > 0){
            newX = x / area;
            newY = y / area;
            src[newY * header.width + newX].r = 255;
            src[newY * header.width + newX].g = 0;
            src[newY * header.width + newX].b = 0;
            for(k = 0; k < 8; k++){     // 該中心點周圍 8 點都畫上顏色
                src[(newY + neighborDirection[k][0]) * header.width + (newX + neighborDirection[k][1])].r = 255;
                src[(newY + neighborDirection[k][0]) * header.width + (newX + neighborDirection[k][1])].g = 0;
                src[(newY + neighborDirection[k][0]) * header.width + (newX + neighborDirection[k][1])].b = 0;
            }
            cout << "CentralLabel: " << l << " Area compute: " << area << " X: " << newX << " Y: " << newY<< endl;
        }
    }
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Find Central Point spend time: " << cpu_time_used << " s " << endl;
}

// =====================================   morphology algorithms ====================================
RGB *padding(RGB *src, int widthPadding, int heighPadding, int *mask, Header header)
{
    int i, j, indexDst, indexSrc;
    RGB *dst = new RGB[(header.width + widthPadding) * (header.heigh + heighPadding)]{};
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            indexDst = (i + heighPadding / 2) * header.width + (j + widthPadding / 2);
            indexSrc = i * header.width + j;
            dst[indexDst].r = src[indexSrc].r;
            dst[indexDst].g = src[indexSrc].g;
            dst[indexDst].b = src[indexSrc].b;
        }
    }
    return dst;
}


void dilation(RGB *src, int *mask, Header header)
{
    int i, j, l, m, index, maskIndex;
//    int *kernelArray = new int[mask[0] * mask[1]]();
    int widthPadding = mask[0] - 1;
    int heighPadding = mask[1] - 1;
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    RGB *dst = padding(src, widthPadding, heighPadding, mask, header);   // 將原始圖做 padding 補0，以利後續做遮罩處理
//    for(k = 0; k < mask[0] * mask[1]; k++){
//        *(kernelArray + k) = 255;
//    }
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            int temNum = 0;
            for(l = 0; l < mask[0]; l++){           // 遮罩迴圈
                for(m = 0; m < mask[1]; m++){
                    index = (i + l) * header.width + (j + m);   // Padding 過的圖點位置
                    maskIndex = l * mask[1] + m;
                    if(temNum < dst[index].r){   // 判斷 kernel 周圍是否有與圖片白點相交，有像素點會大於 temNum，後續直接補 temNum
                        temNum = dst[index].r;
                    }
                }
            }
            src[i * header.width + j].r = temNum;
            src[i * header.width + j].g = temNum;
            src[i * header.width + j].b = temNum;
        }
    }
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Dilation spend time: " << cpu_time_used << " s " << endl;
}

void erosion(RGB *src, int *mask, Header header)
{
    int i, j, l, m, index, maskIndex;
    //    int *kernelArray = new int[mask[0] * mask[1]]();
    int widthPadding = mask[0] - 1;
    int heighPadding = mask[1] - 1;
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    RGB *dst = padding(src, widthPadding, heighPadding, mask, header);   // 將原始圖做 padding 補0，以利後續做遮罩處理
    //    for(k = 0; k < mask[0] * mask[1]; k++){
    //        *(kernelArray + k) = 255;
    //    }
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            int temNum = 255;
            for(l = 0; l < mask[0]; l++){           // 遮罩迴圈
                for(m = 0; m < mask[1]; m++){
                    index = (i + l) * header.width + (j + m);   // Padding 過的圖點位置
                    maskIndex = l * mask[1] + m;
                    if(dst[index].r == 0){   // 判斷 kernel 周圍是否有與圖片白點相交，有像素點會大於 temNum，後續直接補 temNum
                        temNum = dst[index].r;
                    }
                }
            }
            src[i * header.width + j].r = temNum;
            src[i * header.width + j].g = temNum;
            src[i * header.width + j].b = temNum;
        }
    }
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Erosion spend time: " << cpu_time_used << " s " << endl;
}

void opening(RGB *src, int *mask, Header header)
{
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    erosion(src, mask, header);
    dilation(src, mask, header);
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Opening spend time: " << cpu_time_used << " s " << endl;
}

void closing(RGB *src, int *mask, Header header)
{
    clock_t start, end;
    double cpu_time_used;
    start = clock();
    dilation(src, mask, header);
    erosion(src, mask, header);
    end = clock();
    // 計算實際花費時間
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    cout << "Closing spend time: " << cpu_time_used << " s " << endl;
}

void nor(RGB *src, RGB *dst, Header header)
{
    int i, j, index;
    for(i = 0; i < header.heigh; i++){
        for(j = 0; j < header.width; j++){
            index = i * header.width + j;
            if(src[index].r == dst[index].r){
                dst[index].r = 0;
                dst[index].g = 0;
                dst[index].b = 0;
            }
        }
    }
}


// =====================================   openCV functions ====================================
Mat matLabelColor(Mat labelImage, int nLabels)
{
    std::vector<Vec3b> colors(nLabels);
    colors[0] = Vec3b(0, 0, 0);//background
    for(int label = 1; label < nLabels; ++label){
        colors[label] = Vec3b( (rand()&255), (rand()&255), (rand()&255) );
    }
    
    Mat dst(labelImage.size(), CV_8UC3);
    for(int r = 0; r < dst.rows; ++r){
        for(int c = 0; c < dst.cols; ++c){
            int label = labelImage.at<int>(r, c);
            Vec3b &pixel = dst.at<Vec3b>(r, c);
            pixel = colors[label];
        }
    }
    return dst;
}

Mat matSingleDim2threeDim(Mat imBin)
{
    Mat im_coloured = Mat::zeros(imBin.rows,imBin.cols,CV_8UC3);
    vector<Mat> planes;
    for(int i=0;i<3;i++)
        planes.push_back(imBin);
    merge(planes,im_coloured);
    return im_coloured;
}

void matBoundingBox(Mat binImg, Mat labelImg, int nLabels)
{
    int r, c, k, pixelLabel, centralX, centralY;
    Point point1, point2;
    for(k = 1; k < nLabels; ++k){
        int region[2] = {0};
        int area = 0;
        int maxX = INT_MIN, maxY = INT_MIN, minX = INT_MAX, minY = INT_MAX;
        for(r = 0; r < labelImg.rows; r++){
            for(c = 0; c < labelImg.cols; c++){
                pixelLabel = labelImg.at<int>(r, c);
                if(pixelLabel == k){
                    maxX = max(maxX, c);
                    maxY = max(maxY, r);
                    minX = min(minX, c);
                    minY = min(minY, r);
                    area += 1;
                    region[0] += r;
                    region[1] += c;
                }
            }
        }
        cout << "label: " << k << " ";
        point1.x = minX;
        point1.y = maxY;
        point2.x = maxX;
        point2.y = minY;
        //        area = (maxX - minX) * (maxY - minY);
        if(area > labelImg.rows && area > labelImg.cols){
            rectangle(binImg, point1, point2, Scalar(0, 0, 255), 1);
            cout << "Area: " << area << " ";
            centralX = region[1] / area;
            centralY = region[0] / area;
            cout << "centralX: " << centralX << " centralY: " << centralY << endl;
            //            rectangle(binImg, point1, point2, Scalar(0, 0, 255), 1);
            rectangle(binImg, Point(centralX - 1, centralY - 1), Point(centralX + 1, centralY + 1), Scalar(0, 0, 255), -1);
            //            binImg.at<Vec3b>(centralY, centralX) = Vec3b(0, 0, 255);
        }
    }
}

Mat matNor(Mat src, Mat dst)
{
    int r, c;
    Mat srcBuffer;
    src.copyTo(srcBuffer);
    for(r = 0; r < srcBuffer.rows; r++){
        for(c = 0; c < srcBuffer.cols; c++){
            if(srcBuffer.at<uchar>(r, c) == dst.at<uchar>(r, c)){
                srcBuffer.at<uchar>(r, c) = srcBuffer.at<uchar>(r, c) - dst.at<uchar>(r, c);
            }
        }
    }
    return srcBuffer;
}
