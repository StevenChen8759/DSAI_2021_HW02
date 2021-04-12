# Preprocessor -> stock LSTM
# This code is written by Steven HH Chen.

# Python internal module import

# Python external module import
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, RepeatVector, Dense
from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow_addons import <normalizer>
from loguru import logger

# User module import

# 1-To-1 Model
def train(stockTrain, stockValidation, iplen=1, oplen=1):
    # Split Input stockData to training and vaildation set
    trainingSize = len(stockTrain[0])
    validationSize = len(stockValidation[0])
    logger.debug(f"Training Size: {trainingSize}, Validation Size: {validationSize}")

    train_in, train_out = stockTrain
    print(train_in.shape[1])

    model = Sequential()
    model.add(LSTM(10, activation='relu', input_shape=(iplen, 4), return_sequences=False))
    # output shape: (2, 4)
    # model.add(TimeDistributed(Dense(4))) 
    model.add(Dense(1))
    model.add(RepeatVector(2))
    model.compile(loss="mse", optimizer="adam")

    logger.debug("Model structure...")
    model.summary()

    logger.debug("Fitting Model, please wait for a moment...")
    callback = EarlyStopping(monitor="val_loss", patience=25, verbose=1, mode="auto")
    fitinfo = model.fit(train_in, train_out, epochs=50, batch_size=16, verbose=0, validation_data=stockValidation, callbacks=[callback])
    cntEpoch = len(fitinfo.history['val_loss'])
    logger.debug(f"Final Epoch Count: {cntEpoch}, Training Loss: {fitinfo.history['loss'][cntEpoch - 1]:.4f}, Validation Loss: {fitinfo.history['val_loss'][cntEpoch - 1]:.4f}")
    return model

def inference(model, stockInference, iplen=1, oplen=1):

    # Stock data turns to Numpy ndarray
    stockData_inf = stockInference.to_numpy().reshape(len(stockInference.index), 1, 4)

    # Do inference
    result = model.predict(stockData_inf, batch_size=8, verbose=1)

    return result # + np.random.uniform(-0.04, 0.04, result.shape)