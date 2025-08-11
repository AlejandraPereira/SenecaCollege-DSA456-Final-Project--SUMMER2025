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
