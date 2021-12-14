#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Divvy_Exercise_Full_Year_Analysis ###

# This analysis is based on the Divvy case study "'Sophisticated, Clear, and Polished’: Divvy and Data 
# Visualization" written by Kevin Hartman (found here: https://artscience.blog/home/divvy-dataviz-case-study).
# The purpose of this script is to do data analysis of one year data from Divvy, with the purpose of answering 
# the key question: “In what ways do members and casual riders use Divvy bikes differently?”


# In[2]:


# # # # # # # # # # # # # # # # # # # # # # # 
# Install required packages
# pandas for dataframes
# numpy for 
# matplotlib.pyplot, Subplot, labelLine, labelLines for making graphs
# Counter
# datetime
# # # # # # # # # # # # # # # # # # # # # # #  

import pandas as pd
import numpy as np
import datetime 
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import Subplot
from collections import Counter
from labellines import labelLine, labelLines
import time


# In[3]:


time.ctime()


# In[4]:


##===================
#STEP 2: COLLECT DATA
##===================
sep20 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\09_2020.csv")
oct20 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\10_2020.csv")
nov20 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\11_2020.csv")
dec20 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\12_2020.csv")
jan21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\01_2021.csv")
feb21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\02_2021.csv")
mar21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\03_2021.csv")
apr21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\04_2021.csv")
may21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\05_2021.csv")
jun21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\06_2021.csv")
jul21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\07_2021.csv") 
aug21 = pd.read_csv(r"C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Data\Edited\08_2021.csv")



#stack all months to one data frame
# Made sure that all months have the same colunm name before combining them
all_months_data = [jan21, feb21, mar21, apr21, may21, jun21, jul21, aug21, sep20, oct20, nov20, dec20]
sep20_to_aug21 = pd.concat(all_months_data,ignore_index=True)


# In[5]:


#======================================================
# STEP 3: CLEAN UP AND ADD DATA TO PREPARE FOR ANALYSIS
#======================================================

#
# Inspecting our df
#
sep20_to_aug21.head() # Top 10 lines of the df
len(sep20_to_aug21)   # No of rows
sep20_to_aug21.shape  # Dimensions of df
list(sep20_to_aug21)  # Columns of the df
sep20_to_aug21.dtypes # Datatype of each column
for i in range (sep20_to_aug21.shape[1]):
    print (sep20_to_aug21.columns[i], 'is' ,type(sep20_to_aug21.iloc[:,i][14])) #returns the type of object in each column
                                               #type of the 14th line for each column
sep20_to_aug21.isnull().sum() # shows how many null values are in each colunm
sep20_to_aug21.nunique() # shows no of unique values for each column


# In[6]:


#----------------------------
#
#Identifying possible errors:
# 
#----------------------------

#
#ride_id should be unique, is it?
#

non_unique = len(sep20_to_aug21.ride_id) - len(set(sep20_to_aug21.ride_id)) # returns 0 if unique, or the no of non_unique entries if any
#there are (209) non_unique values

Uniq_ride_IDs = Counter(sep20_to_aug21.ride_id) #how many entries for each ride_id
duplicated_ride_ids =  [key for key in Uniq_ride_IDs.keys() if Uniq_ride_IDs[key]>1] #ride_ids that have more than 1 copies

#checking some random duplicated ride_ids:
#sep20_to_aug21.loc[sep20_to_aug21.ride_id==duplicated_ride_ids[201]]

#More problems identified:
# starting date after ending
# station_id's are different for the same station


# In[7]:


#
#Starting date should be before ending date
#

len(sep20_to_aug21.loc[(sep20_to_aug21.started_at >= sep20_to_aug21.ended_at)]) # returns how many have starting date the same or after the ending date
#returns 5846 entries

#
#station names check
#

#comparing the unique station names for start and end
len(set(sep20_to_aug21.start_station_name)) #=758
len(set(sep20_to_aug21.end_station_name)) #=757
#-> one station more for start_station_name. Why?

#Error investigation

#What station?
sorted_a = sep20_to_aug21.sort_values(by=["start_station_name"],ascending=True)
sorted_b = sep20_to_aug21.sort_values(by=["end_station_name"],ascending=True)
start_names = set(sorted_a.start_station_name)
end_names = set(sorted_b.end_station_name)

#comparing start_names and end_names:
start_names
end_names

#comparing start_names and end_names, start_station_name 351 is the extra one.

#What is wrong with this station?
sep20_to_aug21.loc[(sep20_to_aug21.start_station_name == '351')] 
#Error identified: 351 should be the station_id and the station name should be 'Mulligan Ave & Wellington Ave '
#for entries with index 2876561 and 3402481

#finding when the first rides of the station happen:
sep20_to_aug21.started_at.loc[(sep20_to_aug21.start_station_name == 'Mulligan Ave & Wellington Ave')].min()

# Error findings:
#Possibly error happened in the first days of operation of the station. Instead of station name, 
#station ID was recorded.


#Checking for similar errors for other station names
#Are there any more stations that station name is the same as station id?
sep20_to_aug21.loc[(sep20_to_aug21.start_station_name == sep20_to_aug21.start_station_id)]
sep20_to_aug21.loc[(sep20_to_aug21.end_station_name == sep20_to_aug21.end_station_id)]

#New issue with data identified: station names that were used from cyclistic staff for bike maintenance.
#Should be removed from data




#-------------
#
#Data cleaning 
#
#-------------

#Correcting the start_station_name for the error identified:
sep20_to_aug21.start_station_name[2876561]='Mulligan Ave & Wellington Ave'
sep20_to_aug21.start_station_name[3402481]='Mulligan Ave & Wellington Ave'

#Keeping the rides that starting date is before ending date:
cleaned = sep20_to_aug21.loc[sep20_to_aug21.started_at < sep20_to_aug21.ended_at]

#verifying that there are no more ride_id duplicates:
len(cleaned.ride_id) - len(set(cleaned.ride_id)) #returned 0. => no duplicates


#filtering out bikes that went for repair:
cleaned = cleaned.loc[(cleaned.start_station_name != "Base - 2132 W Hubbard Warehouse")&
                        (cleaned.end_station_name != "Base - 2132 W Hubbard Warehouse")&
                        (cleaned.start_station_id != "Hubbard Bike-checking (LBS-WH-TEST)")&
                        (cleaned.end_station_id != "Hubbard Bike-checking (LBS-WH-TEST)")&
                        (cleaned.start_station_name != "HUBBARD ST BIKE CHECKING (LBS-WH-TEST)")&
                        (cleaned.end_station_name != "HUBBARD ST BIKE CHECKING (LBS-WH-TEST)")&
                        (cleaned.end_station_name != "WATSON TESTING - DIVVY")&
                        (cleaned.start_station_name != "WATSON TESTING - DIVVY")&
                        (cleaned.end_station_name != "DIVVY CASSETTE REPAIR MOBILE STATION")&
                        (cleaned.start_station_name != "DIVVY CASSETTE REPAIR MOBILE STATION")&
                        (cleaned.start_station_id != "DIVVY 001")]                        


# In[8]:


#-------------------------------------------
#Adding columns for easier data manipulation
#-------------------------------------------

#Adding columns for
# - the trip duration 
# - the start and end time
# - the day of the week
# - just the date dd/mm/yyy
# - just the month/day
# - Just the month
# - Seasons
# - weekday/weekend

#Defining days, months and seasons for future use
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
seasons =["Winter","Spring","Summer","Fall"]

#finding duration in minutes and adding it to a new column:
cleaned['trip_duration_min'] = (pd.to_datetime(cleaned.ended_at.values)-pd.to_datetime(cleaned.started_at.values)).total_seconds() / 60

#keeping rides that lasted less than two days:
cleaned = cleaned.loc[(cleaned.trip_duration_min < (2*24*60))]#&(cleaned1.trip_duration_min < (48*60))]

#keeping rides that lasted more than a min:
cleaned = cleaned.loc[(cleaned.trip_duration_min > 1)]#&(cleaned1.trip_duration_min < (48*60))]

#finding the hour of day that each trip starts:
cleaned['start_hour_of_day'] = pd.to_datetime(cleaned.started_at).dt.hour + pd.to_datetime(cleaned.started_at).dt.minute/60 #+ pd.to_datetime(cleaned1.started_at).dt.seconds/(60*60)

#finding the hour of the day that each trip ends:
cleaned['end_hour_of_day'] = pd.to_datetime(cleaned.ended_at).dt.hour + pd.to_datetime(cleaned.ended_at).dt.minute/60 #+ pd.to_datetime(cleaned1.ended_at).dt.second/(60*60)

#finding the day of the week that each trip starts
cleaned['day_of_week'] = pd.to_datetime(cleaned.started_at).dt.dayofweek #monday = 0, sunday = 6 ,  numeric for calculations:

cleaned['day_name'] = pd.to_datetime(cleaned.started_at).dt.day_name() #name of day


#adding a colunm that defines if it is weekday or weekend:
conditions_week = [
    (cleaned['day_of_week'] <= 4),
    (cleaned['day_of_week'] >= 5)
    ]  #to be used for weekday/weekends
cleaned['weekday_weekend'] = np.select(conditions_week, ['weekday','weekend'])

#adding a column with the month:
cleaned['date'] =  pd.to_datetime(cleaned.started_at).dt.date 

#adding a column with the month:
cleaned['month'] =  pd.to_datetime(cleaned.started_at).dt.month

#adding a column for each season
conditions = [
    (cleaned['month'] <= 2) | (cleaned['month'] == 12),
    (cleaned['month'] >= 3) & (cleaned['month'] <= 5),
    (cleaned['month'] >= 6) & (cleaned['month'] <= 8),
    (cleaned['month'] >= 9) & (cleaned['month'] <= 11)
    ]  #to be used with seasons
cleaned['season'] = np.select(conditions, seasons)

cleaned.reset_index(inplace = True, drop = True)


# In[9]:


# Renaming final cleaned dataframe:
yearly = cleaned

#saving it to a csv to be used 
yearly.to_csv(r'C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Exported_Tables\yearly.csv',index = False)

# creating other dataframes that will be usefull
yearly_casual = yearly.loc[yearly.member_casual == "casual"]
yearly_member = yearly.loc[yearly.member_casual == "member"]


# In[10]:


# Breaking the dataframe to Months and Seasons

jan_ = yearly.loc[(yearly["started_at"] >= "2021-01-01") & (yearly["started_at"] < "2021-02-01")]
feb_ = yearly.loc[(yearly["started_at"] >= "2021-02-01") & (yearly["started_at"] < "2021-03-01")]
mar_ = yearly.loc[(yearly["started_at"] >= "2021-03-01") & (yearly["started_at"] < "2021-04-01")]
apr_ = yearly.loc[(yearly["started_at"] >= "2021-04-01") & (yearly["started_at"] < "2021-05-01")]
may_ = yearly.loc[(yearly["started_at"] >= "2021-05-01") & (yearly["started_at"] < "2021-06-01")]
jun_ = yearly.loc[(yearly["started_at"] >= "2021-06-01") & (yearly["started_at"] < "2021-07-01")]
jul_ = yearly.loc[(yearly["started_at"] >= "2021-07-01") & (yearly["started_at"] < "2021-08-01")]
aug_ = yearly.loc[(yearly["started_at"] >= "2021-08-01") & (yearly["started_at"] < "2021-09-01")]
sep_ = yearly.loc[(yearly["started_at"] >= "2020-09-01") & (yearly["started_at"] < "2020-10-01")]
oct_ = yearly.loc[(yearly["started_at"] >= "2020-10-01") & (yearly["started_at"] < "2020-11-01")]
nov_ = yearly.loc[(yearly["started_at"] >= "2020-11-01") & (yearly["started_at"] < "2020-12-01")]
dec_ = yearly.loc[(yearly["started_at"] >= "2020-12-01") & (yearly["started_at"] <= "2020-12-31")]

winter_ = pd.concat([dec_,jan_,feb_],ignore_index=True)
spring_ = pd.concat([mar_,apr_,may_],ignore_index=True)
summer_ = pd.concat([jun_,jul_,aug_],ignore_index=True)
fall_ = pd.concat([sep_,oct_,nov_],ignore_index=True)

winter_m = winter_.loc[winter_.member_casual == 'member']
spring_m = spring_.loc[spring_.member_casual == 'member']
summer_m = summer_.loc[summer_.member_casual == 'member']
fall_m = fall_.loc[fall_.member_casual == 'member']

winter_c = winter_.loc[winter_.member_casual == 'casual']
spring_c = spring_.loc[spring_.member_casual == 'casual']
summer_c = summer_.loc[summer_.member_casual == 'casual']
fall_c = fall_.loc[fall_.member_casual == 'casual']


# In[11]:


#---------------------
#Descriptive analysis:
#---------------------



#
#Mean duration:
#

mean_trip_dur = yearly.trip_duration_min.mean()
mean_trip_dur_mem = yearly_member.trip_duration_min.mean()
mean_trip_dur_cas = yearly_casual.trip_duration_min.mean()
#min and max values are set by the filters I used to include rides that their duration was between 1min and two days
print ("The mean trip duration for cyclistic bike riders is:",'{0:.1f}'.format(mean_trip_dur), 'min')
print ('For members:','{0:.1f}'.format(mean_trip_dur_mem),'min')
print ('For casuals:','{0:.1f}'.format(mean_trip_dur_cas),'min')


# In[12]:


#
#Preferred day
#

pref_day = yearly.day_name.mode()[0]
pref_day_mem = yearly_member.day_name.mode()[0]
pref_day_cas = yearly_casual.day_name.mode()[0]

print ("The preferred day for cyclistic bike riders is:",pref_day )
print ('For members:',pref_day_mem)
print ('For casuals:',pref_day_cas)


# In[13]:


#Defining a count function:
def count(df,value):
    return len(df.loc[(df==value)])

# More than a day:
trips_more_than_a_day = yearly.loc[(yearly.trip_duration_min > (1*24*60))]#&(cleaned1.trip_duration_min < (48*60))]
more_than_a_day = len(trips_more_than_a_day) #no of rides that lasted more than a day
print ("No of rides that lasted more than a day:",more_than_a_day,'{0:.2f}'.format(more_than_a_day/len(yearly)*100),"% of total")
print (count(trips_more_than_a_day.member_casual,"casual")," where casual riders (",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"casual")/more_than_a_day*100) ,"%, and",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"casual")/len(yearly_casual)*100),"%of total casual riders)")
print (count(trips_more_than_a_day.member_casual,"member")," where members (",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"member")/more_than_a_day*100) ,"%, and",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"member")/len(yearly_member)*100),"%of total members)")


# In[14]:


#defining functions to be used for our analysis:


#Defining one function to identify members and casual riders.
#this filter will return two new df's, for members and for casual riders
def filter_users(df): 
    df_member = df.loc[(df.member_casual=="member")] 
    df_casual = df.loc[(df.member_casual=="casual")]
    return df_member, df_casual

def no_of_users(df): 
    '''
    Takes a df as an argument. The df should include all users
    Returns the numbers of members, casual_riders and total riders
    '''
    member_no = len(df.loc[(df.member_casual=="member")]) 
    casual_no = len(df.loc[(df.member_casual=="casual")]) 
    total_no = len(df)
    return member_no, casual_no, total_no


def percent_of_users (df): 
    '''
    takes the result of no_of_users and calculates the percentages
    the argument dataframe should include all users
    returns a dataframe that includes:
    total no of rides, no of members, % of members, no fo casuals, # of casuals
    '''
    member_no, casual_no, total_no = no_of_users(df)
    members_percent = member_no/total_no*100
    casual_percent = casual_no/total_no*100
    data = total_no,member_no, members_percent, casual_no, casual_percent
    return pd.DataFrame([data], columns = ['total_rides', 'by_members','by_members_tprc','by_casual','by_casual_tprc'], index = ["test"])


def trip_duration(df):
    '''
    This function identifies the average trip duration for members and for casual riders. 
    Takes a dataframe that should include both members and casuals, and will also include a column  namned trip_duration_min.
    Returns a df with mean duration for members and mean duration of casuals, of the input df.
    '''
    df_members, df_casual = filter_users(df)
    members_av_trip_dur = df_members.trip_duration_min.mean()
    casual_av_trip_dur = df_casual.trip_duration_min.mean()
    data = members_av_trip_dur, casual_av_trip_dur
    return pd.DataFrame([data], columns = ["members_mean_duration", "casual_mean_duration"])

def mod_day(df):
    '''
    Takes for an input a df.
    Returns the most popular day for members and for casual riders, and calculates the percent of rides for each group, done in that day.
    '''
    df_members, df_casual = filter_users(df)
    members_day = int(df_members.day_of_week.mode())
    casual_day = int(df_casual.day_of_week.mode())
    members_no_for_day = len(df_members.loc[df_members.day_of_week == members_day])
    casual_no_for_day = len(df_casual.loc[df_casual.day_of_week == casual_day])
    members_percent = members_no_for_day/len(df_members)*100 
    casual_percent = casual_no_for_day/len(df_casual)*100
    data = members_day, members_percent, casual_day, casual_percent
    return pd.DataFrame([data], columns = ["members_day_mod",'member_Percent',"casual_day_mod","casual_Percent"])



                            
    
def apply_fn_to_seasons (fn):
    '''
    This function applies a function to each season. The result is a dataframe that includes
    the results of the function, each row for each season. 
    Winter, Spring, Summer, Fall
    Takes a function for input
    '''
    df = fn(winter_)
    df = df.append(fn(spring_))
    df = df.append(fn(summer_))
    df = df.append(fn(fall_)) 
    df.index = seasons
    return df


def apply_fn_to_months (fn):

    '''
    This function applies a function to each month. The result is a dataframe that includes
    the results of the function, each row for each month. 
    Winter, Spring, Summer, Fall
    Takes a function as input
    '''
    df = fn(jan_)
    df = df.append(fn(feb_))
    df = df.append(fn(mar_))
    df = df.append(fn(apr_))
    df = df.append(fn(may_))
    df = df.append(fn(jun_))
    df = df.append(fn(jul_))
    df = df.append(fn(aug_))
    df = df.append(fn(sep_))
    df = df.append(fn(oct_))
    df = df.append(fn(nov_))
    df = df.append(fn(dec_))
    df.index = months
    return df


def total_rides_per_day_of_week(df): #creates a df of no of rides for all days, for specific df
    '''
    Returns for each day of the week the no of rides for members and for casual users in a dataframe.
    Takes a df for input
    '''
    df_members =  df.loc[(df.member_casual=="member")]
    members_no = len(df_members)
    df_casual = df.loc[(df.member_casual=="casual")]
    casual_no = len(df_casual)
    #filtering per day:
    daily_rides = pd.DataFrame()
    data = []
    for i in range (7):
        #filtering per day:
        members_ride_no = len(df_members.ride_id.loc[df_members.day_of_week == i])
        members_ride_prc = len(df_members.ride_id.loc[df_members.day_of_week == i])/members_no*100
        data.append(members_ride_prc)
        casual_ride_no = len(df_casual.ride_id.loc[df_casual.day_of_week == i])
        casual_ride_prc = len(df_casual.ride_id.loc[df_casual.day_of_week == i])/casual_no*100
        data.append(casual_ride_prc)
    return pd.DataFrame([data], columns = ["Mon_mem","Mon_cas","Tues_mem","Tues_cas", "Wed_mem","Wed_cas","Thur_mem","Thur_cas","Frid_mem","Frid_cas","Sat_mem","Sat_cas","Sun_mem","Sun_cas"])

def rides_per_day_of_week(df): #creates a df of rides for all days, for total/members/casual for the specific df
    '''
    Returns for each day of the week the no of rides for users in a dataframe, filtered according to users. users can be member or casual
    Takes a df for input
    '''
    total_no = len(df)
    #filtering per day:
    #days =["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    daily_rides = pd.DataFrame()
    data = []
    for i in range (7):
        #filtering per day:
        #total = len(df.ride_id.loc[df.day_of_week == i])
        rides_no = len(df.ride_id.loc[df.day_of_week == i])
        rides_prc = len(df.ride_id.loc[df.day_of_week == i])/total_no*100
        #data.append(members_ride_no)
        data.append(rides_no)
    return pd.DataFrame([data], columns = ["Mon","Tues","Wed","Thur","Frid","Sat","Sun"])
                                           

def join_two_dfs(df1,df2):
    '''
    Adds the columns of the second df (df2) to the first df (df1), and returns them in a new df (df3). 
    df1 and df2 should have the same rows.
    Takes two dfs for input
    '''
    df1['tmp'] = np.arange(df1.shape[0])
    df2['tmp'] = np.arange(df2.shape[0])
    df3 = pd.merge(df1, df2, on=['tmp'])
    del df1['tmp']
    del df2['tmp']
    del df3['tmp']
    return df3

def apply_fn_to_months_df (fn,df):
    '''
    Takes a fn and a df for input.
    Filters the df to months, and applies the fn to each month
    Returns a df with the results of the function for each month
    '''
    _jan = df.loc[(df["started_at"] >= "2021-01-01") & (df["started_at"] < "2021-02-01")]
    _feb = df.loc[(df["started_at"] >= "2021-02-01") & (df["started_at"] < "2021-03-01")]
    _mar = df.loc[(df["started_at"] >= "2021-03-01") & (df["started_at"] < "2021-04-01")]
    _apr = df.loc[(df["started_at"] >= "2021-04-01") & (df["started_at"] < "2021-05-01")]
    _may = df.loc[(df["started_at"] >= "2021-05-01") & (df["started_at"] < "2021-06-01")]
    _jun = df.loc[(df["started_at"] >= "2021-06-01") & (df["started_at"] < "2021-07-01")]
    _jul = df.loc[(df["started_at"] >= "2021-07-01") & (df["started_at"] < "2021-08-01")]
    _aug = df.loc[(df["started_at"] >= "2021-08-01") & (df["started_at"] < "2021-09-01")]
    _sep = df.loc[(df["started_at"] >= "2020-09-01") & (df["started_at"] < "2020-10-01")]
    _oct = df.loc[(df["started_at"] >= "2020-10-01") & (df["started_at"] < "2020-11-01")]
    _nov = df.loc[(df["started_at"] >= "2020-11-01") & (df["started_at"] < "2020-12-01")]
    _dec = df.loc[(df["started_at"] >= "2020-12-01") & (df["started_at"] <= "2020-12-31")]
    df1 = fn(_jan)
    df1 = df1.append(fn(_feb))
    df1 = df1.append(fn(_mar))
    df1 = df1.append(fn(_apr))
    df1 = df1.append(fn(_may))
    df1 = df1.append(fn(_jun))
    df1 = df1.append(fn(_jul))
    df1 = df1.append(fn(_aug))
    df1 = df1.append(fn(_sep))
    df1 = df1.append(fn(_oct))
    df1 = df1.append(fn(_nov))
    df1 = df1.append(fn(_dec))
    df1.index = months
    return df1


# In[16]:


#---------------------------------
#Most popular day for each season:
#---------------------------------

#Calculating the most popular day, and the percent of rides on this day for casuals and for members for every season
mod_day_seasons = mod_day(yearly.loc[yearly.season == 'Winter'])
mod_day_seasons['Season'] = 'Winter'
for season in seasons[1:]:
    test1 = mod_day(yearly.loc[yearly.season == season])
    test1['Season'] = season
    mod_day_seasons = mod_day_seasons.append(test1)
mod_day_seasons


# In[17]:


#--------------------------------
#Most popular day for each month:
#--------------------------------

#Calculating the most popular day, and the percent of rides on this day for casuals and for members for every month
mod_day_months = mod_day(yearly.loc[yearly.month == 1])
mod_day_months['Month'] = months[0]
for i in range (11):
    test1 = mod_day(yearly.loc[yearly.month == (i+2)])
    test1['Month'] = months[i+1]
    mod_day_months = mod_day_months.append(test1)
mod_day_months


# In[18]:


#
#Finding the no of rides for each day of the week, per month, for casuals and memebrs
#

members_weekly_monthly = apply_fn_to_months_df(rides_per_day_of_week,yearly_member)
casual_weekly_monthly = apply_fn_to_months_df(rides_per_day_of_week,yearly_casual)

#for members:
members_weekly_monthly.T

#for casuals:
casual_weekly_monthly.T


# In[19]:


#-----------------------------------------------
#Creating yearly/seasonly/monthly dataframes
#-----------------------------------------------


#They will have the following columns:
#'total_rides', 'by_members','by_members_prc','by_casual",'by_casual_prc'
#"members_mean_duration", "casual_mean_duration"
#"members_day_mod",'members_rides_on_day_mod_prc',"casual_day_mod","casual_rides_on_day_mod_prc"
#percent of rieds for every day of the week for members and for casuals:
#"Mon_mem","Mon_cas","Tues_mem","Tues_cas", "...

#
#Yearly:
#
test1 = percent_of_users(yearly)
#Adds: 'total_rides', 'by_members','by_members_prc','by_casual",'by_casual_prc'
test2 = trip_duration(yearly)
#Adds: "members_mean_duration", "casual_mean_duration"
test3 = mod_day(yearly)
#Ads: "members_day_mod",'members_rides_on_day_mod_prc',"casual_day_mod","casual_rides_on_day_mod_prc"
test4 = total_rides_per_day_of_week(yearly)
#Adds: "Mon_mem","Mon_cas","Tues_mem","Tues_cas", "Wed_mem","Wed_cas","Thur_mem","Thur_cas","Frid_mem","Frid_cas","Sat_mem","Sat_cas","Sun_mem","Sun_cas"
test5 = join_two_dfs(test1,test2)
test6 = join_two_dfs(test5,test3)
yearly_sum = join_two_dfs(test6,test4)

#
#Seasonly
#
test01 = apply_fn_to_seasons(percent_of_users)
test02 = apply_fn_to_seasons(trip_duration)
test03 = apply_fn_to_seasons(mod_day)
test04 = apply_fn_to_seasons(total_rides_per_day_of_week)
test05 = join_two_dfs(test01,test02)
test06 = join_two_dfs(test05,test03)
seasonal_sum = join_two_dfs(test06,test04)
#seasonal_sum.index = seasons
#seasonal_sum

#
#Monthly
#
test001 = apply_fn_to_months(percent_of_users)
test002 = apply_fn_to_months(trip_duration)
test003 = apply_fn_to_months(mod_day)
test004 = apply_fn_to_months(total_rides_per_day_of_week)
test005 = join_two_dfs(test001,test002)
test006 = join_two_dfs(test005,test003)
monthly_sum = join_two_dfs(test006,test004)
monthly_sum.index = months
monthly_sum


# In[20]:


#
#Defining colors for graphs
#

#colors chosen from coolors.co/ to be visible for most color blindness types
five_color = ['#E63946', '#7CA070','#A8DADC','#457B9D','#1D3557'] #red,green, light blue, blue, dark blue
two_color = ['#5975A4','#CC8963'] #blueish,orange
two_color_ = ['#2A9D87','#E9C46A'] 


# In[21]:


#
#Pie chart to visualize the quantity of casual and member rides.
#
total = yearly_sum.total_rides
yearly_pie=[int(yearly_sum.by_casual), int(yearly_sum.by_members)]
year_colors = two_color
explode_year = [0.01, 0.01]
plt.pie(yearly_pie,labels=("Casual","Members"),labeldistance=0.30, autopct='%1.0f%%',pctdistance=0.62,
        colors = year_colors,radius=1.2,startangle=0,explode = explode_year,
        textprops={'fontsize': 20, 'color':'w'})
