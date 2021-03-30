import streamlit as st
import os
import pandas as pd
import altair as alt
import seaborn as sns
from PIL import Image
import plotly.express as px

st.set_option('deprecation.showPyplotGlobalUse', False)
def main():
	create_layout()

def create_layout():
	app_mode = st.sidebar.selectbox("Please select a page", ["Homepage : Data Description",
                                                             "Attribution Models",
                                                             "Visualizations",
                                                             "Conclusions",
                                                             "References"])
	if app_mode == 'Homepage : Data Description':
		load_homepage()
	elif app_mode == 'Attribution Models':
		load_attribution()
	elif app_mode == 'Visualizations':
		load_visualizations()
	elif app_mode == 'Conclusions':
		load_conclusions()
	elif app_mode == 'References':
		load_reference()


def load_homepage():
	st.title('Attribution Modeling and Budget Optimization')
st.title('Attribution Modeling and Budget Optimization')
st.markdown('Customer journey is an integral part of the analysis of the campaigns for marketers. It provides insights about the engagements and impact of the marketing strategies on the customers. As part of the marketing, marketers execute many campaigns and/or run it across channels. It is important to analyze these channels for future implementations. ')
 	# customer Journey Image here
#cust_journey = Image.open('cust_journey.jpg')
st.image('cust_journey.jpg', width = 800)
st.markdown('Marketers make use of multiple channels and campaigns for marketing and targeting customers and this leads to the problem of marketing spend optimization, which requires estimating the true contribution of individual channels and optimally allocating budgets across these channels.')
st.markdown('Criteo has published an online advertising dataset which has details of campaigns and budget allocated for each of them. The aim is to check the cross-channel Optimization using various parameters to access which channel should be getting the maximum budget for advertisement.')
 	# Channel Distribution image here
chan_dist = Image.open('chan_dist.png')
st.image(chan_dist, width = 800)
st.subheader('Data Description')
st.markdown('This dataset represents a sample of 30 days of Criteo live traffic data. Each line corresponds to one impression (a banner) that was displayed to a user. For each banner we have detailed information about the context, if it was clicked, if it led to a conversion and if it led to a conversion that was attributed to Criteo or not.')
st.markdown("♟ Timestamp : timestamp of the impression (starting from 0 for the first impression). The dataset is sorted according to timestamp. ")
st.markdown("♟ UID : Unique User Identifier")
st.markdown("♟ Campaign : Unique Campaign Identifier")
st.markdown("♟ Conversion :  1 if there was a conversion in the 30 days after the impression; 0 otherwise")
st.markdown("♟ Conversion ID :  A unique identifier for each conversion")
st.markdown("♟ Click : 1 if the impression was clicked; 0 otherwise")
st.markdown("♟ Cost: The price paid for this ad ")
st.markdown("♟ Cat1-Cat9 : Categorical features associated with the ad")
st.subheader("Key Figures")
st.markdown("* 2.4Gb uncompressed")
st.markdown("* 16.5M impressions")
st.markdown("* 45K conversions")
st.markdown("* 700 campaigns")




