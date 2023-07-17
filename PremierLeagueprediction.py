#!/usr/bin/env python
# coding: utf-8

# In[111]:


import pandas as pd


# In[112]:


matches = pd.read_csv("matches.csv", index_col=0)


# In[113]:


matches.head()


# In[114]:


matches.shape


# In[115]:


# 2 seasons * 20 squads * 38 matches

2 * 20 * 38


# In[116]:


matches[matches["team"] == "Arsenal"].sort_values("date")


# In[117]:


matches["round"].value_counts()


# In[118]:


matches.dtypes


# In[119]:


matches["date"] = pd.to_datetime(matches["date"])


# In[120]:


matches.dtypes


# In[121]:


matches["target"] = (matches["result"] == "W").astype("int")


# In[122]:


matches


# In[123]:


matches["venue_code"] = matches["venue"].astype("category").cat.codes


# In[124]:


matches


# In[125]:


matches["venue_code"] = matches["venue"].astype("category").cat.codes


# In[126]:


matches


# In[127]:


matches["opp_code"] = matches["opponent"].astype("category").cat.codes


# In[128]:


matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")


# In[129]:


matches["day_code"] = matches["date"].dt.dayofweek


# In[130]:


matches.dtypes


# In[131]:


matches


# In[132]:


from sklearn.ensemble import RandomForestClassifier


# In[133]:


rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)


# In[134]:


train = matches[matches["date"] < '2022-01-01']


# In[135]:


test = matches[matches["date"] > '2022-01-01']


# In[136]:


predictors = ["venue_code", "opp_code", "hour", "day_code"]


# In[137]:


rf.fit(train[predictors], train["target"])


# In[138]:


preds = rf.predict(test[predictors])


# In[139]:


from sklearn.metrics import accuracy_score


# In[140]:


acc = accuracy_score(test["target"], preds)


# In[141]:


acc


# In[142]:


combined = pd.DataFrame(dict(actual=test["target"], predicted=preds))


# In[143]:


pd.crosstab(index=combined["actual"], columns=combined["predicted"])


# In[144]:


from sklearn.metrics import precision_score


# In[145]:


precision_score(test["target"], preds)


# In[146]:


grouped_matches = matches.groupby("team")


# In[147]:


group = grouped_matches.get_group("Manchester City").sort_values("date")


# In[148]:


group


# In[149]:


def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group


# In[150]:


cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]


# In[151]:


cols


# In[152]:


new_cols


# In[153]:


rolling_averages(group, cols, new_cols)


# In[154]:


matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols))


# In[155]:


matches_rolling


# In[156]:


matches_rolling = matches_rolling.droplevel('team')


# In[157]:


matches_rolling


# In[158]:


matches_rolling.index = range(matches_rolling.shape[0])


# In[159]:


matches_rolling


# In[160]:


def make_predictions(data, predictors):
    train = data[data["date"] < '2022-01-01']
    test = data[data["date"] > '2022-01-01']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return combined, precision


# In[161]:


combined, precision = make_predictions(matches_rolling, predictors + new_cols)


# In[162]:


precision


# In[163]:


combined


# In[164]:


combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)


# In[165]:


combined


# In[166]:


class MissingDict(dict):
    __missing__ = lambda self, key: key


# In[167]:


map_values = {"Brighton and Hove Albion": "Brighton", "Manchester United": "Manchester Utd", "Newcastle United": "Newcastle Utd", "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolves"} 


# In[168]:


mapping = MissingDict(**map_values)


# In[169]:


mapping["Arsenal"]


# In[170]:


combined["new_team"] = combined["team"].map(mapping)


# In[171]:


combined


# In[172]:


merged = combined.merge(combined, left_on=["date", "new_team"], right_on=["date", "opponent"])


# In[173]:


merged


# In[174]:


merged[(merged["predicted_x"] == 1) & (merged["predicted_y"] ==0)]["actual_x"].value_counts()


# In[ ]:




