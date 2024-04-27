# Project README

This project is developed using Python and the Flask framework to build a RESTful API.

## Overview
The API allows users to manage calendars, events, groups, and users, as well as sharing functionalities. It leverages MongoDB as its database backend for data storage.

## MongoDB Database
The MongoDB database is used to store data related to calendars, events, groups, and users. You can restore the necessary tables using the files located in the "mongodb" folder.

## Project Structure
The project structure is organized as follows:
- **MODULES**: Contains various Python modules for different functionalities.
  - Basic functions can be found directly within the "MODULES" directory.
  - Validation functions are located in the "MODULES/status" directory.

## Versions Used
- **Python**: 3.12.2
- **Flask**: 3.0.2

## Modules
### Calendar
- Create, retrieve, update, and delete calendars.
### Event
- Create, retrieve, update, and delete events within calendars.
### Group
- Create, retrieve, update, and delete groups of users.
### Share
- Share calendars or events with groups of users.
### Users
- Create, retrieve, update, and delete user accounts.

## Postman Collection
A Postman collection is available in the "postman" folder. It contains a set of requests that can be used to interact with the API endpoints via Postman.