fig = plt.gcf()
fig.set_size_inches(6,6)
plt.savefig("total_yearly.png",bbox_inches = 'tight')
plt.show()### 


# In[22]:


#
# Bar graph to compare how casual and member rides distribute for each season
#

fig, ((ax0)) = plt.subplots(nrows=1, ncols=1)

n_bins = 4

x1 = yearly_casual.season
x2 = yearly_member.season

ind = np.arange(n_bins) 
width = 0.35

#x3 = yearly.day_of_week
colors = two_color#,'lime']

n, bins, patches = ax0.hist((x1,x2), n_bins, density=False, histtype='bar',
                            color=colors, label=["Casual riders","Members"])

#plt.rcParams.update({'font.size': 19})
ax0.legend(prop={'size': 14})
ax0.set_title('Rides per Season',fontsize='16')

ax0.set_xticks([0.4,1.15,1.9,2.65])
ax0.set_xticklabels(seasons)
plt.xticks(fontsize=14)
plt.yticks(fontsize=12)
plt.grid(False)
ax0.minorticks_on()

ax0.grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid
ax0.grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid
ax0.xaxis.set_tick_params(which='minor', bottom=False)

#plt.xlabel('Seasons')
plt.ylabel('No of rides',fontsize='16')

#axs[0,0].set_axisbelow(True) #axes behind data
#ax0.grid(zorder=0)
#ax.bar(range(len(y)), y, width=0.3, align='center', color='skyblue', zorder=3)
#plt.rcParams.update({'font.size': 24})
fig.set_size_inches(6,5)
ax0.set_axisbelow(True)
plt.savefig("total_seasons.png",bbox_inches = 'tight')
fig.tight_layout()

plt.show()


# In[23]:


#
#Bar chart to compare how casual and member rides distribute through seasons compared to their total rides no
#

index = np.arange(0, 4, 2)
x = np.arange(2) + 1
y1 = np.array([len(winter_m)/len(yearly_member)*100,len(winter_c)/len(yearly_casual)*100])
y3 = np.array([len(summer_m)/len(yearly_member)*100,len(summer_c)/len(yearly_casual)*100])
y4 = np.array([len(fall_m)/len(yearly_member)*100,len(fall_c)/len(yearly_casual)*100])
y2 = np.array([len(spring_m)/len(yearly_member)*100,len(spring_c)/len(yearly_casual)*100])
ax = plt.subplot()
ax.set_xticks([1,1.1])
plt.rcParams.update({'font.size': 15})

p4 = ax.bar(x, y4, bottom=y3+y2+y1, label='Fall',width=0.3, color = five_color[3])
p3 = ax.bar(x, y3, bottom=y2+y1, label='Summer',width=0.3, color = two_color[1])
p2 = ax.bar(x, y2, bottom=y1, label='Spring',width=0.3, color = five_color[1])
p1 = ax.bar(x, y1, tick_label=['Members', 'Casual riders'], label='Winter',width=0.3,zorder=3, color = five_color[2])
ax.grid(zorder=4)
plt.xlabel('Riders',fontsize='17')
plt.ylabel('Percent (%)',fontsize='17')

ax.bar_label(p1, label_type='center',fmt='%.0f')
ax.bar_label(p2, label_type='center',fmt='%.0f')
ax.bar_label(p3, label_type='center',fmt='%.0f')
ax.bar_label(p4, label_type='center',fmt='%.0f')

ax.set_axisbelow(True)

plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.title('Seasonal percentage analysis',fontdict={'fontsize': 18},pad=-18)
plt.legend(prop={'size': 14},loc=10)
plt.savefig("seasons_percent.png")
plt.show()


# In[24]:


#
#Calculating percent of casual riders during summer
#
season1 = 'Summer'
casual_no_seasons = len(yearly_casual.loc[yearly_casual.season == season1])
season_no = len(yearly.loc[yearly.season == season1])

#Percent of casual riders for summer:
print (casual_no_seasons/season_no*100)


# In[25]:


#
#Dougnut chart showing Summer rides per member/casual) and weekday/weekend 
#

total = yearly_sum.total_rides
summer_pie=[len(yearly_casual.loc[yearly_casual.season == "Summer"]),
            len(yearly_member.loc[yearly_member.season == "Summer"])]

explode_summer =[0.02,0.02]
explode = [0.02,0.02,0.02,0.02]

weekday_pie = [len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekday")]),
               len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekend")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekday")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekend")])
              ]
summer_colors = two_color
weekday_colors = two_color_
#month_colors = ["darkcyan","darkturquoise","powderblue","lightsalmon","darkgreen","seagreen","Brown","Seashell","darkkhaki","khaki","peru","saddlebrown"]
#test01 = group02+group02
#monthly_pie = (monthly_sum.by_members.values.tolist() + monthly_sum.by_casual.values.tolist())
# Create a pieplot
#my_circle=plt.Circle( (0,0), 3, facecolor='white',edgecolor = "black")
#months_label=('Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov')
#plt.pie(monthly_pie,radius=1.5,labels=months_label,labeldistance=1.1, colors = month_colors,startangle=180)
#my_circle=plt.Circle( (0,0), 1.9, facecolor='white',edgecolor = "black")


plt.pie(weekday_pie,labels=("Weekdays","Weekend", "Weekdays","Weekend"),
        labeldistance=1.05,radius=1.5,autopct='%1.0f%%',pctdistance=0.85, 
        colors = weekday_colors ,startangle=0,explode = explode,
       textprops={'fontsize': 16})
plt.pie(summer_pie,labels=("Casual","Member"),labeldistance=0.53,autopct='%1.0f%%',pctdistance=0.8,
        colors = summer_colors,radius=1,startangle=0,explode = explode_summer,
        textprops={'fontsize': 16})
#plt.pie((test01))

# add a circle at the center to transform it in a donut chart
my_circle=plt.Circle((0,0), 0.45, facecolor='white')#,edgecolor = "black")

p=plt.gcf()
p.gca().add_artist(my_circle)
fig = plt.gcf()


# plt.text(-0.25, -0.15, "rides",fontdict = {'size':23} )
# plt.text(-0.35, 0.07, len(yearly.loc[(yearly.season == "Summer")]),fontdict = {'size':25} )


# fig.tight_layout()

fig.set_size_inches(6,6)
plt.savefig("summer_seasons_pie_v01.png",bbox_inches = 'tight')
plt.show()### 


# In[26]:


#
#doughnut pieces for weekdays
#

total = yearly_sum.total_rides
summer_pie=[len(yearly_casual.loc[yearly_casual.season == "Summer"]),
            len(yearly_member.loc[yearly_member.season == "Summer"])]

explode_summer =[0.02,0.02]
explode = [0.02,0.02,0.02,0.02]

weekday_pie = [len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekday")]),
               len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekend")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekday")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekend")])
              ]
# summer_colors = two_color
weekday_colors = [two_color[0],"#FFFFFF",two_color[1],"#FFFFFF"]


plt.pie(weekday_pie,
        labeldistance=1.05,radius=1,autopct='%1.0f%%',pctdistance=0.25, 
        colors = weekday_colors ,startangle=0,explode = explode,
       textprops={'fontsize': 16})

# add a circle at the center to transform it in a donut chart
my_circle=plt.Circle((0,0), 0.45, facecolor='white')#,edgecolor = "black")

p=plt.gcf()
p.gca().add_artist(my_circle)
fig = plt.gcf()



fig.set_size_inches(6,6)
plt.savefig("summer_seasons_pie_weekday.png",bbox_inches = 'tight')
plt.show()### 

#
#doughnut pieces for weekend
#


total = yearly_sum.total_rides
summer_pie=[len(yearly_casual.loc[yearly_casual.season == "Summer"]),
            len(yearly_member.loc[yearly_member.season == "Summer"])]

explode_summer =[0.02,0.02]
explode = [0.02,0.02,0.02,0.02]

