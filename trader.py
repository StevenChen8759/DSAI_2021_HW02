# Trader - entry of this homework
# This code is written by Steven HH Chen.

# Python internal module import
import argparse

# Python external module import
import numpy as np
import pandas as pd
from loguru import logger

# User module import
from utils import dataIO, visualizer, verifier
from dataprocessor import inputStockData, outputStockData
from predictor import stockLSTM


if __name__ == "__main__":

    logger.success("  DSAI 2021 Spring Homework 02 - AutoTrading  ")
    logger.success("<-- This code is written By Steven HH Chen -->")

    print("-----------------------------------------------------------------------------------------------------------------------")

    logger.info("Reading input arguments...")
    parser = argparse.ArgumentParser()

    parser.add_argument('--training',
                        default='training.csv',
                        help='input training data file name')
    parser.add_argument('--testing',
                        default='testing.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')

    args = parser.parse_args()
    logger.debug(f"Training data input csv file    -> ./datasets/{args.training}")
    logger.debug(f"Testing data input csv file     -> ./datasets/{args.testing}")
    logger.debug(f"Model Prediction Outcome Output -> ./{args.output}")

    logger.success("<-----------------------------------Data Input Phase----------------------------------->")
    stockCol = ["Open", "High", "Low", "Close"]
    logger.info("Reading training set data...")
    stockTrain = dataIO.read_csv_to_pandas_df(f"./datasets/{args.training}", stockCol)
    logger.info("Reading testing set data...")
    stockTest = dataIO.read_csv_to_pandas_df(f"./datasets/{args.testing}", stockCol)

    # visualizer.drawKbar(stockTrain, "train")
    # visualizer.drawKbar(stockTest, "test")

    logger.success("<---------------------------------Preprocessing Phase---------------------------------->")
    normfunc = lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x))

    logger.info("Normalize training set data...")
    stockTrain_norm = inputStockData.normalize(stockTrain, normfunc)
    logger.info("Normalize testing set data...")
    stockTest_norm = inputStockData.normalize(stockTest, normfunc)

    logger.info("Encode Time Series Data - 1 to 2")
    stockTrain_ts_1_2 = inputStockData.encode_tsdata(stockTrain_norm, 1, 2)

    logger.info("Split training data for training phase...")
    stock_tsTrain_1_2, stock_tsValidation_1_2 = inputStockData.train_validation_split(stockTrain_ts_1_2, 0.25)

    logger.success("<-----------------------------------Training Phase------------------------------------->")
    logger.info("Train LSTM Model: 1 to 2")
    lstm_1_2 = stockLSTM.train(stock_tsTrain_1_2, stock_tsValidation_1_2, 1, 2)

    logger.success("<----------------------------------Inference Phase------------------------------------->")
    logger.info("Do inference to obtain price prediction of stock")
    infresult = stockLSTM.inference(lstm_1_2, stockTest_norm, 1, 2)
 
    logger.info("Check rising/falling trend by inference result")
    verifier.trendPerf(stockTest_norm, infresult, 1, 2)

    logger.success("<---------------------------------Postprocessing Phase---------------------------------->")
    logger.info("Generate trading sequence by inference result")
    trade_sequence = outputStockData.makeTradeSequence(stockTest_norm, infresult)

    logger.info("Check trading sequence is valid or not")
    verifier.statusVerify(trade_sequence)

    logger.info(f"Write trading sequence to {args.output}")
    dataIO.write_trade_sequence(args.output, trade_sequence)

    logger.info("Evaluate profit by output trading sequence")
    profit = verifier.profitEval(stockTest, trade_sequence)
    if profit > 0:
        logger.success(f"Evaluated Profit: {profit:.2f}")
    elif profit == 0:
        logger.warning(f"Evaluated Profit: {profit:.2f}")
    else:
        logger.error(f"Evaluated Profit: {profit:.2f}")

    