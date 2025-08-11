# Milestone 2 Analysis

## Describe the assumptions and decisions you made

To reconcile the Paris 2024 Olympic data with the existing datasets, we made key assumptions and decisions to ensure consistency and accuracy:

Matching Athletes: We matched athletes from the Paris data using athlete_id. If a Paris athlete did not exist in the original bio file, we treated them as a new athlete and added them accordingly, avoiding duplicates.

Name Formatting: Names in the Paris dataset were originally in all uppercase. We standardized them to title case to match the formatting of existing records.

Birth Dates and Age Calculation: Birth dates follow the format dd-Mon-yyyy. In order to calculate the age of athletes during the Paris Games, we needed the edition’s start date. Since the Paris edition data did not originally include this information, we manually inserted the correct start date for the 2024 Paris Olympics. If an athlete's birth date was missing or invalid, we left the age field as an empty string ("").

Competition Dates: Competition date ranges follow the format dd-Mon-yyyy to dd-Mon-yyyy.

Result ID: The Paris dataset did not include result_id values (which represent medals or placements). As a result, we left the result_id field as an empty string ("") for all Paris athlete records.

Incomplete Athlete Profiles: If an athlete’s height or weight was missing, we imputed it using the average for their gender based on available data.

New Edition and Country Entries: We incremented the latest edition_id to represent the Paris 2024 Games and ensured any new countries present in the Paris dataset were also added to the countries.csv file if not already there.

## Data structures used

Our application uses built-in Python data structures for all data manipulation. These include:

- **List of Lists (list):**  

Used for storing CSV file data.
Each dataset (e.g., athlete_bio_file, paris_athletes) is represented as a list of rows, and each row is a list of string values.

- **Dictionaries (`dict`)**

To optimize searches and quickly access specific data, dictionaries are created that map unique keys to important values. Some examples are:

    - `athlete_birth_dict`: `athlete_id` key, `datetime` value.
    - `games_start_dates_dict`: `edition_id` key, tuple value with the event's start and end date.
    - `noc_to_country`: NOC code key, country name value.
    - `medal_tally`: Nested dictionary to aggregate medals per edition and NOC.

- **Additional Python methods used**

The application also uses built-in Python functions and methods to simplify data handling and improve readability. Some examples include range() and enumerate() for loops, string methods like strip(), title(), and lower() for text processing, set() for managing unique values, try-except blocks for error handling, and datetime.strptime() for date parsing. These are just a few of the many Python features applied to keep the code clean and efficient.

## General Data Manipulation

- **Read input CSV files** into list-of-lists using `read_csv_file`.  
- **Clean & Integrate data:**  
  - Format names and birth dates. 
  - Format the competition date range 
  - Fill missing height/weight based on gender.  
  - Integrate new athletes while checking for duplicates.  
  - Add new games and countries if not already present.
  - Assign athlete positions based on medals won, or mark as "DNS" (Did Not Start) or "DNF" (Did Not Finish).
  - Validate and handle invalid or missing dates (e.g., accounting for leap years like Feb 29).
  - Normalize athlete name casing (e.g., from ALL CAPS to Proper Case) in paris/athlete.csv olympic_athlete_event_result.csv and olympic_athlete_bio.csv and 

- **Transform:**  
  - Calculate ages based on event start dates.  
  - Normalize medal/position values.  
- **Aggregate:**  
  - Tally medal counts per edition and country.  
  - Track number of unique athletes.  
- **Write output data** using `write_csv_file`.


## Why did you choose the data structure you chose? How did you use it?

**Lists** were chosen to represent tabular CSV data because they preserve the order of records naturally, which is important for CSV files where the row order matters (e.g., header first, then data rows). Lists also provide straightforward iteration and slicing capabilities that simplify reading, processing, and writing CSV data line by line.

Slicing is used strategically in the code to simplify operations on structured data, like lists representing CSV files. For example, it is especially helpful when we need to skip headers ([1:]) or quickly access subsets of rows or columns. These cases benefit from slicing because it reduces repetitive code and improves readability.

