# Outdoor Advertising Management System

This repository contains a web application designed as part of a university project. The application is focused on
managing outdoor advertising using billboards and includes functionalities such as user authorization, query execution,
and order management. The application is containerized using Docker for easy deployment.

## Features

### Main Application

- **Order Processing**: Enable users to rent billboards for specific durations.
- **Query Handling**: Allow managers and other roles to execute SQL-based queries on the system data.
- **Report Generation**: Generate and view reports based on prebuilt scenarios for specific month.

### Authorization Microservice

- **User Authentication**: Secure login system with role-based access control.
- **Registration**: Allow user to sign up as renter.

## Technology Stack

- **Backend**: Flask (Python) for handling API requests and managing database operations.
- **Database**: MySQL for relational data management.
- **Frontend**: HTML, CSS, and Jinja2 templates for rendering user interfaces.
- **Containerization**: Docker for streamlined deployment.

## System Architecture

- **Main Application**: Core functionalities and user interactions.
- **Authorization Microservice**: Dedicated service for managing authentication.

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed.
- Basic knowledge of Python and Flask.

### Steps to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/Fsxdx/advertising.git
   cd advertising/apps
   ```
2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```
3. Access the application:
    - Main Application: `http://localhost:5000`
    - Authorization Microservice: `http://localhost:5001`

## Usage

### User Roles

- **External Users**: Rent billboards.
- **Managers**: Generate and view reports.
- **Directors**: View reports.
- **Support Staff**: Executing queries to database.

### Sample Data

The system includes preloaded test data for quick evaluation:

- Users:
  | Login | Password | Role |
  |--------|----------|------------|
  | man | 123 | Manager |
  | timofeev | 1 | Renter |
  | sup | 12 | Support |
  | dir | 1234 | Director |