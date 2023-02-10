import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
# clean data
df = pd.read_csv('final.csv')

# print(df.isnull().sum())
#df.drop('transactionType', axis=1, inplace=True)
# df.drop(df[df['type'] == 'apartmentgroup'].index, inplace=True)
# df.drop(df[df['type'] == 'housegroup'].index, inplace=True)


# 'id', 'type', 'subtype', 'price', 'transactionType', 'zip', 'kitchen_type',
#                                'building_constructionYear', 'building_condition',
#                                'energy_heatingType', 'certificates_primaryEnergyConsumptionLevel',
#                                'bedroom_count', 'land_surface','atticExists', 'basementExists',
#                                'wellnessEquipment_hasSwimmingPool', 'parkingSpaceCount_indoor',
#                                'parkingSpaceCount_outdoor',
#                                'outdoor_terrace_exists', 'outdoor_garden_surface'
#                              'condition_isNewlyBuilt'
result = df.dtypes
print(result)
df["type"] = df["type"].apply(str)
df['type'] = df['type'].fillna('not-known')

df["subtype"] = df["subtype"].apply(str)
df['subtype'] = df['subtype'].fillna('not-known')

df["transactionType"] = df["transactionType"].apply(str)
df["transactionType"] = df["transactionType"].fillna('not-known')

df['kitchen_type'] = df['kitchen_type'].apply(str)
df['kitchen_type'] = df['kitchen_type'].fillna('not-installed')

df['building_condition']=df['building_condition'].apply(str)
df['building_condition']=df['building_condition'].fillna('not-known')

df['energy_heatingType'] = df['energy_heatingType'].apply(str)
df['energy_heatingType'] = df['energy_heatingType'].fillna('varied')

df['atticExists']=df['atticExists'].apply(str)
df['atticExists']=df['atticExists'].fillna(False)
df['atticExists']=df['atticExists'].replace(['1'],[True])
df['atticExists']=df['atticExists'].replace(['0'],[False])

df['basementExists']=df['basementExists'].apply(str)
df['basementExists']=df['basementExists'].fillna(False)
df['basementExists']=df['basementExists'].replace(['1'],[True])
df['basementExists']=df['basementExists'].replace(['0'],[False])

df['wellnessEquipment_hasSwimmingPool'] = df['wellnessEquipment_hasSwimmingPool'].apply(str)
df['wellnessEquipment_hasSwimmingPool'] = df['wellnessEquipment_hasSwimmingPool'].fillna(False)
df['wellnessEquipment_hasSwimmingPool'] = df['wellnessEquipment_hasSwimmingPool'].replace(['1'],[True])
df['wellnessEquipment_hasSwimmingPool'] = df['wellnessEquipment_hasSwimmingPool'].replace(['0'],[False])

df['outdoor_terrace_exists'] = df['outdoor_terrace_exists'].apply(str)
df['outdoor_terrace_exists'] = df['outdoor_terrace_exists'].fillna(False)
df['outdoor_terrace_exists'] = df['outdoor_terrace_exists'].replace(['1'],[True])
df['outdoor_terrace_exists'] = df['outdoor_terrace_exists'].replace(['0'],[False])

df['condition_isNewlyBuilt'] = df['condition_isNewlyBuilt'].fillna('to-renovate')
df['condition_isNewlyBuilt'] = df['condition_isNewlyBuilt'].apply(str)
df['condition_isNewlyBuilt'] = df['condition_isNewlyBuilt'].replace(['1'],[True])
df['condition_isNewlyBuilt'] = df['condition_isNewlyBuilt'].replace(['0'],[False])


df['id'] = pd.to_numeric(df['id'], errors='coerce')
df = df[~df['price'].str.contains('-')]
df['price'] = float(df['price'])
df['zip'] = df['zip'].to_numeric(df['zip'], errors='coerce')
df.drop(df[df['zip'] == ''].index, inplace=True)
df.drop(df[df['zip'] > 9999].index, inplace=True)
df['building_constructionYear']=pd.to_numeric(df['building_constructionYear'], errors='coerce')
df['building_constructionYear']=df['building_constructionYear'].fillna(0)
df['certificates_primaryEnergyConsumptionLevel']=pd.to_numeric(df['certificates_primaryEnergyConsumptionLevel'], errors='coerce')
df['certificates_primaryEnergyConsumptionLevel']=df['certificates_primaryEnergyConsumptionLevel'].fillna(0)
df['bedroom_count'] = pd.to_numeric(df['bedroom_count'], errors='coerce')
df['bedroom_count'] = df['bedroom_count'].fillna(0)
df['land_surface'] = pd.to_numeric(df['land_surface'], errors='coerce')
df['land_surface'] = df['land_surface'].fillna(0)
df['Parking Space Count indoor'] = df['parkingSpaceCount_indoor'].fillna(0)
df['Parking Space Count indoor'] = df['parkingSpaceCount_indoor'].replace([True], [1])
df['Parking Space Count indoor'] = df['parkingSpaceCount_indoor'].replace([False], [0])
df['Parking SpaceCount outdoor'] = df['parkingSpaceCount_outdoor'].fillna(0)
df['Parking SpaceCount outdoor'] = df['parkingSpaceCount_outdoor'].replace([True], [1])
df['Parking Space Count indoor'] = df['parkingSpaceCount_indoor'].replace([False], [0])
df['outdoor_garden_surface'] = pd.to_numeric(df['outdoor_garden_surface'], errors='coerce')
df['outdoor_garden_surface'] = df['outdoor_garden_surface'].fillna(0)


