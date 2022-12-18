#Importing Libraries
import pandas as pd
import lasio as la
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

#### DATA LOADING AND CLEANSING
#Enter File Path here
file= r'C:\Users\user\Downloads\Plots\1051661275.las'

#Reading the las file
well=la.read(file)

#Conversion of las file to dataframe
df=well.df()

#Reset the index of pandas dataframe 
df=df.reset_index()
#Cleansing na values
df_dropped=df.dropna(axis=0,how='any')

#Selecting valid range values from selective logs
df_filt1 = df_dropped.loc[(df_dropped.CNPOR > -15) & (df_dropped.CNPOR <= 50)]
df_filt2 = df_filt1.loc[(df_dropped.GR > 0) & (df_dropped.GR  <= 150)]
df_filt3 = df_filt2.loc[(df_dropped.RHOB> 1) & (df_dropped.RHOB<= 3)]
df_filt = df_filt3.loc[(df_dropped.DT > 30) & (df_dropped.DT <= 140)]
df_filt = df_filt3.loc[(df_dropped.RILD > 0.2) & (df_dropped.RILD <= 2000)]

#Options to display max number of columns
pd.set_option('display.max_columns', None)
# Display statistics of the data
print(df_filt.describe(include='all'))


#### DATA VISUALIZATION
# Set up the scatter plot Neutron porosity and Density log
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

