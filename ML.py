from Utopia_tools import *

import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn import datasets, linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR


# P_enable_logging()

All_data = [
[137, 92, 11, 247, -1.0, 26, 19.5, 33.0]
,[134, 105, 4, 247, -5.8, 34, 96.7, 21.4]
,[142, 91, 6, 249, -5.8, 26, 44.5, 20.2]
,[120, 109, 6, 245, -5.8, 34, 132.0, 19.2]
,[145, 91, 5, 247, -5.8, 26, 64.3, 18.0]
,[136, 92, 7, 245, -1.0, 26, 28.1, 17.3]
,[44, 159, 17, 228, -46.4, 25, 60.2, 17.0]
,[20, 64, 156, 240, 4.0, 28, 20.6, 16.2]
,[21, 62, 141, 232, 4.0, 25, 15.9, 16.0]
,[22, 60, 160, 245, 4.0, 28, 26.3, 14.8]
,[54, 147, 29, 231, 1.2, 20, 132.5, 14.3]
,[101, 132, 0, 239, -1.3, 21, 1.5, 11.2]
,[33, 128, 25, 232, -46.4, 25, 74.7, 11.2]
,[99, 140, 0, 240, -1.3, 21, 0.7, 10.9]
,[103, 133, 0, 237, -1.3, 21, 1.1, 10.8]
,[60, 111, 83, 257, 15.8, 38, 13.6, 10.6]
,[97, 106, 27, 238, 13.3, 64, 13.2, 9.8]
,[57, 183, 1, 244, 100, 16, 3.0, 9.7]
,[80, 100, 51, 247, 89.4, 27, 164.5, 9.6]
,[73, 134, 18, 252, 89.4, 27, 69.8, 9.5]
,[26, 66, 74, 232, -46.4, 25, 103.8, 9.5]
,[91, 16, 158, 233, -26.8, 29, 9.0, 9.0]
,[3, 9, 230, 239, -4.1, 12, 2.7, 8.9]
,[75, 135, 1, 239, -1.3, 21, 1.8, 8.8]
,[60, 86, 74, 223, 0.1, 13, 4.1, 8.8]
,[69, 114, 78, 263, 15.8, 38, 13.8, 8.6]
,[4, 226, 2, 241, -5.6, 18, 5.8, 8.5]
,[84, 141, 21, 258, -11.3, 5, 12.4, 8.4]
,[71, 126, 59, 257, 15.8, 51, 13.2, 7.8]
,[100, 82, 50, 246, 89.4, 27, 177.3, 7.6]
,[43, 125, 48, 227, 1.2, 20, 132.7, 7.1]
,[74, 118, 59, 262, 15.8, 38, 14.3, 7.1]
,[109, 114, 10, 239, 13.3, 64, 17.3, 7.0]
,[1, 9, 229, 239, -4.1, 12, 2.5, 6.7]
,[78, 75, 60, 250, 33.1, 1, 10.8, 6.3]
,[113, 116, 6, 243, -5.8, 34, 362.6, 6.2]
,[63, 122, 53, 251, 89.4, 27, 98.2, 6.1]
,[70, 168, 1, 244, -2.6, 16, 23.8, 5.9]
,[33, 162, 33, 231, -24.8, 254, 11.0, 5.8]
,[55, 156, 19, 232, 1.2, 20, 81.4, 5.7]
,[93, 110, 32, 239, 13.3, 64, 11.6, 5.7]
,[82, 155, 0, 238, 15.5, 21, 0.7, 5.6]
,[77, 131, 12, 221, 100, 28, 31.4, 5.6]
,[125, 74, 52, 248, 100, 26, 14.4, 5.4]
,[73, 116, 52, 250, 89.4, 27, 126.1, 5.4]
,[82, 121, 13, 222, 100, 34, 37.4, 5.4]
,[49, 93, 75, 227, 0.1, 13, 5.0, 5.2]
,[89, 146, 11, 251, -10.7, 30, 126.5, 5.1]
,[88, 127, 20, 246, -10.7, 23, 68.3, 5.1]
,[60, 105, 71, 229, 0.1, 13, 5.1, 5.1]
,[61, 90, 73, 227, 0.1, 13, 4.6, 5.0]
,[4, 234, 1, 240, -5.6, 18, 6.5, 4.8]
,[80, 122, 11, 221, 100, 34, 41.7, 4.7]
,[33, 21, 192, 236, -4.4, -15, 7.5, 4.6]
,[30, 8, 219, 241, -4.4, -15, 7.8, 4.5]
,[76, 160, 1, 243, -1.3, 21, 2.0, 4.4]
,[94, 125, 19, 248, -10.7, 23, 54.6, 4.4]
,[134, 78, 21, 235, -10.6, 12, 11.6, 4.2]
,[84, 93, 29, 227, -10.6, 12, 13.7, 4.1]
,[1, 10, 230, 241, -4.1, 12, 2.3, 4.0]
,[43, 159, 1, 244, -1.3, 21, 2.1, 3.9]
,[122, 122, 0, 248, -2.6, 16, 22.1, 3.8]
,[95, 142, 13, 251, -10.7, 30, 106.6, 3.8]
,[76, 65, 100, 246, 33.1, 1, 10.4, 3.6]
,[92, 132, 18, 246, -10.7, 23, 87.4, 3.4]
,[29, 14, 180, 241, -25.2, 5, 6.5, 3.2]
,[74, 164, 0, 240, 15.5, 21, 0.8, 3.2]
,[129, 86, 3, 232, -0.6, 29, 9.5, 3.1]
,[136, 74, 25, 235, -10.6, 12, 10.8, 3.1]
,[118, 107, 7, 240, -5.8, 34, 233.1, 2.9]
,[122, 93, 15, 236, -10.6, 12, 12.4, 2.9]
,[108, 97, 18, 230, -10.6, 12, 12.9, 2.7]
,[1, 10, 156, 242, -4.1, 12, 2.1, 2.6]
,[61, 112, 83, 255, 14.0, 48, 22.1, 2.6]
,[143, 73, 16, 245, -15.9, -1, 19.1, 2.5]
,[162, 89, 9, 262, 2.7, 30, 23.1, 2.4]
,[98, 61, 99, 247, 31.5, 12, 5.5, 2.4]
,[4, 7, 231, 242, -4.1, 3, 2.9, 2.3]
,[64, 163, 22, 257, 100, 7, 6.1, 2.2]
,[152, 102, 1, 260, -2.6, 21, 15.7, 2.1]
,[62, 103, 87, 256, 14.0, 38, 14.7, 1.9]
,[64, 100, 65, 228, -10.6, 13, 14.0, 1.9]
,[101, 104, 37, 246, 13.3, 12, 6.1, 1.8]
,[95, 148, 0, 245, -2.6, 16, 24.6, 1.6]
,[133, 81, 16, 242, -15.9, 6, 21.0, 1.5]
,[76, 13, 180, 240, -26.8, 5, 5.1, 1.4]
,[82, 106, 44, 260, -10.2, 47, 53.8, 1.4]
,[96, 57, 99, 247, 31.5, 12, 5.7, 1.2]
,[146, 61, 27, 239, -10.6, 6, 9.9, 1.1]
,[1, 85, 103, 240, -4.1, 12, 1.9, 1.0]
,[9, 230, 0, 240, 1.9, 22, 3.6, 1.0]
,[72, 120, 31, 232, -21.4, 30, 29.9, 1.0]
,[54, 153, 5, 225, -17.1, 28, 41.8, 1.0]
,[85, 102, 32, 239, 13.3, 12, 9.5, 0.8]
,[139, 88, 1, 232, 3.5, 29, 15.6, 0.7]
,[108, 111, 13, 239, 13.3, 64, 18.3, 0.7]
,[166, 72, 25, 261, 6.0, 30, 25.1, 0.6]
,[79, 146, 11, 251, 89.4, 30, 41.7, 0.6]
,[72, 105, 30, 229, -21.4, 30, 33.3, 0.4]
,[53, 110, 88, 257, 14.0, 38, 19.9, 0.4]
,[129, 95, 3, 231, -9.7, 29, 22.1, 0.3]
,[34, 33, 175, 241, -18.3, 310, 13.6, 0.2]
,[89, 58, 100, 247, 20.2, 1, 5.2, 0.2]
,[61, 156, 22, 258, 8.3, 7, 9.6, 0.2]
,[88, 12, 180, 235, -26.8, 5, 6.9, 0.1]
,[95, 59, 101, 249, 31.5, 1, 5.2, 0.1]
,[29, 167, 6, 232, -24.8, 92, 12.4, -0.0]
,[55, 139, 39, 259, 8.3, 7, 10.1, 0.0]
,[73, 138, 41, 261, -19.1, 0, 10.5, -0.0]
,[12, 229, 0, 242, 1.9, 22, 3.2, -0.2]
,[31, 161, 32, 231, -24.8, 254, 11.6, -0.3]
,[144, 102, 0, 257, -2.6, 21, 17.7, -0.4]
,[57, 155, 39, 259, 8.3, 7, 9.9, -0.4]
,[157, 90, 12, 262, 2.7, 30, 19.6, -0.5]
,[88, 129, 14, 241, -3.4, 34, 184.7, -0.7]
,[86, 129, 33, 259, 3.6, 0, 12.9, -0.7]
,[82, 110, 39, 251, 33.1, 1, 11.3, -0.9]
,[40, 33, 151, 224, 12.8, -15, 29.2, -1.3]
,[154, 89, 10, 261, 2.7, 30, 22.1, -1.3]
,[37, 38, 121, 231, -18.8, 254, 12.9, -1.4]
,[69, 120, 56, 258, -40.0, 51, 15.5, -1.4]
,[136, 89, 1, 262, -2.6, 21, 15.8, -1.5]
,[16, 227, 0, 244, 4.2, 22, 3.0, -1.6]
,[82, 123, 24, 253, 33.1, 5, 11.1, -1.6]
,[63, 107, 54, 223, -28.2, 17, 2.6, -1.6]
,[157, 96, 1, 261, -2.6, 21, 14.9, -1.8]
,[99, 122, 19, 251, 2.7, 23, 11.0, -1.8]
,[5, 7, 232, 242, -4.1, 3, 3.2, -2.0]
,[67, 130, 12, 222, -28.5, 34, 17.4, -2.1]
,[64, 128, 16, 222, -28.2, 17, 2.8, -2.1]
,[30, 55, 137, 222, 11.4, 13, 64.8, -2.2]
,[95, 95, 21, 232, -21.4, 29, 36.2, -2.2]
,[77, 116, 58, 261, -40.0, 51, 15.2, -2.2]
,[126, 66, 23, 241, -10.6, 6, 6.7, -2.2]
,[67, 119, 31, 229, 4.0, 30, 28.8, -2.3]
,[163, 69, 26, 263, 6.0, 47, 24.4, -2.3]
,[32, 44, 141, 225, 11.4, 13, 92.2, -2.4]
,[74, 119, 12, 221, -17.1, 34, 16.9, -2.4]
,[30, 127, 33, 229, -18.8, 254, 10.5, -2.5]
,[1, 135, 10, 239, -4.1, 18, 1.7, -2.5]
,[146, 69, 30, 263, 6.0, 47, 23.9, -2.5]
,[106, 115, 20, 239, 63.8, 64, 17.0, -2.5]
,[35, 75, 63, 229, -18.8, 254, 11.9, -2.8]
,[120, 96, 9, 230, -21.4, 29, 36.6, -2.8]
,[66, 114, 42, 225, -28.2, 17, 2.7, -2.9]
,[5, 234, 1, 240, -5.6, 22, 5.5, -3.0]
,[38, 182, 6, 230, 22.9, 92, 3.7, -3.1]
,[91, 109, 34, 241, 13.3, 12, 7.4, -3.1]
,[144, 67, 25, 242, -10.6, 6, 7.6, -3.1]
,[76, 141, 21, 253, 33.1, 5, 11.4, -3.2]
,[87, 129, 36, 260, 3.6, 0, 12.8, -3.3]
,[134, 116, 0, 251, -2.6, 21, 19.4, -3.4]
,[27, 51, 161, 248, 4.0, 28, 32.2, -3.5]
,[41, 195, 0, 237, -2.6, 21, 0.9, -3.7]
,[80, 128, 45, 257, 3.6, 0, 12.5, -3.7]
,[70, 137, 9, 216, -17.1, 28, 30.5, -3.7]
,[31, 190, 5, 232, 22.9, 92, 3.5, -3.9]
,[9, 231, 1, 241, 1.9, 22, 4.0, -4.2]
,[35, 35, 180, 241, -18.3, 310, 12.7, -4.3]
,[95, 123, 15, 242, -3.4, 34, 167.1, -4.3]
,[69, 154, 11, 257, -19.1, 7, 11.7, -4.4]
,[74, 161, 9, 256, -18.6, 20, 15.4, -4.6]
,[67, 136, 14, 221, -28.5, 17, 14.2, -4.6]
,[21, 219, 0, 240, 4.2, 21, 3.1, -4.7]
,[41, 34, 125, 224, 11.4, -15, 34.7, -4.8]
,[49, 177, 6, 235, 2.3, 92, 25.2, -5.0]
,[67, 133, 27, 236, 0.4, 30, 67.2, -5.1]
,[74, 149, 34, 255, -18.6, 20, 18.7, -5.1]
,[54, 164, 13, 232, 2.3, 20, 19.4, -5.3]
,[66, 121, 32, 233, -18.2, 30, 47.5, -5.3]
,[113, 115, 19, 255, 2.7, 23, 13.9, -5.9]
,[31, 50, 138, 222, 11.4, 13, 84.6, -6.1]
,[83, 144, 23, 256, 33.1, 5, 11.1, -6.1]
,[107, 121, 3, 243, -3.4, 34, 149.9, -6.2]
,[60, 155, 8, 225, -17.1, 28, 37.0, -6.2]
,[138, 100, 16, 258, 2.7, 30, 17.0, -6.4]
,[17, 11, 217, 239, 21.9, -39, 3.4, -6.5]
,[80, 137, 31, 256, 3.6, 5, 13.1, -6.5]
,[74, 132, 44, 259, 11.2, 0, 10.9, -6.6]
,[56, 134, 10, 221, -28.5, 34, 18.2, -6.7]
,[50, 45, 165, 248, 4.0, 20, 41.9, -6.8]
,[66, 144, 9, 222, -17.1, 28, 33.7, -6.9]
,[81, 133, 18, 237, -3.4, 34, 181.2, -7.5]
,[64, 143, 8, 224, -28.5, 17, 16.1, -7.6]
,[48, 176, 3, 232, 2.3, 92, 34.0, -7.8]
,[136, 80, 32, 258, -10.2, 47, 29.2, -7.8]
,[38, 51, 135, 219, 11.4, 13, 50.2, -8.1]
,[6, 11, 226, 241, 80.8, 3, 1.7, -9.0]
,[143, 62, 29, 240, -10.6, 6, 8.5, -9.3]
,[94, 123, 16, 241, -3.4, 34, 166.7, -9.8]
,[67, 124, 48, 258, -40.0, 51, 14.1, -10.0]
,[72, 129, 54, 255, 4.0, 20, 54.9, -10.2]
,[39, 35, 151, 227, -4.4, -15, 6.5, -10.8]
,[13, 11, 220, 236, 21.9, 3, 3.1, -10.9]
,[106, 92, 34, 261, -10.2, 47, 45.3, -11.1]
,[39, 50, 133, 220, 11.4, 13, 43.9, -11.4]
,[74, 133, 50, 258, -40.0, 51, 13.2, -11.5]
,[71, 134, 20, 236, -3.4, 34, 193.5, -14.5]
,[62, 82, 114, 251, 4.0, 20, 49.7, -14.5]
,[153, 112, 6, 280, 3.0, -8, 6.4, -1.5]
]


