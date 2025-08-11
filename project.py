# Feel free to add additional python files to this project and import
# them in this file. However, do not change the name of this file
# Avoid the names ms1check.py and ms2check.py as those file names
# are reserved for the autograder

# To run your project use:
#     python runproject.py

# This will ensure that your project runs the way it will run in the
# the test environment


# supports the use of csv library
import csv



# This function reads a csv file and return a list of lists
# each element of the returned list is a row in the csv file
# The first row is the header row
def read_csv_file(file_name):
    data_set = []
    with open(file_name, mode='r', encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data_set.append(row)
    return data_set

# This function writes out a list of lists to a csv file
# each element of the list is a row in the csv file
# The first row is the header row
def write_csv_file(file_name, data_set):
    with open(file_name, mode='w', newline='', encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file)
        for row in data_set:
            csv_writer.writerow(row)

def create_athlete_birth_dict(new_athlete_bio_data):
    """
    Generates a dictionary mapping athlete IDs to their birth dates
    from the new Olympic athlete bio data file.

    Parameters:
        new_athlete_bio_data (list): A list of lists where the first row is the header,
                                     and subsequent rows contain athlete bio data.
                                     Must include 'athlete_id' and 'born' columns.

    Returns:
        dict: Keys are athlete IDs (str), values are birth dates as datetime objects.
              If 'born' is missing or incorrectly formatted, the value is None.
    """
    birth_dict = {}
    is_header = True
    for row in new_athlete_bio_data:
        if is_header:
            id_index = row.index("athlete_id")
            born_index = row.index("born")
            is_header = False
            continue
        
        athlete_id = row[id_index]
        born_str = row[born_index]
        
        try:
            birth_date = datetime.strptime(born_str, "%d-%b-%Y")
        except Exception:
            birth_date = None
        
        birth_dict[athlete_id] = birth_date
    
    return birth_dict

def create_games_start_dates_dict(games):
    """
    Creates a dictionary mapping edition IDs to their start and end dates.
    Parameters:
        games_list: List containing Olympic games data rows,
        where the first row is the header.
    Returns:
        dict: Keys are edition IDs (str), and values are tuples 
        of (start_date, end_date) as datetime objects. 
        If parsing fails, the tuple will be (None, None).
    """
    start_dates_dict = {}
    is_header = True
    
    for row in games:
        if is_header:
            edition_id_index = row.index("edition_id")
            start_date_index = row.index("start_date")
            end_date_index = row.index("end_date")
            is_header = False
            continue

        edition_id = row[edition_id_index]

        try:
            start_date = datetime.strptime(row[start_date_index], "%d-%b-%Y")
            end_date = datetime.strptime(row[end_date_index], "%d-%b-%Y")
        except Exception:
            start_date = None
            end_date = None
    
        start_dates_dict[edition_id] = (start_date, end_date)
        
    return start_dates_dict

def calculate_age(birth_date, start_date, end_date):
    """
    Calculates the age of an athlete at the time of a sporting event.
    Parameters:
        birth_date (datetime or None): The athlete's date of birth.
        start_date (datetime or None): The start date of the event.
        end_date (datetime or None): The end date of the event.
    Limitations:
        If any of the three parameters is None, the function returns an empty string.   
    Returns:
        str: The athlete's age at the start of the event as a string, 
        or an empty string if any of the dates are missing.
    """
    if not birth_date or not start_date or not end_date:
        return ""

    # Age calculation based on year difference
    age = start_date.year - birth_date.year

    # Try to replace year in birth_date; handle Feb 29 in non-leap years
    try:
        birthday_this_year = birth_date.replace(year=start_date.year)
    except ValueError:
        # If birth_date is Feb 29 and start_date.year is not leap, use Feb 28
        birthday_this_year = birth_date.replace(year=start_date.year, day=28)

    # If the event starts before the athlete's birthday, subtract 1
    if start_date < birthday_this_year:
        age -= 1

    return str(age)


def create_noc_dict(countries_data):
    """
    Creates a dictionary mapping NOC codes to country names.
    Parameters:
        countries_data (list): A list of lists representing country data
    Returns:
        dict: A dictionary with NOC codes as keys (strings) and country names as values (strings).
    """
    noc_to_country = {}
    for i, row in enumerate(countries_data):
        if i == 0:  # Skip header row
            continue
        noc = row[0]
        country_name = row[1]
        noc_to_country[noc] = country_name
    return noc_to_country

def process_medal_tally(athletes_data):
    """
    Processes athlete event data to compute medal tallies by edition and country.
    Parameters:
        athletes_data (list): List of athlete event rows, including headers.
    Limitations:
        Assumes that the data contains the expected columns at the specified indexes.
        Does not aggregate medals beyond the scope of edition and country.
        Athlete IDs are used only to count unique athletes per country and edition.
    Returns:
        dict: Nested dictionary with medal counts and athlete IDs per edition and NOC.
    """
    medal_tally = {}
    for i, row in enumerate(athletes_data):
        if i == 0:  # Skip header row
            continue
        edition_name = row[0]
        edition_id = row[1]
        country_noc = row[2]
        athlete_id = row[7]
        medal = row[9]

        # Initialize the edition in the medal tally if not present
        if edition_name not in medal_tally:
            medal_tally[edition_name] = {}

        # Initialize the country data for this edition if not present
        if country_noc not in medal_tally[edition_name]:
            medal_tally[edition_name][country_noc] = {
                'edition_id': edition_id,
                'athletes': set(),
                'gold': 0,
                'silver': 0,
                'bronze': 0
            }
        # Count medals
        if medal == 'Gold':
            medal_tally[edition_name][country_noc]['gold'] += 1
        elif medal == 'Silver':
            medal_tally[edition_name][country_noc]['silver'] += 1
        elif medal == 'Bronze':
            medal_tally[edition_name][country_noc]['bronze'] += 1

        # Track unique athlete IDs for each country and edition
        medal_tally[edition_name][country_noc]['athletes'].add(athlete_id)
    return medal_tally

def generate_summary_data(medal_tally, noc_to_country):
    """
    Creates a summary table of medals by Olympic edition and country.
    Parameters:
        medal_tally (dict): Medal data organized by edition and NOC, including medal counts and athletes.
        noc_to_country (dict): Maps NOC codes to full country names.
    Limitations:
        Assumes all required keys ('edition_id', 'gold', 'silver', 'bronze', 'athletes') are present in data.
    Returns:
        list: Summary data as rows, starting with a header. Each row includes edition, country, NOC, athlete count, and medal counts.
    """
    summary_data = []
    header = [
        "edition", "edition_id", "Country", "NOC",
        "number_of_athletes", "gold_medal_count", "silver_medal_count",
        "bronze_medal_count", "total_medals"
    ]
    summary_data.append(header)

    # Iterate through medal tally to build the summary rows
    for edition_name, countries in medal_tally.items():
        for country_noc, data in countries.items():
            edition_id = data['edition_id']
            country_name = noc_to_country.get(country_noc, "Unknown")
            num_athletes = len(data['athletes'])
            gold = data['gold']
            silver = data['silver']
            bronze = data['bronze']
            total = gold + silver + bronze

            summary_data.append([
                edition_name, edition_id, country_name, country_noc,
                num_athletes, gold, silver, bronze, total
            ])
    return summary_data


# This main function is the function that the runner will call
# The function prototype cannot be changed

def main():
    # example to read the csv file
    athlete_bio_file = read_csv_file("olympic_athlete_bio.csv")
    paris_athletes = read_csv_file("paris/athletes.csv")
    # example to write the data back from csv file
    format_athlete_born(athlete_bio_file)
    format_p_athlete_born(paris_athletes)
    integrate_paris_athletes(paris_athletes, athlete_bio_file)
    write_csv_file("new_olympic_athlete_bio.csv",athlete_bio_file)
 
    # new_olympics_games.csv
    games_file = read_csv_file("olympics_games.csv")
    format_games_dates(games_file)
    games_start_dates_dict = create_games_start_dates_dict(games_file)
    paris_games = []
    merged_games = mergeGamesData(games_file, paris_games)
    write_csv_file("new_olympics_games.csv", merged_games)
 
    #new_olympic_athlete_events_result.csv
 
    #Read event and medallist files
    athlete_event_file = read_csv_file("olympic_athlete_event_results.csv")
    paris_medallists = read_csv_file("paris/medallists.csv")
    events = read_csv_file("paris/events.csv")  
    teams = read_csv_file("paris/teams.csv")
 
    #Read the updated bio and games files
    games= read_csv_file("new_olympics_games.csv")
    new_athlete_bio_data= read_csv_file("new_olympic_athlete_bio.csv")
    
    #Create the dicctionaries
    next_edition_id = calculate_next_edition_id(athlete_event_file)
    teams_dict = create_teams_dict(teams)
    new_athlete_bio_data = read_csv_file("new_olympic_athlete_bio.csv")
    athlete_birth_dict = create_athlete_birth_dict(new_athlete_bio_data)
    games_start_dates_dict = create_games_start_dates_dict(games)
    
    #Process medallists and update the event file
    process_medals_and_update_file(athlete_event_file, paris_medallists, teams_dict, next_edition_id, athlete_birth_dict, games_start_dates_dict)
    clean_all_positions(athlete_event_file)
 
    #Write out the updated athlete event results file
    write_csv_file("new_olympic_athlete_event_results.csv", athlete_event_file)
 
    #Read original country file and Paris NOC data
    original_countries = read_csv_file("olympics_country.csv")
    paris_nocs = read_csv_file("paris/nocs.csv")
    
    #Integrate and write updated country data
    new_country_data = integrate_paris_countries(original_countries, paris_nocs)
    write_csv_file("new_olympics_country.csv", new_country_data)
 
    #new_medal_tally.csv
    new_athlete_event_file = read_csv_file("new_olympic_athlete_event_results.csv")
    countries_file = read_csv_file("new_olympics_country.csv")
 
    noc_to_country = create_noc_dict(countries_file)
    medal_tally = process_medal_tally(new_athlete_event_file)
    summary_data = generate_summary_data(medal_tally, noc_to_country)
 
    write_csv_file("new_medal_tally.csv", summary_data)
