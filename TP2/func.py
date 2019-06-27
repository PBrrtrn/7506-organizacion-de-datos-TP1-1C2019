import numpy as np
import pandas as pd

def generateSessions(df, timeDiff="60 min"):
    """
        Genera sesiones para el dataframe segun el tiempo entre interacciones
    """
    dfSorted = df.sort_values(by=["ip_address", "date"])[["ip_address", "date"]]
    nextEvents = dfSorted[["date"]]                                                 
    nextEvents.index = nextEvents.index-1
    ev = nextEvents.loc[nextEvents.index[-1]]
    nextEvents.loc[nextEvents.index[-1]+1] = ev
    dfSorted = dfSorted.join(nextEvents.loc[0:], rsuffix="_next")
    dfSorted["date_next"] = dfSorted.date_next - dfSorted.date
    breakIndexes = (dfSorted.groupby("ip_address")["date"].count().cumsum()-1).values
    dfSorted.loc[breakIndexes, ["date_next"]] = np.nan
    serSes = dfSorted.groupby("ip_address")["date_next"].transform(lambda x: x > pd.Timedelta(timeDiff))
    dfSorted["session_number"] = serSes
    dfSorted["session_number"] = dfSorted.groupby("ip_address")["session_number"].transform(lambda x: x.cumsum())
    dfSorted.session_number = dfSorted.groupby(["ip_address"]).session_number.shift(1).fillna(0)
    dfSorted = dfSorted.drop(["date_next", "date", "ip_address"], axis=1)
    return dfSorted["session_number"]

#def installSessions(df):
    """
        Genera sesiones se instalaciones
    """
#    dfSorted = df.sort_values(by=["ip_address", "date"])[["ip_address", "date","event_id"]]
    
    
    
    
    
    
    