All_data = [[a for a in b[0:8]]+[a for a in b[8:]] for b in All_data]

# print(All_data)

# CHECK MODEL IF NORMAL


# t = [[0.1,0.2],[0.3,0.4],[0.3,0.6],[0.2,0.5],[0.06,0.07],[0.12,0.05]]
# m = [0.3,0.7,0.9,0.7,0.14,0.17]
# # scalar1 = StandardScaler()
# # scalar1.fit(t)
# # t = scalar1.transform(t)
# # scalar2 = StandardScaler()
# # scalar2.fit(m)
# # m = scalar2.transform(m)
# # print(t)
# # print(m)


# # model = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=1000)
# # model = LogisticRegression(C=1000.0, random_state=0)
# # model = SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1,
# #                coef0=1)
# model = MLPRegressor(hidden_layer_sizes=(10), activation="relu",
#                  solver='lbfgs', alpha=0.001,
#                  batch_size='auto', learning_rate="constant",
#                  learning_rate_init=0.01,
#                  power_t=0.5, max_iter=2000,tol=1e-4)
# model.fit(t, m)
# # tt = [[2,3],[4,5]]
# # mm = [5,9]
# # tt = scalar1.transform([[0.3,0.4]])
# # mm = model.predict(tt)
# # mm = scalar2.inverse_transform(mm)
# # print(tt)
# # print(mm)
# # print(model.score(tt,mm))
# tt = [[0.2,0.3],[0.4,0.5]]
# mm = [0.5,0.9]
# print(model.score(tt,mm))
# print(model.predict([[0.3,0.55]]))

