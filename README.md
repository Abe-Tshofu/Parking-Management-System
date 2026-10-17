# KZN Smart Mall Parking Management System

This project is a Python console-based parking management application for the KZN Smart Mall Parking case study.

## How to run

1. Open a terminal in the project folder.
2. Run:
   `python main.py`

## Features

- Customer registration and login
- Admin and owner login
- Multi-mall pricing rules for three malls
- Vehicle entry and exit tracking
- Capacity control
- Payment recording and history
- Reporting for administrators and owners
- Data persistence using text files in the `data` folder

## Input and data validation

- Usernames must be 3-30 characters and use only letters, numbers, periods, underscores, or hyphens.
- Passwords must contain at least 4 characters; names and vehicle registrations are checked for invalid or excessive input.
- Only customers can enter or exit their own vehicles or make payments.
- Payments must be positive, finite numeric amounts and cannot exceed the outstanding balance.
- Invalid parking durations, pricing rules, entry timestamps, and malformed JSON data are rejected with an explanatory error.

## Default roles

- Admin username: `admin`
- Admin password: `admin123`
- Owner username: `owner`
- Owner password: `owner123`
