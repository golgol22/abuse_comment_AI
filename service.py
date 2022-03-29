from types import new_class
import numpy as np
import pandas as pd
import re
from konlpy.tag import Okt
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Service:
    
    def __init__(self):
        self.okt = Okt()
        self.tokenizer = Tokenizer()
        self.stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    
    def encode(self, text):
        text = re.sub(r'[^ㄱ-ㅎ가-힣]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        text = self.okt.morphs(text, stem=True)
        new_text = [word for word in text if not word in self.stopwords]
        mmmm = pd.read_csv('model/a.csv')
        mmmm.drop('Unnamed: 0', axis=1, inplace=True)
        mmmm = mmmm.fillna('l')
        pppp = mmmm.values.tolist()
        for i in pppp:
            while 'l' in i:
                i.remove('l')
        tokenizer = self.tokenizer
        tokenizer.fit_on_texts(pppp)
        tokenizer.fit_on_texts(new_text)
        threshold = 3
        total_cnt = len(tokenizer.word_index)  # 단어의 수
        rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
        total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
        rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합
        for key, value in tokenizer.word_counts.items():
            total_freq = total_freq + value

            # 단어의 등장 빈도수가 threshold보다 작으면
            if (value < threshold):
                rare_cnt = rare_cnt + 1
                rare_freq = rare_freq + value
        vocab_size = total_cnt - rare_cnt + 1
        tokenizer = Tokenizer(vocab_size)
        tokenizer.fit_on_texts(pppp)
        tokenizer.fit_on_texts(new_text)
        print(new_text)
        encoded = tokenizer.texts_to_sequences([new_text])
        print(encoded)
        x_train = np.array(encoded)
        print(x_train)
        pad_value = pad_sequences(x_train, maxlen=128)
        print(pad_value)
        return pad_value
    
    def predict_test(self, text):
        model = keras.models.load_model('model/abuse.h5')
        indices = self.encode(text)
        result = model.predict(indices) 
        print(result)
        result = np.where(result > 0.5, 1, 0)
        print(result)
        if result == 0.0:
            return '욕 아님'
        else:
            return '욕'
        
if __name__ == "__main__": 
    s = Service()
    print(s.predict_test('시1발')) # ㅅㅂ 제목으로 낚시 잘하네. 신문기자냐?
