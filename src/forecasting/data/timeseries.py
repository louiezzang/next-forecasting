import numpy as np
import pandas as pd
from torch.utils.data import Dataset


class TimeSeriesDataset(Dataset):
    """
    Args:
        data (pd.DataFrame): dataframe containing raw data
        entity_column (str): name of column containing entity data
        time_column (str): name of column containing date data
        target_column (str): name of column we need to predict
        input_columns (list): list of string names of columns used as input
        encoder_steps (int): number of known past time steps used for forecast. Equivalent to size of LSTM encoder
        decoder_steps (int): number of input time steps used for each forecast date. Equivalent to the width N of the decoder
    """
    def __init__(self, 
                 data: pd.DataFrame, 
                 entity_column: str, 
                 time_column: str, 
                 target_column: str, 
                 input_columns: list, 
                 encoder_steps: int, 
                 decoder_steps: int):
        self.encoder_steps = encoder_steps
             
        inputs = []
        outputs = []
        entity = []
        time = []

        for e in data[entity_column].unique():
          entity_group = data[data[entity_column]==e]
          
          data_time_steps = len(entity_group)

          if data_time_steps >= decoder_steps:
            x = entity_group[input_columns].values.astype(np.float32)
            inputs.append(np.stack([x[i:data_time_steps - (decoder_steps - 1) + i, :] for i in range(decoder_steps)], axis=1))

            y = entity_group[[target_column]].values.astype(np.float32)
            outputs.append(np.stack([y[i:data_time_steps - (decoder_steps - 1) + i, :] for i in range(decoder_steps)], axis=1))

            e = entity_group[[entity_column]].values.astype(np.float32)
            entity.append(np.stack([e[i:data_time_steps - (decoder_steps - 1) + i, :] for i in range(decoder_steps)], axis=1))

            t = entity_group[[time_column]].values.astype(np.int64)
            time.append(np.stack([t[i:data_time_steps - (decoder_steps - 1) + i, :] for i in range(decoder_steps)], axis=1))

        self.inputs = np.concatenate(inputs, axis=0)
        self.outputs = np.concatenate(outputs, axis=0)[:, encoder_steps:, :]
        self.entity = np.concatenate(entity, axis=0)
        self.time = np.concatenate(time, axis=0)
        self.active_inputs = np.ones_like(outputs)

        self.sampled_data = {
            "inputs": self.inputs,
            "outputs": self.outputs[:, self.encoder_steps:, :],
            "active_entries": np.ones_like(self.outputs[:, self.encoder_steps:, :]),
            "time": self.time,
            "identifier": self.entity
        }
        
    def __getitem__(self, index):
        s = {
            "inputs": self.inputs[index],
            "outputs": self.outputs[index], 
            "active_entries": np.ones_like(self.outputs[index]), 
            "time": self.time[index],
            "identifier": self.entity[index],
            "index": int(self.inputs[index, 0, -1]) 
        }

        return s

    def __len__(self):
        return self.inputs.shape[0]