# Creating Histograms of GR
plt.hist(df_filt['GR'], bins=30, color='green', alpha=0.5, edgecolor='black')
plt.xlabel('Gamma Ray - API', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.xlim(0,200)

plt.savefig('histogram(GR).png', dpi=300)
plt.show()

#Creating Histogram of RILD
plt.hist(df_filt['RILD'], bins=1000, color='red', alpha=0.5, edgecolor='black')
plt.xlabel('RILD', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.semilogx()

plt.savefig('histogram(RILD).png', dpi=300)
plt.show()

#Changing the DEPT to DEPTH
df_filt.rename(columns={'DEPT':'DEPTH'},inplace=True)

#Creating Subplots to plot all logs in tracks
fig, axes = plt.subplots(figsize=(10,10))

#Defining name of the logs
curve_names = ['Gamma', 'Deep Res', 'Shallow Res','Density', 'Neutron','Vsh']

#Set up the plot axes
ax1 = plt.subplot2grid((1,4), (0,0), rowspan=1, colspan = 1) 
ax2 = plt.subplot2grid((1,4), (0,1), rowspan=1, colspan = 1)
ax3=ax2.twiny()
ax4 = plt.subplot2grid((1,4), (0,2), rowspan=1, colspan = 1)
ax5 = ax4.twiny()
ax6=plt.subplot2grid((1,4), (0,3), rowspan=1, colspan = 1)


#Set up the individual log tracks / subplots
ax1.plot("GR", "DEPTH", data = df_filt, color = "green", lw = 0.5)
ax1.fill_betweenx(df_filt['DEPTH'], 55, df_filt['GR'], where=df_filt['GR']<=55, facecolor='yellow')
ax1.fill_betweenx(df_filt['DEPTH'], df_filt['GR'], 55, where=df_filt['GR']>=60, facecolor='green')
ax1.set_xlim(0, 150) 
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

#Paramters for fill the RHOB and CNPOR cross overs with yellow and otherwise green
x = np.array(ax4.get_xlim())
z = np.array(ax5.get_xlim())

x1 = df_filt['RHOB']
x2 = df_filt['CNPOR']

nz=((x2-np.max(z))/(np.min(z)-np.max(z)))*(np.max(x)-np.min(x))+np.min(x)

ax4.fill_betweenx(df_filt['DEPTH'], x1, nz, where=x1>=nz, interpolate=True, color='green')
ax4.fill_betweenx(df_filt['DEPTH'], x1, nz, where=x1<=nz, interpolate=True, color='yellow')

#Set up the common elements between the subplots
for i, ax in enumerate(fig.axes):
    ax.set_ylim(5000, 400) # Set the depth range
    
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



### DATA ANALYSIS
# Making Copy of the data frame
new_df_filt=df_filt.copy()

# Calculating Volume of Shale 
new_df_filt['Vsh'] = (new_df_filt.GR - new_df_filt.GR.min()) / (new_df_filt.GR.max() - new_df_filt.GR.min())
# Print Volume of shale log
print(new_df_filt['Vsh'])

# Plotting Volume of shale in the log plot
ax6.plot("Vsh", "DEPTH", data = new_df_filt, color = "green", lw = 0.5)
ax6.fill_betweenx(df_filt['DEPTH'], 0, new_df_filt['Vsh'], facecolor='green')
ax6.set_xlim(0, 1) 
ax6.spines['top'].set_edgecolor('green')
plt.savefig('logplot.png', dpi=150)
#Defining Cuts based on GR (volume of shale)
new_df_filt['facies_gr'] = pd.cut(new_df_filt['Vsh'], bins=[0,0.15,1], labels=['clean', 'shaly'] )

# Delineating Clean zones to check reservoir quality
value=new_df_filt.loc[lambda new_df_filt:new_df_filt['GR']<25]
# Function to determine Reservoir Quality
def ReservoirQuality():
    
    for i in value['DEPTH']:
        print ('Reservoir Quality high at ' + str(i) )  
    
ReservoirQuality()

# Delineating High Resistive zones to mark hydrocarbons shows
hc=new_df_filt.loc[lambda new_df_filt:new_df_filt['RILD']>400]
# Function to determine Hydrocarbon zones
def Hydrocarbonshows():

    for i in hc['DEPTH']:
        print ('Hydrocarbons shows at ' + str(i) )  

Hydrocarbonshows()

#Function to determine Hydrocarbon Height
def Hydrocarbonheight():
    height=hc['DEPTH'].max()-hc['DEPTH'].min()
    return height
  
print('Hydrocarbon Thickness is '+ str(Hydrocarbonheight()))   

# Function to Calculate Effective Stress
def Effectivestress():
    matrix_density = 2.7   # in (g/cc)
    fluid_density = 1      # in (g/cc)
    phi_init = 0.40        # initial porosity
    beta = 0.03            # compaction coefficient in 1/MPa

    # Calculate Porosity  
    new_df_filt['Porosity'] = (matrix_density - new_df_filt['RHOB']) / (matrix_density - fluid_density)
    new_df_filt['Porosity'] = np.where(new_df_filt['Porosity']>=0, new_df_filt['Porosity'], 0)
    depth=new_df_filt['DEPTH']
    density=new_df_filt['RHOB']
    density_water = 1. * np.ones_like(density)
    g = 9.8 # in (m/s2)
    
    # Compute Sv(vertical stress) in MPa
    new_df_filt['Sv(MPa)'] = integrate.cumtrapz(density * 9.81 * 1000 / 1e6, depth, initial=0)

    # Compute Shydro(Hydrostatic Pressure) in MPa
    new_df_filt['Shydro(MPa)'] = integrate.cumtrapz(density_water * 9.81 * 1000 / 1e6, depth, initial=0)
    # Compute Pp(Pore Pressure) in MPa
    new_df_filt['Pp(MPa)'] =  new_df_filt['Sv(MPa)'][-len( new_df_filt['Porosity']):] - (np.log(new_df_filt['Porosity'] / phi_init) / -beta)
    # Compute sigma_eff(Effective Pressure) in MPa
    new_df_filt['Sigma_Eff(MPa)'] = new_df_filt['Sv(MPa)'][-len(new_df_filt['Porosity']):] - new_df_filt['Pp(MPa)']
    #Plot For Vertical Stress, Hydrostatic Pressure, Pore Pressure,Effective Stress
    fig = plt.figure(figsize=(14,10))
    ax1 = fig.add_subplot(111)
    plt.plot(new_df_filt['Sv(MPa)'], depth, 'k', label="Vertical Stress") 
    plt.plot(new_df_filt['Shydro(MPa)'], depth, 'b', label="Hydrostatic Pressure") 
    plt.plot(new_df_filt['Pp(MPa)'], depth, 'r', label="PorePressure", linewidth=0.4)
    plt.plot(new_df_filt['Sigma_Eff(MPa)'], depth, 'g', label="Effective Stress", linewidth=0.3);
    plt.grid()
    plt.legend(loc=1)
    plt.xlabel("Pressure (MPa)", fontsize = '14')
    plt.ylabel("Depth (m)", fontsize = '14')
    ax1.set_yticks(np.arange(new_df_filt['DEPTH'].min(), new_df_filt['DEPTH'].max()+100, step=200))
    ax1.set_xlim(0, new_df_filt['Sv(MPa)'].max()+5)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()    
Effectivestress()
# Marking of Hydrocarbons zones on logs
ax6.axhline(hc['DEPTH'].min(), color = 'r', linestyle = '-')
ax6.axhline(hc['DEPTH'].max(), color = 'r', linestyle = '-')