# MAIN

np.random.shuffle(All_data)

x = [ a[0:7] for a in All_data[:(len(All_data)-20)]]
y = [ a[7] for a in All_data[:(len(All_data)-20)]]

x, y = np.array(x), np.array(y)
print('Median is '+str(np.median(y)))
model = RandomForestRegressor()

model.fit(x, y)
r_sq = model.score(x, y)
result = []
result_guess = []
guess_data = [ a[7] for a in All_data[-20:]]
# print(guess_data)
# print(np.median(guess_data))
# print(np.mean(guess_data))
guess_low_range = np.median(guess_data)-np.mean(guess_data)/2
guess_high_range = np.median(guess_data)+np.mean(guess_data)/2
print(guess_low_range)
print(guess_high_range)

for i in range(1,20):
    # print('-----------------')
    x =  [All_data[-i][0:7]]
    y = All_data[-i][7]
    y_pred = model.predict(x)
    y_guess = random.uniform(guess_low_range,guess_high_range)
    result.append(abs(y_pred - y))
    result_guess.append(abs(y_guess - y))
    # print(y)
    # print(y_pred)
    # print(y_guess)

a=[ a[0:7] for a in All_data[-20:]]
b=[ a[7] for a in All_data[-20:]]
for aa,bb in zip(a,b):
    # print('input:')
    # print(aa)
    output = model.predict([aa])
    if output > 3:
        print('-----------------')
        print('answer:')
        print(bb)
        print('output:')
        print(output)
