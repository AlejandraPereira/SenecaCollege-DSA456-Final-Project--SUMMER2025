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
import time 
from datetime import datetime


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


#Create the new_olympic_athlete_bio.csv

def format_athlete_born(athlete_bio_list):
    """
    Formats the birth dates for each athlete in the athlete_bio_file.

    Parameters:
    athlete_bio_list (list): The list containing athlete bio data where birth dates need to be formatted.

    Returns:
    None
    """
    pass

def format_p_athlete_born(paris_athletes_list):
    """
    Formats the birth dates for each athlete in the Paris athletes list.

    Parameters:
    paris_athletes_list (list): The list containing Paris athlete data where birth dates need to be formatted.

    Returns:
    None
    """
    pass

def format_games_dates(games_list):
    pass

def integrate_paris_athletes(paris_athletes, athlete_bio_file):
    """
    Integrates new athletes from the Paris athletes list into the athlete_bio_file list.
    Assigns new unique IDs to any new athletes found.
    Also fills in missing height and weight values for existing athletes.

    Parameters:
    paris_athletes (list): The list of Paris athletes to be integrated.
    athlete_bio_file (list): The existing athlete bio data to which new athletes may be added.

    Returns:
    None
    """
    # First, fill in missing height and weight for existing athletes
    height_idx = col_index(athlete_bio_file[0], "height")
    weight_idx = col_index(athlete_bio_file[0], "weight")
    sex_idx = col_index(athlete_bio_file[0], "sex")
    name_idx_existing = col_index(athlete_bio_file[0], "name")  
    
    if height_idx != -1 and weight_idx != -1 and sex_idx != -1 and name_idx_existing != -1:
        for i in range(1, len(athlete_bio_file)):
            # Convert existing name to title format (First letter capitalized)
            athlete_bio_file[i][name_idx_existing] = athlete_bio_file[i][name_idx_existing].title()

            height = athlete_bio_file[i][height_idx].strip()
            weight = athlete_bio_file[i][weight_idx].strip()
            sex = athlete_bio_file[i][sex_idx].strip()

            # Add height if missing
            if not height:
                if sex.lower() == 'male':
                    athlete_bio_file[i][height_idx] = "175"
                elif sex.lower() == 'female':
                    athlete_bio_file[i][height_idx] = "165"
                else:
                    athlete_bio_file[i][height_idx] = "170"

            # Add weight if missing
            if not weight:
                if sex.lower() == 'male':
                    athlete_bio_file[i][weight_idx] = "75"
                elif sex.lower() == 'female':
                    athlete_bio_file[i][weight_idx] = "65"
                else:
                    athlete_bio_file[i][weight_idx] = "70"

    # Now integrate Paris athletes
    # Use correct column names from Paris CSV
    code_idx = col_index(paris_athletes[0], "code")
    name_idx = col_index(paris_athletes[0], "name")
    dob_idx = col_index(paris_athletes[0], "birth_date")
    paris_sex_idx = col_index(paris_athletes[0], "gender")
    country_idx = col_index(paris_athletes[0], "country")
    country_code_idx = col_index(paris_athletes[0], "country_code")

    # Check if columns exist
    if name_idx == -1 or dob_idx == -1 or paris_sex_idx == -1:
        print(f"Warning: Could not find required columns in Paris data")
        return


    # Create a set of existing athlete identifiers for fast lookup
    existing_athlete_identifiers = set()
    name_idx_existing = col_index(athlete_bio_file[0], "name")
    dob_idx_existing = col_index(athlete_bio_file[0], "born")
    for row in athlete_bio_file[1:]:
        existing_athlete_identifiers.add((row[name_idx_existing].strip().lower(), row[dob_idx_existing].strip()))

    added_count = 0
    for i in range(1, len(paris_athletes)):
        # Convert existing name to title format (First letter capitalized)
        code = paris_athletes[i][code_idx].strip()
        name = paris_athletes[i][name_idx].strip().title()
        dob = paris_athletes[i][dob_idx].strip()
        sex = paris_athletes[i][paris_sex_idx].strip()
        country = paris_athletes[i][country_idx].strip() if country_idx != -1 else ""
        country_noc = paris_athletes[i][country_code_idx].strip() if country_code_idx != -1 else ""

        # Skip if already in bio file using the optimized is_duplicate_athlete
        if is_duplicate_athlete([name, dob], existing_athlete_identifiers):
            continue

        # Add reasonable placeholder values for height and weight based on gender
        if sex.lower() == 'male':
            height = "175"  # Average male height in cm
            weight = "75"   # Average male weight in kg
        elif sex.lower() == 'female':
            height = "165"  # Average female height in cm
            weight = "65"   # Average female weight in kg
        else:
            height = "170"  # Default height
            weight = "70"   # Default weight

        new_row = [code, name, sex, dob, height, weight, country, country_noc]
        athlete_bio_file.append(new_row)