However, not every function uses slicing — and that’s by design. In scenarios where precise control over each element is needed, or where clarity is more important than brevity, traditional loops are preferred. This blend ensures that the code remains efficient without sacrificing maintainability or making the logic harder to follow.

By combining both slicing and explicit iteration as needed, the code achieves a practical balance between expressiveness and clarity.

**Dictionaries** were used to enhance performance and enable efficient lookups. For example, searching for an athlete by athlete_id or looking up game start dates by edition_id would be costly if done via linear scans over lists, especially as the datasets grow large. By mapping keys to values, dictionaries provide average O(1) time complexity for these lookups, greatly improving overall application speed.

The combination of lists and dictionaries balances simplicity with efficiency. Lists provide a straightforward and direct way to represent raw CSV data, while dictionaries add fast indexing and retrieval capabilities without the complexity or overhead of more advanced data structures or external databases. Dictionaries also improve code readability and maintainability by explicitly linking keys (such as athlete IDs or edition IDs) to their related data, which helps avoid errors that can occur with manual index handling in nested lists. This approach offers flexibility as well — since CSV files can change structure (for example, with columns added or reordered), helper functions like col_index dynamically locate the needed columns, allowing the program to adapt while keeping data storage simple. Finally, this design conserves memory by storing data once in lists and using dictionaries only for lightweight mappings or references, which is especially helpful when processing large Olympic datasets.

## Usage example

In the create_athlete_birth_dict function, a dictionary is created where the key is the athlete_id and the value is the athlete’s date of birth. This structure allows very fast lookups — typically O(1) time complexity — meaning it can retrieve the birth date almost instantly without searching through the entire list. This makes it easy to quickly calculate an athlete's age for any event without traversing the entire original list.

---

## runtime needed to clean all data

**Function clean_pos**
- Input size: pos_value (string)
- Runtime: O(1)

**Function clean_all_positions**
- Input size: n = rows in athlete_event_file
- Runtime: O(n)

**Function parse_date**
- Input size: l = length of date string
- Runtime: O(l)

**Function format_athlete_born**
- Input size: a = rows in athlete_bio_list
- Runtime: O(a)

**Function format_p_athlete_born**
- Input size: p = rows in paris_athletes_list
- Runtime: O(p)

**Function format_games_dates**
- Input size: g = rows in games_list
- Runtime: O(g)

**Total runtime to clean all data**
- The overall time complexity is: O(n) + O(a) + O(p) + O(g) + O(l) + O(1) = **O(n + a + p + g)**

---

## runtime needed to add paris data into the records
**Function col_index**  
- Input size: *a* = number of columns in header  
- Runtime: O(a) worst-case (searching column name), O(1) best-case

**Function is_duplicate_athlete**  
- Input size: *a* = number of rows in existing_data (olympic_athlete_bio), *p* = number of columns  
- Runtime: O(a + p) (searching header columns + linear scan for duplicates)

**Function get_max_id**  
- Input size: *a* = number of rows in data (olympic_athlete_bio)  
- Runtime: O(a) (linear scan to find max id)

**Function calculate_next_edition_id**  
- Input size: *n* = number of rows in olympic_athlete_events_results, *p* = number of columns  
- Runtime: O(n + p) (lookup index + linear scan + max)

**Function integrate_paris_athletes**  
- Input size: *a* = number of rows in athlete_bio_file, *p* = number of rows in paris_athletes  
- Runtime: O(p × a) (loop over Paris athletes × duplicate checks in existing bio)

**Function mergeGamesData**  
- Input size: *m* = rows in games_file, *n* = rows in paris_data  
- Runtime: O(m + n)

**Function integrate_paris_countries**  
- Input size: *m* = rows in original_countries, *n* = rows in paris_nocs  
- Runtime: O((m + n) log(m + n))

