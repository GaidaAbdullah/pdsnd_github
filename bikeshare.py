import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    a function to get the filter desired by the user
    ex: the month, day, and/or city
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # take the input for the city from the user.
        chosen_city = input('\nChoose a city from (chicago, new york city, washington):')
        # convert the input into a lowercase letters.
        chosen_city = chosen_city.lower()
        cities_list = ['chicago', 'new york city', 'washington']
        # if the input city is available, break out of the loop,
        # or show an error message and ask the user again for an input
        if chosen_city in cities_list: break
        else: print('Invalid city!')

    while True:
        # take the inpot for the month from the user
        chosen_month = input('\nChoose a month from (all, january, february, ... , june):')
        # convert the input into a lowercase letters.
        chosen_month = chosen_month.lower()
        months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        # validate the user's input if it's within the first 6 months.
        if chosen_month in months_list[6:]: print('Please choose a valid month from (all, january, february, ... , june)')
        # if the user's input month is valid or if it's 'all', break out of the loop,
        # or show an error message and ask the user again for an input
        elif (chosen_month in months_list) or (chosen_month == 'all'): break
        else: print('Invalid Month!')

    while True:
        # take the inpot for the day from the user
        chosen_day = input('\nChoose a day from (all, monday, tuesday, ... sunday):')
        # convert the input into a lowercase letters.
        chosen_day = chosen_day.lower()
        day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        # if the user's input day is valid or if it's 'all', break out of the loop,
        # or show an error message and ask the user again for an input
        if (chosen_day in day_list) or (chosen_day == 'all'): break
        else: print('Invalid Day!')

    print('-'*40)
    # return the chosen city, month, day of the week.
    return chosen_city, chosen_month, chosen_day

def load_data(city, month, day):
    """
    a function to load the data for a city chosen by the user from a csv file into a dataframe.
    """
    
    global CITY_DATA
    # read the csv file and load it in a dataframe.
    df = pd.read_csv(CITY_DATA[city])
    # convert the two columns [Start Time, End Time] to a datetime type.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # if the user did not choose all months, filter the dataframe with the chosen month.
    if month != 'all':
        month_cond = df['Start Time'].dt.month_name() == month.capitalize()
        df = df[month_cond]
    # if the user did not choose all days of the week, filter the dataframe with the chosen day.
    if day != 'all':
        day_condition = df['Start Time'].dt.day_name() == day.capitalize()
        df = df[day_condition]
    # return the dataframe after it got loaded with the filtered data.
    return df

