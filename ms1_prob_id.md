# Milestone 1 Problem Identification
1- what unknown wrong data is there?

When I loaded the raw CSVs it quickly became clear that they’re a bit of a time capsule: early-edition rows often have height, weight or even birth-date completely missing, country codes jump between current and long-retired versions like URS or FRG, and the same athlete can appear more than once either because they earned multiple medals or later switched nationality. Event names aren’t consistent either—sometimes it’s “100 m”, sometimes “100m”, accents come and go—so simply joining the files produces a lot of near-duplicates that need taming before any analysis makes sense.

2- how will wrong/unknown data be handled?

Wrong or unknown data will be handled by identifying missing or invalid values in key fields, such as height, weight or results. In these cases, placeholder values (e.g., empty strings) will be used to preserve the dataset structure while preventing the inclusion of incorrect or misleading information. Additionally, all date values will be standardized into the dd-Mon-yyyy format to ensure consistency across datasets. For example, if the Paris data contains a date like "1995-02-25", it will be converted into "25-Feb-1995". If a date cannot be correctly parsed due to an invalid format, the corresponding field will be assigned an empty string ('') to preserve the dataset structure without introducing incorrect values.

3- how will Paris data organized? How does this relate to the original data file? how will you determine the duplicate athlete entries?

The Paris data will be organized to match the structure of the original dataset. For example, when integrating data from paris/athletes.csv into the combined new_olympic_athlete_bio.csv file, only the fields required by the original structure will be extracted. Fields like country name, country length, and nationality that exist in the Paris dataset will be ignored or removed, keeping only the country code field (e.g., "USA") to ensure consistency and reduce redundancy

This process allows the Paris data to be merged seamlessly into the existing dataset structure. New athletes will be assigned unique IDs by incrementing the highest existing ID found in the current olympic_athlete_bio.csv file. To avoid duplicate athletes, entries will be compared based on a combination of name, birth_date, and country_code. For example, if an athlete "John Doe" born "25-Feb-1995" from country "USA" already exists, the Paris record with the same information will not be inserted again.

4- How will you be able to tell if your application was working?
    Are there specfic records that you can check?

I’ll trust the pipeline once three things line up: first, the automated tests stop flagging duplicates and the medal-tally equation gold + silver + bronze = total holds for every country-edition pair; second, well-known athletes like Michael Phelps (gold in the 100 m butterfly at Beijing 2008) and Usain Bolt (gold in the 100 m at Rio 2016) show up exactly once with the right age and medal; and third, a tricky historical case—say Hélène de Pourtalès from the 1900 Paris sailing events—lands in the final table with her medal and her mapped NOC (SUI) intact. When those checks all pass, I’ll know the data-cleaning rules and joins are doing their job.