def load_attribution():
	st.title('Attribution Modeling and Budget Optimization')
	st.subheader('What is Attribution Modeling?')

	st.markdown('An attribution model is the rule, or set of rules, that determines how credit for sales and conversions is assigned to touchpoints in conversion paths. By analyzing each attribution model one can derive the ROI for each marketing channel.')
	imageAttribution = Image.open('AttributionModeling.jpg')
	st.image(imageAttribution, width = 800)
	st.markdown('There are six common attribution models and below are the attributions which we have implemented.')
	st.markdown('1. Single Touch Attribution Model')
	st.markdown('* Last Touch Attribution')
	st.markdown('* First Touch Attribution')
	st.markdown('2. Multi Touch Attribution')
	st.markdown('* Linear Attribution')
	st.markdown('* Time Decay Attribution')
	st.markdown('* U Shaped Attribution')
	st.markdown('3. Data Driven Attribution')
	st.markdown('* Logistic Regression')

	st.subheader('Last Touch Attribution')
	st.markdown('This is the simplest form of attribution which assigns all the credits to the last touch point right before conversion.It gives 100% of the credit for a conversion to the last click or visit that happened in a conversion path. If there was no click or visit, then it will credit the last impression.')
	st.markdown('* Pros')
	st.markdown('It’s easy to implement.')
	st.markdown('It\'s good for short sales cycles.')
	st.markdown('Smallest possibility of error to occur in the analysis phase.')
	st.markdown('* Cons')
	st.markdown('Whole customer journey is not taken into consideration.')
	st.markdown('It does not provide proper feedback about the content created.')

	#Add image here.
	#lta_model = Image.open('lta_model.png')
	st.image('lta_model.png')

	st.subheader('First Touch Attribution')
	st.markdown('This is another simple form of attribution modelling. It over-emphasizes the top of the funnel. It gives 100% of the credit for a conversion to the first click or visit that happened in a conversion path.')
	st.markdown('* Pros')
	st.markdown('It is critically important because it tells you how customers first heard about marketers campaign. Marketers call this \'New lead generation superstars\'')
	st.markdown('* Cons')
	st.markdown('Similar to Last Touch Attribution, giving all the importance to first click does not provide much information/feedback about the overall campaigns.')

	#Add image here.
	st.image('fta_model.png')

	st.subheader('Linear Attribution')
	st.markdown('This model assigns credit evenly to every marketing touch throughout the customer journey.')
	st.markdown('* Pros')
	st.markdown('Instead of focusing on a particular touchpoint, marketers can take a balanced look at your whole marketing strategy.')
	st.markdown('* Cons')
	st.markdown('Giving equal credits to low-value and high-value activities results in improper tuning of the campaigns.')

	st.image('la_model.png')
	#Add image here.

	st.subheader('Time Decay Attribution')
	st.markdown('Time Decay Attribution model assigns more the most credit to the events that are closer to the date of conversion.')
	st.markdown('* Pros')
	st.markdown('It recognizes the significance of the interaction leading up to the conversion while still placing value on the activities.')
	st.markdown('Since the recent touchpoint resulted in conversion, time-decay attribution assigns not the full but maximum reward to the last touchpoint.')
	st.markdown('* Cons')
	st.markdown('It lacks the ability to recognize the interaction of the event that introduced the customer to your brand. It may result in a low amount of credit for highly influential touches.')

	st.image('tda-model.png')
	#Add image here.

	st.subheader('U Shaped Attribution')
	st.markdown('This model combines the best features of linear and time decay by giving weightage of 40% to the extreme touchpoints and the rest 20% is equally split between the intermediate touchpoints.')
	st.markdown('* Pros')
	st.markdown('This model ensures that every touchpoint receives some credit for the contribution towards conversion. It lets you assign significant credit to the event that introduced the customer to the product and point that got to the conversion.')
	st.markdown('* Cons')
	st.markdown('This could result in two very low value touches being given too much credit. Might cause problem in optimization of the campaigns.')

	st.image('ua_model.png')
	#Add image here.

	st.subheader('Logistic Regression')
	st.markdown('Every journey is represented as a vector in which each campaign is represented by a feature, a regression model is fit to predict conversions. The regression coefficients are interpreted as attribution weights.')

