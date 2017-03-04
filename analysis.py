#!/usr/bin/env python

from ggplot import *
import matplotlib.pyplot as plt
import pandas as pd
import itertools
import random
import scipy.stats as stats
import numpy as np

TOTAL_SAMPLES = 40
CARDS = list(itertools.product(range(1,14),['Spade','Heart','Diamond','Club']))

def getAllCardValues(cards):
	values = []
	for card in cards:
		value = card[0]
		if (value >= 10):
			value = 10
		values.append(value)
	return values

def getOneSample(cards):
	deck = list(cards)
	value = drawOneCard(deck)[0] + drawOneCard(deck)[0] + drawOneCard(deck)[0]
	return value

def drawOneCard(cards):
	# shuffle the cards
	random.shuffle(cards)
	drawnCard = cards[0]
	cards = cards[1:]
	return drawnCard

def plotFrequency(dataFrame, column, title_suffix, file_path):
	plot = ggplot(dataFrame, aes(x=column)) + geom_bar(fill='dodgerblue')
        plot = plot + labs(title="Histogram for Frequecy for " + title_suffix) + labs(x="Card values", y="Frequecy")
        print (plot)
        plot.save(file_path + '_frequency.png')

def plotRelativeFrequency(dataFrame, column, title_suffix, file_path):
        plot_relative = dataFrame.plot(kind='hist', normed=1, bins=20, stacked=False, alpha=.5, title='Histogram for Relative Frequency of ' + title_suffix)
        plot_relative.set_xlabel("Card Value")
        plot_relative.set_ylabel("Relative Frequency")
        fig = plt.gcf()
        plt.show()
        fig.savefig(file_path + '_relative_frequency.png')

def plotSampledDistribution(dataFrame, column, file_path):
	sorted_data = sorted(dataFrame[column])
	# Add histogram
	plot_relative = dataFrame.plot(kind='hist', normed=1, bins=20, stacked=False, alpha=.5, title='Histogram for Sampled Distribution')
        plot_relative.set_xlabel("Card Value")
        plot_relative.set_ylabel("Relative Frequency")
	# Add mean
	print 'Mean :- '
        print np.mean(sorted_data)
	# Add median
	print 'Median :- '
        print np.median(sorted_data)
	# Add Mode 
	print 'Mode :- '
        print stats.mode(sorted_data)[0][0]
	# Add normal distribution
	fit = stats.norm.pdf(sorted_data, np.mean(sorted_data), np.std(sorted_data))
	plt.plot(sorted_data, fit, '-o')
	# Show and save the image
	fig = plt.gcf()
	plt.show()
	fig.savefig(file_path + '_distribution.png')

if __name__ == "__main__":
	# print CARDS
	cardValues = getAllCardValues(CARDS)
	# print cardValues
	rfDataFrame = pd.DataFrame({'values':cardValues})
	# print rfDataFrame

	# Plot the frequency and the relative frequency for card values
	plotFrequency(rfDataFrame, 'values', "Card Values", 'graph/card')
	plotRelativeFrequency(rfDataFrame, 'values', "Card Values", 'graph/card')

	# Generate the sample Distribution
	samples = []
	for i in range(TOTAL_SAMPLES):
		samples.append(getOneSample(CARDS))
	sampleDistributionDF = pd.DataFrame({'samples': samples})
	# print sampleDistributionDF

	# Plot the sample distribution
	plotSampledDistribution(sampleDistributionDF, "samples", 'graph/sampled_normal')

	# Print the variability for the sampled distribution
	sorted_data = sorted(sampleDistributionDF['samples'])
	print 'Standard Deviation :-'
        print np.std(sorted_data)
	print 'Interquartile range(IQR) :- '
	print np.percentile(sorted_data, 75) - np.percentile(sorted_data, 25)

