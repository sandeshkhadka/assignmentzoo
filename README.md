# AssignmentZoo

AssignmentZoo is a platform for Fusemachines 2025 Fellow to share and showcase their project.

## Project Overview

AssignmentZoo is a web application that allows users to share, discover, and collaborate on projects. The platform enables students to upload their projects, view others' work, and upvote projects they find interesting or useful.

## Features

- Project showcase with GitHub integration
- Search by project name or author (Only through api, no UI for this yet)

## Development Requirements

- Python 3.11+
- Uv (Python Package Manager)

## Setup and Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/sandeshkhadka/assignmentzoo.git
   cd assignmentzoo
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   make install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

4. Run the application:
   ```bash
   make run
   ```

### Docker Development

1. Make sure Docker and Docker Compose are installed on your system

2. Build and run the container:
   ```bash
   docker-compose up --build
   ```

3. The application will be available at http://localhost:8080

## Testing

Run the tests using pytest:

```bash
make test
```

Or run a specific test file:

```bash
pytest tests/test_crud_project.py
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8080/docs

## Project Structure

```
assignmentzoo/
├── app/
│   ├── crud/           # Database operations
│   ├── db/             # Database models and connection
│   ├── schemas/        # Pydantic models
│   ├── routes/         # API endpoints
│   ├── frontend/       # Minimal UI for project list
│   └── main.py         # Application entry point
├── tests/              # Test files
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── Makefile            # Make file to install and run application
└── pyroject.toml       # Python dependencies
```

## Demo

[Link to Demo Video](https://youtu.be/-oK9pRUzNu8) - A screen recording of the application running with passing tests and ci
workflows.
