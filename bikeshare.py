import time
import pandas as pd
import datetime


CITY_DATA = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}

# city_chosen defined globaly becasue its used in user_stats function
# to check if the city is 'Washington' to print no gender and birth data for it
city_chosen=" "


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city_chosen
    city_chosen= input('Please specify the city you want to get some insights about: Chicago, New York or Washington ').strip()
    city_chosen = city_chosen.title()
    while city_chosen not in ('Chicago', 'New York', 'Washington'):
        city_chosen = input('No available data for the city entered, please choose between: Chicago, New York or Washington ')
        city_chosen = city_chosen.title()

    # get user input for month (all, january, february, ... , june)
    month_chosen = input('Please specify the month you want to get some insights about: (January, February, ... , June)\nIf you have no preference at all please enter All ').strip()
    month_chosen = month_chosen.title()
    while month_chosen not in ('All', 'January', 'February', 'March', 'April', 'May', 'June'):
        month_chosen = input('No available data for the month entered, please choose in: (January, February, ... , June) or All if you have no preference ')
        month_chosen = month_chosen.title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_chosen = input('Please specify the day of week you want to get some insights about: (Monday, Tuesday, ... Sunday)\nIf you have no preference at all please enter All ').strip()
    day_chosen = day_chosen.title()
    while day_chosen not in ('All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
        day_chosen = input('Please enter a valid name of the week, choose between: (Monday, Tuesday, ... Sunday) or All if you have no preference ')
        day_chosen = day_chosen.title()

    # output message
    print('-' * 40)
    print('A wise choice, {} is so cool!\nlet me look this up for you!'.format(city_chosen, month_chosen, day_chosen))
    print('-' * 40)
    time.sleep(3)
    return city_chosen, month_chosen, day_chosen


def load_data(city, month, day):
    """
    Loads data for the specified city, month and day (if specified or all if nothing specified)

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    file_name= CITY_DATA[city]
    data = pd.read_csv(file_name)

    # convert the Start Time column to datetime
    data['Start Time'] = pd.to_datetime(data['Start Time'])

    # extract month and day of week from Start Time to create new columns
    data['Month'] = data['Start Time'].dt.month_name()
    data['Day'] = data['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        data= data[data['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'All':
        data = data[data['Day'] == day.title()]

    return data


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (DataFrame) df - filtered DataFrame as requested from user
    """

    print('\nSome useful insights about the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most popular Month for traveling: {}'.format(popular_month))

    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print('The most popular Day for traveling: {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular Hour for traveling: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    time.sleep(3)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nSome useful insights about the most popular stations and trips...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station for traveling: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station for traveling: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most popular combination of start station and end station for traveling: {} with {}'.format(popular_combination[0], popular_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    time.sleep(3)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nSome useful insights about trip durations...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_formatted=str(datetime.timedelta(seconds=int(total_travel_time)))
    print('The total travel time: {}'.format(total_travel_formatted))

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    average_travel_formatted=str(datetime.timedelta(seconds=int(average_travel_time)))
    print('The average travel time: {}'.format(average_travel_formatted))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    time.sleep(3)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_data_count = df['User Type'].value_counts()
    print('The different types of users count:\n{}\n'.format(user_data_count.to_string()))

    if city_chosen != 'Washington':
        # Gender count
        gender_count = df['Gender'].value_counts()
        print('The gender count:\n{}\n'.format(gender_count.to_string()))

        # Earliest year of birth
        earliest = df['Birth Year'].min()
        print('The earlist year of birth: {}'.format(int(earliest)))

        # Most recent year of birth
        recent = df['Birth Year'].max()
        print('The most recent year of birth: {}'.format(int(recent)))

        # Most common year of birth
        common = df['Birth Year'].mode()[0]
        print('The most common year of birth: {}'.format(int(common)))

    else:
        print('Washington has no gender and birth year data!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    time.sleep(3)


def raw_data(df):
    x, y= 0, 5
    while True:
        show_data = input("\nWould you like to view individual trip data? please type 'yes' or 'No'.\n")
        if show_data.lower() == 'yes':
            print(df[x:y])
            x= y
            y+= 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or anything else to exit the program.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
