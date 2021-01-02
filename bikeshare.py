#In this project, we will write Python code to import US bike share data and
# answer interesting questions about it by computing descriptive statistics.
#We will also write a script that takes in raw input to create an interactive
#experience in the terminal to present these statistics.

#1 Popular times of travel 

#most common month
#most common day of week
#most common hour of day

#2 Popular stations and trip

#most common start station
#most common end station
#most common trip from start to end 

#3 Trip duration

#total travel time
#average travel time

#4 User info

#counts of each user type
#counts of each gender (only available for NYC and Chicago)
#earliest, most recent, most common year of birth (only available for NYC and Chicago)

################################################################
import time
import pandas as pd
import numpy as np
######################################################

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
##########################################################

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
##############CITY############    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    
    while city not in CITY_DATA.keys():
        print("\nSELECT A CITY PLEASE!")
        print("\n<1> Chicago \n<2> New York City \n<3> Washington")
        
        #Taking user input and converting into lower 
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nInvalid! \nPlease try again.")
            

    print(f"\nYou chose {city.title()} as your city.") 

###############MONTH###############
    MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    # get user input for month (all, january, february, ... , june) 
    month = ""
    
    while month not in MONTH_DATA:
        print("\nPlease enter a month, between January to June")
        print("\n(You may also view data for all months by entering 'all')")
        
        month = input().lower()

        if month not in MONTH_DATA:
            print("\nInvalid! Please try again.")
           

    print(f"\nYou chose {month.title()} as your month.")
#############DAY##################
    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week you're seeking the data of.")
        print("\n(You may also view data for all days in week by entering 'all')")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid! Please try again.")
           
    print(f"\nYou chose {day.title()} as your day.")
    print(f"\nYou chose to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*40)
    return city, month, day

################################################################
    
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
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

##################################################################
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = January,...,6 = June): {popular_month}")

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    
    popular_hour = df['hour'].mode()[0]

    print(f"\nMost Popular Start Hour: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
################################################################
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station']+"and"+df['End Station']
    combination = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combination}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
######################################################################
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    
    mins, sec = divmod(average_duration, 60)
    #filter if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

######################################################################
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"Counts of user types are w:\n\n{user_type}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nTypes of users by gender are:\n\n{gender}")
        
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#######################################################################
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """
    start = 0
    end = 5

    display_active = input("Do you want to display the raw data?: ").lower()

    if display_active == 'yes':
        while end <= df.shape[0] - 1:

            print(df.iloc[start:end,:])
            start += 5
            end += 5

            end_display = input("Do you wish to continue?: ").lower()
            if end_display == 'no':
                break

    print('-'*40)    
#######################################################################
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
