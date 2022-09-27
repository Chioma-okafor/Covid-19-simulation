import pandas as pd
import numpy as np
from Covid_model import *
import mesa
df =  pd.read_excel('Parameters.xlsx')      #file that holds parameters for the model


params_key = ['no_agents', 'width', 'height', 
             'exposed_prob', 'infected_prob', 'exposed_tran', 'infected_tran',
             'masked_prob', 'vaccinated_prob', 'masked_dec', 'vaccinated_dec',
             'exposed_period_max', 'exposed_period_min' , 'infected_period_max','infected_period_min', 'immunity_period_max', 'immunity_period_min']
  

df_total = pd.DataFrame()      #create an empty dataframe that will hold the result of the runs


for i in range(df.shape[0]):   #a loop that goes through each parameter set and save it to the database
    params_val = df.iloc[i]
    params = dict(zip(params_key, params_val))
    
    results = mesa.batch_run(          
        Covid_model,
        parameters=params,
        iterations=1,
        max_steps=250,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )
    
    results_df = pd.DataFrame(results)
    results_df['RunId'] = i                                    #set the RunID in the dataframe so they can be differentiated
    df_total=df_total.append(results_df, ignore_index=True)




df_total.to_excel('output.xlsx')     #export the dataframe