result = df.dtypes()
print(result)
print(df.isnull().sum())

#df['zip'] = df['zip'].astype('int')
def new_col_provinces(col):
    if col >= 9000:
        return 'Oost - Vlaanderen'
    if col >= 8000:
        return 'West-Vlaanderen'
    if col >= 7000:
        return 'Hainaut'
    if col >= 6600:
        return 'Luxembourg'
    if col >= 6000:
        return 'Hainaut'
    if col >= 5000:
        return 'Namur'
    if col >= 4000:
        return 'Liege'
    if col >= 3500:
        return 'Limburg'
    if col >= 3000:
        return 'Vlaams-Brabant'
    if col >= 2000:
        return 'Antwerpen'
    if col >= 1501:
        return 'Vlaams-Brabant'
    if col >= 1300:
        return 'Brabon Wallon'
    if col >= 1000:
        return 'Brussel'
df['province'] =pd.DataFrame(df['zip'].apply(new_col_provinces))
# df['price'] = df['price'].astype('int')

# def new_col_price(col):
#     if col >= 2000000:
#         return 'more then 2000000'
#     if col >= 1500000:
#         return 'between 2000000 and 1500000'
#     if col >= 1000000:
#         return 'between 100000 and 1500000'
#     if col >= 900000:
#         return 'between 800000 and 9000000'
#     if col >= 800000:
#         return 'between 700000 and 8000000'
#     if col >= 700000:
#         return 'between 600000 and 7000000'
#     if col >= 600000:
#         return 'between 500000 and 6000000'
#     if col >= 500000:
#         return 'between 500000 and 1000000'
#     if col >= 400000:
#         return 'between 500000 and 1000000'
#     if col >= 500000:
#         return 'between 500000 and 1000000'
#     if col >= 400000:
#         return 'between 400000 and 500000'
#     if col >= 300000:
#         return 'between 300000 and 400000 '
#     if col >= 200000:
#         return 'between 200000 and 300000'
#     if col >= 100000:
#         return 'between 100000 and 200000'
#     if col < 100000:
#         return 'below 100000'
#
# df['price_cat'] =pd.DataFrame(df['price'].apply(new_col_price))
X = df.drop('price', axis=1)
X= X.drop('zip', axis=1)
# X=X.drop('id',axis=1)
y = df["price"]
print(X.columns)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_col_names = list(X_train.columns)
feature_names = X_col_names
categorical_features = ["type", "subtype",'transactionType', 'kitchen_type','building_condition', 'energy_heatingType',
                        'atticExists', 'basementExists',
                        'outdoor_terrace_exists', 'wellnessEquipment_hasSwimmingPool', 'condition_isNewlyBuilt',
                        'province']
numerical_features = ['id','building_constructionYear', 'certificates_primaryEnergyConsumptionLevel', 'bedroom_count',
                      'land_surface', 'parkingSpaceCount_indoor', 'parkingSpaceCount_outdoor',
                      'outdoor_garden_surface']
result = df.dtypes
transformer = ColumnTransformer(transformers=[
    ('imputer', SimpleImputer(fill_value='missing'), numerical_features),
    ('scaler', StandardScaler(), numerical_features),
    ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore', categories='auto'), categorical_features)])
regressor = Pipeline(steps=[("preprocessor", transformer), ("model", LinearRegression())])
print(55555555555555555555555555555555555555555555555555555555555555555555555555555555555555)
regressor.fit(X_train, y_train)
print(66666666666666666666666666666666666666666666666666666)
# test the model
y_pred = regressor.predict(X_test)
print(777777777777777777777777777777777777777777)
# save the model to disk
filename = 'finalized_model.sav'
joblib.dump(regressor, filename)

# test the model
df_pred = pd.DataFrame({'Price': y_test.squeeze(), 'Predicted Price': y_pred.squeeze()})
print('mean_squared_error : ', mean_squared_error(y_test, y_pred))
print('mean_absolute_error : ', mean_absolute_error(y_test, y_pred))
print(regressor.score(X_test, y_test))
print(y_pred)
print(df_pred)