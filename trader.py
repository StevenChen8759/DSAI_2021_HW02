# Trader - entry of this homework
# This code is written by Steven HH Chen.

# Python internal module import
import argparse

# Python external module import
import pandas as pd
from loguru import logger

# User module import
from utils import dataIO, visualizer

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
    logger.debug(f"Model Prediction Outcome Output -> ./output/{args.output}")

    stockCol = ["Open", "High", "Low", "Close"]
    stockTrain = dataIO.read_csv_to_pandas_df(f"./datasets/{args.training}", stockCol)
    stockTest = dataIO.read_csv_to_pandas_df(f"./datasets/{args.testing}", stockCol)

    # visualizer.drawKbar(stockTrain, "train")
    # visualizer.drawKbar(stockTest, "test")