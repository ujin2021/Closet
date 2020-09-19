import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

path = '/home/ubuntu/srv/Closet/accounts/Recommendation_algo/'

class Recommendation:
    def __init__(self, user_clothes):
        self.count_vector = CountVectorizer()
        self.sex = user_clothes['sex']
        self.del_re = user_clothes['delete']
        #self.weather = user_clothes['weather']
        if user_clothes['weather'] >= 27:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "27_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        elif 26 <= user_clothes['weather'] <= 23:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "26_23_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        elif 20 <= user_clothes['weather'] <= 21:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "22_20_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        elif 17 <= user_clothes['weather'] <= 19:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "19_17_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        elif 10 <= user_clothes['weather'] <= 16:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "16_10_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        elif 6 <= user_clothes['weather'] <= 9:
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "9_6_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        else:#5~
            self.weather = {'weather':user_clothes['weather'],
                            'pan':pd.read_csv(path + "5_fashion.csv").drop(['Unnamed: 0'],axis=1)}
        
        self.clothes= dict()
        if self.sex == 'F':
            self.all_woman_vector = pd.read_csv(path + "all_clothes_woman.csv")
            self.all_woman_vector.set_index(self.all_woman_vector['clothes'], inplace=True)
            self.all_woman_vector=self.all_woman_vector.drop(['clothes'], axis=1).T
            #color
            if user_clothes['filtering_freq']['top']:
                self.clothes['color_top'] = self.all_woman_vector.loc[:,user_clothes['filtering']['top']]
                self.clothes['color_top'].loc[8]=user_clothes['filtering_freq']['top']
            if user_clothes['filtering_freq']['bottom']:
                self.clothes['color_bottom'] = self.all_woman_vector.loc[:,user_clothes['filtering']['bottom']]
                self.clothes['color_bottom'].loc[8]=user_clothes['filtering_freq']['bottom']
            if user_clothes['filtering_freq']['dress']:
                self.clothes['color_dress'] = self.all_woman_vector.loc[:,user_clothes['filtering']['dress']]
                self.clothes['color_dress'].loc[8]=user_clothes['filtering_freq']['dress']
            if user_clothes['filtering_freq']['outer']:
                self.clothes['color_outer'] = self.all_woman_vector.loc[:,user_clothes['filtering']['outer']]
                self.clothes['color_outer'].loc[8]=user_clothes['filtering_freq']['outer']
                
            #default
            if user_clothes['filtering_freq']['top_df']:
                self.clothes['top'] = self.all_woman_vector.loc[:,user_clothes['filtering']['top_df']]
                self.clothes['top'].loc[8]=user_clothes['filtering_freq']['top_df']
            if user_clothes['filtering_freq']['bottom_df']:
                self.clothes['bottom'] = self.all_woman_vector.loc[:,user_clothes['filtering']['bottom_df']]
                self.clothes['bottom'].loc[8]=user_clothes['filtering_freq']['bottom_df']
            if user_clothes['filtering_freq']['dress_df']:
                self.clothes['dress'] = self.all_woman_vector.loc[:,user_clothes['filtering']['dress_df']]
                self.clothes['dress'].loc[8]=user_clothes['filtering_freq']['dress_df']
            if user_clothes['filtering_freq']['outer_df']:
                self.clothes['outer'] = self.all_woman_vector.loc[:,user_clothes['filtering']['outer_df']]
                self.clothes['outer'].loc[8]=user_clothes['filtering_freq']['outer_df']
            
            self.categories = {'campus': np.array([0,1,0,0,0,0,0,0]),
                              'casual': np.array([0,0,0,1,0,0,0,0]),
                              'femi': np.array([0,0,0,0,1,0,0,0]),
                              'lovely': np.array([0,0,0,0,0,0,1,0]),
                              'modern': np.array([0,0,0,0,0,1,0,0]),
                              'ofice': np.array([1,0,0,0,0,0,0,0]),
                              'simple': np.array([0,0,0,0,0,0,0,1]),
                              'travel': np.array([0,0,1,0,0,0,0,0])}
            
        else:
            self.all_man_vector = pd.read_csv(path + "all_clothes_man.csv")
            self.all_man_vector.set_index(self.all_man_vector['clothes'], inplace=True)
            self.all_man_vector=self.all_man_vector.drop(['clothes'], axis=1).T
            #color
            if user_clothes['filtering_freq']['top']:
                self.clothes['color_top'] = self.all_man_vector.loc[:,user_clothes['filtering']['top']]
                self.clothes['color_top'].loc[8]=user_clothes['filtering_freq']['top']
            if user_clothes['filtering_freq']['bottom']:
                self.clothes['color_bottom'] = self.all_man_vector.loc[:,user_clothes['filtering']['bottom']]
                self.clothes['color_bottom'].loc[8]=user_clothes['filtering_freq']['bottom']
            if user_clothes['filtering_freq']['outer']:
                self.clothes['color_outer'] = self.all_man_vector.loc[:,user_clothes['filtering']['outer']]
                self.clothes['color_outer'].loc[8]=user_clothes['filtering_freq']['outer']
                
            #default
            if user_clothes['filtering_freq']['top_df']:
                self.clothes['top'] = self.all_man_vector.loc[:,user_clothes['filtering']['top_df']]
                self.clothes['top'].loc[8]=user_clothes['filtering_freq']['top_df']
            if user_clothes['filtering_freq']['bottom_df']:
                self.clothes['bottom'] = self.all_man_vector.loc[:,user_clothes['filtering']['bottom_df']]
                self.clothes['bottom'].loc[8]=user_clothes['filtering_freq']['bottom_df']
            if user_clothes['filtering_freq']['outer_df']:
                self.clothes['outer'] = self.all_man_vector.loc[:,user_clothes['filtering']['outer_df']]
                self.clothes['outer'].loc[8]=user_clothes['filtering_freq']['outer_df']
            
            self.categories = {'campus': np.array([0,1,0,0,0,0]),
                              'casual': np.array([0,0,0,1,0,0]),
                              'modern': np.array([0,0,1,0,0,0]),
                              'ofice': np.array([0,0,0,0,1,0]),
                              'simple': np.array([1,0,0,0,0,0]),
                              'travel': np.array([0,0,0,0,0,1])}
            
        self.hashtag = self.categories[user_clothes['hashtag']]
        self.complete_outfit = []
        
        
    def cos_similarity(self, v1, v2):
        dot_product = np.dot(v1, v2)
        l2_norm = (np.sqrt(sum(np.square(v1))) * np.sqrt(sum(np.square(v2))))
        similarity = dot_product / l2_norm     
    
        return similarity
    
    # cosine similarity 값이 1이면 두 벡터는 완전히 동일한 벡터
    # cosine similarity 값이 0이면 두 벡터는 상관 관계가 없다
    # cosine similarity 값이 -1이면 두 벡터는 완전히 반대인 벡터
    
    #피처 벡터 행렬은 음수값이 없으므로 코사인 유사도가 음수가 되지는 않는다.
    #따라서 코사인 유사도는 0~1 사이의 값을 갖는다
    
    def result_similarity(self):
        for i in self.clothes.keys():
            result=dict()
            for j in self.clothes[i].columns.tolist():
                result[j] = (0.4 * self.clothes[i][j][8]) + (0.6 * self.cos_similarity(np.array(self.clothes[i][j].tolist()[:-1]), self.hashtag))
            self.clothes[i] = self.clothes[i].append(result, ignore_index=True)
            self.clothes[i] = self.clothes[i].drop(self.clothes[i].index[:9])
            self.clothes[i] = self.clothes[i].T.sort_values(by=[9], ascending=False)
            if 'outer' in i:
                if self.weather['weather'] >= 10:
                    if len(self.clothes[i].index.tolist()) > 3:
                        self.clothes[i] = self.clothes[i].drop(self.clothes[i].index[3:])
            else:
                if len(self.clothes[i].index.tolist()) > 3:
                    self.clothes[i] = self.clothes[i].drop(self.clothes[i].index[3:])
            self.clothes[i] = self.clothes[i].T
            
    def outfit(self):
        colors=[n for n in self.clothes.keys() if 'color' in n]
        if self.weather['weather'] >= 23:
            for i in colors:
                if i == 'color_top':
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes[i])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))]
                    for j,k in zip(temp['top'],temp['bottom']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0])/2, (j,k)))
                elif i == 'color_bottom':
                    temp = self.weather['pan'][(self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['top'].isin(self.clothes['top']))]
                    for j,k in zip(temp['top'],temp['bottom']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                elif i == 'color_dress':
                    for j in self.clothes[i].columns.tolist():
                        self.complete_outfit.append((self.clothes[i][j].values.tolist()[0],(j)))
                else: pass
#             self.complete_outfit = list(set(self.complete_outfit))
#             self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
#             return self.complete_outfit[:3]
        
        elif 20 <= self.weather['weather'] <= 22:
            for i in colors:
                if i == 'color_top':
                    c1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))]
                    for j,k in zip(temp['top'],temp['bottom']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0])/2, (j,k)))
                    c1 = self.clothes[i].filter(regex='shortsleeve|shortshirt')
                    b1 = self.clothes['bottom'].filter(regex='skirt|longpants')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(b1))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    del [[c1]]
                    del [[b1]]
                    del [[temp]]
                elif i == 'color_bottom':
                    c1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['top'].isin(c1))]
                    for j,k in zip(temp['top'],temp['bottom']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    c1 = self.clothes['top'].filter(regex='shortsleeve|shortshirt')
                    b1 = self.clothes[i].filter(regex='skirt|longpants|jogger')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(b1))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    del [[c1]]
                    del [[b1]]
                    del [[temp]]
                elif i == 'color_dress':
                    c1 = self.clothes[i].filter(regex='winshortdress')
                    for j in c1.columns.tolist():
                        self.complete_outfit.append((self.clothes[i][j].values.tolist()[0],(j)))
                    c1 = self.clothes[i].filter(regex='sumlongdress|sumshortdress')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(c1)) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0])/2, (j,k)))
                    del [[c1]]
                    del [[temp]]
                elif i == 'color_outer':
                    c1 = self.clothes['top'].filter(regex='shortsleeve|shortshirt')
                    b1 = self.clothes['bottom'].filter(regex='skirt|longpants|jogger')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(b1))& (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['dress'].filter(regex='sumlongdress|sumshortdress')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(c1)) & (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    del [[c1]]
                    del [[b1]]
                    del [[temp]]
                else: pass
#             self.complete_outfit = list(set(self.complete_outfit))
#             self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
#             return self.complete_outfit[:3]     
        elif 17 <= self.weather['weather'] <= 19:
            for i in colors:
                if i == 'color_top':
                    c1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes[i].filter(regex='longneat')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))]
                    for j,k in zip(temp['top'], temp['bottom']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0])/2, (j,k)))
                    del [[c1]]
                    del [[temp]]

                elif i == 'color_bottom':
                    c1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(self.clothes[i]))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['top'].filter(regex='longneat')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(c1)) & (self.weather['pan']['bottom'].isin(self.clothes[i]))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    del [[c1]]
                    del [[temp]]    
                elif i == 'color_dress':
                    for j in self.clothes[i].columns.tolist():
                        self.complete_outfit.append((self.clothes[i][j].values.tolist()[0],(j)))
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0])/2, (j,k)))
                    del [[temp]]
                elif i == 'color_outer':
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    del [[temp]]
                else: pass