**Function process_medals_and_update_file**  
- Input size: *m* = rows in athlete_event_file, *p* = rows in paris_medallists  
- Runtime: O(m + p)

**Total Runtime for Inserting Paris Data**  
- The overall time complexity is:  O(p × a) + O((m + n) log(m + n)) + O(m + n + p + a)  
- Since *p × a* is a product and typically grows faster than sums or log terms, the overall complexity is:  
  **O(p × a)**

---

## runtime needed to generate the medal results for all games
**Function create_noc_dict**
- Input size: c = rows in countries_data
- Runtime: O(c)

**Function process_medal_tally**
- Input size: c = rows in athletes_data
- Runtime: O(c)

**Function generate_summary_data**
- Input size: I editions, K total countries across all editions
- Runtime: O(K)

**Total runtime to generate medal results for all games**
- The overall time complexity is:  O(c)+ O(c)+ O(K)= **O(c+K)**

---

## Function-1: col_index
```
def col_index(header, col_name):
    try:
        return header.index(col_name)   # n (worst-case scans all n header entries)
    except ValueError:
        return -1                       # 1
```       
**Step 1 — Variables & functions:**

a = number of columns in 'header' (list length).
col_index() → returns position of 'col_name' or -1 if not found.
T(a) = total operations to find column index.

**Step 2 — Count operations:**

**header.index(col_name) worst case:**
O(a) comparisons.
Best case: O(1).

**Step 3 — Expression: Worst:**
T(a) = a, Best: T(a) = 1

**Step 4 — Simplify: Worst:**
O(a), Best: O(1)

**Step 5 — Final result:**

Worst-case: O(a)

---

## Function-2: is_duplicate_athlete
```
def is_duplicate_athlete(new_athlete_row, existing_data):
    name_idx = col_index(existing_data[0], "athlete_full_name")  # <= n (worst-case header lookup)
    dob_idx  = col_index(existing_data[0], "born")               # <= n
    new_name = new_athlete_row[0].strip().lower()                # 1
    new_dob  = new_athlete_row[1].strip()                        # 1
    for row in existing_data[1:]:                                # (n-1) iterations
        if row[name_idx].strip().lower() == new_name and row[dob_idx].strip() == new_dob:  
            # ~4 constant ops per iteration (strip/compare)   # 4*(n-1)
            return True                                         # 1 (on hit)
    return False                                                 # 1
```
**Step 1 — Variables & functions:**

a = rows in existing_data (olympic_athlete_bio),
p = columns.
Checks if athlete already exists.

**Step 2 — Count operations:**

2 × col_index(): O(p)
Loop over a-1 rows: O(a)

**Step 3 — Expression:**
T(a, p) = 2p + a

**Step 4 — Simplify:**
O(a + p)

**Step 5 — Final result:**

Worst-case: O(a + p)

---

## Function-3: get_max_id
```
def get_max_id(data, id_col):
    max_id = 0                          # 1
    for i, row in enumerate(data):      # n iterations (including header)
        if i == 0:
            continue                    # skip header (cost counted in loop control)
        try:
            max_id = max(max_id, int(row[id_col]))  # ~3 ops per non-header row
        except ValueError:
            continue                    # 1 (exception path)
    return max_id                       # 1
```
**Step 1 — Variables & functions:**

a = rows in data (olympic_athlete_bio).
Finds largest numeric ID.

**Step 2 — Count operations:**

Loop through a rows: O(a)

**Step 3 — Expression:**

T(a) = a

**Step 4 — Simplify:**

O(a)

**Step 5 — Final result:**

Worst-case: O(a)

---

## Function-4: calculate_next_edition_id
```
def calculate_next_edition_id(athlete_event_file):
    edition_ids = set()                                  # 1
    edition_id_idx = col_index(athlete_event_file[0], "edition_id")  # <= n
    for row in athlete_event_file[1:]:                   # (n-1) iterations
        if row[edition_id_idx].isdigit():                # 1 per iteration
            edition_ids.add(int(row[edition_id_idx]))   # ~2 ops per valid numeric entry
    return str(max(edition_ids) + 1)                     # max over up to (n-1) items => (n-1) ops + 1
```
**Step 1 — Variables & functions:**