# Create the new_olympic_athlete_events_result.csv 

def create_teams_dict(teams):
    """
    Creates a dictionary mapping event IDs to team sport details.

    Args:
        teams (list): List containing team data rows.

    Returns:
        dict: A dictionary where keys are event IDs and values are dictionaries with team info and athlete codes.
    """
    teams_dict = {}
    for row in teams[1:]:
        event_id = row[9]              
        athletes_codes = row[12]       
        teams_dict[event_id] = {
            "isTeamSport": "True",
            "team": row[2],           
            "athletes_codes": athletes_codes
        }
    return teams_dict

def calculate_next_edition_id(athlete_event_file):
    """
    Calculates the next available edition ID based on existing data.

    Args:
        athlete_event_file (list): List of existing athlete event result rows.

    Returns:
        str: The next available edition ID as a string.
    """

    edition_ids = set()
    edition_id_idx = col_index(athlete_event_file[0], "edition_id")
    for row in athlete_event_file[1:]:
        if row[edition_id_idx].isdigit():
            edition_ids.add(int(row[edition_id_idx]))
    
    # Handle case where no edition IDs are found
    if not edition_ids:
        return "1"
    
    return str(max(edition_ids) + 1)

def create_athlete_birth_dict(athlete_bio_list):
    """
    Generates a dictionary mapping athlete IDs to their birth dates.

    Parameters:
        athlete_bio_list (list): A list of lists, where the first row is the header
        and the remaining rows contain athlete bio data.
        Each row must include 'athlete_id' and 'born' fields.
    Limitations:
        If 'born' is missing or incorrectly formatted, the value is stored as None.                        
    Returns:
        dict: A dictionary where keys are athlete IDs (as strings) and values are
        birth dates as datetime objects. If a birth date is invalid or missing,
        the value will be None.
    """
    birth_dict = {}
    is_header = True  # Flag to track the header
    
    for row in athlete_bio_list:
        if is_header:
            #Find the index of relevant columns in the header
            id_index = row.index("athlete_id")
            birth_index = row.index("born")
            is_header = False
            continue 

        athlete_id = row[id_index] # Get athlete ID from the row
        birth_str = row[birth_index] # Get birth date from the row

        try:
            birth_date = datetime.strptime(birth_str, "%d-%b-%Y")
        except Exception:
            birth_date = None

        birth_dict[athlete_id] = birth_date

    return birth_dict

def create_games_start_dates_dict(games_list):
    """
    Creates a dictionary mapping edition IDs to their start and end dates.

    Parameters:
        games_list (list): List containing Olympic games data rows, 
        where the first row is the header.
    Limitations:
        - If the date format is incorrect or missing, the function will assign (None, None) as the value.
    Returns:
        dict: Keys are edition IDs (str), and values are tuples 
        of (start_date, end_date) as datetime objects. 
        If the date parsing fails, the tuple will be (None, None).
    """
    start_dates_dict = {}
    is_header = True  # Flag to track the header
    
    for row in games_list:
        if is_header:
            # Find the index of relevant columns in the header
            edition_id_index = row.index("edition_id")
            competition_date_index = row.index("competition_date")
            is_header = False
            continue 
        edition_id = row[edition_id_index]  # Get edition ID from the row
        competition_date_str = row[competition_date_index]  # Get competition date range string

        try:
            # Split range into start and end date strings
            start_str, end_str = competition_date_str.split(" to ")
        
            start_date = datetime.strptime(start_str.strip(), "%d-%b-%Y")
            end_date = datetime.strptime(end_str.strip(), "%d-%b-%Y")
        except Exception:
            start_date = None
            end_date = None
        # Save tuple (start_date, end_date) in dictionary
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

    #age calculation based on year difference
    age = start_date.year - birth_date.year

    # if the athlete's birthday in the event's start year
    birthday_this_year = birth_date.replace(year=start_date.year)

    # If the event starts before the athlete's birthday, subtract 1
    if start_date < birthday_this_year:
        age -= 1

    # Check if the athlete's birthday occurs during the event
    birthday_during_event = start_date <= birthday_this_year <= end_date

    return str(age) 

