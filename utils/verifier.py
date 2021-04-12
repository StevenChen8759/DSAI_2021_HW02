# Verify Output Value of the model
# This code is written by Steven HH Chen.

# Python internal module import

# Python external module import
import numpy as np
from loguru import logger

# User module import

def statusVerify(input_sequence):
    logger.debug("Do output status verification")
    status = 0
    for iter in range(len(input_sequence)):
        assert(-1 <= status <= 1)
        if input_sequence[iter] == 0:
            continue
        elif input_sequence[iter] == 1:
            if status == 1:
                logger.error(f"Verify failed: Action +1 while status is 1 at {iter}")
                return False
            else:
                status = status + 1
        elif input_sequence[iter] == -1:
            if status == -1:
                logger.error(f"Verify failed: Action -1 while status is -1 at {iter}")
                return False
            else:
                status = status - 1
    logger.success("Verification Passed!")

def trendPerf(ipStock, infresult, iplen=1, oplen=1):
    rhit, rmiss, fhit, fmiss = 0, 0, 0, 0

    for order in range(oplen):
        rhit, rmiss, fhit, fmiss = 0, 0, 0, 0
        # print(f"Verify Trend of future {order + 1} day(s)...")
        for i in range(len(infresult) - 1 - order):
            op_price = ipStock["Open"][i:i + oplen + 1].reset_index(drop=True)
            
            if op_price[0] <= op_price[order + 1]:      # Rising Price

                # Statistics Data
                diff = infresult[i][order][0] - op_price[0]
                if op_price[0] <= infresult[i][order][0]:   # Predicted Price is also rising 
                    # print(f"[{i}] Rising Trend Hit", end="")
                    rhit = rhit + 1
                else:
                    # print(f"[{i}] Rising Trend Miss", end="")
                    rmiss = rmiss + 1
            else:                                      # Falling Price

                # Statistics Data
                diff = op_price[0] - infresult[i][order][0]
                if  op_price[0] > infresult[i][order][0]:   # Predicted Price is also falling
                    # print(f"[{i}] Falling Trend Hit", end="")
                    fhit = fhit + 1
                else:
                    # print(f"[{i}] Falling Trend Miss", end="")
                    fmiss = fmiss + 1

            # print(f", {op_price[0]:.2f} -> {op_price[order + 1]:.2f}({infresult[i][order][0]:.2f}), predicted diff: {diff:.2f}")
        logger.debug(f"Trend of future {order + 1} day(s): Rising Hit: {rhit}, Rising Miss: {rmiss}, Falling Hit: {fhit}, Falling Miss: {fmiss}")


@logger.catch
def profitEval(input_df, mani_sequence):
    status = 0
    overall_profit = 0
    cost_record = 0

    for iter in range(len(input_df.index) - 1):
        # print(f"[{iter}] {input_df['Open'][iter]} -> {input_df['Open'][iter + 1]}, Stat: {status}, Mani: {mani_sequence[iter]}")
        assert(-1 <= status <= 1)

        # Buy one stock
        if mani_sequence[iter] == 1:
            if status == 0:
                # Calculate sell hold cost
                cost_record = input_df["Open"][iter + 1]
                # print(f"Buy Hold 1, cost: {cost_record}")
            elif status == -1:
                # Calculate sell short profit
                temp = (cost_record - input_df["Open"][iter + 1])
                overall_profit = overall_profit + temp
                logger.debug(f"Buy Short 1, cost: {input_df['Open'][iter + 1]}, gain: {cost_record}, profit: {temp:.2f}, acc_profit: {overall_profit:.2f}")
                
        elif mani_sequence[iter] == -1:
            if status == 1:
                # Calculate sell hold profit
                temp = (input_df["Open"][iter + 1] - cost_record)
                overall_profit = overall_profit + temp
                logger.debug(f"Sell Hold 1, cost: {cost_record}, gain: {input_df['Open'][iter + 1]}, profit: {temp:.2f}, acc_profit: {overall_profit:.2f}")
            elif status == 0:
                # Calculate sell short cost
                cost_record = input_df["Open"][iter + 1]
                # print(f"Sell short 1, cost: {cost_record}")

        # Update status
        status = status + mani_sequence[iter]

    # Calculate Final Profit
    if status == 1:
        # Calculate sell hold profit
        temp = input_df["Close"][iter + 1] - cost_record
        overall_profit = overall_profit + temp
        logger.debug(f"Final Sell Hold 1, cost: {cost_record}, gain: {input_df['Close'][iter + 1]}, profit: {temp:.2f}, acc_profit: {overall_profit:.2f}")
    elif status == -1:
        # Calculate sell short profit
        temp = cost_record - input_df["Close"][iter + 1]
        overall_profit = overall_profit + temp
        plogger.debug(f"Final Buy Short 1, cost: {input_df['Close'][iter + 1]}, gain: {cost_record}, profit: {temp:.2f}, acc_profit: {overall_profit:.2f}")

    return overall_profit