n = rows in olympic_athlete_events_results,
p = columns.
Finds max edition_id and returns next one.

**Step 2 — Count operations:**

col_index(): O(p)
Loop over n-1 rows: O(n)
max() over set: O(n)

**Step 3 — Expression:**
T(n, p) = p + 2n

**Step 4 — Simplify:**
O(n + p)

**Step 5 — Final result:**

Worst-case: O(n + p)

---

## Function-5: integrate_paris_athletes

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
    
**Step 1 — Establish variables and functions:**
a = number of rows in athlete_bio_file (olympic_athlete_bio, including header)
p = number of rows in paris_athletes (including header)
k = number of columns in these tables (small constant, treat as O(1))
col_index(header, col_name) → worst case O(1)
is_duplicate_athlete([name, dob], athlete_bio_file) → worst case O(a)

**Step 2 — Count operations:**
Part 1 — Filling missing height & weight: loops through a − 1 rows → O(a)
Part 2 — Setting up indexes: col_index calls → O(1) total
Part 3 — Integrating Paris athletes: loops through p − 1 rows, each calls is_duplicate_athlete → O(a) per iteration → O(p × a) total

**Step 3 — Mathematical expression**
T(p, a) = a + (p × a)

**Step 4 — Simplify:**
T(p, a) = O(p × a) (since p × a dominates for large p and a)

**Step 5 — Final result:**
Worst-case time complexity: O(p × a)

---

## Function-6 create_teams_dict

```
def create_teams_dict(teams):
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
```

**Step 1 — Variables & Functions**
- n = number of rows in teams (including header)

**Step 2 — Count operations**
- Loop through (n - 1) rows → O(n)
- Each iteration → O(1) to extract and assign to dict

**Step 3 — Expression**
- T(n) = (n - 1) * O(1)

**Step 4 — Simplify**
- T(n) = O(n)

**Step 5 — Final Result**

- Time Complexity: O(n)**

---

## Function-7 clean_pos 

```
def clean_pos(pos_value):
    if pos_value.isdigit() or pos_value in ("DNF", "DNS"):
        return pos_value
    else:
        return ""
```

** Step 1 — Variables & Functions**
- Input: `pos_value` (string)
- Uses `.isdigit()` and membership check

**Step 2 — Count operations**
- Constant-time logic → O(1)

**Step 3 — Expression**
- T(n) = O(1)

**Step 4 — Simplify**
- T(n) = O(1)

**Step 5 — Final Result**
- Time Complexity: O(1)

---

## Function-8 clean_all_positions

```
def clean_all_positions(athlete_event_file):
    pos_idx = athlete_event_file[0].index("pos")
    for row in athlete_event_file[1:]:
        row[pos_idx] = clean_pos(row[pos_idx])
```

**Step 1 — Variables & Functions**
- n = number of rows in athlete_event_file
- Calls clean_pos() on each row

**Step 2 — Count operations**
- Index lookup: O(m)
- Loop through n-1 rows → Each call to clean_pos = O(1)

**Step 3 — Expression**
- T(n) = O(n)

**Step 4 — Simplify**
- T(n) = O(n)

**Step 5 — Final Result**
- Time Complexity: O(n)

---

## Function-9 mergeGamesData

```
def mergeGamesData(games_file, paris_data):
    existing_ids = set()
    edition_id_idx = col_index(games_file[0], "edition_id")

    for row in games_file[1:]:
        existing_ids.add(row[edition_id_idx])

    merged_games = games_file[:]
    for row in paris_data[1:]:
        if row[edition_id_idx] not in existing_ids:
            merged_games.append(row)
        existing_ids.add(row[edition_id_idx])

    return merged_games
```

