import time
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 50)

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'washington': 'washington.csv' }

global_weekday = {'monday':1,'tuesday':2,'wednesday':3,'thursday':4,'friday':5,'saturday':6,'sunday':7,'all':8}
global_months = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'all':7}

def display_lines(city):

    df = pd.read_csv(CITY_DATA[city])

    counter=1
    start_from=0
    end_at=5

    while counter == 1:
        #print('\nNew start value is : ',start_from)
        #print('\nNew end value is : ',end_at)
        print()
        print(df.loc[start_from:end_at,:])
        ask_user = input('\nWould you like to view more lines? Enter yes or no.')
        if ask_user.lower() != 'yes':
            print()
            print('-'*80)
            print()
            break
        else:
            start_from=end_at + 1
            end_at=start_from + 4


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nEnter the name of the city you want to explore.Possible options -- chicago or newyork or washington  : ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nEnter the month you are interested in.Possible options -- january to june OR all: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nEnter the day of the week.Possible options -- monday to sunday OR all : ').lower()

    print()
    print('-'*80)
    print()

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Decide if stats should be computed based on all days or months
    if(month == 'all'):

        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # display the most common month
        popular_month = df['month'].mode()[0]
        month = months[popular_month - 1]
        print('\nThe most popular month is : {}'.format(month))

    if(day == 'all'):
        # display the most common day of week
        popular_day = df['day_of_week'].mode()[0]
        print('\nThe mostpopular day of week is : {}'.format(popular_day))

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most popular hour is : {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)
    print()


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station is : {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost commonly used end station is : {}'.format(popular_end_station))


    # display most frequent combination of start station and end station trip

    popular_combination = df.groupby(['Start Station','End Station']).size().reset_index(name="Time").sort_values(by='Time',ascending=False).head(1)

    #print('\nMost frequent combination of start and end station trip is :',popular_combination['Time'].to_string(index = False))
    print('\nMost frequent combination of start and end station trip is :')
    print()
    print(popular_combination)
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)
    print()

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Compute start time
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total duration is :',df['Trip Duration'].sum(),'seconds')

    # display mean travel time
    print('\nThe mean duration is :',df['Trip Duration'].mean(),'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)
    print()


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nThe different user types are :')
    print()
    print(df.groupby(['User Type']).size())

    if(city == 'washington'):
        print('\nNo Gender or Year of birth related statistics available for Washington')
    else:
        #popular_combination['Time'].to_string(index = False)

        # Display counts of gender
        print('\nThe gender counts are :')
        print()
        print(df.groupby(['Gender']).size())

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth is : ',int(df['Birth Year'].min()))
        print('\nRecent year of birth is : ',int(df['Birth Year'].max()))
        print('\nCommon year of birth is : ',int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print()
    print('-'*80)
    print()

def main():
    while True:

        city, month, day = get_filters()

        # Check the validity of user input
        is_city_valid = CITY_DATA.get(city)
        is_month_valid = global_months.get(month)
        is_day_valid = global_weekday.get(day)

        #print('\n The values are {},{},{}'.format(is_city_valid,is_month_valid,is_day_valid))

        if( is_city_valid == None or is_month_valid == None or is_day_valid == None  ):
            print('Please verify the inputs.One or more are incorrect')
            break

        ask_user = input('\nWould you like to view lines from {} file? Enter yes or no.'.format(city))
        if ask_user.lower() == 'yes':
            display_lines(city)

        df = load_data(city, month, day)

        #print(df)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