def time_stats(df):
    """
    a function to calculate most common month, day, and hour for traveling
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # set up a counter that's incremented each time in the loop
    # to determine what message to show for the result
    counter = 0
    # loop through the month names, day name, and hour.
    for most_common_value in [df['Start Time'].dt.month_name(), df['Start Time'].dt.day_name(), df['Start Time'].dt.hour]:
        # group the values for [most_common_value] and count them
        # ex: group the values for a month, day of week, hour.
        count_df = df['Start Time'].groupby([most_common_value]).agg('count')
        # sort the values and get the first index, this is to get the most common value.
        result = count_df.sort_values(ascending=False).index[0]
        # check for the counter, and display the message to the user.
        if counter == 0: print('Most common month is:', result)
        elif counter == 1: print('Most common day is:', result)
        elif counter == 2: print('Most common hour is:', result)
        counter = counter + 1

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    a function to calculate the most popular stations for trips, in term of
    most common starting station, ending station, and the most popular combination
    of starting and ending stations. 
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # add a new column for the combination of a starting station and an ending station.
    df['Station Combination'] = df['Start Station'] + " - " + df['End Station']
    # loop through the station columns.
    for col in ['Start Station', 'End Station', 'Station Combination']:
        # group the values by the station and count them 
        count_df = df[col].groupby([df[col]]).agg('count')
        # sort the values and get the first index, this is to get the most common value.
        result = count_df.sort_values(ascending=False).index[0]
        # print the result to the user.
        print('Most common', col, 'is:', result)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def calculate_age_group(age):
    """ 
    a function to calculate the age group for each customer.
    """ 
    if age <= 9: age_group = '0 - 9'
    elif age <= 19: age_group = '10 - 19 years'
    elif age <= 29: age_group = '20 - 29 years'
    elif age <= 39: age_group = '30 - 39 years'
    elif age <= 49: age_group = '40 - 49 years'
    else: age_group = '50 years and more'
    return age_group

def trip_duration_stats(df):
    """
    a function to calculate the total/mean travel time in minutes.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate the total/mean, and round the value to the nearest 2 decimal places.
    trip_sum = round(df['Trip Duration'].sum(), 2)
    trip_mean = round(df['Trip Duration'].mean(), 2)
    # print the results to the user.
    print('the total travel time is:', trip_sum, 'minutes')
    print('the mean of travel time is:', trip_mean, 'minutes')

    # check if the [Gender, Birth Year] columns exist, otherwise show an error message.
    if 'Gender' in df.columns and 'Birth Year' in df.columns:
        # add a new columns with the age group for each customer
        df['Age Group'] = (2021 - df['Birth Year']).apply(calculate_age_group)
        # get the available age groups, and sort them.
        age_group_list = df['Age Group'].unique()
        age_group_list.sort()
        # loop through the age groups.
        for age_group in age_group_list:
            # make a condition to filter the age group.
            age_group_cond = df['Age Group'] == age_group
            # calculate the total/mean for the age group, and round the value to the nearest 2 decimal places.
            trip_sum = round(df[age_group_cond]['Trip Duration'].sum(), 2)
            trip_mean = round(df[age_group_cond]['Trip Duration'].mean(), 2)
            # print the results to the user.
            print()
            print('the total travel time for the age group [', age_group,'] is:', trip_sum, 'minutes')
            print('the mean of travel time for the age group [', age_group,'] is:', trip_mean, 'minutes')
    else: print('Unavailable Birth Year and Gender Information!')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    a function to calculate the customers stats in the data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # get the count for each value in [User Type] column.
    user_types_values = df['User Type'].value_counts()
    # loop through the results, with the two values [usr_type, type_count]
    for usr_type, type_count in user_types_values.iteritems():
        # print the results to the user.
        print('Count of user type', usr_type, 'is:', type_count)
    
    # check if the [Gender] column exist, otherwise show an error message.
    if 'Gender' in df.columns:
        # get the count for each value in [Gender] column.
        gender_values = df['Gender'].value_counts()
        # loop through the results, with the two values [gender, gender_count]
        for gender, gender_count in gender_values.iteritems():
            # print the results to the user.
            print('Count of gender', gender, 'is:', gender_count)
    # show an error message if the [Gender] columns doesn't exist in the dataframe
    else: print('Unavailable Gender Information!')

    # check if the [Birth Year] column exist, otherwise show an error message.
    if 'Birth Year' in df.columns:
        # get the count for each value in [Birth Year] column.
        birth_year_values = df['Birth Year'].value_counts()
        # print the results to the user.
        print('Most common year of birth is:', int(birth_year_values.idxmax()), 'with a count of:', birth_year_values.max())
        print('Earliest year of birth is:', int(birth_year_values.index.min()))
        print('Most recent year of birth is:', int(birth_year_values.index.max()))
    # show an error message if the [Birth Year] columns doesn't exist in the dataframe
    else: print('Unavailable Birth Year Information!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_periods_stats(df):
    """ 
    a function to calculate the most common time periods for each gender
    """
    print('\nCalculating Time Periods For Each Gender...\n')
    start_time = time.time()
    # check if the [Gender] column exist, otherwise show an error message.
    if 'Gender' in df.columns:
        # add a new column [Period] with the time period from [Late Night, Early Morning, ..., Night].
        df['Period'] = (df['Start Time'].dt.hour % 24 + 4) // 4
        df['Period'].replace({1: 'Late Night',
                              2: 'Early Morning',
                              3: 'Morning',
                              4: 'Noon',
                              5: 'Evening',
                              6: 'Night'}, inplace=True)
        # group the values by each gender and time period and count them.
        periods_genders_groups = df.groupby(['Gender','Period']).count()['Start Time']
        # get the values and sort them to get the most common time period for each gender.
        females_group = periods_genders_groups['Female'].sort_values(ascending=False)
        males_group = periods_genders_groups['Male'].sort_values(ascending=False)
        # print the results to the user.
        print('The most common time period for females is:', females_group.index[0], 'with', females_group[0], 'times.')
        print('The most common time period for males is:', males_group.index[0], 'with', males_group[0], 'times.')
    # show an error message if the [Gender] columns doesn't exist in the dataframe
    else: print('Unavailable Gender Information!')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Display the raw data of a dataframe to the user.
    """
    # store the index for the rows, starting from 0
    i = 0
    # ask the user if they wants to view the raw data
    raw = input("Do you want to view the raw data? (yes/no)").lower()
    # set the maximum columns view of a dataframe
    pd.set_option('display.max_columns',200)

    while True:
        # if the user's input is [no], break out of the loop.
        if raw == 'no': break
        # if the user's input is [yes], print the 5 rows starting from [i] and ending with [i+5].
        elif raw == 'yes':
            print(df[i:i+5]) 
            # ask the user again if they wants to view the next 5 rows
            raw = input("Do you want to view 5 more raws? (yes/no)").lower() 
            # add 5 to the index for the next loop.
            i += 5
        # if the user's input is invalid, ask them again.
        else: raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()    
    
def main():
    """
    the start of the program
    """
    # loop indefinitely, until the user choose an input to break out.
    while True:
        # get the filters for the data [city, month, day]
        city, month, day = get_filters()
        # load the data into a dataframe
        df = load_data(city, month, day)
        # print the most common month, day, and hour for traveling
        time_stats(df)
        # print the most popular stations for trips
        station_stats(df)
        # print the total/mean travel time in minutes
        trip_duration_stats(df)
        # print the customers stats
        user_stats(df)
        # print the most common time period for each gender
        time_periods_stats(df)
        # view the raw data
        display_raw_data(df)
        # ask the user if they want to restart the program
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            # if the user chose anything but [yes], break out of the loop.
            if restart in ['yes','no']: break
        if restart != 'yes': break

if __name__ == '__main__':
    main()