**Step 1 — Variables & Functions**
- m = rows in games_file
- n = rows in paris_data

**Step 2 — Count operations**
- Set lookup + copy → O(m + n)

**Step 3 — Expression**
- T(m, n) = O(m + n)

**Step 4 — Simplify**
- T(m, n) = O(m + n)

**Step 5 — Final Result**
- Time Complexity: O(m + n)

---

## Function-10 integrate_paris_countries
```
def integrate_paris_countries(original_countries, paris_nocs):
    existing_nocs = set()
    noc_idx = col_index(original_countries[0], "noc")
    updated_countries = original_countries[:]

    for row in original_countries[1:]:
        existing_nocs.add(row[noc_idx])

    for row in paris_nocs[1:]:
        if row[0] not in existing_nocs:
            updated_countries.append([row[0], row[1]])
            existing_nocs.add(row[0])

    header = updated_countries[0]
    data_rows = sorted(updated_countries[1:], key=lambda x: x[1])
    return [header] + data_rows
```

**Step 1 — Variables & Functions**
- m = rows in original_countries
- n = rows in paris_nocs

**Step 2 — Count operations**
- Set creation → O(m)
- Insert + sort → O((m + n) log(m + n))

**Step 3 — Expression**
- T(m, n) = O((m + n) log(m + n))

**Step 4 — Simplify**
- T(m, n) = O((m + n) log(m + n))

**Step 5 — Final Result**
- Time Complexity: O((m + n) log(m + n))

---

## Function-11 process_medals_and_update_file
```
def process_medals_and_update_file(athlete_event_file, paris_medallists, teams_dict, next_edition_id, athlete_birth_dict, games_start_dates_dict):
    if '63' not in games_start_dates_dict or None in games_start_dates_dict['63']:
        games_start_dates_dict['63'] = (
            datetime.strptime('26-Jul-2024', '%d-%b-%Y'),
            datetime.strptime('11-Aug-2024', '%d-%b-%Y')
        )

    if "age" not in athlete_event_file[0]:
        athlete_event_file[0].append("age")
        for row in athlete_event_file[1:]:
            row.append("")

    edition_id_idx = athlete_event_file[0].index("edition_id")
    athlete_id_idx = athlete_event_file[0].index("athlete_id")
    age_idx = athlete_event_file[0].index("age")

    for row in athlete_event_file[1:]:
        edition_id = row[edition_id_idx]
        athlete_id = row[athlete_id_idx]
        birth_date = athlete_birth_dict.get(athlete_id)
        start_date, end_date = games_start_dates_dict.get(edition_id, (None, None))
        row[age_idx] = calculate_age(birth_date, start_date, end_date) if birth_date and start_date else ""

    if not paris_medallists or not next_edition_id:
        return

    unique_entries = set(
        (row[athlete_id_idx], row[athlete_event_file[0].index("event")] if "event" in athlete_event_file[0] else "")
        for row in athlete_event_file[1:]
    )

    medallist_header = paris_medallists[0]
    idx_country_noc = col_index(medallist_header, "country_code")
    idx_sport = col_index(medallist_header, "discipline")
    idx_event = col_index(medallist_header, "event")
    idx_athlete_name = col_index(medallist_header, "name")
    idx_athlete_id = col_index(medallist_header, "code_athlete")
    idx_medal = col_index(medallist_header, "medal_type")

    for medallist in paris_medallists[1:]:
        edition = "2024 Summer Olympics"
        edition_id = str(next_edition_id).strip()

        country_noc = medallist[idx_country_noc]
        sport = medallist[idx_sport]
        event = medallist[idx_event]
        athlete_id = medallist[idx_athlete_id]
        medal = medallist[idx_medal]
        athlete_name = medallist[idx_athlete_name].title()

        is_team_sport = "False"
        if event in teams_dict:
            is_team_sport = "True"
            if athlete_id not in teams_dict[event]["athletes_codes"]:
                continue

        unique_key = (athlete_id, event)
        if unique_key in unique_entries:
            continue
        unique_entries.add(unique_key)

        if medal in ["Gold Medal", "Gold"]:
            medal = "Gold"
            pos = "1"
        elif medal in ["Silver Medal", "Silver"]:
            medal = "Silver"
            pos = "2"
        elif medal in ["Bronze Medal", "Bronze"]:
            medal = "Bronze"
            pos = "3"
        else:
            pos = ""

        result_id = ""
        birth_date = athlete_birth_dict.get(athlete_id)
        start_date, end_date = games_start_dates_dict.get(edition_id, (None, None))
        age = calculate_age(birth_date, start_date, end_date) if birth_date and start_date else ""

        new_result = [
            edition, edition_id, country_noc, sport, event, result_id,
            athlete_name, athlete_id, pos, medal, is_team_sport, age
        ]
        athlete_event_file.append(new_result)
```
**Step 1 — Variables & Functions**
- m = rows in athlete_event_file
- p = rows in paris_medallists

