from Model import *
import numpy as np
from trainGan import dataProcessing, one_hot_encoder
import sys

### 訓練 CNN 來辨識 驗證碼

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need save model name!!')
        sys.exit()
    datas, labels = dataProcessing('./Extract_image/')   ### 重新取得 data & label
    model = CNN_discriminator(num_classes = 26)
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    dd = np.expand_dims(datas, axis=3)   ## (846,28,28) => (846,28,28,1)
    history = model.fit(dd, labels,  epochs=1000, batch_size=32, shuffle=True)
    model.save(sys.argv[1])