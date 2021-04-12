# DSAI_2021_HW02

## :camera_flash: Running my code
*   Hardware Environment Requirement
    *   In this repo, I utilize `tensorflow v2.3.1` with `cuda v10.2` and `cuDNN v7.6.5` on my PC.
    *   GPU of my computer: `NVIDIA GeForce GTX 1070`
    *   Under this hardware environment, the GPU acceleration works.
    *   If GPU acceleration is not available, computer will spend more time on training phase. (But still in a acceptable range)
*   Virtual Python Environment
    *   If you use `virtualenv`, launch your environment and run `pip install -r requiements.txt`.
    *   If you use `pipenv`, run `pipenv install` after your environment is created.
        *   If you failed to run `pipenv install` due to failed lock, run `pipenv lock --pre` to resolve failed lock.
        *   The failed locking is due to `mplfinance` Python Module.
*   **!!!Plese put all of your input file in the directory *datasets*!!!**
    *   Or the trader cannot read the file correctly.     
*   Run trader.py to output output.csv, some log info will show on your screen.
*   Example with using `pipenv`
```shell
$ pipenv run python trader.py
2021-04-13 00:48:20.186112: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudart.so.10.1
2021-04-13 00:48:21.144 | SUCCESS  | __main__:<module>:20 -   DSAI 2021 Spring Homework 02 - AutoTrading  
2021-04-13 00:48:21.144 | SUCCESS  | __main__:<module>:21 - <-- This code is written By Steven HH Chen -->
-----------------------------------------------------------------------------------------------------------------------
2021-04-13 00:48:21.144 | INFO     | __main__:<module>:25 - Reading input arguments...
2021-04-13 00:48:21.145 | DEBUG    | __main__:<module>:39 - Training data input csv file    -> ./datasets/training.csv
2021-04-13 00:48:21.146 | DEBUG    | __main__:<module>:40 - Testing data input csv file     -> ./datasets/testing.csv
2021-04-13 00:48:21.146 | DEBUG    | __main__:<module>:41 - Model Prediction Outcome Output -> ./output.csv
2021-04-13 00:48:21.146 | SUCCESS  | __main__:<module>:43 - <-----------------------------------Data Input Phase----------------------------------->
2021-04-13 00:48:21.146 | INFO     | __main__:<module>:45 - Reading training set data...
2021-04-13 00:48:21.150 | INFO     | __main__:<module>:47 - Reading testing set data...
2021-04-13 00:48:21.151 | SUCCESS  | __main__:<module>:53 - <---------------------------------Preprocessing Phase---------------------------------->
...
2021-04-13 00:48:21.275 | DEBUG    | dataprocessor.inputStockData:train_validation_split:45 - Training Size: 1114, Validation Size: 372
2021-04-13 00:48:21.275 | SUCCESS  | __main__:<module>:67 - <-----------------------------------Training Phase------------------------------------->
2021-04-13 00:48:21.275 | INFO     | __main__:<module>:68 - Train LSTM Model: 1 to 2
2021-04-13 00:48:21.276 | DEBUG    | predictor.stockLSTM:train:21 - Training Size: 1114, Validation Size: 372
...
2021-04-13 00:48:21.978 | DEBUG    | predictor.stockLSTM:train:37 - Fitting Model, please wait for a moment...
2021-04-13 00:48:33.016 | DEBUG    | predictor.stockLSTM:train:41 - Final Epoch Count: 50, Training Loss: 0.0004, Validation Loss: 0.0011
2021-04-13 00:48:33.016 | SUCCESS  | __main__:<module>:71 - <----------------------------------Inference Phase------------------------------------->
2021-04-13 00:48:33.017 | INFO     | __main__:<module>:72 - Do inference to obtain price prediction of stock
...
2021-04-13 00:48:33.221 | SUCCESS  | __main__:<module>:78 - <---------------------------------Postprocessing Phase---------------------------------->
2021-04-13 00:48:33.221 | INFO     | __main__:<module>:79 - Generate trading sequence by inference result
...
2021-04-13 00:48:33.222 | INFO     | __main__:<module>:85 - Write trading sequence to output.csv
2021-04-13 00:48:33.222 | INFO     | __main__:<module>:88 - Evaluate profit by output trading sequence
...
2021-04-13 00:48:33.223 | SUCCESS  | __main__:<module>:91 - Evaluated Profit: 3.68
$ ls -l output.csv
-rw-rw-r-- 1 netdb-ml netdb-ml 42  四  13 00:48 output.csv
```

## 🗜️ Highlight of each phase in trader.py.
*   Data Input Phase 
    *   Input training and testing csv data
*   Preprocessing Phase
    *   Do normalization for each training and testing input
    *   Encode time series data input and output for fitting model.
        *   Format: input today`s data, output next day and next two day`s data
    *   Split encoded time series data into training set and validation set
*   Training Phase
    *   Utilize LSTM by Keras, with the structure downward:
    *   Train 50 epoches with early stopping callback.
```shell
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
lstm (LSTM)                  (None, 10)                600       
_________________________________________________________________
dense (Dense)                (None, 1)                 11        
_________________________________________________________________
repeat_vector (RepeatVector) (None, 2, 1)              0         
=================================================================
Total params: 611
Trainable params: 611
Non-trainable params: 0
_________________________________________________________________
```
*   Infernece Phase
    *   Input normalized testing data to model, call `model.predict()` to implement inferencing task.
    *   Do simple performance analysis ->  Compare rising/falling trend with ground truth.
*   Postprocessing Phase
    *   **Based on inference result, evaluate trend of stock price for next two days.**
    *   **Then, cooperate with rule-based action determiner to output assigned action.**
        *   **Implement with very simple if-statement based on personal strategy and experience on real stock market.**
    *   Check correctness of returned trading sequence in Python list data format, then write this sequence to `output.csv`.
    *   In final, the profit is calculated by generated trading sequence.
        *   current optimal profit: **5.32**
        *   May be more or less due to training situation.
* We use some Python modules to finish our work
    *   NumPy, Pandas, Tensorflow, Keras, Logru...etc. 

# Reference
[LSTM Mode with Keras](https://medium.com/@daniel820710/%E5%88%A9%E7%94%A8keras%E5%BB%BA%E6%A7%8Blstm%E6%A8%A1%E5%9E%8B-%E4%BB%A5stock-prediction-%E7%82%BA%E4%BE%8B-1-67456e0a0b)