**Step 2 — Count operations**
- Add column + age calc = O(m)
- Unique set creation = O(m)
- Loop & append Paris data = O(p)

**Step 3 — Expression**
- T(m, p) = O(m) + O(p)

**Step 4 — Simplify**
- T(m, p) = O(m + p)

**Step 5 — Final Result**
- Time Complexity: O(m + p)

---

## Function-12 create_athlete_birth_dict
```def create_athlete_birth_dict(new_athlete_bio_data):
    birth_dict = {}                                             # 1
    is_header = True                                            # 1
    for row in new_athlete_bio_data:                            # a 
        if is_header:                                           # 6 ops in the if statement
            id_index = row.index("athlete_id")                  # 2 ops (assignment + .index())
            born_index = row.index("born")                      # 2 ops (assignment + .index())
            is_header = False                                   # 1 
            continue                                            # 1
        
        athlete_id = row[id_index]                              # 1 * (a-1)
        born_str = row[born_index]                              # 1 * (a-1)
        
        try:
            birth_date = datetime.strptime(born_str, "%d-%b-%Y")  # 2 * (a-1)
        except Exception:
            birth_date = None                                   # 1 * (a-1)
        
        birth_dict[athlete_id] = birth_date                     # 1 * (a-1)
    
    return birth_dict                                          # 1
```
**Step 1 - Variables & fuctions**
- Let a = number of records (rows) in new_athlete_bio_data

**tep 2 — Count operations**
- 2  assignments → O(1)
- 6 operations for the if statement block
- 1 operation for athlete_id assignment
- 1 operation for born_str assignment
- 2 operations for datetime.strptime inside try block
- 1 except assignment if exception raised (worst case)
- 1 dictionary assignment
- 1 return statement → O(1)

**Step 3 — Expression**
- T(a)=2+6+2+2+1+1+(a−1)×(1+1+2+1+1)+1=14+6(a−1)+1=6a+9

**Step 4 — Simplify:**
- T(a)=6a+9
- O(a)

**Step 5 — Final result**
- Worst-case runtime complexity is O(a)

---

## Function-13 create_games_start_dates_dict

```
def create_games_start_dates_dict(games):
    start_dates_dict = {}                       # 1 op 
    is_header = True                            # 1 op 
    
    for row in games:                           # c iterations 
        if is_header:                          # 8 ops in the if statement: 
            edition_id_index = row.index("edition_id")   # 2 ops (assignment + .index())
            start_date_index = row.index("start_date")   # 2 ops
            end_date_index = row.index("end_date")       # 2 ops
            is_header = False                 # 1 op 
            continue                          # 1 op
       
        edition_id = row[edition_id_index]    # 1 op
        
        try:
            start_date = datetime.strptime(row[start_date_index], "%d-%b-%Y")  # 2 op
            end_date = datetime.strptime(row[end_date_index], "%d-%b-%Y")      # 2 op
        except Exception:
            start_date = None                # 1 op
            end_date = None                  # 1 op
    
        start_dates_dict[edition_id] = (start_date, end_date)  # 1 op
        
    return start_dates_dict                    # 1 op
```
**Step 1 — Variables & functions**
- c = total number of rows in the games list (including header).

