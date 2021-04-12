# Data processor -> Output Stock Data
# This code is written by Steven HH Chen.

# Python internal module import

# Python external module import
import numpy as np
from loguru import logger

# User module import

# Make decision of stock trend
def makeTradeSequence(ipStock, infresult, order=1):
    trade_sequence = []
    status = 0
    for i in range(len(infresult) - 1):

        op_price = ipStock["Open"][i]
        decision = 0

        # Predict small rising
        if 0 < infresult[i][1][0] - op_price <= 0.03:
            # Make decision
            if status == 1:
                decision = 0    # (一般持有且預測小漲，觀望)
            elif status == -1:
                decision = 1    # (套利持有且預測小漲，買入獲利了結)
            else:
                # (尚無持有且預測小漲，考量明日與後日預測價差)
                if infresult[i][1][0] - infresult[i][0][0] > 0:   # 預測後天較明天上漲, 買進
                    decision = 1
                elif infresult[i][1][0] - infresult[i][0][0] < 0: # 預測後天較明天下跌, 賣出
                    decision = -1
        # Predict large rising
        elif infresult[i][1][0] - op_price > 0.03:
            # Make decision
            if status == 1:
                decision = 0    # (一般持有且預測大漲，觀望)
            elif status == -1:
                decision = 1    # (套利持有且預測大漲，買入獲利了結)
            else:
                decision = 1    # (尚無持有且預測大漲，買進)
        # Predict small falling
        elif -0.03 <= infresult[i][1][0] - op_price < 0:
            # Make decision
            if status == 1:
                decision = -1   # (一般持有且預測小跌，賣出獲利了結)
            elif status == -1:
                decision = 0    # (套利持有且預測小跌，觀望)
            else:
                # (尚無持有且預測小跌，考量明日與後日預測價差)
                if infresult[i][1][0] - infresult[i][0][0] > 0:   # 預測後天較明天上漲, 買進
                    decision = 1
                elif infresult[i][1][0] - infresult[i][0][0] < 0: # 預測後天較明天下跌, 賣出
                    decision = -1
        # Predict large falling
        elif infresult[i][1][0] - op_price  < -0.03:
            # Make decision
            if status == 1:
                decision = -1   # (一般持有且預測大跌，賣出獲利了結)
            elif status == -1:
                decision = 0    # (套利持有且預測大跌，觀望)
            else:
                decision = -1   # (尚無持有且預測大跌，套利賣出)

        trade_sequence.append(decision)
        status = status + decision


    # print(len(trade_sequence), trade_sequence)
    return trade_sequence