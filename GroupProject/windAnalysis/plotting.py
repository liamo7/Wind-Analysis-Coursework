from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib import cm
from matplotlib.colors import ListedColormap
from scipy.stats import shapiro, normaltest, exponweib


def correlation(data, column1, column2, axes, showRegressionLine=True, showR2=True):
    axes.set_title('Correlation: '+column1+' vs. '+column2)
    axes.scatter(data[column1], data[column2], color=['r'])

    if showRegressionLine:
        par = np.polyfit(data[column1], data[column2], 1, full=True)

        slope=par[0][0]
        intercept=par[0][1]
        xl = [min(data[column1]), max(data[column1])]
        yl = [slope*xx + intercept  for xx in xl]

        if showR2:
            variance = np.var(data[column2])
            residuals = np.var([(slope*xx + intercept - yy)  for xx,yy in zip(data[column1],data[column2])])
            R2 = np.round(1-residuals/variance, decimals=2)
            plt.text(min(data[column1]),max(data[column2]),'$R^2 = %0.2f$'% R2, fontsize=20)
            plt.grid(axis='both')
            # plt.text(-11,20,'$R^2 = %0.2f$'% R2, fontsize=20)

    axes.set_ylabel(column1)
    axes.set_xlabel(column2)

    # # error bounds
    # yerr = [abs(slope*xx + intercept - yy)  for xx,yy in zip(data[column1],data[column2])]
    # par = np.polyfit(data[column1], yerr, 2, full=True)
    #
    # yerrUpper = [(xx*slope+intercept)+(par[0][0]*xx**2 + par[0][11]*xx + par[0][2]) for xx,yy in zip(data[column1],data[column2])]
    # yerrLower = [(xx*slope+intercept)-(par[0][0]*xx**2 + par[0][11]*xx + par[0][2]) for xx,yy in zip(data[column1],data[column2])]

    axes.plot(xl, yl, '--r')

def distribution(data, column, norm=True, plotWeibull=False, upperLimit=1.0, title=''):
    x = np.linspace(data[column].min(), data[column].max(), 1000)
    if plotWeibull:
        plt.plot(x, exponweib.pdf(x, *exponweib.fit(data[column], 1, 1)))
    plt.title(title)
    return plt.hist(data[column], bins=np.linspace(0, upperLimit), normed=norm, alpha=0.5);

def fft(data, column, ax):
    trend = np.mean(data[column])
    spectrum = np.fft.fft(data[column]-trend)
    frequencies = np.fft.fftfreq(len(data[column]))
    ax.plot(frequencies, spectrum.real)

def isDataLine(x):
    return isinstance(x, mlines.Line2D) and isinstance(x.get_xdata(), np.ndarray)

def lidarProfile(data, columns, heights, ax, title='Wind profiles'):
    try:
        print(data)
        cmap = cm.get_cmap('rainbow')
        line_colors = cmap(np.linspace(0,1,24))
        colors = np.asarray(data.index.hour)

        ax.set_title(title)
        profiles = ax.plot(data[columns].T, heights)
        ax.set_ylabel('Height agl (m)')
        ax.set_xlabel('Wind speed')

        colors = [line_colors[int(i.strftime('%H'))] for i in data.index]
        for l, c in zip(profiles, colors):
            l.set_color(c)

        cmap2 = ListedColormap(line_colors)
        sm = plt.cm.ScalarMappable(cmap=cmap2, norm=plt.Normalize(vmin=0,vmax=23))
        sm.set_array([])

        cbar = plt.colorbar(sm)
        cbar.set_label('Hour of the day')
        cbar.set_ticks(np.arange(0,24))
        cbar.set_ticklabels(np.arange(0,24))

    except:
        print('No data to plot')

def mapToColorHex(rangeMin, rangeMax, value):
    oldRange = rangeMax - rangeMin + 1
    newRange = 16777215
    return '#'+hex(((value - rangeMin) * newRange) / oldRange).replace('0x','').replace('L','').zfill(6)

def orderedWindShearExponent(data):
    plt.figure()
    plt.title('Ordered wind shear exponent')
    print(data)
    scatter = plt.scatter(range(len(data['WindShearExponent'])), sorted(data['WindShearExponent']), color=['r'])
    plt.show()

def powerCurve(data, windSpeedBinColumn, powerColumn, axes, useColor=['b']):
    axes.scatter(data[windSpeedBinColumn], data[powerColumn], marker='.', s=1, color=useColor)
    axes.set_ylabel(windSpeedBinColumn)
    axes.set_xlabel(powerColumn)


def shearExponent(data, threshold=10.0):
    plt.figure()
    plt.title('Wind shear exponent frequency (hub height wind speed > '+str(threshold)+' m/s)')
    thresholded = data[data['mean_wind_speed_73.5m']>=threshold]
    belowZero = plt.hist(thresholded[thresholded['WindShearExponent']>=0]['WindShearExponent'], bins = np.linspace(-5, 5, 1000), linewidth=0, color=['b'])
    aboveZero = plt.hist(thresholded[thresholded['WindShearExponent']<0]['WindShearExponent'], bins = np.linspace(-5, 5, 1000), linewidth=0, color=['r'])
    plt.legend(('>= 0', '< 0'))
    plt.show()

def surface(data, col1, col2, col3):
    data1 = data.dropna().sort(col3)
    print(data1.head())
    x = data1[col1]
    y = data1[col2]
    z = data1[col3]

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)

    plt.show()

def TI(data):
    plt.figure()
    plt.title('TI frequency at hub height')
    plt.hist(data['TI_73.5m'], bins = np.linspace(0, 1, 1000), linewidth=0, color=['r'])
    plt.show()

def timestampToInt(ts):
    return int(ts.strftime('%H')) * 6 + int(ts.strftime('%M'))

def TIScatter(data):
    plt.figure()
    plt.title('TI vs. hub height wind speed')
    scatter = plt.scatter(data['mean_wind_speed_73.5m'], data['TI_73.5m'], color=['r'])
    plt.show()

def TIShearScatter(data):
    plt.figure()
    plt.title('TI vs. wind shear exponent')
    scatter = plt.scatter(data['WindShearExponent'], data['TI_73.5m'], color=['r'])
    plt.show()



def windShearScatter(data):
    plt.figure()
    plt.title('Wind shear exponent vs. hub height wind speed')
    scatter = plt.scatter(data['mean_wind_speed_73.5m'], data['WindShearExponent'], color=['r'])
    plt.show()


