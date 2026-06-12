# DSA Final Project — Olympics Data Integration

A Python data processing application that integrates Paris 2024 Olympic Games data into existing historical Olympic datasets, generating cleaned and updated output files.

## Project Overview

This project processes and cleans multiple Olympic datasets, merges Paris 2024 data with historical records, and generates a medal tally summary. The application was built as part of a group academic project at Seneca Polytechnic.

## Output Files

The application generates the following 5 output files:

| File | Description |
|------|-------------|
| `new_olympic_athlete_bio.csv` | Cleaned athlete biographical data |
| `new_olympic_athlete_event_results.csv` | Event results with added age column |
| `new_olympics_country.csv` | Country data |
| `new_olympics_games.csv` | Games data |
| `new_medal_tally.csv` | Medal tally with gold, silver, bronze counts |

## Medal Tally Header

```
edition, edition_id, Country, NOC, number_of_athletes, gold_medal_count, silver_medal_count, bronze_medal_count, total_medals
```

## Data Sources

- Historical Olympic athlete biography data
- Historical Olympic athlete event results
- Historical Olympic country and games data
- Paris 2024 athletes, events, and medallists data

## How to Run

```bash
python project.py
```

## Data Processing

The application handles the following:

- **Missing/unknown data** — identified and handled consistently across all files
- **Duplicate athlete entries** — detected and resolved between historical and Paris data
- **Paris data integration** — Paris 2024 records reconciled with existing data structure
- **Age calculation** — computed and added to event results

## Team

- Alejandra Pereira
- Jaspinder
- Manpreet
- Anurag

## Academic Context

**Course:** Data Structures and Algorithms — Seneca Polytechnic  
**Milestone 1:** June 16  
**Milestone 2:** August 9  
**Total Weight:** 10% of final grade (1% MS1 + 9% MS2)

## AI & External Resources

All AI prompts and external resources used during development are logged in `prompts.md` as required by course guidelines.
