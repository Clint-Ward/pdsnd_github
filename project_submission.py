import pandas as pd
import numpy as np
import time
#define dictionaries
city_set=('washington', 'new york city', 'chicago')
day_set=('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')
month_set=('january' ,'february' , 'march' , 'april' , 'may' , 'june' , 'july' , 'august' , 'september' ,
           'october' , 'november' , 'december', 'all')
day_lookup={'monday':1, 'tuesday':2, 'wednesday':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7, 'all': 'all'}
month_lookup={'january':1 ,'february':2 , 'march':3 , 'april':4 , 'may':5 , 'june':6 , 'july':7 , 'august':8 , 'september':9 ,
           'october':10 , 'november':11 , 'december':12, 'all': 'all'}
CITY_DATA={ 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAY_DATA={ 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday' }
MONTH_DATA={1:  'January' , 2:  'February' , 3:  'March' , 4:  'April' , 5:  'May' , 6:  'June' , 7:  'July' , 
            8:  'August' , 9:  'September' , 10:  'October' , 11:  'November' , 12:  'December' }
#Fuctions
def get_filters():
    # input city
    while True:
        try:
            city_input = (input("Hello World! ;) Welcome to BykShare, your Bike Share analysis tool! \
            Please select a city from Chicago, New York City or Washington")).lower() 
            if city_input in city_set:
                print('Thanks!')
                break;
            else:
                print('Please try again, that city isn\'t in our database...')
        except:
            continue

    while True:
        try:
            month_input = (input("Please input the name of the month to filter by, or ""all"" to apply no month filter")).lower() 
            if month_input in month_set:
                print('Thanks!')
                break;
            else:
                print('Please try again, we don\'t have data for that month...')
        except:
            continue

    while True:
        try:
            day_input = (input("Please input the day to filter by, or ""all"" to apply no day filter")).lower() 
            if day_input in day_set:
                print('Thanks!')
                break;
            else:
                print('Please try again, we don\'t have data for that day...')
        except:
            continue
    print('-'*40)
    city=city_input
    month=month_lookup[month_input]
    day=day_lookup[day_input]
    return city, month, day

def load_data(city, month, day):
    # Load csv directly into Pandas DataFrame
    t1 = pd.read_csv(CITY_DATA[city])
    # Change Date and Time fields from Object to Date time 
    t1['Start Time'] = pd.to_datetime(t1['Start Time'])
    t1['End Time'] = pd.to_datetime(t1['End Time'])
    # Create the Month, Day, and Hour fields for later analysis for Times of travel
    t1['Weekday'] = t1['Start Time'].dt.weekday
    t1['Month'] = t1['Start Time'].dt.month
    t1['Hour'] = t1['Start Time'].dt.hour
    #Filter the data
    if month=='all' and day=='all':
        df=t1
    elif month=='all' and day!='all':
        df=t1.loc[(t1.Weekday == day)]
    elif month!='all' and day=='all':    
        df=t1.loc[(t1.Month == month)]
    else:    
        df=t1.loc[(t1.Weekday == day) & (t1.Month == month)]
    return df

def view_5_lines(df):
    response=(input('Would you like to see the first 5 lines of the database? Enter Yes or No.')).lower()
    i=0
    while response=='yes':
        print(df.iloc[i:i+5])
        response=(input('Continue to see the next 5 lines of the database? Enter Yes or No.')).lower()
        if response=='no': break
        i+=5 
        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Month_word'] = df['Month'].map(MONTH_DATA)
    print('Bikesharing occurs most commonly in '+df['Month_word'].mode().values)

    # TO DO: display the most common day of week
    df['Day_word'] = df['Weekday'].map(DAY_DATA)
    print('Bikesharing occurs most commonly on '+df['Day_word'].mode().values)

    # TO DO: display the most common start hour
    print('Bikesharing start most commonly at '+str(int(df['Hour'].mode())) +'H00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Bikesharing is initiated most commonly from '+df['Start Station'].mode().values)

    # TO DO: display most commonly used end station
    print('Bikesharing ends most commonly at '+df['End Station'].mode().values)

    # TO DO: display most frequent combination of start station and end station trip
    print('The most common journey however is starting at ' +(df['Start Station']+' and ending at '+df['End Station']).mode().values)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The total time spent on shared bikes is '+str(int(df['Trip Duration'].sum()//(60*60*24*7*52)))+' year(s), '+
    str(int((df['Trip Duration'].sum()%(60*60*24*7*52))//(60*60*24*7*52/12)))+' month(s), '+
    str(int((df['Trip Duration'].sum()%(60*60*24*7*52))%(60*60*24*7*52/12))//(60*60*24*7))+' week(s), '+
    str(int((((df['Trip Duration'].sum()%(60*60*24*7*52))%(60*60*24*7*52/12))%(60*60*24*7))//(60*60*24)))+' day(s), '+
    str(int(((((df['Trip Duration'].sum()%(60*60*24*7*52))%(60*60*24*7*52/12))%(60*60*24*7))%(60*60*24))//(3600)))+' hour(s), '+
    str(int((((((df['Trip Duration'].sum()%(60*60*24*7*52))%(60*60*24*7*52/12))%(60*60*24*7))%(60*60*24))%(3600))//60))+' minute(s) and '+
    str(int((((((df['Trip Duration'].sum()%(60*60*24*7*52))%(60*60*24*7*52/12))%(60*60*24*7))%(60*60*24))%(3600))%60))+' seconds! \
    Thats assuming a 365 day year though ;)')

    # TO DO: display mean travel time
    print('The average trip duration is '+str(int(df['Trip Duration'].mean()//60))+' minutes and '+
      str(int(df['Trip Duration'].mean()%60))+' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())
    else:
        print('Sorry, data of this type is not captured for this city')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('Sorry, gender data is not captured for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The most senior bike sharer was born in '+str(int(df['Birth Year'].min()))+', the most junior in '+
            str(int(df['Birth Year'].max()))+', with the most common birth year being '+str(int(df['Birth Year'].mean()))+'.')
    else:
        print('Sorry, birth year data is not captured for this city')    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        view_5_lines(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


