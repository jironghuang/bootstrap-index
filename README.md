# bootstrap-index

1. The aim of this package is to produce indexes of dataset used for Walk Forward Optimization.
2. Walk Forward Analysis optimizes on a training set; test on a period after the set and then rolls it all forward and repeats the process. There are multiple out-of-sample periods and the combined results can be analyzed.
3. To faciliate Walk Forward Analysis, the package produces start and end of block bootstrap indexes within each training set data chunk.
4. Block boostrap indexes basically represents continuous chunks of time series indexes that are sampled with replacement within a training set data chunk. You may optimize your parameters within each of these block boostrapped data chunks and averaged them to be tested on testing dataset. 
5. There is a 'window' argument that allows you to divide the data through a sliding or expanding window. See <a href="https://stackoverflow.com/questions/59854723/backtesting-which-is-better-sliding-window-or-expanding-window#:~:text=When%20you%20come%20up%20to,the%20Expanding%20Window%20form%20better.">here</a> for further explanations on sliding and expanding window.

## Examples

### Initiating class

```
import pandas as pd
import numpy as np
import random
import io
import requests
from bootstrapindex import bootstrapindex

url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
s=requests.get(url).content
data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.set_index('Date', inplace=True)    

bootstrap = bootstrapindex(data, window='sliding', #expanding
                            num_samples_per_period=10, 
                            min_sample_size=300, 
                            prop_block_bootstrap=0.25, 
                            days_block=252, 
                            starting_index = 5
                            )   
```
### Creating in-sample and out-of-sample index

```
import pandas as pd
import numpy as np
import random
import io
import requests
from bootstrapindex import bootstrapindex

url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
s=requests.get(url).content
data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.set_index('Date', inplace=True)           
bootstrap = bootstrapindex(data, window='sliding', #expanding
                            num_samples_per_period=10, 
                            min_sample_size=300, 
                            prop_block_bootstrap=0.25, 
                            days_block=252, 
                            starting_index = 5
                            )        
bootstrap = bootstrap_index(data)
bootstrap.create_window_index()
Out[93]: 
[[[0, 251], [252, 503]],
 [[0, 503], [504, 755]],     
...            
```

### Producing block boostrap indexes from a data chunk

```
import pandas as pd
import numpy as np
import random
import io
import requests
from bootstrapindex import bootstrapindex

url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
s=requests.get(url).content
data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.set_index('Date', inplace=True)       
bootstrap = bootstrapindex(data, window='sliding', #expanding
                            num_samples_per_period=10, 
                            min_sample_size=300, 
                            prop_block_bootstrap=0.25, 
                            days_block=252, 
                            starting_index = 5
                            )        
bootstrap.extract_block_bootstrap_periods(sample_size = 100, start_sample_index = 50, end_sample_index = 500)
Out[143]: 
{'start_index': array([247, 118,  78, 171, 170, 368, 343, 215, 166, 287]),
 'end_index': array([372, 243, 203, 296, 295, 493, 468, 340, 291, 412])} 
```


### Producing block boostrap indexes from all training set data chunks

```
import pandas as pd
import numpy as np
import random
import io
import requests
from bootstrapindex import bootstrapindex

url="https://github.com/jironghuang/trend_following/raw/main/quantopian_data/futures_incl_2016.csv"
s=requests.get(url).content
data=pd.read_csv(io.StringIO(s.decode('utf-8')))    
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data.set_index('Date', inplace=True)    

bootstrap = bootstrapindex(data, window='sliding', #expanding
                            num_samples_per_period=10, 
                            min_sample_size=300, 
                            prop_block_bootstrap=0.25, 
                            days_block=252, 
                            starting_index = 5
                            )
bootstrap.create_dictionary_window_n_bootstrap_index()
bootstrap.expanding_windows_w_bootstrap_info
Out[132]: 
{1: {'in_sample_index': [5, 256],
  'out_sample_index': [257, 508],
  'bootstrap_index': {'start_index': array([3, 1, 0, 1, 1, 4, 4, 2, 1, 3]),
   'end_index': array([252, 250, 249, 250, 250, 253, 253, 251, 250, 252])}},
 2: {'in_sample_index': [257, 508],
  'out_sample_index': [509, 760],
  'bootstrap_index': {'start_index': array([ 98,  34,  14,  60,  60, 159, 203,  82,  58, 118]),    
...
```