weekday_pie = [len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekday")]),
               len(yearly_casual.loc[(yearly_casual.season == "Summer")&(yearly_casual.weekday_weekend == "weekend")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekday")]),
               len(yearly_member.loc[(yearly_member.season == "Summer")&(yearly_member.weekday_weekend == "weekend")])
              ]
weekday_colors = ["#FFFFFF",two_color[0],"#FFFFFF",two_color[1]]


plt.pie(weekday_pie,
        labeldistance=1.05,radius=1,autopct='%1.0f%%',pctdistance=0.25, 
        colors = weekday_colors ,startangle=0,explode = explode,
       textprops={'fontsize': 16})

# add a circle at the center to transform it in a donut chart
my_circle=plt.Circle((0,0), 0.45, facecolor='white')#,edgecolor = "black")

p=plt.gcf()
p.gca().add_artist(my_circle)
fig = plt.gcf()




# fig.tight_layout()

fig.set_size_inches(6,6)
plt.savefig("summer_seasons_pie_weekend.png",bbox_inches = 'tight')
plt.show()### 

#
# Comparing percentages for weekdays and weeekends:
#


mem_no = len (yearly_member)
cas_no = len (yearly_casual)


##Percentage calculation
member_no_weekdays_all = len(yearly_member.loc[yearly_member.weekday_weekend == 'weekday'])/mem_no*100 
member_no_weekend_all = len(yearly_member.loc[yearly_member.weekday_weekend == 'weekend'])/mem_no*100
casual_no_weekdays_all = len(yearly_casual.loc[yearly_casual.weekday_weekend == 'weekday'])/cas_no*100
casual_no_weekend_all = len(yearly_casual.loc[yearly_casual.weekday_weekend == 'weekend'])/cas_no*100


numbers_all = [member_no_weekdays_all,member_no_weekend_all,casual_no_weekdays_all,casual_no_weekend_all]

#percentages: 
for i in numbers_all:
    print (i)


# In[27]:


#Verifying percentages:
len(yearly_casual.loc[(yearly_casual.season == "Summer")&
                      (yearly_casual.weekday_weekend == "weekend")])/len(yearly.loc[(yearly.season == "Summer")])*100 
#20.72 ->Matches with graph


# In[28]:


#
#Top 10 starting bike stations:
#


#Starting stations
##Grouping per member/casual and weekday/weekend
##Choosing only the start_station_name
df = (yearly.loc[yearly.season == 'Summer']
.groupby(['member_casual','weekday_weekend'])['start_station_name']
.value_counts(normalize=False)
#.mul(100)
.rename('counts')
.reset_index())

#Ending stations
##Grouping per member/casual and weekday/weekend
##Choosing only the end_station_name
df1 = (yearly.loc[yearly.season == 'Summer']
.groupby(['member_casual','weekday_weekend'])['end_station_name']
.value_counts(normalize=False)
#.mul(100)
.rename('counts')
.reset_index())


#
#defining dfs to be visualized:
#

casual_start_station_weekday = df.loc[(df.member_casual == 'casual')&(df.weekday_weekend == 'weekday')][0:10].reset_index()
casual_start_station_weekend = df.loc[(df.member_casual == 'casual')&(df.weekday_weekend == 'weekend')][0:10].reset_index()
member_start_station_weekday = df.loc[(df.member_casual == 'member')&(df.weekday_weekend == 'weekday')][0:10].reset_index()
member_start_station_weekend = df.loc[(df.member_casual == 'member')&(df.weekday_weekend == 'weekend')][0:10].reset_index()

casual_end_station_weekday = df1.loc[(df1.member_casual == 'casual')&(df1.weekday_weekend == 'weekday')][0:10].reset_index()
casual_end_station_weekend = df1.loc[(df1.member_casual == 'casual')&(df1.weekday_weekend == 'weekend')][0:10].reset_index()
member_end_station_weekday = df1.loc[(df1.member_casual == 'member')&(df1.weekday_weekend == 'weekday')][0:10].reset_index()
member_end_station_weekend = df1.loc[(df1.member_casual == 'member')&(df1.weekday_weekend == 'weekend')][0:10].reset_index()

#start stations used by casuals:
test = casual_start_station_weekday
casual_start_station = test.append(casual_start_station_weekend,ignore_index=True)

#start stations used by members:
test = member_start_station_weekday
member_start_station = test.append(member_start_station_weekend,ignore_index=True)

#all top 10 start stations used by cyclistic riders:
test = casual_start_station
all_start_station = test.append(member_start_station,ignore_index=True)

#names of the top 10 start_stations:
casual_start_station_names = pd.DataFrame(np.unique(casual_start_station.start_station_name)) #identify all start station names for 
member_start_station_names = pd.DataFrame(np.unique(member_start_station.start_station_name))#identify all start station names for 
all_start_station_names = pd.DataFrame(np.unique(all_start_station.start_station_name))


test = casual_end_station_weekday
casual_end_station = test.append(casual_end_station_weekend,ignore_index=True)
test = member_end_station_weekday
member_end_station = test.append(casual_end_station_weekend,ignore_index=True)

test = casual_end_station
all_end_station = test.append(member_end_station,ignore_index=True)
casual_end_station_names = pd.DataFrame(np.unique(casual_end_station.end_station_name)) #identify all start station names for 
member_end_station_names = pd.DataFrame(np.unique(member_end_station.end_station_name))#identify all start station names for 
all_end_station_names = pd.DataFrame(np.unique(all_end_station.end_station_name))


# In[29]:


#
#finding the percent of casual and member rides that use these top 10 staring stations:
#

## For the weekdays:
print ('Top 10 start stations during the weekdays by members include',
       member_start_station_weekday['counts'].sum()/len(yearly_member.loc[(yearly_member.season == 'Summer')])*100,
       '% of all summer member rides' )
print ('Top 10 start stations during the weekdays by casual riders include',
       casual_start_station_weekday['counts'].sum()/len(yearly_casual.loc[(yearly_casual.season == 'Summer')])*100,
       '% of all summer casual rides')
##]

## For the weekends:[
print ('Top 10 start stations during the weekend by members include',
       member_start_station_weekend['counts'].sum()/len(yearly_member.loc[(yearly_member.season == 'Summer')])*100,
       '% of all summer member rides' )
print ('Top 10 start stations during the weekend by casual riders include',
       casual_start_station_weekend['counts'].sum()/len(yearly_casual.loc[(yearly_casual.season == 'Summer')])*100,
       '% of all summer casual rides')
##]

#finding the percent of casual and member ride  between these top 10 ending stations:

## For the weekdays:[
print ('Top 10 end stations during the weekdays by members include',
       member_end_station_weekday['counts'].sum()/len(yearly_member.loc[(yearly_member.season == 'Summer')])*100,
       '% of all summer member rides' )
print ('Top 10 end stations during the weekdays by casual riders include',
       casual_end_station_weekday['counts'].sum()/len(yearly_casual.loc[(yearly_casual.season == 'Summer')])*100,
       '% of all summer casual rides')
##]

## For the weekend:[
print ('Top 10 end stations during the weekend by members include',
       member_end_station_weekend['counts'].sum()/len(yearly_member.loc[yearly_member.season == 'Summer'])*100,
       '% of all summer member rides' )
print ('Top 10 end stations during the weekend by casual riders include',
       casual_end_station_weekend['counts'].sum()/len(yearly_casual.loc[yearly_casual.season == 'Summer'])*100,
       '% of all summer casual rides')
##]


# In[30]:


#
#Identifying common stations between members and casuals (between top 10 stations):
#

# For start stations
##For Weekdays:
print('Common starting stations during weekdays are:')
print(pd.merge(casual_start_station_weekday, 
               member_start_station_weekday,
               on=['start_station_name','start_station_name'])
     .start_station_name)

##For Weekends:
print('Common starting stations during weekends are:')
print(pd.merge(casual_start_station_weekend,
               member_start_station_weekend,
               on=['start_station_name','start_station_name'])
     .start_station_name)
print ('')

# For end stations
##for weekdays:
print ('The common stations between the top 10 ending stations during weekdays are:' )
print(pd.merge(casual_end_station_weekday, 
               member_end_station_weekday,
               on=['end_station_name','end_station_name'])
     .end_station_name)

##for weekends:
print ('The common ending stations during the weekdend are:' )
print(pd.merge(casual_end_station_weekend,
               member_end_station_weekend,
               on=['end_station_name','end_station_name'])
     .end_station_name)


# In[31]:


#Identifying common stations:


#preparing dfs to join (renaming column with station name):

##for weekdays (wkd)
cas_start_wkd_common = pd.DataFrame(casual_start_station_weekday.start_station_name).rename(columns={'start_station_name':'common'}, inplace=False)
cas_end_wkd_common = pd.DataFrame(casual_end_station_weekday.end_station_name).rename(columns={'end_station_name':'common'}, inplace=False)
mem_start_wkd_common = pd.DataFrame(member_start_station_weekday.start_station_name).rename(columns={'start_station_name':'common'}, inplace=False)
mem_end_wkd_common = pd.DataFrame(member_end_station_weekday.end_station_name).rename(columns={'end_station_name':'common'}, inplace=False)

##for weekends (wknd)
cas_start_wknd_common = pd.DataFrame(casual_start_station_weekend.start_station_name).rename(columns={'start_station_name':'common'}, inplace=False)
cas_end_wknd_common = pd.DataFrame(casual_end_station_weekend.end_station_name).rename(columns={'end_station_name':'common'}, inplace=False)
mem_start_wknd_common = pd.DataFrame(member_start_station_weekend.start_station_name).rename(columns={'start_station_name':'common'}, inplace=False)
mem_end_wknd_common = pd.DataFrame(member_end_station_weekend.end_station_name).rename(columns={'end_station_name':'common'}, inplace=False)


## preparing lists to use in loops
cas_wknd = [cas_start_wknd_common,cas_end_wknd_common]
mem_wknd = [mem_start_wknd_common,mem_end_wknd_common]
cas_wkd = [cas_start_wkd_common,cas_end_wkd_common]
mem_wkd = [mem_start_wkd_common,mem_end_wkd_common]


cas_mem_top_stations = [[cas_wkd,cas_wknd],[mem_wkd,mem_wknd]]
rider_type = ['casuals','members']
week_period = ['weekday','weekend']
start_end = ['start','end']


# Structure:
# cas_mem_top_stations[i][k][l]
# cas_mem_top_stations[casual/member][weekday/weekend][start/end]


for i in range (2):
    for k in range (2):
        print ('Common start and end stations during the',week_period[i], 'for', rider_type[k],
              'are:', pd.merge(cas_mem_top_stations[i][k][0],cas_mem_top_stations[i][k][1],on='common'))

for i in range (2): #for start/end
    for k in range (2): #for week_period
        print ('Common',start_end[i], 'stations between members and casuals during the',week_period[k],
              'are:', pd.merge(cas_mem_top_stations[0][k][i],cas_mem_top_stations[1][k][i],on='common'))


# In[32]:


#
#Bar charts showing the top 10 stations (starting and ending) for the weekdays 
#

fig, (axs) = plt.subplots(nrows=2, ncols=2)

colors = two_color#,'lime']

x1 = casual_start_station_weekday
x2 = member_start_station_weekday
x3 = casual_end_station_weekday
x4 = member_end_station_weekday

g1 = axs[0,0].barh(x1.start_station_name, x1.counts, color = colors[0])
g2 = axs[1,0].barh(x2.start_station_name, x2.counts, color = colors[1])
g3 = axs[0,1].barh(x3.end_station_name, x3.counts, color = colors[0])
g4 = axs[1,1].barh(x4.end_station_name, x4.counts, color = colors[1])

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.setp(axs, xlim=axs[0,0].get_xlim()) #manualy select the maximum

# axs[0].invert_yaxis()
axs[0,1].invert_xaxis()
axs[1,1].invert_xaxis()

axs[1,0].invert_yaxis()
axs[1,1].invert_yaxis()

axs[0,0].grid(which='major', axis='x', linestyle='-', linewidth='1') 
axs[1,0].grid(which='major', axis='x', linestyle='-', linewidth='1')
axs[0,1].grid(which='major', axis='x', linestyle='-', linewidth='1') 
axs[1,1].grid(which='major', axis='x', linestyle='-', linewidth='1')

axs[0,0].minorticks_on()
axs[1,0].minorticks_on()
axs[0,1].minorticks_on()
axs[1,1].minorticks_on()

axs[0,0].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5')#, color='black') # Customize the minor grid

# -------------
#axs[1,0].set_xlabel('Rides')
#axs[1,0].set_xlabel('Rides',fontsize='20')


axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()


axs[0,0].tick_params(labeltop=True)
axs[0,0].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[0,0].tick_params(axis='x', labelsize=16)
axs[1,0].tick_params(axis='x', labelsize=16)

axs[0,1].tick_params(labeltop=True)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='x', labelsize=16)
axs[1,1].tick_params(axis='x', labelsize=16)

axs[0,0].text(10000, 9.1, "Casual",fontdict = {'size':23} )
axs[1,0].text(10000, 0.1, "Member",fontdict = {'size':23} )

axs[0,1].yaxis.tick_right()
axs[1,1].yaxis.tick_right()

axs[0,1].set_axisbelow(True)
axs[1,1].set_axisbelow(True)
axs[0,0].set_axisbelow(True)
axs[1,0].set_axisbelow(True)

axs[1,0].set_title('Start stations',fontsize=23,pad=15)
axs[1,1].set_title('End stations',fontsize=23,pad=15)

fig.set_size_inches(17,12)
fig.tight_layout()
plt.savefig("top_10_stations_weekday.png",bbox_inches = 'tight')
plt.show()


# In[33]:


#
#Bar charts showing the top 10 stations (starting and ending) for the weekend
#

fig, (axs) = plt.subplots(nrows=2, ncols=2)

colors = two_color

x1 = casual_start_station_weekend
x2 = member_start_station_weekend
x3 = casual_end_station_weekend
x4 = member_end_station_weekend

g1 = axs[0,0].barh(x1.start_station_name, x1.counts, color = colors[0])
g2 = axs[1,0].barh(x2.start_station_name, x2.counts, color = colors[1])
g3 = axs[0,1].barh(x3.end_station_name, x3.counts, color = colors[0])
g4 = axs[1,1].barh(x4.end_station_name, x4.counts, color = colors[1])

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.setp(axs, xlim=axs[0,0].get_xlim()) #manualy select the maximum

# axs[0].invert_yaxis()
axs[0,1].invert_xaxis()
axs[1,1].invert_xaxis()

axs[1,0].invert_yaxis()
axs[1,1].invert_yaxis()

axs[0,0].grid(which='major', axis='x', linestyle='-', linewidth='1') 
axs[1,0].grid(which='major', axis='x', linestyle='-', linewidth='1')
axs[0,1].grid(which='major', axis='x', linestyle='-', linewidth='1') 
axs[1,1].grid(which='major', axis='x', linestyle='-', linewidth='1')

axs[0,0].minorticks_on()
axs[1,0].minorticks_on()
axs[0,1].minorticks_on()
axs[1,1].minorticks_on()

axs[0,0].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle='-.', linewidth='0.5')#, color='black') # Customize the minor grid

# -------------
#axs[1,0].set_xlabel('Rides')
#axs[1,0].set_xlabel('Rides',fontsize='20')


axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()


axs[0,0].tick_params(labeltop=True)
axs[0,0].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[0,0].tick_params(axis='x', labelsize=16)
axs[1,0].tick_params(axis='x', labelsize=16)

axs[0,1].tick_params(labeltop=True)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='x', labelsize=16)
axs[1,1].tick_params(axis='x', labelsize=16)

axs[0,0].text(10000, 9.1, "Casual",fontdict = {'size':23} )
axs[1,0].text(10000, 0.1, "Member",fontdict = {'size':23} )

axs[1,0].set_title('Start stations',fontsize=23,pad=15)
axs[1,1].set_title('End stations',fontsize=23,pad=15)

axs[0,1].set_axisbelow(True)
axs[1,1].set_axisbelow(True)
axs[0,0].set_axisbelow(True)
axs[1,0].set_axisbelow(True)

axs[0,1].yaxis.tick_right()
axs[1,1].yaxis.tick_right()

fig.set_size_inches(18,12)
fig.tight_layout()
plt.savefig("top_10_stations_weekend.png",bbox_inches = 'tight')
plt.show()


# In[34]:


#-------------------
#Round Trip Analysis
#-------------------

#defining the round trips:
## Based on the same station name:
round_trips_station_name = yearly.loc[(yearly.start_station_name == yearly.end_station_name)]
## Based on coordinates:
round_trips_coordinates = yearly.loc[(yearly.start_lat == yearly.end_lat)&
                                     (yearly.start_lng == yearly.end_lng)]

#comparing the round trips based on coordinates and based on station names:
len(round_trips_station_name) - len(round_trips_coordinates)  #they are not equal.
#based on station names we have more round trips. We chose to move forward with the 
#station name definition for round trips.

round_trips_prc = len(round_trips_station_name)/len(yearly)*100
round_trips_member_prc = len(round_trips_station_name.loc[(round_trips_station_name.member_casual == 'member')] )/len(yearly_member)*100
round_trips_casual_prc = len(round_trips_station_name.loc[(round_trips_station_name.member_casual == 'casual')] )/len(yearly_casual)*100

round_trips_member_prc_of_total = len(round_trips_station_name.loc[(round_trips_station_name.member_casual == 'member')] )/len(yearly)*100
round_trips_casual_prc_of_total = len(round_trips_station_name.loc[(round_trips_station_name.member_casual == 'casual')] )/len(yearly)*100

print ("For all the year, round trip percent for:")
print ("All riders is:",round_trips_prc,'%')
print ("Members is:",round_trips_member_prc,'%')
print ("Casuals is:",round_trips_casual_prc,'%')
print ("Compared to all the rides:")
print ("Member round trips are",round_trips_member_prc_of_total,'%')
print ("Casual round trips are",round_trips_casual_prc_of_total,'%')


# In[35]:


#
#Round trips for every season:
#

def round_trip_percents_season (season1):
    '''
    Defining a function that calculates the percentages of round trips for
    casuals and memebers, for weekdays and weekends, for any season.
    The percentage is of casuals/members respectively, not total.
    Takes the season as input the season in quotes (i.e. 'Winter', or 'Summer', or 'Fall' or 'Spring')
    '''
    #    season1 = 'Summer'
    member_rnd = round_trips_station_name.loc[(round_trips_station_name.season == season1)&
                                              (round_trips_station_name.member_casual =='member')]
    casual_rnd = round_trips_station_name.loc[(round_trips_station_name.season == season1)&
                                              (round_trips_station_name.member_casual =='casual')]
    member_rnd_wkd = member_rnd.loc[member_rnd.weekday_weekend == 'weekday']
    member_rnd_wknd = member_rnd.loc[member_rnd.weekday_weekend == 'weekend']
    casual_rnd_wkd =  casual_rnd.loc[casual_rnd.weekday_weekend == 'weekday']
    casual_rnd_wknd = casual_rnd.loc[casual_rnd.weekday_weekend == 'weekend']
    member_rnd_wkd_prc =len(member_rnd_wkd)/len(yearly_member.loc[yearly_member.season == season1])*100
    member_rnd_wknd_prc =len(member_rnd_wknd)/len(yearly_member.loc[yearly_member.season == season1])*100
    casual_rnd_wkd_prc =len(casual_rnd_wkd)/len(yearly_casual.loc[yearly_casual.season == season1])*100
    casual_rnd_wknd_prc =len(casual_rnd_wknd)/len(yearly_casual.loc[yearly_casual.season == season1])*100
    data = pd.DataFrame([[casual_rnd_wkd_prc,member_rnd_wkd_prc],
                         [casual_rnd_wknd_prc,member_rnd_wknd_prc]])
    data = data.append([[data[0][0]+data[0][1],data[1][0]+data[1][1]]])
    data.index = ['Weekday','Weekend','Total']
    data.columns = ["Casuals","Members"]
    return data

