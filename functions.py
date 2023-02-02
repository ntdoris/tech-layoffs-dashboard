
'''
Function to prepare user input for use in model that will
generate a prediction. User input should be in following format:
['Aerospace', 'United Kingdom', 10000000, 3, 0.5, 2, 2021, 320, 2018, 50000000]

'''

def prep_pred(example_co):
    
    import pandas as pd
    
    example_df = pd.DataFrame(columns=X.columns[-11:])
    
    ex = example_co
    ex[0] = 'industry_'+ example_co[0]
    ex[1] = 'country_'+ example_co[1]
    ex[5] = 'Number of Employees_'+ example_co[5]
    example_df.rename(columns={'Industries': ex[0], 
                               'Industry Groups': ex[1], 
                               'Number of Employees': ex[5]}, inplace=True)
    
    ex[0] = 1
    ex[1] = 1
    ex[5] = 1
   
    example_df.loc[0] = ex
    
    for col in X_train_processed:
        if col not in example_df:
            print("Adding missing feature {}".format(col))
            example_df[col] = 0
            
    example_df = example_df.reindex(sorted(example_df.columns), axis=1)

    return example_df