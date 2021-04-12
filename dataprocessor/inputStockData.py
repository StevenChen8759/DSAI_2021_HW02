# Preprocessor -> Input Stock Data
# This code is written by Steven HH Chen.

# Python internal module import

# Python external module import
import numpy as np
from loguru import logger

# User module import

def normalize(ip_train, norm_function):
    train_norm = ip_train.apply(norm_function)
    return train_norm


def encode_tsdata(input_df, iplen=1, oplen=1):
    assert(iplen >= 1 and oplen >= 1)

    iplist = []
    oplist = []
    for iter in range(iplen, len(input_df.index) - oplen + 1):
        ip_part = input_df.loc[iter - iplen:iter - 1].to_numpy()
        op_part = input_df["Open"].loc[iter:iter + oplen - 1].to_numpy()

        iplist.append(ip_part)
        oplist.append(op_part)

    # Input Data:  (N, 1, 4)
    # Output Data: (N, 1, 4)

    ret_ipdata = np.concatenate(iplist, axis=0).reshape(len(iplist), iplen, 4)
    ret_opdata = np.concatenate(oplist, axis=0).reshape(len(oplist), oplen, 1)

    return ret_ipdata, ret_opdata


def train_validation_split(input_nptuple, validation_ratio):

    data_in, data_out = input_nptuple

    trainingSize = round(len(data_in) * (1 - validation_ratio))
    validationSize = round(len(data_in)  * validation_ratio)

    logger.debug(f"Training Size: {trainingSize}, Validation Size: {validationSize}")

    train_in = data_in[validationSize:]
    train_out = data_out[validationSize:]

    validation_in = data_in[:validationSize]
    validation_out = data_out[:validationSize]

    return (train_in, train_out), (validation_in, validation_out)