def clean_pos(pos_value):
    """
    Validates and cleans a position value.
    Parameters:
        pos_value (str): The position value to validate.
    Returns:
        str: The original position if it is a digit or one of the
             accepted codes ("DNF", "DNS"), otherwise an empty string.
    """
    if pos_value.isdigit() or pos_value in ("DNF", "DNS"):
        return pos_value
    else:
        return ""

def clean_all_positions(athlete_event_file):
    """
    Cleans the 'pos' column values in the athlete_event_file.

    It iterates through all rows (except the header) and updates
    the 'pos' field to ensure only valid position values remain.
    Valid values are digits or specific codes like "DNF" or "DNS".
    Any invalid value is replaced with an empty string.
    Parameters:
        athlete_event_file (list): Existing athlete event result data.
    Returns:
        None: The function modifies the list in place.
    """
    pos_idx = athlete_event_file[0].index("pos")
    for row in athlete_event_file[1:]: 
        row[pos_idx] = clean_pos(row[pos_idx])

def process_medals_and_update_file( athlete_event_file, paris_medallists, teams_dict, next_edition_id, athlete_birth_dict, games_start_dates_dict):
    """
    Updates athlete event results by appending processed Paris medallists data.
    Adds an 'age' column if missing, formats athlete names, identifies team sports,
    normalizes medal and position values, calculates athlete ages, and avoids duplicates.
    Also calculates age for all existing rows (all editions).
    Parameters: 
        athlete_event_file (list): Existing athlete event result data to be updated.
        paris_medallists (list or None): List containing Paris medallists data or None.
        teams_dict (dict): Dictionary containing team sport information.
        next_edition_id (str or None): The edition ID to assign for the Paris 2024 data.
        athlete_birth_dict (dict): Dictionary mapping athlete_id to birth date.
        games_start_dates_dict (dict): Dictionary mapping edition_id to games start date.
    Returns:
        None
    """
    # Ensure Paris 2024 dates exist and are not None
    if '63' not in games_start_dates_dict or None in games_start_dates_dict['63']:
        games_start_dates_dict['63'] = (
            datetime.strptime('26-Jul-2024', '%d-%b-%Y'),
            datetime.strptime('11-Aug-2024', '%d-%b-%Y')
        )

    # Add "age" column to existing data if missing
    header = athlete_event_file[0]
    if "age" not in header:
        header.append("age")
        for row in athlete_event_file[1:]:
            row.append("")

    # Get important column indexes from existing data
    edition_id_idx = header.index("edition_id")
    athlete_id_idx = header.index("athlete_id")
    age_idx = header.index("age")

    # Calculate age for all existing rows based on birth date and games start date
    for row in athlete_event_file[1:]:
        edition_id = row[edition_id_idx]
        athlete_id = row[athlete_id_idx]
        birth_date = athlete_birth_dict.get(athlete_id)
        start_date, end_date = games_start_dates_dict.get(edition_id, (None, None))
        if birth_date and start_date and end_date:
            row[age_idx] = calculate_age(birth_date, start_date, end_date)
        else:
            row[age_idx] = ""

    # If no Paris data or no edition ID provided, stop here
    if not paris_medallists or not next_edition_id:
        return

    # Create a set of unique (athlete_id, event) pairs to avoid duplicates when adding new data
    unique_entries = set(
        (row[athlete_id_idx], row[header.index("event")] if "event" in header else "")
        for row in athlete_event_file[1:]
    )

    # Get indexes from Paris medallists header
    medallist_header = paris_medallists[0]
    idx_country_noc = col_index(medallist_header, "country_code")
    idx_sport = col_index(medallist_header, "discipline")
    idx_event = col_index(medallist_header, "event")
    idx_athlete_name = col_index(medallist_header, "name")
    idx_athlete_id = col_index(medallist_header, "code_athlete")
    idx_medal = col_index(medallist_header, "medal_type")

    # Process each Paris medallist row
    for medallist in paris_medallists[1:]:
        edition = "2024 Summer Olympics"
        edition_id = str(next_edition_id).strip()

        country_noc = medallist[idx_country_noc]
        sport = medallist[idx_sport]
        event = medallist[idx_event]
        athlete_id = medallist[idx_athlete_id]
        medal = medallist[idx_medal]

        # Format athlete name to title case
        athlete_name = medallist[idx_athlete_name].title()

        is_team_sport = "False"
        if event in teams_dict:
            is_team_sport = "True"
            if athlete_id not in teams_dict[event]["athletes_codes"]:
                continue  # Skip if athlete not on the team

        unique_key = (athlete_id, event)
        if unique_key in unique_entries:
            continue
        unique_entries.add(unique_key)
        
        if medal in ["Gold Medal", "Gold"]:
            medal = "Gold"
        elif medal in ["Silver Medal", "Silver"]:
            medal = "Silver"
        elif medal in ["Bronze Medal", "Bronze"]:
            medal = "Bronze"

        # Set position based on medal type
        if medal == "Gold":
            pos = "1"
        elif medal == "Silver":
            pos = "2"
        elif medal == "Bronze":
            pos = "3"
        else:
            pos = ""

        result_id = ""

        birth_date = athlete_birth_dict.get(athlete_id)
        start_date, end_date = games_start_dates_dict.get(edition_id, (None, None))
        age = calculate_age(birth_date, start_date, end_date) if birth_date and start_date else ""

        # Build the new result row and append it
        new_result = [
            edition,
            edition_id,
            country_noc,
            sport,
            event,
            result_id,
            athlete_name,
            athlete_id,
            pos,
            medal,
            is_team_sport,
            age
        ]

        athlete_event_file.append(new_result)