#             self.complete_outfit = list(set(self.complete_outfit))
#             self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
#             return self.complete_outfit[:3]     
        elif 10 <= self.weather['weather'] <= 16:
            for i in colors:
                if i == 'color_top':
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes[i])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(b1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    del [[c1]]
                    del [[temp]]
                
                elif i == 'color_bottom':
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes[i]))& (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(b1)) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    del [[c1]]
                    del [[temp]]
                    
                elif i == 'color_dress':
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(self.clothes['outer']))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0])/2, (j,k)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(self.clothes['outer']))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    del [[c1]]
                    del [[temp]]
                elif i == 'color_outer':
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        d1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(b1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(d1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        d1 = self.clothes[i].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(b1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(d1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        d1 = self.clothes[i].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(b1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(d1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(self.clothes[i]))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='cardigan|jacket')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    del [[c1]]
                    del [[b1]]
                    del [[temp]]
                else: pass
#             self.complete_outfit = list(set(self.complete_outfit))
#             self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
#             return self.complete_outfit[:3]
        elif 6 <= self.weather['weather'] <= 9:
            for i in colors:
                if i == 'color_top':
                    c1 = self.clothes['outer'].filter(regex='coat|parka|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes[i])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    d1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan')
                    b1 = self.clothes['outer'].filter(regex='coat|rider|ma-1')
                    d1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[temp]]
                elif i == 'color_bottom':
                    c1 = self.clothes['outer'].filter(regex='coat|parka|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes[i]))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan')
                    b1 = self.clothes['outer'].filter(regex='coat|rider|ma-1')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[temp]]
                elif i == 'color_dress':
                    c1 = self.clothes['outer'].filter(regex='coat|parka|rider')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(c1))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0])/2, (j,k)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka|rider')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    del [[c1]]
                    del [[b1]]
                    del [[temp]]
                elif i == 'color_outer':
                    c1 = self.clothes[i].filter(regex='coat|parka|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    c1 = self.clothes[i].filter(regex='hoodie|cardigan')
                    b1 = self.clothes['outer'].filter(regex='coat|rider|ma-1')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan')
                    b1 = self.clothes[i].filter(regex='coat|rider|ma-1')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes[i].filter(regex='hoodie|cardigan')
                    b1 = self.clothes[i].filter(regex='coat|rider|ma-1')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    c1 = self.clothes[i].filter(regex='coat|parka|rider')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(c1))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='coat|parka|rider')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka|rider')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))             
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka|rider')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) &(self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))             
                    
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[temp]]
                else: pass
            self.complete_outfit = list(set(self.complete_outfit))
            self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
            return self.complete_outfit[:3]
        else:
            for i in colors:
                if i == 'color_top':
                    c1 = self.clothes['outer'].filter(regex='coat|parka')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes[i])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    d1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan|rider|jacket')
                    b1 = self.clothes['outer'].filter(regex='coat|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes[i])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    
                    if not c1.empty:
                        d1 = self.clothes[i].filter(regex='longsleeve|longshirt')
                        b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        e1 = self.clothes['outer'].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(e1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l,m,n in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer'],temp['outer2']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0] + self.clothes['outer'][n].values.tolist()[0])/5, (j,k,l,m,n)))
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[temp]] 
                elif i == 'color_bottom':
                    c1 = self.clothes['outer'].filter(regex='coat|parka')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes[i]))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan|rider|jacket')
                    b1 = self.clothes['outer'].filter(regex='coat|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                    e1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(e1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l,m,n in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer'],temp['outer2']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0] + self.clothes['outer'][n].values.tolist()[0])/5, (j,k,l,m,n)))
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[temp]] 
                elif i == 'color_dress':
                    c1 = self.clothes['outer'].filter(regex='coat|parka')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(c1))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0])/2, (j,k)))
                    c1 =  self.clothes['outer'].filter(regex='cardigan|jacket|rider')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                    e1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes[i])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes[i][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    del [[c1]]
                    del [[b1]]
                    del [[e1]]
                    del [[temp]]
                elif i == 'color_outer':
                    c1 = self.clothes[i].filter(regex='coat|parka')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom']))& (self.weather['pan']['outer'].isin(c1))]
                    for j,k,l in zip(temp['top'],temp['bottom'],temp['outer']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka')
                        d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l,m in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    c1 = self.clothes[i].filter(regex='hoodie|cardigan|rider|jacket')
                    b1 = self.clothes['outer'].filter(regex='coat|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 = self.clothes['outer'].filter(regex='hoodie|cardigan|rider|jacket')
                    b1 = self.clothes[i].filter(regex='coat|rider')
                    temp = self.weather['pan'][(self.weather['pan']['top'].isin(self.clothes['top'])) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                    for j,k,l,m in zip(temp['top'],temp['bottom'],temp['outer'],temp['outer2']):
                        self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    c1 = self.clothes[i].filter(regex='vest')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                    e1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(e1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l,m,n in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer'],temp['outer2']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0] + self.clothes['outer'][n].values.tolist()[0])/5, (j,k,l,m,n)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    b1 = self.clothes[i].filter(regex='cardigan|jacket')
                    e1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(e1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l,m,n in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer'],temp['outer2']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0] + self.clothes[i][n].values.tolist()[0])/5, (j,k,l,m,n)))
                    c1 = self.clothes['outer'].filter(regex='vest')
                    d1 = self.clothes['top'].filter(regex='longsleeve|longshirt')
                    b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                    e1 = self.clothes[i].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['top'].isin(d1)) & (self.weather['pan']['bottom'].isin(self.clothes['bottom'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(e1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l,m,n in zip(temp['top'],temp['bottom'],temp['vest'],temp['outer'],temp['outer2']):
                            self.complete_outfit.append(((self.clothes['top'][j].values.tolist()[0] + self.clothes['bottom'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0] + self.clothes['outer'][n].values.tolist()[0])/5, (j,k,l,m,n)))
                    
                    c1 = self.clothes[i].filter(regex='coat|parka')
                    temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(c1))]
                    for j,k in zip(temp['dress'], temp['outer']):
                        self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0])/2, (j,k)))
                    c1 =  self.clothes[i].filter(regex='cardigan|jacket|rider')
                    b1 = self.clothes['outer'].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='cardigan|jacket|rider')
                    b1 = self.clothes[i].filter(regex='coat|parka')
                    if not c1.empty:
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['outer'].isin(c1)) & (self.weather['pan']['outer2'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0])/3, (j,k,l)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1))]
                        for j,k,l in zip(temp['dress'], temp['vest'], temp['outer']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0])/3, (j,k,l)))
                    
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        e1 = self.clothes['outer'].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='cardigan|jacket')
                        e1 = self.clothes['outer'].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        e1 = self.clothes[i].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='cardigan|jacket')
                        e1 = self.clothes['outer'].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes['outer'][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 =  self.clothes[i].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes['outer'].filter(regex='cardigan|jacket')
                        e1 = self.clothes[i].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes[i][k].values.tolist()[0] + self.clothes['outer'][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    c1 =  self.clothes['outer'].filter(regex='vest')
                    if not c1.empty:
                        b1 = self.clothes[i].filter(regex='cardigan|jacket')
                        e1 = self.clothes[i].filter(regex='coat|parka')
                        temp = self.weather['pan'][(self.weather['pan']['dress'].isin(self.clothes['dress'])) & (self.weather['pan']['vest'].isin(c1)) & (self.weather['pan']['outer'].isin(b1)) & (self.weather['pan']['outer2'].isin(e1))]
                        for j,k,l,m in zip(temp['dress'], temp['vest'], temp['outer'], temp['outer2']):
                            self.complete_outfit.append(((self.clothes['dress'][j].values.tolist()[0] + self.clothes['outer'][k].values.tolist()[0] + self.clothes[i][l].values.tolist()[0] + self.clothes[i][m].values.tolist()[0])/4, (j,k,l,m)))
                    
                    del [[c1]]
                    del [[b1]]
                    del [[d1]]
                    del [[e1]]
                    del [[temp]] 
                else: pass
        temp = list(set(self.complete_outfit))
        self.complete_outfit = list(set(self.complete_outfit))
        
        for k in temp:
            for m in self.del_re:
                if set(k[1]) == set(m): self.complete_outfit.remove(k)
                
        self.complete_outfit = sorted(self.complete_outfit, key=lambda x:x[0], reverse=True)
        return [i[1] for i in self.complete_outfit[:3]]
                    
# test1=Recommendation(user1)
# test1.result_similarity()
# test1.outfit() -> 이게 진짜 추천 set
# test1.complete_outfit