# Define an empty list
round_trips_prc_season_list = []

# fill it with the percents for the weekday, weekend and total for every season
for season in seasons:
    round_trips_prc_season_list.append(round_trip_percents_season(season))

    
test = pd.DataFrame(round_trips_prc_season_list[0])
for i in range (1,4,1):
    test = test.append(round_trips_prc_season_list[i])
test.reset_index(inplace=True)    

first_column = pd.DataFrame([])
for i in range (4):
    first_column = first_column.append(pd.DataFrame([seasons[i],seasons[i],seasons[i]]))
first_column.reset_index(drop=True, inplace=True)

round_trips_prc_season = pd.concat([first_column, test], axis=1, join='outer')
round_trips_prc_season.columns = ['Season','Day Period','Casuals','Members']
display(round_trips_prc_season)

#Export data for use elsewhere
round_trips_prc_season.to_csv(r'C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Exported_Tables\round_trip_percents_season.csv')

for i in range(4):
    print ('During', seasons[i],'the percentages of round trips for casual/members are:')
    print (round_trips_prc_season_list[i])


# In[36]:


#
#finding the top 10 station names of the round trips for weekdays and weekends:
#

df3 = (round_trips_station_name.loc[round_trips_station_name.season == 'Summer']
.groupby(['member_casual','weekday_weekend'])['end_station_name']
.value_counts(normalize=False)
.rename('counts')
.reset_index())


#weekday top 10 stations for round trips, for casuals:
casual_end_station_weekday_r = df3.loc[(df3.member_casual == 'casual')&
                                       (df3.weekday_weekend == 'weekday')].reset_index()[0:10]

#weekend top 10 stations for round trips, for casuals:
casual_end_station_weekend_r = df3.loc[(df3.member_casual == 'casual')&
                                       (df3.weekday_weekend == 'weekend')].reset_index()[0:10]

#weekday top 10 stations for round trips, for members:
member_end_station_weekday_r = df3.loc[(df3.member_casual == 'member')&
                                       (df3.weekday_weekend == 'weekday')].reset_index()[0:10]

#weekend top 10 stations for round trips, for members
member_end_station_weekend_r = df3.loc[(df3.member_casual == 'member')&
                                       (df3.weekday_weekend == 'weekend')].reset_index()[0:10]

#Stations by casuals
test = casual_end_station_weekday_r
casual_end_station_r = test.append(casual_end_station_weekend_r,ignore_index=True)

#Stations by members
test = member_end_station_weekday_r
member_end_station_r = test.append(casual_end_station_weekend_r,ignore_index=True)

#All stations:
test = casual_end_station_r
all_end_station_r = test.append(member_end_station_r,ignore_index=True)


#Identifying the unique stations mostly used for round trips:
casual_end_station_names_r = pd.DataFrame(np.unique(casual_end_station_r.end_station_name))
member_end_station_names_r = pd.DataFrame(np.unique(member_end_station_r.end_station_name)) 
all_end_station_names_r = pd.DataFrame(np.unique(all_end_station_r.end_station_name))


# In[37]:


#
#Identifying the percent of casual and member summer rides that is round trips:
#

## For the weekdays:
print ('Roundtrips during the weekdays by members include',
       member_end_station_weekday_r['counts'].sum()/len(yearly_member.loc[(yearly_member.season == 'Summer')])*100,
       '% of all summer member rides' )
print ('Roundtrips during the weekdays by casual riders include',
       casual_end_station_weekday_r['counts'].sum()/len(yearly_casual.loc[(yearly_casual.season == 'Summer')])*100,
       '% of all summer casual rides')


## For the weekend:
print ('Roundtrips during the weekend by members include',
       member_end_station_weekend_r['counts'].sum()/len(yearly_member.loc[yearly_member.season == 'Summer'])*100,
       '% of all summer member rides' )
print ('Roundtrips during the weekend by casual riders include',
       casual_end_station_weekend_r['counts'].sum()/len(yearly_casual.loc[yearly_casual.season == 'Summer'])*100,
       '% of all summer casual rides')


# In[38]:


#
#Bar charts showing the ride numbers for the days of the week, for casuals and members per season 
#

fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
bins = np.arange(8) - 0.5
#n_bins = 7
x02 = yearly_member.day_of_week.loc[yearly_member.season == "Winter"]
x01 = yearly_casual.day_of_week.loc[yearly_casual.season == "Winter"]

x12 = yearly_member.day_of_week.loc[yearly_member.season == "Spring"]
x11 = yearly_casual.day_of_week.loc[yearly_casual.season == 'Spring']

x22 = yearly_member.day_of_week.loc[yearly_member.season == 'Summer']
x21 = yearly_casual.day_of_week.loc[yearly_casual.season == 'Summer']

x32 = yearly_member.day_of_week.loc[yearly_member.season == 'Fall']
x31 = yearly_casual.day_of_week.loc[yearly_casual.season == 'Fall']

#x3 = yearly.day_of_week
colors = two_color#,'lime']

axs[0, 0].hist((x01,x02), bins, density=False, histtype='bar', color=colors, label=["Casual riders","Members"])
axs[0, 1].hist((x11,x12), bins, density=False, histtype='bar', color=colors)
axs[1, 0].hist((x21,x22), bins, density=False, histtype='bar', color=colors)
axs[1, 1].hist((x31,x32), bins, density=False, histtype='bar', color=colors)


axs[0,0].set_title('Winter', y=1.0, pad=-17,fontdict={'fontsize': 16})
axs[0,1].set_title('Spring', y=1.0, pad=-17,fontdict={'fontsize': 16})
axs[1,0].set_title('Summer', y=1.0, pad=-17,fontdict={'fontsize': 16})
axs[1,1].set_title('Fall', y=1.0, pad=-17,fontdict={'fontsize': 16})


# axs[1,0].set_xlabel('Day',fontsize='14')
# axs[1,1].set_xlabel('Day',fontsize='14')

axs[0,0].set_ylabel('No of rides',fontsize='14')
axs[1,0].set_ylabel('No of rides',fontsize='14')

#plt.ylabel('No of rides',fontsize='16')
axs[1,0].set_xticks(np.arange(7))
axs[1,1].set_xticks(np.arange(7))
axs[0,0].set_xticks(np.arange(7))
axs[0,1].set_xticks(np.arange(7))

axs[0,0].set_xticklabels([])
axs[0,1].set_xticklabels([])
axs[1,0].set_xticklabels(days, rotation = 45,fontsize='13')
axs[1,1].set_xticklabels(days, rotation = 45, fontsize='13')

axs[0,1].set_yticklabels([])
axs[1,1].set_yticklabels([])

axs[0,0].legend(prop={'size': 13},loc=6)

plt.setp(axs, ylim=axs[1,0].get_ylim())

axs[0,0].ticklabel_format(axis='y', style='scientific', scilimits=(4,4))
axs[1,0].ticklabel_format(axis='y', style='scientific', scilimits=(4,4))

axs[0,0].minorticks_on()
axs[0,1].minorticks_on()
axs[1,0].minorticks_on()
axs[1,1].minorticks_on()

axs[0,0].grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid


axs[0,0].grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid
axs[0,1].grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid
axs[1,0].grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid
axs[1,1].grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid

fig.tight_layout()

plt.subplots_adjust(hspace=0.1,wspace=0.1)
plt.savefig("Day_season.png",bbox_inches = 'tight')
plt.show()


# In[39]:


#
#Histogram showing the rides per starting time for weekday and weekend during summer 
#Rides calculated for every 10 min
#

#starting hour analysis for summer
fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min
y1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                                       (yearly_member.season == season1)]
y2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
y3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
y4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
y5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]
y6 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 5)&
                                       (yearly_member.season == season1)]
y7 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 6)&
                                       (yearly_member.season == season1)]

x1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
x2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
x3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
x4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
x5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]
x6 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 5)&
                                       (yearly_casual.season == season1)]
x7 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 6)&
                                       (yearly_casual.season == season1)]


axs[0,0].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[1,0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color)

axs[0,1].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color[:2])
axs[1,1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)


handles0, labels0 = axs[0,0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1,0].get_legend_handles_labels() #For reversing labels

axs[0,0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[0,1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)

axs[1,0].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,0].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

axs[1,1].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,1].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

# axs[1,1].set_xlabel('Time of day')
# axs[1,0].set_xlabel('Time of day')

# axs[0,0].set_ylabel('Rides per 10 min')
# axs[1,0].set_ylabel('Rides per 10 min')

axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()

axs[0,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[0,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()
axs[0,0].tick_params(labeltop=True)
axs[0,1].tick_params(labeltop=True)

#axs[0,0].set_xticklabels([])
#axs[0,1].set_xticklabels([])

axs[0,0].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)

# Don't allow the axis to be on top of your data
axs[0,0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].minorticks_on()
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[1,0].get_ylim()) #choosing the axs with the highest peak to normalize the rest
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Sumer_daily_starting_hour.png",bbox_inches = 'tight')
plt.show()


# In[40]:


#
#Histogram showing the rides per time for weekday during summer 
#Rides calculated for every 10 min
#

fig, (axs) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min
x1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                                       (yearly_member.season == season1)]
x2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
x3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
x4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
x5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]

y1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
y2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
y3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
y4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
y5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]


axs[1].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)

xmin = 0
xmax = 24
axs[0].set_xlim(xmin, xmax)
axs[1].set_xlim(xmin, xmax)


handles0, labels0 = axs[0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1].get_legend_handles_labels() #For reversing labels

axs[0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)


axs[0].set_title('Casual riders', y=1.0,x=0.14, pad=-30,fontdict={'fontsize': 20})
axs[1].set_title('Members',y=1.0,x=0.11,pad=-30,fontdict={'fontsize': 20})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0].xaxis.tick_top()
axs[0].tick_params(labeltop=True)



# axs[0].set_ylabel('Rides per 10 min')
# axs[1].set_ylabel('Rides per 10 min')
#axs[1,0].set_ylabel('Rides per 10 min')

#axs[1,1].yaxis.tick_right()
axs[1].yaxis.tick_right()
axs[1].yaxis.tick_left()

#axs[0].set_xticklabels([])

#axs[1].set_xticklabels([])
# Don't allow the axis to be on top of your data
#axs[1].set_axisbelow(False)
axs[0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0].minorticks_on()
axs[0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1].minorticks_on()
axs[1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,1].minorticks_on()
# axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,0].minorticks_on()
# axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

axs[0].tick_params(axis='y', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)

plt.setp(axs, ylim=axs[1].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Seasonal_weekday_starting_hour.png",bbox_inches = 'tight')
plt.show()


# In[41]:


#
#Histogram showing the rides per time for the weekend during summer 
#Rides calculated for every 10 min
#

fig, (axs) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min
# x1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
#                                        (yearly_member.season == season1)]
# x2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
#                                        (yearly_member.season == season1)]
# x3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
#                                        (yearly_member.season == season1)]
# x4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
#                                        (yearly_member.season == season1)]
# x5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
#                                        (yearly_member.season == season1)]


# y1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
#                                        (yearly_casual.season == season1)]
# y2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
#                                        (yearly_casual.season == season1)]
# y3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
#                                        (yearly_casual.season == season1)]
# y4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
#                                        (yearly_casual.season == season1)]
# y5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
#                                        (yearly_casual.season == season1)]


axs[0].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])
axs[1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0].set_xlim(xmin, xmax)
axs[1].set_xlim(xmin, xmax)


axs[1].set_title('Members', y=1.0,x=0.11, pad=-30,fontdict={'fontsize': 20})
axs[0].set_title('Casual riders',y=1.0,x=0.14,pad=-30,fontdict={'fontsize': 20})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].xaxis.tick_top()
axs[0].tick_params(labeltop=True)

handles0, labels0 = axs[0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1].get_legend_handles_labels() #For reversing labels

axs[0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=1)
axs[1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=1)

# axs[0].set_ylabel('Rides per 10 min')
# axs[1].set_ylabel('Rides per 10 min')
#axs[1,0].set_ylabel('Rides per 10 min')

#axs[1,1].yaxis.tick_right()
axs[1].yaxis.tick_right()
axs[1].yaxis.tick_left()
axs[0].tick_params(axis='y', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)
#axs[0].set_xticklabels([])

#axs[1].set_xticklabels([])
# Don't allow the axis to be on top of your data
#axs[1].set_axisbelow(False)
axs[0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0].minorticks_on()
axs[0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1].minorticks_on()
axs[1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,1].minorticks_on()
# axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,0].minorticks_on()
# axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[0].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Seasonal_weekend_starting_hour.png",bbox_inches = 'tight')
plt.show()


# # Identifying percent during peak hour for all year:

# In[42]:


def casual_yearly_prc_between_t(t1,t2):
    '''
    Returns the % of casual rides between the specified time range. time is only hours (1hour30min is 1.5)
    '''
    group1 = yearly_casual.loc[(yearly_casual.start_hour_of_day < t2)&(yearly_casual.start_hour_of_day > t1)]
    peak_hour_prc = len(group1.loc[group1.weekday_weekend == "weekday"])/len(yearly_casual)*100
    return(peak_hour_prc)