**Step 2 — Count operations**
- 2  assignments → O(1)
- c 
- 8 ops if statement
- 1 assignment for edition_id
- 4 ops( 2 assignment and two calls to  to datetime.strptime() )
- 2 assigments dates as None
- 1 dictionary assignment
- 1 return statement → O(1)

**Step 3 — Expression**
- T(c)=2+8+(c−1)×(1+4+2+1)+1=2+8+8(c−1)+1=8c+2

**Step 4 — Simplify**
- T(c)=8c+2

**Step 5 — Final result**

- Worst-case runtime complexity is O(c)

---

## Function-14 calculate_age

```
def calculate_age(birth_date, start_date, end_date):
      if not birth_date or not start_date or not end_date:  # 3 checks
        return ""                                        # 1 operation (return)

    age = start_date.year - birth_date.year        # 1 

    try:
        birthday_this_year = birth_date.replace(year=start_date.year)  # 1 method call + 1 assignment
    except ValueError:
        # If birth_date is Feb 29 and start_date.year is not leap, use Feb 28
        birthday_this_year = birth_date.replace(year=start_date.year, day=28)  # 1 method call + 1 assignment

    if start_date < birthday_this_year:                   # 1 comparison
        age -= 1                                          # 1 

    return str(age)                                       # 1 conversion + 1 return
```

**Step 1 — Variables & functions**
- Inputs: 3 single datetime objects or None.

**Step 2 — Count operations**
- Initial conditional checks (if not birth_date or not start_date or not end_date): 3 operations
- Early return if any are None: 1 operation
- Subtract years: 1 operation
- birth_date.replace(year=start_date.year): 1 operation
- Except block (if exception):
- birth_date.replace(year=start_date.year, day=28): 1 operation
- Compare dates (start_date < birthday_this_year): 1 operation
- Decrement age: 1 operation
- 1 conversion + 1 return

**Step 3 — Expression***
- Total operations = 3 + 1 + 1 + 2 + 2 + 1 + 1 + 2 = 13 operations (all constant)

**Step 4 — Simplify**
- O(1)

**Step 5 — Final result**
- Worst-case: O(1)

---

