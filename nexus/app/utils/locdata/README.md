Files in this directory
===========================
google_cities_nodups.csv - contains cities' name as per google, their ID and SID of state. No duplicated names. (main output)
google_state.csv - contains state name as per google and their ID (main output)
google_cities.csv - contains cities' name as per google, their ID and SID of their state (main output)
google_cities_err.csv - contains those cities in city_state.csv for which there are no specific states given(Not merged)
city_state.csv - contains cities and their respective states as returned from Google Geocode API using cities_all.csv
city_state_err.csv - those cities for which Google API gave results fetched them manually. (Not merged)
states.csv - whizz api states list
cities_all.csv - whizz api all major cities statewise
India_State_District_SubDistrict - Indian States district subdistrict (Not used)
README.md - this readme file

Other Info
=============================
google_cities_nodups created from google_cities removing the duplicates.
Duplicate city names in google_cities.csv
Delhi has been chosen a common name for Delhi East,West, Central as city names.
Goa city names replaced from North, South goa to their actual names.

cities_all.csv, states.csv are original data.
city_state.csv - generated from cities_all, states using Google API.
google_cities.csv, google_state.csv  - generated from city_state.csv and states.csv