def member_yearly_prc_between_t(t1,t2):
    '''
    Returns the % of member rides between the specified time range. time is only hours (1hour30min is 1.5)
    '''
    group1 = yearly_member.loc[(yearly_member.start_hour_of_day < t2)&(yearly_member.start_hour_of_day > t1)]
    peak_hour_prc = len(group1.loc[group1.weekday_weekend == "weekday"])/len(yearly_member)*100
    return(peak_hour_prc)

casual_yearly_prc_between_t(12,21)
member_yearly_prc_between_t(10,21)


# In[43]:


zoneA_prc_cas = casual_yearly_prc_between_t(7.5,9)
zoneB_prc_cas = casual_yearly_prc_between_t(11.5,13.5)
zoneC_prc_cas = casual_yearly_prc_between_t(17,19)

zoneA_prc_mem = member_yearly_prc_between_t(7.5,9)
zoneB_prc_mem = member_yearly_prc_between_t(11.5,13.5)
zoneC_prc_mem = member_yearly_prc_between_t(17,19)


# In[44]:


print ('ZoneA annual percent of casuals',zoneA_prc_cas)
print ('ZoneB annual percent of casuals',zoneB_prc_cas)
print ('ZoneC annual percent of casuals',zoneC_prc_cas)
print ('')
print ('ZoneA annual percent of members',zoneA_prc_mem)
print ('ZoneB annual percent of members',zoneB_prc_mem)
print ('ZoneC annual percent of members',zoneC_prc_mem)


# In[45]:


#
#Percentages for weekends and weekdays
#

total_rides = len(yearly)
all_weekday = len(yearly.loc[yearly.weekday_weekend == 'weekday'])
all_weekend = len(yearly.loc[yearly.weekday_weekend == 'weekday'])
weekday_prc = all_weekday / total_rides * 100
weekend_prc = all_weekend / total_rides * 100



total_member = len(yearly_member) 
all_weekday_member = len(yearly_member.loc[yearly_member.weekday_weekend == 'weekday']) 
all_weekend_member = len(yearly_member.loc[yearly_member.weekday_weekend == 'weekend'])
weekday_member_prc = all_weekday_member / total_member * 100
weekend_member_prc = all_weekend_member / total_member * 100

total_casual = len(yearly_casual) 
all_weekday_casual = len(yearly_casual.loc[yearly_casual.weekday_weekend == 'weekday']) 
all_weekend_casual = len(yearly_member.loc[yearly_member.weekday_weekend == 'weekend'])
weekday_casual_prc = all_weekday_casual / total_casual * 100
weekend_casual_prc = all_weekend_casual / total_casual * 100

casual_week_prc = pd.DataFrame()
member_week_prc = pd.DataFrame()

casual_week_prc['Weekday'] = [weekday_casual_prc]
member_week_prc['Weekday'] = [weekday_member_prc]

casual_week_prc['Weekend'] = [weekend_casual_prc]
member_week_prc['Weekend'] = [weekend_member_prc]

# duration_comparison['members'] = member_duration
# duration_comparison['casual'] = casual_duration
# duration_comparison.index = months

week_prc = pd.DataFrame()
week_prc['casual'] = casual_week_prc.T
week_prc['member'] = member_week_prc.T
week_prc


# In[ ]:





# In[ ]:





# In[46]:


#
#histograms for ending hour analysis for summer, for all days
#

fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min
x1 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                                       (yearly_member.season == season1)]
x2 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
x3 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
x4 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
x5 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]
x6 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 5)&
                                       (yearly_member.season == season1)]
x7 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == 6)&
                                       (yearly_member.season == season1)]

y1 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
y2 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
y3 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
y4 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
y5 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]
y6 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 5)&
                                       (yearly_casual.season == season1)]
y7 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == 6)&
                                       (yearly_casual.season == season1)]


axs[0,0].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[0,1].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)

axs[1,0].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])
axs[1,1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)

axs[0,1].legend(prop={'size': 11},loc=6)
axs[1,1].legend(prop={'size': 11},loc=6)

axs[0,0].set_title('Members', y=1.0, pad=-17,fontdict={'fontsize': 15})
axs[0,1].set_title('Casual riders',y=1.0,pad=-17,fontdict={'fontsize': 15})

axs[1,0].set_title('Members', y=1.0, pad=-17,fontdict={'fontsize': 15})
axs[1,1].set_title('Casual riders',y=1.0,pad=-17,fontdict={'fontsize': 15})

axs[1,1].set_xlabel('Time of day')
axs[1,0].set_xlabel('Time of day')

axs[0,0].set_ylabel('Rides per 10 min')
axs[1,0].set_ylabel('Rides per 10 min')

axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()
axs[0,0].set_xticklabels([])
axs[0,1].set_xticklabels([])
# Don't allow the axis to be on top of your data
axs[0,0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].minorticks_on()
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[0,0].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Seasonal_daily_end_hour.png",bbox_inches = 'tight')
plt.show()


# In[47]:


#
#Comparing starting and ending times for a specific day:
#

fig, (axs) = plt.subplots(nrows=1, ncols=2, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6
day_no = 2
x1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == day_no)&
                                       (yearly_member.season == season1)]
x2 = yearly_member.end_hour_of_day.loc[(yearly_member.day_of_week == day_no)&
                                       (yearly_member.season == season1)]


y1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == day_no)&
                                       (yearly_casual.season == season1)]
y2 = yearly_casual.end_hour_of_day.loc[(yearly_casual.day_of_week == day_no)&
                                       (yearly_casual.season == season1)]

axs[0].hist((x1,x2), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=['Start','End'], color= five_color[:2])
axs[1].hist((y1,y2), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=['Start','End'], color= five_color[:2])
axs[0].set_title('Members',pad=-12)
axs[0].set_xlim(0, 24)
axs[0].legend(prop={'size': 11},loc=2)
axs[1].legend(prop={'size': 11},loc=2)
axs[1].set_title('Casuals',pad=-12)
axs[1].set_xlim(0, 24)


# axs[0].set_yticklabels([])
# axs[1].set_yticklabels([])
# axs[0].set_xticklabels([])
# axs[1].set_xticklabels([])

axs[1].set_xlabel('Time of day')
axs[0].set_xlabel('Time of day')

axs[0].set_ylabel('Rides')
axs[1].set_ylabel('Rides')

axs[0].text(0.25, 2500, ('day =', day_no) ,fontdict = {'size':23} )

plt.setp(axs, ylim=axs[0].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)

plt.show()


# In[48]:


#
#Histogram showing the time duration per day for summer
#

fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Summer'
n_bins = 6*10 # 1min intervals
g = [[],[],[],[]]
x1 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 0)&(yearly_member.season == season1)]
x2 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 1)&(yearly_member.season == season1)]
x3 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 2)&(yearly_member.season == season1)]
x4 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 3)&(yearly_member.season == season1)]
x5 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 4)&(yearly_member.season == season1)]
x6 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 5)&(yearly_member.season == season1)]
x7 = yearly_member.trip_duration_min.loc[(yearly_member.day_of_week == 6)&(yearly_member.season == season1)]

y1 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 0)&(yearly_casual.season == season1)]
y2 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 1)&(yearly_casual.season == season1)]
y3 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 2)&(yearly_casual.season == season1)]
y4 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 3)&(yearly_casual.season == season1)]
y5 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 4)&(yearly_casual.season == season1)]
y6 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 5)&(yearly_casual.season == season1)]
y7 = yearly_casual.trip_duration_min.loc[(yearly_casual.day_of_week == 6)&(yearly_casual.season == season1)]

g[0] = axs[0,1].hist((x1,x2,x3,x4,x5), n_bins, (0,60), density=False, histtype='step', stacked=False,fill=False, linewidth=2,label=days, color= five_color)
g[1] = axs[0,0].hist((y1,y2,y3,y4,y5), n_bins, (0,60), density=False, histtype='step', stacked=False,fill=False, linewidth=2,label=days, color= five_color)
g[2] = axs[1,1].hist((x6,x7), n_bins, (0,60), density=False, histtype='step', stacked=False,fill=False, linewidth=2,label=days[5:], color= five_color[:2])
g[3] = axs[1,0].hist((y6,y7), n_bins, (0,60), density=False, histtype='step', stacked=False,fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 60
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)

axs[0,1].legend(prop={'size': 11},loc=1)
axs[1,1].legend(prop={'size': 11},loc=1)
axs[0,1].set_title('Members', y=1.0, pad=-17,fontdict={'fontsize': 15})
axs[0,0].set_title('Casual riders',y=1.0,pad=-17,fontdict={'fontsize': 15})
axs[1,1].set_title('Members', y=1.0, pad=-17,fontdict={'fontsize': 15})
axs[1,0].set_title('Casual riders',y=1.0,pad=-17,fontdict={'fontsize': 15})
axs[1,1].set_xlabel('Trip duration (min)',fontdict={'fontsize': 15})
axs[1,0].set_xlabel('Trip duration (min)',fontdict={'fontsize': 15})
axs[0,0].set_ylabel('No of rides',fontdict={'fontsize': 15})
axs[1,0].set_ylabel('No of rides',fontdict={'fontsize': 15})
axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()
axs[0,0].set_xticklabels([])
axs[0,1].set_xticklabels([])

axs[0,0].set_axisbelow(True)# Don't allow the axis to be on top of your data
axs[0,0].minorticks_on()# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[0,1].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Seasonal_daily_duration.png",bbox_inches = 'tight')
plt.show()


# In[49]:


#
#Finding the peak duration for each day shown in the histograms
#

peak_duration = pd.DataFrame(columns=('Day',"Members_Dur_Peak",'Casual_Dur_peak'))
for m in range(5): # index of days of week - weekdays
    bins_day_member = g[0][0][m] # Choosing the array that contains the bin heights
    bins_day_casual = g[1][0][m] # Choosing the array that contains the bin heights
    bin_max_member = np.argmax(bins_day_member)
    bin_max_casual = np.argmax(bins_day_casual)
    time_peak_member = g[0][1][bin_max_member]
    time_peak_casual = g[1][1][bin_max_casual]
    data =  pd.DataFrame([[days[m],time_peak_member,time_peak_casual]],columns=('Day',"Members_Dur_Peak",'Casual_Dur_peak'))
#    peak_duration['Day'] = peak_duration['Day'].append(days[m]) 
    peak_duration = peak_duration.append(data)

for m in range(2): # index of days of week - weekdays
    bins_day_member = g[2][0][m] # Choosing the array that contains the bin heights
    bins_day_casual = g[3][0][m] # Choosing the array that contains the bin heights
    bin_max_member = np.argmax(bins_day_member)
    bin_max_casual = np.argmax(bins_day_casual)
    time_peak_member = g[2][1][bin_max_member]
    time_peak_casual = g[3][1][bin_max_casual]
    data =  pd.DataFrame([[days[5+m],time_peak_member,time_peak_casual]],columns=('Day',"Members_Dur_Peak",'Casual_Dur_peak'))
#    peak_duration['Day'] = peak_duration['Day'].append(days[m]) 
    peak_duration = peak_duration.append(data)

peak_duration


# In[50]:


#
#Identifying when the peaks take place throughout the day for weekdays
#For members I filter rides for 4-8 min, and for casuals for 7-11 min (4min duration arount the peak)
#

fig, (axs) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min

#filtering for summer:
member_summer = yearly_member.loc[(yearly_member.season == season1)]
casual_summer = yearly_casual.loc[(yearly_casual.season == season1)]

#filtering for specific hours:
mem_min_t = 4
mem_max_t = 8

cas_min_t = 8
cas_max_t = 12

member_summer_peak = member_summer.loc[(member_summer.trip_duration_min >= mem_min_t)&
                                       (member_summer.trip_duration_min <= mem_max_t)]

casual_summer_peak = casual_summer.loc[(casual_summer.trip_duration_min >= mem_min_t)&
                                       (casual_summer.trip_duration_min <= mem_max_t)]


# filtering for each day seperately and defining the variables
x1 = member_summer_peak.start_hour_of_day.loc[(member_summer_peak.day_of_week == 0)]
x2 = member_summer_peak.start_hour_of_day.loc[(member_summer_peak.day_of_week == 1)]
x3 = member_summer_peak.start_hour_of_day.loc[(member_summer_peak.day_of_week == 2)]
x4 = member_summer_peak.start_hour_of_day.loc[(member_summer_peak.day_of_week == 3)]
x5 = member_summer_peak.start_hour_of_day.loc[(member_summer_peak.day_of_week == 4)]

y1 = casual_summer_peak.start_hour_of_day.loc[(casual_summer_peak.day_of_week == 0)]
y2 = casual_summer_peak.start_hour_of_day.loc[(casual_summer_peak.day_of_week == 1)]
y3 = casual_summer_peak.start_hour_of_day.loc[(casual_summer_peak.day_of_week == 2)]
y4 = casual_summer_peak.start_hour_of_day.loc[(casual_summer_peak.day_of_week == 3)]
y5 = casual_summer_peak.start_hour_of_day.loc[(casual_summer_peak.day_of_week == 4)]


axs[1].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)

xmin = 0
xmax = 24
axs[0].set_xlim(xmin, xmax)
axs[1].set_xlim(xmin, xmax)


handles0, labels0 = axs[0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1].get_legend_handles_labels() #For reversing labels

axs[0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)


axs[0].set_title('Casual riders', y=1.0,x=0.14, pad=-30,fontdict={'fontsize': 20})
axs[1].set_title('Members',y=1.0,x=0.11,pad=-30,fontdict={'fontsize': 20})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0].xaxis.tick_top()
axs[0].tick_params(labeltop=True)



# axs[0].set_ylabel('Rides per 10 min')
# axs[1].set_ylabel('Rides per 10 min')
#axs[1,0].set_ylabel('Rides per 10 min')

#axs[1,1].yaxis.tick_right()
axs[1].yaxis.tick_right()
axs[1].yaxis.tick_left()

#axs[0].set_xticklabels([])

