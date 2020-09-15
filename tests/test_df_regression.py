import pytest
import pandas as pd 



def test_df_diff(df_regression):

    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4.0]})
    df2 = pd.DataFrame({"a": [1, 2], "b": [3, 4.0]})

    # pick on df1 or df2 
    df_regression.check(df2)