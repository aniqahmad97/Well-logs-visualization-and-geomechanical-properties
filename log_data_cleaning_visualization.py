import pandas as pd
import lasio as la
import numpy as np
import matplotlib.pyplot as plt


# Add Las file Path below
file= r'C:\Users\user\Downloads\Plots\1051661161.las'
well=la.read(file)
df=well.df()
df=df.reset_index()

df_dropped=df.dropna(axis=0,how='any')

df_filt1 = df_dropped.loc[(df_dropped.CNPOR > -15) & (df_dropped.CNPOR <= 50)]
df_filt2 = df_filt1.loc[(df_dropped.GR > 0) & (df_dropped.GR  <= 250)]
df_filt3 = df_filt2.loc[(df_dropped.RHOB> 1) & (df_dropped.RHOB<= 3)]
df_filt = df_filt3.loc[(df_dropped.DT > 30) & (df_dropped.DT <= 140)]
#print(df_dropped.isna().sum())
#print(df.isna().sum())
pd.set_option('display.max_columns', None)
print(df_filt.describe(include='all'))
# Set up the scatter plot
plt.scatter(x='CNPOR', y='RHOB', data=df, c='GR', vmin=0, vmax=250, cmap='rainbow')

# Change the X and Y ranges
plt.xlim(-15, 45)

# For the y axis, we need to flip by passing in the scale values in reverse order
plt.ylim(3.0, 1.0)

# Add in labels for the axes
plt.ylabel('Bulk Density (DEN) - g/cc', fontsize=14)
plt.xlabel('Neutron Porosity (NEU) - %', fontsize=14)

# Make the colorbar show
plt.colorbar(label='Gamma Ray - API')

plt.savefig('scatterplot.png', dpi=300)
plt.show()

# Creating Histograms
plt.hist(df_filt['GR'], bins=30, color='green', alpha=0.5, edgecolor='black')
plt.xlabel('Gamma Ray - API', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xlim(0,200)

plt.savefig('histogram.png', dpi=300)
plt.show()

plt.hist(df_filt['RILD'], bins=30, color='red', alpha=0.5, edgecolor='black')
plt.xlabel('RILD', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.semilogx()

plt.savefig('histogramRILD.png', dpi=300)

plt.show()

df_filt.rename(columns={'DEPT':'DEPTH'},inplace=True)
#print(df_filt.head())


fig, axes = plt.subplots(figsize=(10,10))

curve_names = ['Gamma', 'Deep Res', 'Shallow Res','Density', 'Neutron','Vsh']


#Set up the plot axes
ax1 = plt.subplot2grid((1,3), (0,0), rowspan=1, colspan = 1) 
ax2 = plt.subplot2grid((1,3), (0,1), rowspan=1, colspan = 1)
ax3=ax2.twiny()
ax4 = plt.subplot2grid((1,3), (0,2), rowspan=1, colspan = 1)
ax5 = ax4.twiny()


#Set up the individual log tracks / subplots
ax1.plot("GR", "DEPTH", data = df_filt, color = "green", lw = 0.5)
#ax1.fill_betweenx(df_filt['DEPTH'], 0, df_filt['GR'], facecolor='green')
ax1.set_xlim(0, 250) 
ax1.spines['top'].set_edgecolor('green')

ax2.plot("RILD", "DEPTH", data = df_filt, color = "red", lw = 0.5)
ax2.set_xlim(0.2, 2000)
ax2.semilogx()
ax2.spines['top'].set_edgecolor('red')

ax3.plot("RLL3", "DEPTH", data = df_filt, color = "blue", lw = 0.5)
ax3.set_xlim(0.2, 2000)
ax3.semilogx()
ax3.spines['top'].set_edgecolor('blue')

ax4.plot("RHOB", "DEPTH", data = df_filt, color = "red", lw = 0.5)
ax4.set_xlim(1, 3)
ax4.spines['top'].set_edgecolor('red')


ax5.plot("CNPOR", "DEPTH", data = df_filt, color = "blue", lw = 0.5)
ax5.set_xlim(45, -15)
ax5.spines['top'].set_edgecolor('blue')


left_value = 0
right_value = 250
span = abs(left_value-right_value)

cmap=plt.get_cmap('hot_r')

color_index = np.arange(left_value, right_value, span/100)


for index in sorted(color_index):
    index_value = (index - left_value)/span
    color = cmap(index_value)
    ax1.fill_betweenx(df_filt['DEPTH'], left_value, df_filt['GR'], where=df_filt['GR']>=index, color=color)

x = np.array(ax4.get_xlim())
z = np.array(ax5.get_xlim())

x1 = df_filt['RHOB']
x2 = df_filt['CNPOR']

nz=((x2-np.max(z))/(np.min(z)-np.max(z)))*(np.max(x)-np.min(x))+np.min(x)

ax4.fill_betweenx(df_filt['DEPTH'], x1, nz, where=x1>=nz, interpolate=True, color='green')
ax5.fill_betweenx(df_filt['DEPTH'], x1, nz, where=x1<=nz, interpolate=True, color='yellow')

#Set up the common elements between the subplots
for i, ax in enumerate(fig.axes):
    ax.set_ylim(3000, 195) # Set the depth range
    
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")
    ax.set_xlabel(curve_names[i])
 
    if (i == 3) or (i == 2):
        ax.spines["top"].set_position(("axes", 1.08))
    else:
        ax.grid()
        

#Hide tick labels on the y-axis 
for ax in [ax2, ax3]:
    plt.setp(ax.get_yticklabels(), visible = False)

#Reduce the space between each subplot
fig.subplots_adjust(wspace = 0.05)

plt.savefig('logplot.png', dpi=150)