#axs[1].set_xticklabels([])
# Don't allow the axis to be on top of your data
#axs[1].set_axisbelow(False)
axs[0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0].minorticks_on()
axs[0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1].minorticks_on()
axs[1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,1].minorticks_on()
# axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,0].minorticks_on()
# axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

axs[0].tick_params(axis='y', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)

plt.setp(axs, ylim=axs[1].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Hours_for_peak_duration_weekday_starting_hour.png",bbox_inches = 'tight')
plt.show()


#identifying how much percent of the summer casuals are the ones shown in the graph (casual, weekday, peak_duration):
casual_peak_duration_prc = len( casual_summer_peak.start_hour_of_day
                               .loc[(casual_summer_peak.day_of_week < 5 )]) / (len(casual_summer))*100

print ('These casual rides are:',casual_peak_duration_prc,'% of total summer casual rides')
#they are evenly spread out through the day
                                                                         
                                                                        


# In[51]:


#
#Identifying WHEN trips for more than 1h occur:
#

fig, (axs) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min

#filtering for summer:
member_summer = yearly_member.loc[(yearly_member.season == season1)]
casual_summer = yearly_casual.loc[(yearly_casual.season == season1)]

#filtering for specific hours:
min_t = 60
max_t = 60*24

member_summer_1h_plus = member_summer.loc[(member_summer.trip_duration_min >= min_t)&
                                          (member_summer.trip_duration_min <= max_t)]

casual_summer_1h_plus = casual_summer.loc[(casual_summer.trip_duration_min >= min_t)&
                                          (casual_summer.trip_duration_min <= max_t)]


# filtering for each day seperately and defining the variables

x1 = member_summer_1h_plus.start_hour_of_day.loc[(member_summer_1h_plus.day_of_week == 0)]
x2 = member_summer_1h_plus.start_hour_of_day.loc[(member_summer_1h_plus.day_of_week == 1)]
x3 = member_summer_1h_plus.start_hour_of_day.loc[(member_summer_1h_plus.day_of_week == 2)]
x4 = member_summer_1h_plus.start_hour_of_day.loc[(member_summer_1h_plus.day_of_week == 3)]
x5 = member_summer_1h_plus.start_hour_of_day.loc[(member_summer_1h_plus.day_of_week == 4)]

y1 = casual_summer_1h_plus.start_hour_of_day.loc[(casual_summer_1h_plus.day_of_week == 0)]
y2 = casual_summer_1h_plus.start_hour_of_day.loc[(casual_summer_1h_plus.day_of_week == 1)]
y3 = casual_summer_1h_plus.start_hour_of_day.loc[(casual_summer_1h_plus.day_of_week == 2)]
y4 = casual_summer_1h_plus.start_hour_of_day.loc[(casual_summer_1h_plus.day_of_week == 3)]
y5 = casual_summer_1h_plus.start_hour_of_day.loc[(casual_summer_1h_plus.day_of_week == 4)]


axs[1].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)

xmin = 0
xmax = 24
axs[0].set_xlim(xmin, xmax)
axs[1].set_xlim(xmin, xmax)


handles0, labels0 = axs[0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1].get_legend_handles_labels() #For reversing labels

axs[0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)


axs[0].set_title('Casual riders', y=1.0,x=0.14, pad=-30,fontdict={'fontsize': 20})
axs[1].set_title('Members',y=1.0,x=0.11,pad=-30,fontdict={'fontsize': 20})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0].xaxis.tick_top()
axs[0].tick_params(labeltop=True)



# axs[0].set_ylabel('Rides per 10 min')
# axs[1].set_ylabel('Rides per 10 min')
#axs[1,0].set_ylabel('Rides per 10 min')

#axs[1,1].yaxis.tick_right()
axs[1].yaxis.tick_right()
axs[1].yaxis.tick_left()

#axs[0].set_xticklabels([])

#axs[1].set_xticklabels([])
# Don't allow the axis to be on top of your data
#axs[1].set_axisbelow(False)
axs[0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0].minorticks_on()
axs[0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1].minorticks_on()
axs[1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,1].minorticks_on()
# axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,0].minorticks_on()
# axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

axs[0].tick_params(axis='y', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)

plt.setp(axs, ylim=axs[0].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Hours_for_trip_duration_more_1h_starting_hour.png",bbox_inches = 'tight')
plt.show()


#identifying how much percent of the summer casuals are the ones shown in the graph (casual, weekday, peak_duration):
casual_peak_duration_prc = len( casual_summer_1h_plus.start_hour_of_day
                               .loc[(casual_summer_1h_plus.day_of_week < 5 )]) / (len(casual_summer))*100
print ('These casual rides are:',casual_peak_duration_prc,'% of total summer casual rides')

#Identifying  the top 10 stations used:
stations_used = Counter(casual_summer_1h_plus.start_station_name.loc[(casual_summer_1h_plus.day_of_week < 5)])
top_10_for_over1h = stations_used.most_common(10)
top_10_for_over1h


# In[62]:


#
#Identifying WHEN trips for less than 1h occur
#

fig, (axs) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))
season1 = 'Summer'
n_bins = 24*6 #per 10 min

#filtering for summer:
member_summer = yearly_member.loc[(yearly_member.season == season1)]
casual_summer = yearly_casual.loc[(yearly_casual.season == season1)]

#filtering for specific hours:
min_t = 0
max_t = 60

member_summer_1h_less = member_summer.loc[(member_summer.trip_duration_min >= min_t)&
                                          (member_summer.trip_duration_min <= max_t)]

casual_summer_1h_less = casual_summer.loc[(casual_summer.trip_duration_min >= min_t)&
                                          (casual_summer.trip_duration_min <= max_t)]


# filtering for each day seperately and defining the variables

x1 = member_summer_1h_less.start_hour_of_day.loc[(member_summer_1h_less.day_of_week == 0)]
x2 = member_summer_1h_less.start_hour_of_day.loc[(member_summer_1h_less.day_of_week == 1)]
x3 = member_summer_1h_less.start_hour_of_day.loc[(member_summer_1h_less.day_of_week == 2)]
x4 = member_summer_1h_less.start_hour_of_day.loc[(member_summer_1h_less.day_of_week == 3)]
x5 = member_summer_1h_less.start_hour_of_day.loc[(member_summer_1h_less.day_of_week == 4)]

y1 = casual_summer_1h_less.start_hour_of_day.loc[(casual_summer_1h_less.day_of_week == 0)]
y2 = casual_summer_1h_less.start_hour_of_day.loc[(casual_summer_1h_less.day_of_week == 1)]
y3 = casual_summer_1h_less.start_hour_of_day.loc[(casual_summer_1h_less.day_of_week == 2)]
y4 = casual_summer_1h_less.start_hour_of_day.loc[(casual_summer_1h_less.day_of_week == 3)]
y5 = casual_summer_1h_less.start_hour_of_day.loc[(casual_summer_1h_less.day_of_week == 4)]


axs[1].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)

xmin = 0
xmax = 24
axs[0].set_xlim(xmin, xmax)
axs[1].set_xlim(xmin, xmax)


handles0, labels0 = axs[0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1].get_legend_handles_labels() #For reversing labels

axs[0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)


axs[0].set_title('Casual riders', y=1.0,x=0.14, pad=-30,fontdict={'fontsize': 20})
axs[1].set_title('Members',y=1.0,x=0.11,pad=-30,fontdict={'fontsize': 20})

# axs[1].set_xlabel('Time of day')
# axs[0].set_xlabel('Time of day')
axs[0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0].xaxis.tick_top()
axs[0].tick_params(labeltop=True)



# axs[0].set_ylabel('Rides per 10 min')
# axs[1].set_ylabel('Rides per 10 min')
#axs[1,0].set_ylabel('Rides per 10 min')

#axs[1,1].yaxis.tick_right()
axs[1].yaxis.tick_right()
axs[1].yaxis.tick_left()

#axs[0].set_xticklabels([])

#axs[1].set_xticklabels([])
# Don't allow the axis to be on top of your data
#axs[1].set_axisbelow(False)
axs[0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0].minorticks_on()
axs[0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1].minorticks_on()
axs[1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,1].minorticks_on()
# axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
# axs[1,0].minorticks_on()
# axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
# axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

axs[0].tick_params(axis='y', labelsize=16)
axs[1].tick_params(axis='y', labelsize=16)

plt.setp(axs, ylim=axs[1].get_ylim())
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Hours_for_trip_duration_less_1h_starting_hour.png",bbox_inches = 'tight')
plt.show()


#identifying how much percent of the summer casuals are the ones shown in the graph (casual, weekday, peak_duration):
casual_peak_duration_prc = len( casual_summer_1h_less.start_hour_of_day
                               .loc[(casual_summer_1h_less.day_of_week < 5 )]) / (len(casual_summer))*100


                                                                        


# In[55]:


#
#Bar chart showing the rides per month for members/casuals
#

fig, ((ax0)) = plt.subplots(nrows=1, ncols=1)

#n_bins = 12
bins_ = np.arange(14) - 0.5
x2 = yearly_member.month
x1 = yearly_casual.month

#ind = np.arange(n_bins) 
width = 0.35

#x3 = yearly.day_of_week
colors = two_color#,'lime']

n, bins, patches = ax0.hist((x1,x2), bins_, density=False, histtype='bar',
                            color=colors, label=["Casual riders","Members"])

ax0.set_xticks(np.arange(12)+1)
#plt.rcParams.update({'font.size': 19})
ax0.legend(prop={'size': 14})
ax0.set_title('Monthly rides',fontsize='16')

#ax0.set_xticks([0.4,1.15,1.9,2.65])
ax0.set_xticklabels(months, rotation = 45,fontsize='15')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(False)
ax0.minorticks_on()

ax0.grid(which='major', axis='y',linestyle='-', linewidth='1') # Customize the major grid
ax0.grid(which='minor', axis='y', linestyle=':', linewidth='0.5')# Customize the minor grid
ax0.xaxis.set_tick_params(which='minor', bottom=False)

#plt.xlabel('Seasons')
plt.ylabel('No of rides',fontsize='16')
ax0.ticklabel_format(axis='y', style='scientific', scilimits=(4,4))
#ax0.grid(zorder=0)
#ax.bar(range(len(y)), y, width=0.3, align='center', color='skyblue', zorder=3)
#plt.rcParams.update({'font.size': 24})
fig.set_size_inches(8,6)
ax0.set_xlim(0.2, 12.7)
ax0.set_axisbelow(True)
plt.savefig("total_months.png",bbox_inches = 'tight')
fig.tight_layout()

plt.show()


# In[56]:


#
#Heatmap showing day preferences for each month
#

fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(6, 6))

# generate randomly populated arrays
data1 = members_weekly_monthly.T
data2 = casual_weekly_monthly.T

# find minimum of minima & maximum of maxima
minmin = np.min([np.min(data1), np.min(data2)])
maxmax = np.max([np.max(data1), np.max(data2)])

im1 = axes[1].imshow(data1, vmin=minmin, vmax=maxmax,
                     extent=(0,12,0,7), aspect='auto', cmap='cividis',origin='lower')
im2 = axes[0].imshow(data2, vmin=minmin, vmax=maxmax,
                     extent=(0,12,0,7), aspect='auto', cmap='cividis',origin='lower')

axes[1].set_title('Members',x= 0.15, y=1.0, pad=-17,fontdict={'fontsize': 16}, color = 'white')
axes[0].set_title('Casual riders',x= 0.19, y=1.0, pad=-17,fontdict={'fontsize': 16},color = 'white')

axes[0].set_yticks(np.arange(7)+0.5)
axes[1].set_yticks(np.arange(7)+0.5)

#axes[1].set_yticks([])

axes[0].set_xticks([])
axes[1].set_xticks(np.arange(12)+0.5)

#axes[0].set_xticklabels(months, rotation = 45, fontsize='14')
axes[1].set_xticklabels(months, rotation = 45, fontsize='14')
axes[0].set_yticklabels(days, fontsize='13')
axes[1].set_yticklabels(days, fontsize='13')
plt.subplots_adjust(hspace=0.1,wspace=0.05)
# add space for colour bar
fig.subplots_adjust(right=0.75)
cbar_ax = fig.add_axes([0.78, 0.13, 0.04, 0.65])
fig.colorbar(im2, cax=cbar_ax)

plt.savefig("Days_per_month_heatmap.png",bbox_inches = 'tight')
#fig.tight_layout()


# In[57]:


#
#Comparing starting hours of day, for a specific day
#
fig, ((ax0)) = plt.subplots(nrows=1, ncols=1)
season1 = 'Spring'
n_bins = 24*6
x1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                        (yearly_member.season == season1)]
x2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                        (yearly_casual.season == season1)]
colors = ['firebrick','dodgerblue']#, 'lime']
#ax0.hist((x1,x2), n_bins, (0,24), density=False, histtype='bar', color=colors, label=["member","casual"])
ax0.hist((x1,x2), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2, color=colors, label=["member","casual"])

ax0.legend(prop={'size': 11})
ax0.set_title('Starting hour')
ax0.set_xlim(0, 24)
ax0.grid(color='b', which='minor',ls = '-.', lw = 0.55)

plt.xlabel('Time (hours)')
plt.ylabel('Trips')

fig.tight_layout()
fig.set_size_inches(6,6)
plt.show()


# In[58]:


#
## Yearly percentages:
#
members_no_yearly = count(yearly.member_casual,"member")
casual_no_yearly = count(yearly.member_casual,"casual")
no_of_rides = len(yearly)

print ("Last year there were",no_of_rides,"rides,")
print (f"{members_no_yearly} ({members_no_yearly/no_of_rides*100:.1f}%) of which were made by members, and")
print (f"{casual_no_yearly} ({casual_no_yearly/no_of_rides*100:.1f}%) of which were made by casual riders")


