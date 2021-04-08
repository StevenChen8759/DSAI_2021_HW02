# Data visualizer for input data...
# This code is written by Steven HH Chen.

# Python internal module import
import os
from datetime import datetime

# Python external module import
from loguru import logger
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates

# User module import

@logger.catch
def drawKbar(input_df, df_title):

    # Draw CandleStick Chart
    # Ref: https://saralgyaan.com/posts/python-candlestick-chart-matplotlib-tutorial-chapter-11/
    # Ref: https://stackoverflow.com/questions/61238162/why-cant-i-import-candlestick-ohlc-from-mplfinance

    df_draw = input_df.reset_index()

    plt.style.use('ggplot')

    # Extracting Data for plotting
    # TODO: add column name and date information
    ohlc = df_draw.loc[:, ['index', 'Open', 'High', 'Low', 'Close']]
    '''ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)'''

    # Creating Subplots
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='red', colordown='green', alpha=0.8)

    # Setting labels & titles
    ax.set_xlabel('Data No')
    ax.set_ylabel('Price')
    fig.suptitle(f'Daily Candlestick Chart of {df_title}')

    # Formatting Date
    '''date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()'''

    fig.tight_layout()

    if not os.path.isdir('output'):
        os.mkdir('output')
    
    opname = f"./output/cschart_{df_title}_{datetime.now(): %Y-%m-%dT%H-%M-%S}.jpg"
    plt.savefig(opname)