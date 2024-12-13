import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\leono_sg\OneDrive\Desktop\FCUL\FCD\Data_Cleaned.csv')

neighbourhood  = df['neighbourhood group'].unique()
print(neighbourhood)
Brooklyn = df[(df['neighbourhood group']=='Brooklyn')]
Manhattan = df[(df['neighbourhood group']=='Manhattan')]
Queens = df[(df['neighbourhood group']=='Queens')]
Staten_Island = df[(df['neighbourhood group']=='Staten Island')]
Bronx = df[(df['neighbourhood group']=='Bronx')]


brookV = Brooklyn[(Brooklyn['host_identity_verified']=='verified')]
brookNV = Brooklyn[(Brooklyn['host_identity_verified']=='unconfirmed')]
ManV = Manhattan[(Manhattan['host_identity_verified']=='verified')]
ManNV = Manhattan[(Manhattan['host_identity_verified']=='unconfirmed')]
QueensV = Queens[(Queens['host_identity_verified']=='verified')]
QueensNV = Queens[(Queens['host_identity_verified']=='unconfirmed')]
StatenIV = Staten_Island[(Staten_Island['host_identity_verified']=='verified')]
StatenINV = Staten_Island[(Staten_Island['host_identity_verified']=='unconfirmed')]
BronxV = Bronx[(Bronx['host_identity_verified']=='verified')]
BronxNV = Bronx[(Bronx['host_identity_verified']=='unconfirmed')]

userVerificationPrice = {
    'Verified': (brookV.loc[:,"price"].mean(), ManV.loc[:,"price"].mean(), QueensV.loc[:,"price"].mean(),StatenIV.loc[:,"price"].mean(), BronxV.loc[:,"price"].mean()),
    'Unconfirmed': (brookNV.loc[:,"price"].mean(), ManNV.loc[:,"price"].mean(), QueensNV.loc[:,"price"].mean(),StatenINV.loc[:,"price"].mean(), BronxNV.loc[:,"price"].mean())
}

x = np.arange(len(neighbourhood))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in userVerificationPrice.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Mean Price')
ax.set_title('Mean price by neighbourhood')
ax.set_xticks(x + width, neighbourhood)
ax.legend(loc='upper left', ncols=3)
ax.set_ylim(0, 600)

plt.show()

#print(brooNV.loc[:,"price"].mean())