def load_visualizations():
	import matplotlib.pyplot as plt
	st.set_option('deprecation.showPyplotGlobalUse', False)
	st.subheader('Last Touch Attribution')
	st.image(Image.open('Results- LTA.png'), width = 800)
	# Add LTA results herre

	st.markdown('In this model, we gave all the 100% credit to the touchpoint that lead to conversion. We found the normalized maximum timestamp and assigned it the full weightage. The con of this touchpoint is that it could miss all the  other touchpoints that lead to the conversion.')


	st.subheader('First Touch Attribution')
	st.image(Image.open('Results- fta.png'), width = 800)
	# Add FTA results here

	st.markdown('In this model, we found the minimum value of the normalized timestamp and gave it 100% of the weightage.')

	st.subheader('Linear Attribution')
	st.image(Image.open('Results- lin.png'), width = 800)
	# Add LA results here


	st.markdown('For this model, the timestamp was normalized and equal weightage was given to all the touchpoints in the journey. It gives a balanced outlook to all the touchpoints but could miss to provide more weightage to high-value touchpoints.')

	st.subheader('Time Decay Attribution')
	st.image(Image.open('Results- tda.png'), width = 800)
	# Add TD results here

	st.markdown('In this model, we gave weightage to all the touchpoints but the way it gives weightage drastically varies as the touchpoints closer to the time of conversion is given more weightage.')

	st.subheader('U Shaped Attribution')
	st.image(Image.open('Results- Ua.png'), width = 800)
	# Add UA results here

	st.markdown('This model counts all the touchpoints emphasizing on the first and last touch points. For this, we have give 40% credit to the first and last touch points and ther est 20% is split between the intermediate touchpoints equally.')

	st.subheader('Logistic Regression')
	st.image(Image.open('Results- logreg.png'), width = 800)
	# Add LR results here

	st.markdown('logistic regression estimates the true incremental number of purchases or conversions that can be attributed to or give credit to a given marketing channel.')

	st.subheader('Comparison of Multi Touch Attribution')
	st.image(Image.open('Results- comparison.png'), width = 800)
	#Add image here


	st.markdown('After Modeling, we created a simulation algorithm to validate the whether the model will work if we allocated budgets to different channels based on the attribution weights. The below graph is used to compare different Return of Investment Models and to decide the marketing objective.')

	reward_list= [1076,1066,1148,1036,1066,1076,934,908,1132,1062,922,934,620,440,957,1062,416,620,307,321,294,1027,319,307,386,398,358,1048,399,386,421,449,403,1151,443,421,453,472,427,1315,468,453,484,502,493,524,500,484]

	print(len(reward_list))
	pitch_list= [0.1,0.25,0.5,1.0,1.5,2.0,2.5,3.0]
	print(len(pitch_list))
	lta_list=[]
	lin_list=[]
	usa_list=[]
	log_list=[]
	tda_list=[]
	fta_list=[]
	i = 0
	while i < len(reward_list):

	  lta_list.append(reward_list[i])
	  usa_list.append(reward_list[i+1])
	  tda_list.append(reward_list[i+2])
	  log_list.append(reward_list[i+3])
	  lin_list.append(reward_list[i+4])
	  fta_list.append(reward_list[i+5])
	  i = i + 6
	import matplotlib.pyplot as plt
	a=[lta_list,usa_list,tda_list,log_list, lin_list]
	b=['LTA','USA','TDA','LogReg', 'Linear', 'FTA']
	variables = st.sidebar.multiselect("Select the variables: LTA- Last Touch Attribution, USA- U Shaped Attribution, TDA- Time Decay Attribution, LogReg- Logistic Regression, Linear- Linear Attribution, FTA - First Touch Attribution", b)
	for i, j in zip(a, variables):
	  plt.plot(pitch_list, i,marker='o',label=j)
	plt.legend()
	plt.xlabel('Pitch')
	plt.ylabel('Return on Investment')
	plt.show()
	st.pyplot()



def load_reference():
	st.title('REFERENCES')

	st.markdown('https://www.youtube.com/watch?v=BfnJwYuFWVM')
	st.markdown('https://accutics.com/blog/last-touch-attribution-the-good-the-bad-and-the-ugly')
	st.markdown('https://www.callrail.com/blog/guide-to-u-shaped-attribution/')
	st.markdown('https://agencyanalytics.com/blog/marketing-attribution-models')
	st.markdown('https://nation.marketo.com/t5/Product-Discussions/Channel-based-vs-Campaign-based-tracking/td-p/135041')
	st.markdown('https://www.adroll.com/blog/marketing-analytics/first-last-touch-attribution-why-its-out-of-style')

def load_conclusions():
	st.title("Conclusions")
	st.markdown("Attribution facilitates the evaluation the performance of marketing efforts. It provides feedback on how your various channels/campaigns and touchpoints work together to produce optimal results. By measuring and evaluating the performance of your marketing channels on a user level, you can distribute resources in a way that drives the most conversions at the lowest cost to your business.")
	st.markdown('* We see that the raw attribution weights are not necessarily optimal for all models.')
	st.markdown('* Logistic Regression model provides the best budget allocation ')
	st.markdown('* Logistic Regression model seems to give a higher return of investment almost throughout the pitch though initially time decay attribution gives more return of investments in pitches of 0.0, 0.25.')
	st.markdown('* All the other models perform more or less similar to each other. These have poor performance as they focus on the campaigns at the end of the journey.')
main()
