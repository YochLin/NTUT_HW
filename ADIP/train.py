from model import *
from dataProcessing import generate_data, load_data
from keras.callbacks import EarlyStopping, ModelCheckpoint

IMG_WIDTH = 256
IMG_HEIGHT = 256
TRAIN_PATH = 'xxxx'   ## 圖片路徑
TRAIN_MASK = 'xxxx'   ## 遮罩路徑 
#########  將圖片 & 遮罩路徑轉為 txt
txtWriter(TRAIN_PATH, TRAIN_MASK, './DataAndMask/Train')

### 將剛剛產生的 txt 讀取
train = generate_data('./humanparsing/TestHuman.txt', 16, IMG_WIDTH, IMG_HEIGHT)
checkpointer = ModelCheckpoint('./humanparsing/model-person_testSeg.h5', monitor='loss', verbose=1, save_best_only=True)
model = UnetModel()
result = model.fit_generator(train,
                        steps_per_epoch=  17808 // 16,
#                         validation_data=val,
#                         validation_steps=5000 // 16,
                        epochs=50,
                        callbacks=[checkpointer])

