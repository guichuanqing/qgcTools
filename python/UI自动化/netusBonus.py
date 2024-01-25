import numpy as np
import matplotlib.pyplot as plt


def logistic_growth(n, P1, m, v, C):
    return P1 * (1 + m / (1 + np.exp(-(v * (n - C)))))

def bonus_pool(b, N, P1, m, v, C):
    # for i in range(1, N):
    # print(list(b*sum(j for j in range(1, i+1)) for i in range(1, N+1)))
    # return list(b*sum(j for j in range(1, i+1)) for i in range(1, N+1))
    return list(b*sum(logistic_growth(j, P1, m, v, C) for j in range(1, i+1)) for i in range(1,N+1))

def p(n):
    return n+1

def user_dividend(N, j):
    if N==j:
        return 0
    else:
        return p(N)/(N-1) + user_dividend(N-1, j)

def pool_dividend(b, N, P1, m, v, C):
    result = {}
    for i in range(1, N):
        result["用户"+str(i)] = user_dividend(N, i)
    return result

P1=1              # 用户设置的珍藏价格初始值。
m=199             # 珍藏价格最高为初始价格提升的倍率。
v=0.056           # 函数的斜率，决定了增长的速度。
C=120             # 函数的中点，即函数增长最快时所需的人数，2倍C为到达最高点所需的参与人数
b=0.3            # 珍藏费用加入贡献池的比例，提供0.3和0.6两种供用户选择
N=400             # 珍藏的总人数。

# """ 计算珍藏费增长公式 """
# 生成数据
n_values = np.arange(0, 400, 1)
P_values = logistic_growth(n_values, P1, m, v, C)
print(n_values, P_values)
# 绘制趋势图
plt.plot(n_values, P_values, label='Logistic Growth')
plt.xlabel('n')
plt.ylabel('P(n)')

plt.legend()
plt.show()
#
# """ 计算贡献池总量增长公式 """
# # 生成数据
# n_values = np.arange(0, 1000, 1)
# T_values = bonus_pool(b, N, P1, m, v, C)
# # 绘制趋势图
# plt.plot(n_values, T_values, label='T Growth')
# plt.xlabel('N')
# plt.ylabel('T(N)')
# plt.title('T Growth Trend')
# plt.legend()
# plt.show()

""" 计算贡献池结算公式 """
# 第n个用户珍藏，前N - 1个用户将平均获得：p(n) / (N - 1)

# P_values = pool_dividend(b, N, P1, m, v, C)
# print(P_values)