print('-----------------')
print('Guess error is '+str(sum(result_guess)/len(result_guess)))
print('Prediction error is '+str(sum(result)/len(result)))
print('Score is '+str(model.score(a,b)))

# a=[ a[0:7] for a in All_data[-3:]]
# b=[ a[7] for a in All_data[-3:]]
# print(a)
# print(b)
# today_input = a
# final = []
# for ti in today_input:
#     print(ti)
#     final.append([model.predict([ti]),ti])
# final.sort(key=lambda x: x[0], reverse=True)
# print(final)

today_input = [
[109, 285, 37, 431, -18.5, 1, 13.1]
,[109, 285, 37, 431, -29.8, 1, 6.3]
,[109, 285, 37, 431, 1.7, 1, 4.4]
,[109, 285, 37, 431, -10.7, 1, 4.1]
,[109, 285, 37, 431, 14.4, 1, 3.8]
,[109, 285, 37, 431, 36.6, 1, 3.7]
,[109, 285, 37, 431, -5.7, 1, 3.2]
,[109, 285, 37, 431, -5.6, 1, 3.0]
,[109, 285, 37, 431, 4.6, 1, 2.9]
,[109, 285, 37, 431, 41.2, 1, 2.8]
,[109, 285, 37, 431, 21.0, 1, 2.4]
,[109, 285, 37, 431, -4.4, 1, 2.4]
,[109, 285, 37, 431, -0.6, 1, 2.4]
,[109, 285, 37, 431, 8.8, 1, 2.2]
,[109, 285, 37, 431, 24.4, 1, 2.1]
,[109, 285, 37, 431, -6.6, 1, 2.1]
,[109, 285, 37, 431, 12.2, 1, 2.1]
,[109, 285, 37, 431, 12.6, 1, 2.0]
,[109, 285, 37, 431, 8.8, 1, 2.0]
,[109, 285, 37, 431, 3.3, 1, 1.9]
,[109, 285, 37, 431, -9.3, 1, 1.9]
,[109, 285, 37, 431, -8.4, 1, 1.9]
,[109, 285, 37, 431, -8.2, 1, 1.9]
,[109, 285, 37, 431, 5.7, 1, 1.9]
,[109, 285, 37, 431, 24.9, 1, 1.9]
,[109, 285, 37, 431, -13.5, 1, 1.8]
,[109, 285, 37, 431, -26.8, 1, 1.8]
,[109, 285, 37, 431, 24.9, 1, 1.8]
,[109, 285, 37, 431, -14.9, 1, 1.8]
,[109, 285, 37, 431, -16.0, 1, 1.8]
,[109, 285, 37, 431, 19.5, 1, 1.8]
,[109, 285, 37, 431, -33.4, 1, 1.8]
,[109, 285, 37, 431, -6.8, 1, 1.8]
,[109, 285, 37, 431, 1.0, 1, 1.8]
,[109, 285, 37, 431, 13.2, 1, 1.8]
,[109, 285, 37, 431, -20.0, 1, 1.7]
,[109, 285, 37, 431, -13.3, 1, 1.7]
,[109, 285, 37, 431, -3.8, 1, 1.7]
,[109, 285, 37, 431, 19.1, 1, 1.7]
,[109, 285, 37, 431, -36.7, 1, 1.6]
,[109, 285, 37, 431, -12.7, 1, 1.6]
,[109, 285, 37, 431, -10.6, 1, 1.6]
,[109, 285, 37, 431, -0.2, 1, 1.6]
,[109, 285, 37, 431, -42.4, 1, 1.6]
,[109, 285, 37, 431, 19.1, 1, 1.6]
,[109, 285, 37, 431, 3.1, 1, 1.6]
,[109, 285, 37, 431, 17.9, 1, 1.6]
,[109, 285, 37, 431, -10.3, 1, 1.6]
,[109, 285, 37, 431, 16.2, 1, 1.6]
,[109, 285, 37, 431, 19.1, 1, 1.6]
,[109, 285, 37, 431, -19.9, 1, 1.5]
,[109, 285, 37, 431, 0.3, 1, 1.5]
,[109, 285, 37, 431, -16.1, 1, 1.5]
,[109, 285, 37, 431, -1.9, 1, 1.5]
,[109, 285, 37, 431, 58.4, 1, 1.5]
,[109, 285, 37, 431, 16.0, 1, 1.5]
,[109, 285, 37, 431, 6.1, 1, 1.5]
,[109, 285, 37, 431, -5.8, 1, 1.4]
,[109, 285, 37, 431, -5.7, 1, 1.4]
,[109, 285, 37, 431, 3.7, 1, 1.4]
,[109, 285, 37, 431, -17.7, 1, 1.4]
,[109, 285, 37, 431, -18.0, 1, 1.4]
,[109, 285, 37, 431, 6.5, 1, 1.4]
,[109, 285, 37, 431, 8.4, 1, 1.4]
,[109, 285, 37, 431, 3.4, 1, 1.3]
,[109, 285, 37, 431, -4.5, 1, 1.3]
,[109, 285, 37, 431, 7.2, 1, 1.3]
,[109, 285, 37, 431, -16.2, 1, 1.3]
,[109, 285, 37, 431, -50.4, 1, 1.3]
,[109, 285, 37, 431, -20.1, 1, 1.3]
,[109, 285, 37, 431, 27.4, 1, 1.3]
,[109, 285, 37, 431, 24.7, 1, 1.3]
,[109, 285, 37, 431, -1.8, 1, 1.3]
,[109, 285, 37, 431, 10.9, 1, 1.3]
,[109, 285, 37, 431, 12.8, 1, 1.2]
,[109, 285, 37, 431, 1.4, 1, 1.2]
,[109, 285, 37, 431, -8.5, 1, 1.2]
,[109, 285, 37, 431, -2.7, 1, 1.2]
,[109, 285, 37, 431, -9.0, 1, 1.2]
,[109, 285, 37, 431, 3.7, 1, 1.2]
,[109, 285, 37, 431, 37.7, 1, 1.2]
,[109, 285, 37, 431, -14.8, 1, 1.2]
,[109, 285, 37, 431, -20.9, 1, 1.2]
,[109, 285, 37, 431, 0.3, 1, 1.2]
,[109, 285, 37, 431, -10.5, 1, 1.1]
,[109, 285, 37, 431, 2.2, 1, 1.1]
,[109, 285, 37, 431, -5.2, 1, 1.1]
,[109, 285, 37, 431, -28.9, 1, 1.1]
,[109, 285, 37, 431, 1.3, 1, 1.0]
,[109, 285, 37, 431, 16.6, 1, 1.0]
,[109, 285, 37, 431, 17.2, 1, 1.0]
,[109, 285, 37, 431, -15.6, 1, 1.0]
,[109, 285, 37, 431, 15.5, 1, 1.0]
,[109, 285, 37, 431, 31.4, 1, 0.9]
,[109, 285, 37, 431, -6.9, 1, 0.9]
,[109, 285, 37, 431, -24.5, 1, 0.9]
,[109, 285, 37, 431, 1.8, 1, 0.9]
,[109, 285, 37, 431, 3.4, 1, 0.9]
,[109, 285, 37, 431, 17.3, 1, 0.8]
,[109, 285, 37, 431, 55.7, 1, 0.8]
,[109, 285, 37, 431, 6.6, 1, 0.8]
,[109, 285, 37, 431, 3.1, 1, 0.7]
,[109, 285, 37, 431, 10.1, 1, 0.7]
,[109, 285, 37, 431, -21.7, 1, 0.6]
,[109, 285, 37, 431, -16.4, 1, 0.6]
,[109, 285, 37, 431, 55.7, 1, 0.6]
,[109, 285, 37, 431, 53.9, 1, 0.6]
,[109, 285, 37, 431, 9.8, 1, 0.6]
,[109, 285, 37, 431, 12.1, 1, 0.5]
]
final = []
for ti in today_input:
    print(ti)
    final.append([model.predict([ti]),ti])