# In[59]:


#
#Average duration:
#
print ("Average trip duration is",yearly.trip_duration_min.mean())
print ("Average trip duration for members is",yearly_member.trip_duration_min.mean())
print ("Average trip duration for casual riders is",yearly_casual.trip_duration_min.mean())


# # Duration of rides (yearly) analysis:

# In[60]:


def duration_less(min):
    print ("for less than",min,"min:")
    less_than_1min = yearly.loc[(yearly.trip_duration_min < (min))]#&(cleaned2.me < (48*60))]
    less_than_1min_members = yearly.loc[(yearly.trip_duration_min < (min))&(yearly.member_casual == "member")]
    less_than_1min_casual = yearly.loc[(yearly.trip_duration_min < (min))&(yearly.member_casual == "casual")]

    test01 = len(less_than_1min)/len(cleaned)*100
    test02 = len(less_than_1min_members)/len(yearly_member)*100
    test03 = len(less_than_1min_casual)/len(yearly_casual)*100
    print (len(less_than_1min),test01,"all")
    print (len(less_than_1min_members),test02,"members")
    print (len(less_than_1min_casual),test03,"casual")
    return

def duration_between(min,max):
    print ("Duration between", min,"and", max,"min")
    all_users = yearly.loc[(yearly.trip_duration_min > (min))&(yearly.trip_duration_min < (max))]#&(cleaned2.me < (48*60))]
    members = yearly.loc[(yearly.trip_duration_min > (min))&(yearly.trip_duration_min < (max))&(yearly.member_casual == "member")]
    casual = yearly.loc[(yearly.trip_duration_min > (min))&(yearly.trip_duration_min < (max))&(yearly.member_casual == "casual")]

    test01 = len(all_users)/len(yearly)*100
    test02 = len(members)/len(yearly_member)*100
    test03 = len(casual)/len(yearly_casual)*100
    print (len(all_users),test01,"all")
    print (len(members),test02,"members")
    print (len(casual),test03,"casual")
    return

def duration_between_df(min,max,df):
    print ("Duration between", min,"and", max,"min for")
    all_users = df.loc[(df.trip_duration_min > (min))&(df.trip_duration_min < (max))]#&(cleaned2.me < (48*60))]
    test01 = len(all_users)/len(df)*100
    print (len(all_users),test01,"all")
    return

def duration_between_all_members_casual(min,max,df1,df2,df3):
    duration_between_df(min,max,df1)
    duration_between_df(min,max,df2)
    duration_between_df(min,max,df3)


# In[68]:


#
#finding the most common starting and ending time of trips
#

yearly.start_hour_of_day.mean() #14:48 is the average starting time
yearly_member.start_hour_of_day.mean() #14:32 is the average starting time
yearly_casual.start_hour_of_day.mean() #15:07 is the average starting time

yearly.end_hour_of_day.mean() #14:58 is the average ending time
yearly_member.end_hour_of_day.mean() #14:42 is the average ending time
yearly_casual.end_hour_of_day.mean() #15:18 is the average ending time


# In[78]:


#
#day of the week analysis
#

yearly.day_of_week.mode() #5
yearly_member.day_of_week.mode() #2
yearly_casual.day_of_week.mode() #5


# In[79]:


#
#trips that lasted more than a day
#
trips_more_than_a_day = yearly.loc[(yearly.trip_duration_min > (1*24*60))]#&(cleaned1.trip_duration_min < (48*60))]

more_than_a_day = len(trips_more_than_a_day) #no of rides that lasted more than a day
print ("No of rides that lasted more than a day:",more_than_a_day,'{0:.2f}'.format(more_than_a_day/len(yearly)*100),"% of total")
print (count(trips_more_than_a_day.member_casual,"casual")," where casual riders (",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"casual")/more_than_a_day*100) ,"%, and",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"casual")/len(yearly_casual)*100),"%of total casual riders")
print (count(trips_more_than_a_day.member_casual,"member")," where members (",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"member")/more_than_a_day*100) ,"%, and",'{0:.2f}'.format(count(trips_more_than_a_day.member_casual,"member")/len(yearly_member)*100),"%of total members")


# In[80]:


#
#Trip duration per month
#


member_duration = pd.DataFrame()
casual_duration = pd.DataFrame()

for i in range (12):
    mean_duration = yearly.trip_duration_min.loc[yearly.month == i+1 ].sum()/len(yearly.loc[yearly.month == i+1])
    mean_duration_member = yearly_member.trip_duration_min.loc[yearly_member.month == i+1].sum()/len(yearly_member.loc[yearly_member.month == i+1 ])
    mean_duration_casual = yearly_casual.trip_duration_min.loc[yearly_casual.month == i+1].sum()/len(yearly_casual.loc[yearly_casual.month == i +1])
    member_duration = member_duration.append([mean_duration_member])
    casual_duration = casual_duration.append([mean_duration_casual])


duration_comparison = pd.DataFrame()
duration_comparison['members'] = member_duration
duration_comparison['casual'] = casual_duration
duration_comparison.index = months
duration_comparison

duration_comparison.to_csv(r'C:\Users\Savvas\Documents\DataAnaytics\CaseStudy1\Exported_Tables\duration_monthly_comparison.csv')


# In[82]:


#
#Bar chart showing the trip duration per month
#
labels = months
x1 = duration_comparison.casual
x2 = duration_comparison.members

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, x1, width, label='Casual', color = two_color[0])
rects2 = ax.bar(x + width / 2, x2, width, label='Member',color = two_color[1] )

ax.set_ylabel('Trip duration (min)', fontsize = 20)

ax.set_xlabel('Months', fontsize = 22)
#ax.set_title('Trip duration per month')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize = 18)
#ax.set_xticklabels(fontsize = 18)
ax.legend(fontsize = 18)

# def autolabel(rects):
#    for rect in rects:
#       height = rect.get_height()
#       ax.annotate('{}'.format(height),
#          xy=(rect.get_x() + rect.get_width() / 2, height),
#          xytext=(0, 3), # 3 points vertical offset
#          textcoords="offset points",
#          ha='center', va='bottom')
plt.yticks(fontsize=18)
# autolabel(rects1)
# autolabel(rects2)
fig.set_size_inches(8,6)
plt.savefig("ride_duration_monthly.png",bbox_inches = 'tight')
plt.show()


# In[84]:


#
#starting hour analysis for winter
#
fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Winter'
n_bins = 24*6 #per 10 min
y1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                                       (yearly_member.season == season1)]
y2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
y3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
y4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
y5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]
y6 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 5)&
                                       (yearly_member.season == season1)]
y7 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 6)&
                                       (yearly_member.season == season1)]

x1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
x2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
x3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
x4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
x5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]
x6 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 5)&
                                       (yearly_casual.season == season1)]
x7 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 6)&
                                       (yearly_casual.season == season1)]


axs[0,0].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[1,0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color)

axs[0,1].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color[:2])
axs[1,1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)


handles0, labels0 = axs[0,0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1,0].get_legend_handles_labels() #For reversing labels

axs[0,0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[0,1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)

axs[1,0].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,0].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

axs[1,1].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,1].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

# axs[1,1].set_xlabel('Time of day')
# axs[1,0].set_xlabel('Time of day')

# axs[0,0].set_ylabel('Rides per 10 min')
# axs[1,0].set_ylabel('Rides per 10 min')

axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()

axs[0,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[0,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()
axs[0,0].tick_params(labeltop=True)
axs[0,1].tick_params(labeltop=True)

#axs[0,0].set_xticklabels([])
#axs[0,1].set_xticklabels([])

axs[0,0].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)

# Don't allow the axis to be on top of your data
axs[0,0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].minorticks_on()
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[1,0].get_ylim()) #choosing the axs with the highest peak to normalize the rest
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Winter_daily_starting_hour.png",bbox_inches = 'tight')
plt.show()


# In[86]:


#
#starting hour analysis for spring
#
fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Spring'
n_bins = 24*6 #per 10 min
y1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                                       (yearly_member.season == season1)]
y2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
y3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
y4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
y5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]
y6 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 5)&
                                       (yearly_member.season == season1)]
y7 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 6)&
                                       (yearly_member.season == season1)]

x1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
x2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
x3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
x4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
x5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]
x6 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 5)&
                                       (yearly_casual.season == season1)]
x7 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 6)&
                                       (yearly_casual.season == season1)]


axs[0,0].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[1,0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color)

axs[0,1].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color[:2])
axs[1,1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)


handles0, labels0 = axs[0,0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1,0].get_legend_handles_labels() #For reversing labels

axs[0,0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[0,1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)

axs[1,0].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,0].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

axs[1,1].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,1].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

# axs[1,1].set_xlabel('Time of day')
# axs[1,0].set_xlabel('Time of day')

# axs[0,0].set_ylabel('Rides per 10 min')
# axs[1,0].set_ylabel('Rides per 10 min')

axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()

axs[0,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[0,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()
axs[0,0].tick_params(labeltop=True)
axs[0,1].tick_params(labeltop=True)

#axs[0,0].set_xticklabels([])
#axs[0,1].set_xticklabels([])

axs[0,0].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)

# Don't allow the axis to be on top of your data
axs[0,0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].minorticks_on()
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[1,0].get_ylim()) #choosing the axs with the highest peak to normalize the rest
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Spring_daily_starting_hour.png",bbox_inches = 'tight')
plt.show()


# In[87]:


#
#starting hour analysis for fall
#
fig, (axs) = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
season1 = 'Fall'
n_bins = 24*6 #per 10 min
y1 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 0)&
                         (yearly_member.season == season1)]
y2 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 1)&
                                       (yearly_member.season == season1)]
y3 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 2)&
                                       (yearly_member.season == season1)]
y4 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 3)&
                                       (yearly_member.season == season1)]
y5 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 4)&
                                       (yearly_member.season == season1)]
y6 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 5)&
                                       (yearly_member.season == season1)]
y7 = yearly_member.start_hour_of_day.loc[(yearly_member.day_of_week == 6)&
                                       (yearly_member.season == season1)]

x1 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 0)&
                                       (yearly_casual.season == season1)]
x2 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 1)&
                                       (yearly_casual.season == season1)]
x3 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 2)&
                                       (yearly_casual.season == season1)]
x4 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 3)&
                                       (yearly_casual.season == season1)]
x5 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 4)&
                                       (yearly_casual.season == season1)]
x6 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 5)&
                                       (yearly_casual.season == season1)]
x7 = yearly_casual.start_hour_of_day.loc[(yearly_casual.day_of_week == 6)&
                                       (yearly_casual.season == season1)]


axs[0,0].hist((x1,x2,x3,x4,x5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color)
axs[1,0].hist((y1,y2,y3,y4,y5), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color)

axs[0,1].hist((x6,x7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days, color= five_color[:2])
axs[1,1].hist((y6,y7), n_bins, (0,24), density=False, histtype='step', stacked=False,
         fill=False, linewidth=2,label=days[5:], color= five_color[:2])

xmin = 0
xmax = 24
axs[0,0].set_xlim(xmin, xmax)
axs[0,1].set_xlim(xmin, xmax)
axs[1,1].set_xlim(xmin, xmax)
axs[1,0].set_xlim(xmin, xmax)


handles0, labels0 = axs[0,0].get_legend_handles_labels() #For reversing labels
handles1, labels1 = axs[1,0].get_legend_handles_labels() #For reversing labels

axs[0,0].legend(reversed(handles0), reversed(labels0),prop={'size': 13},loc=6)
axs[0,1].legend(reversed(handles1), reversed(labels1),prop={'size': 13},loc=6)

axs[1,0].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,0].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

axs[1,1].set_title('Members', y=1.0,x = .16, pad=-21.5,fontdict={'fontsize': 20})
axs[0,1].set_title('Casual rides',y=1.0,x = .2,pad=-21.5,fontdict={'fontsize': 20})

# axs[1,1].set_xlabel('Time of day')
# axs[1,0].set_xlabel('Time of day')

# axs[0,0].set_ylabel('Rides per 10 min')
# axs[1,0].set_ylabel('Rides per 10 min')

axs[1,1].yaxis.tick_right()
axs[0,1].yaxis.tick_right()

axs[0,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[0,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,0].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})
axs[1,1].set_xticklabels(['00:00','05:00','10:00','15:00','20:00'],fontdict={'fontsize': 16})

axs[0,0].xaxis.tick_top()
axs[0,1].xaxis.tick_top()
axs[0,0].tick_params(labeltop=True)
axs[0,1].tick_params(labeltop=True)

#axs[0,0].set_xticklabels([])
#axs[0,1].set_xticklabels([])

axs[0,0].tick_params(axis='y', labelsize=16)
axs[0,1].tick_params(axis='y', labelsize=16)
axs[1,0].tick_params(axis='y', labelsize=16)
axs[1,1].tick_params(axis='y', labelsize=16)

# Don't allow the axis to be on top of your data
axs[0,0].set_axisbelow(True)
# Turn on the minor TICKS, which are required for the minor GRID
axs[0,0].minorticks_on()
axs[0,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[0,1].minorticks_on()
axs[0,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[0,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,1].minorticks_on()
axs[1,1].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,1].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid
axs[1,0].minorticks_on()
axs[1,0].grid(which='major', axis='both',linestyle='-', linewidth='1') # Customize the major grid
axs[1,0].grid(which='minor', axis='x', linestyle=':', linewidth='0.5')#, color='black') # Customize the minor grid

plt.setp(axs, ylim=axs[1,0].get_ylim()) #choosing the axs with the highest peak to normalize the rest
plt.subplots_adjust(hspace=0.1,wspace=0.05)
plt.savefig("Fall_daily_starting_hour.png",bbox_inches = 'tight')
plt.show()


# In[88]:


time.ctime()


# In[ ]:


#Last corrections: 
#Remove time