## Function-15 create_noc_dict
```
def create_noc_dict(olympics_country, paris_nocs):
    noc_to_country = {}                              # 1 
    for i, row in enumerate(olympics_country):        # c1 
        if i == 0:                                  # 1 
            continue                                # 1 
        noc = row[0]                                # 1 
        country_name = row[1]                        # 1 
        noc_to_country[noc] = country_name          # 1 

    for i, row in enumerate(paris_nocs):    #c
        if i == 0:  # Skip header row      #1
            continue                      #1
        noc = row[0]        #1
        country_name = row[1]       #1
        noc_to_country[noc] = country_name  # 1
    
    return noc_to_country                            # 1 
````
**Step 1 — Variables & functions**
- c = total number of rows in olympics_country and paris_nocs
- c1= number of rows in olympics_country (including header)
- c2 = number of rows in paris_nocs (including header)

**Step 2 — Count operations**

- 1 initialize dictionary
- c1 ops
- 5 op in the if statement

- 1 initialize dictionary
- c2 ops
- 5 op in the if statement
- 1 return statement → O(1)

**Step 3 — Expression**
- T(c)= 1+ 5c1 + 1 + 5c2 + 1

**Step 4 — Simplify**
- T(c) = 3+ 5(c1+c2)

**Step 5 — Final result**
- T(c) = 2+ 5c  where c = c1+c2

- Worst-case runtime complexity: O(c)

---

## Function-16 process_medal_tally
```
    medal_tally = {}                                  # 1 op
    for i, row in enumerate(athletes_data):          # c iterations 
        if i == 0:                                   # 1 
            continue                                 # 1 

        edition_name = row[0]                         # 1 
        edition_id = row[1]                           # 1 
        country_noc = row[2]                          # 1 
        athlete_id = row[7]                           # 1 
        medal = row[9]                                # 1 

        # Check if edition exists and possibly add it
        if edition_name not in medal_tally:           # 1 
            medal_tally[edition_name] = {}            # 1 

        # Check if country exists and possibly add it
        if country_noc not in medal_tally[edition_name]:  # 1 
            medal_tally[edition_name][country_noc] = {    # 1 
                'edition_id': edition_id,                   
                'athletes': set(),                          # 1 op
                'gold': 0,                                  
                'silver': 0,                                
                'bronze': 0                                 
            }

        if medal == 'Gold':                             # 1
            medal_tally[edition_name][country_noc]['gold'] += 1  # 2
        elif medal == 'Silver':                         # 1 
            medal_tally[edition_name][country_noc]['silver'] += 1  # 2
        elif medal == 'Bronze':                         # 1 
            medal_tally[edition_name][country_noc]['bronze'] += 1  # 1 

        # Add athlete to set (average O(1) per set insertion)
        medal_tally[edition_name][country_noc]['athletes'].add(athlete_id)  # 1 

    return medal_tally                                 # 1 
```
**Step 1 — Variables & functions**
- Let c = number of rows in athletes_data (including header)
- Number of editions and countries per edition ≤ c (worst case)
- Set insertions are average O(1)

**Step 2 — Count operations**

- 1 initialization
- c ops 
- 19 attribute accesses/assignments
- 1 return statement → O(1)

**Step 3 — Expression**
- T(c)=1+c×18+1

**Step 4 — Simplify**
- T(c) = 2+18c

**Step 5 — Final result**
- Worst-case runtime complexity: O(c)

---

## Function-17 process_medal_tally
```
    summary_data = []      # 1
    header = [
        "edition", "edition_id", "Country", "NOC",
        "number_of_athletes", "gold_medal_count", "silver_medal_count",
        "bronze_medal_count", "total_medals"
    ]
    summary_data.append(header)  # 1 operation

    # Iterate through medal tally to build the summary rows
    for edition_name, countries in medal_tally.items():        # I iterations (number of editions)
        for country_noc, data in countries.items():            # K iterations per edition
            edition_id = data['edition_id']                    # 1
            country_name = noc_to_country.get(country_noc, "Unknown")  # 1 (dict lookup)
            num_athletes = len(data['athletes'])               # 1
            gold = data['gold']                                 # 1
            silver = data['silver']                             # 1
            bronze = data['bronze']                             # 1
            total = gold + silver + bronze                      # 3 
            summary_data.append([                               # 1 
                edition_name, edition_id, country_name, country_noc,
                num_athletes, gold, silver, bronze, total
            ])
    return summary_data # 1 
```
**Step 1 — Variables & functions**
- Let I be number of editions (keys in medal_tally)
- Let K be  Number of countries in the 𝑖 edition (inner loop iterations)

**Step 2 — Count operations**
- 1 operation append header
- For each of the I editions:  I ops
    - For each of the 𝐾 countries:    K ops 
       - 1 operation for edition_id retrieval
       - 1 operation for dict lookup noc_to_country.get()
       - 2 operation for length and assignment
       - 1 operation for gold, 
       - 1 operation for silver
       - 1 operation for bronze  
       - 3 operations to sum medals
       - 1 operation to append the new row
- 1 return statement → O(1)

**Step 3 — Expression:**
- T = 2 + 11 × (number of countries in edition 1+in edition 2+⋯+in edition I)

**Step 4 — Simplify**
- T = 2 + 11 × K

**Step 5 — Final result**
- T= O(K)