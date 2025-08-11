# Milestone 2 Analysis
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