def col_index(header, col_name):
    """
    Returns the index of a column by its name from the header list.

    Args:
        header (list): The header row of a CSV file.
        col_name (str): The column name to search for.

    Returns:
        int: The index of the column if found, -1 otherwise.
    """

    try:
        return header.index(col_name)
    except ValueError:
        return -1

def is_duplicate_athlete(new_athlete_row, existing_data):
    """
    Checks whether a new athlete already exists in the existing dataset.

    Args:
        new_athlete_row (list): The new athlete's data row.
        existing_data (list): The current athlete bio dataset.

    Returns:
        bool: True if the athlete already exists, False otherwise.
    """

    name_idx = col_index(existing_data[1], "name")
    dob_idx = col_index(existing_data[0], "born")
    new_name = new_athlete_row[0].strip().lower()
    new_dob = new_athlete_row[1].strip()

    for row in existing_data[1:]:
        if row[name_idx].strip().lower() == new_name and row[dob_idx].strip() == new_dob:
            return True
    return False

def get_max_id(data, id_col):
    """
    Finds the maximum numeric ID in the given dataset based on column index.

    Args:
        data (list): Dataset including header.
        id_col (int): Index of the ID column.

    Returns:
        int: The maximum numeric ID found.
    """

    max_id = 0
    for i, row in enumerate(data):
        if i == 0:
            continue  # skip header
        try:
            max_id = max(max_id, int(row[id_col]))
        except ValueError:
            continue
    return max_id 

def mergeGamesData(games_file, paris_data):
    """
    Prototype function for merging Olympic games data.

    Parameters:
    - games_file: List of original Olympic games
    - paris_data: Placeholder list for Paris games

    Returns:
    - List: Merged data list (currently just original)
    """

    existing_ids = set()
    edition_id_idx = col_index(games_file[0], "edition_id")

    for row in games_file[1:]:
        existing_ids.add(row[edition_id_idx])

    merged_games = games_file[:]
    for row in paris_data[1:]: # skip header
        if row[edition_id_idx] not in existing_ids:
            merged_games.append(row)
        existing_ids.add(row[edition_id_idx])

    return merged_games

def integrate_paris_countries(original_countries, paris_nocs):
    """
    Integrates new or updated country (NOC) information from the Paris data into the original countries list.

    Args:
        original_countries (list): List of lists containing the existing countries data (from olympics_country.csv).
        paris_nocs (list): List of lists containing NOC (country) information from the Paris 2024 data (from nocs.csv).

    Returns:
        list: Updated list of countries, ready to be written to new_olympics_country.csv.
    """
    existing_nocs = set()
    noc_idx = col_index(original_countries[0], "noc")
    updated_countries = original_countries[:]

    for row in original_countries[1:]:
        existing_nocs.add(row[noc_idx])

    for row in paris_nocs[1:]:  # skip header
        if row[0] not in existing_nocs:
            # Add only first two columns (noc, country)
            updated_countries.append([row[0], row[1]])
            existing_nocs.add(row[0])

    # Sort the data by country name (second column), but keep header first
    header = updated_countries[0]
    data_rows = sorted(updated_countries[1:], key=lambda x: x[1])
    return [header] + data_rows

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
