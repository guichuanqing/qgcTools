import numpy as np
import matplotlib.pyplot as plt
from decimal import *

# getcontext().prec = 18
CREATOR_PREMINT = Decimal(10 ** 8)
totalSupply = Decimal(1)

def curve(x):
    if x <= CREATOR_PREMINT:
        return 0
    return (x - CREATOR_PREMINT) * (x - CREATOR_PREMINT) * (x - CREATOR_PREMINT)

def price(supply, amount):
    return Decimal((curve(supply + amount) - curve(supply)) / CREATOR_PREMINT /Decimal(500)) / Decimal(10 ** 18)

def buyPrice(totalSupply, amount):
    totalSupply = totalSupply * CREATOR_PREMINT
    amount = amount * CREATOR_PREMINT
    a = price(totalSupply, amount)
    return a

def sellPrice(totalSupply, amount):
    totalSupply = totalSupply * CREATOR_PREMINT
    amount = amount * CREATOR_PREMINT
    a = price(totalSupply-amount, amount)
    return a

# 计算用户购买/售卖的价值费用
def user_fee(user, type, supply=1):
    fees =[]
    fee = 0
    if user:
        for i in user:
            if type == 'buy':
                fee = buyPrice(supply, i)
                supply += i
            if type == 'sell' and supply > 0:
                fee = sellPrice(supply, i)
                supply -= i
            fees.append(fee)
    return fees

# 当前购买总vote数
def sum_l(l):
    sum = Decimal(1)
    if l:
        for i in l:
            sum +=Decimal(i)
    return sum

# 基础质押费公式
def base_stack_fee(user_fee):
    return Decimal(user_fee)*Decimal('0.05')

#返回所有用户的基础质押费
def users_base_stack(user_fees):
    all_base_stack = []
    for i in user_fees:
        all_base_stack.append(base_stack_fee(i))
    return all_base_stack

#总质押奖池费用
def base_stack_pool(users_base_stack):
    stack_pool = 0
    for i in users_base_stack:
        stack_pool+=Decimal(i)
    return stack_pool



# 生成数据 Decimal('0.00000001')
# a = Decimal('0.001')
buy_user = [Decimal('10'),Decimal('10'),Decimal('10'),Decimal('100')]
sell_user = [Decimal('1')]
print(buy_user)
n_values = np.arange(1, len(buy_user)+1, 1)
type1 = 'buy'
type2 = 'sell'
user_fee_buy = user_fee(buy_user, type1)
user_fee_sell = user_fee(sell_user, type2, sum_l(buy_user))

user_base_stack1 = users_base_stack(user_fee_buy)
stack_pool1 = base_stack_pool(user_base_stack1)

user_base_stack2 = users_base_stack(user_fee_sell)
stack_pool2 = base_stack_pool(user_base_stack2)

print('购买费:', [format(a, 'f') for a in user_fee_buy], end=' ')
print('质押费:', [format(a, 'f') for a in user_base_stack1], '一半',[format(a/2, 'f') for a in user_base_stack1],end=' ')
print('总质押奖励:', stack_pool1,)

print('售出费:', [format(a, 'f') for a in user_fee_sell], end=' ')
print('质押费:', [format(a, 'f') for a in user_base_stack2], '一半', [format(a/2, 'f') for a in user_base_stack2], end=' ')
print('总质押奖励:', stack_pool2,)







# P_values = user_fee(user, type, 30)
# 绘制趋势图
# plt.plot(n_values, P_values, label='Logistic Growth')
# plt.xlabel('n')
# plt.ylabel('P(n)')
#
# plt.legend()
# plt.show()