final.sort(key=lambda x: x[0])
P_printl(final)









#  STRESS TEST

# TURE_FINAL = []
# for mm in range(1,11):
#     n_estimators_c = mm * 100
#     for nn in range(1,11):
#         random_state_c = nn * 100
#         final_result_list = []
#         for n in range(1,10):

#             np.random.shuffle(All_data)

#             x = [ a[0:7] for a in All_data[:(len(All_data)-20)]]
#             y = [ a[7] for a in All_data[:(len(All_data)-20)]]

#             x, y = np.array(x), np.array(y)
#             # P_printl(x)
#             # print(y)

#             # model = linear_model.LinearRegression().fit(x, y)
#             model = RandomForestRegressor(n_estimators=n_estimators_c, oob_score=True, random_state=random_state_c, warm_start = True)
#             model.fit(x, y)
#             r_sq = model.score(x, y)
#             # print('coefficient of determination:', r_sq)
#             # print('intercept:', model.intercept_)
#             # print('slope:', model.coef_)
#             result = []
#             result_guess = []
#             for i in range(1,20):
#                 x =  [All_data[-i][0:7]]
#                 y = All_data[-i][7]
#                 y_pred = model.predict(x)
#                 result.append(abs(y_pred - y))

#             final_result_list.append(sum(result)/len(result))


#         TURE_FINAL.append([n_estimators_c,random_state_c,(sum(final_result_list)/len(final_result_list))])
# print(TURE_FINAL)