# Welcome to Nick's Playground

This is where I experimented with different approaches to attack the cryptocurrency problem and where I came up with the Target and Stop Loss approach.  While this area is a bit of a mess, the target and stop loss approach has been organized into a pipeline of notebooks which I will discuss here.  I won't necessarily discuss all notebooks here since there use was fleeting but were necessary in the understanding and development of the final pipeline.


A lot of the initial prototyping was performed in the notebook `plotting_mpf_and_features.ipynb`.  The feature engineering in particular was converted to Postgres stored procedures to run off of triggers from new data available from the Binance API.


## Basic Models

### Step 0 - Getting Data

The pipeline discussed in here relies on a data extract from our PostgreSQL database.  To get this, you need access to our database.  If you don't have this you can look at the AWS section for how the data is gathered and stored and do it your own way.  If you have credentials, then in the subfolder `db`, create a `hidden.py` file with the following content and replace the `url`, `db_name`, `username`, and `password` text with your own.

```python
def secrets():
    return {"host": "url",
            "port": 5432,
            "database": "db_name",
            "user": "username",
            "pass": "password"}

def psycopg2(secrets) :
     return ('dbname='+secrets['database']+' user='+secrets['user']+
        ' password='+secrets['pass']+' host='+secrets['host']+
        ' port='+str(secrets['port']))
```

After this, you can run the notebook `build_data_file_with_features.ipynb`.  This will build a pickle file in the subfolder `data` called `candlestick_15m_ETHBTC_{timestamp}.pkl`.

### Step 1 - Building Xy Dataset

For this step, there are two notebooks.  The first is the optional `0_find_atr_ratio.ipynb` notebook since the output is not a file but rather some graphs and knowledge about what might be some good ratios to use in later notebooks.  The second notebook is `1_build_Xy.ipynb` which does what it says on the can.  Meaning, it builds the dataset and the labels.  As discussed in the post, the labeling strategy does have some complexities so running this notebook several times with different parameters is suggested.

In addition to the `X` and `y` pickle files, this notebook outputs a `data_file_hist.pkl` with some information about each dataset generated with this notebook.

### Step 2 - Simulation

The notebook `2_label_data_simulation.ipynb` explores what the maximum profit would be on the labelled test set.  The result is added to the `data_file_hist.pkl`.

For future notebooks, the `data_file_hist.pkl` should now be copied into 3 new files:

- `data_file_hist_all_cols.pkl`
- `data_file_hist_some_cols.pkl`
- `data_file_hist_no_lkbk.pkl`

### Step 3 - Basic Model / Dataset Comparison

To see how different models perform against each of the datasets, the notebook `3_model_dataset_comparison.ipynb` runs 6 classifier models against each dataset.  The process is repeated but with the number of lookback features reduced to 3 and again reduced to 0.

A custom scaler, which scales the data in insoluation from other records in the dataset, is then used to repeat the same process above.


### Step 4 - Rank Best Model / Dataset Combination

In the notebook `4_best_model_dataset.ipynb`, the evaluation results from the previous notebook are ranked based on a ranking algorithm. The successful models were exported using the `model_xxx.ipynb` notebooks.  Grid searches were also explored in the `grid_searches.ipynb` notebook.


### Step 5 - Ensembling and Scaling

The `5a_xxx.ipynb` notebooks focus on the creation of ensemble models using logistic regression and other successful models.  The `5b_xxx.ipynb` notebooks look into scaling or scaling with ensemble.  The scaling used here is the same as mentioned in step 3 and later in the neural network section.

## Deep Neural Networks

In the `torch` folder, pyTorch was used to create a ResNet28 deep neural network.  There are 5 iterations of the `py_torch_mdoel_trainX.ipynb` notebooks:

- `py_torch_model_train1.ipynb` - Initial version usign a ResNet28 model with a "one cycle" scheduler and SGD optimizer.  A standard scaler is also used but is fit/saved outside the model.
- `py_torch_model_train2.ipynb` - The scheduler was removed, optimizer was changed to Adam, and standard scaler was integrated into the model.  Also adds support for limiting features (removing lookbacks).  The loss function can also now be configured to control the `pos_weight` with the goal of improving precision.
- `py_torch_model_train3.ipynb` - This version uses a fully connected neural network instead of the ResNet28.  Optimizer was changed back to SGD and feature limiting was removed.
- `py_torch_model_train4.ipynb` - Back to ResNet28 and SGD optimizer.  This time using the custom scaler.
- `py_torch_model_train5.ipynb` - Changed the optimizer to AdamW and moved custom scaler to `py` file to support AWS structure.

To visualize the results, the models are saved with training/validation data for each epoch.  The notebook `py_torch_model_validation.ipynb` extracts this from the trained models and plots the data and the configurations so differenceds in models can be seen both in the graphs and in the table.

The `py_torch_sim_validate.ipynb` notebook puts the models through a simulator to see how profitable (or not) a trained model becomes.
