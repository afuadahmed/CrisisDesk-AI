# CrisisDesk AI

CrisisDesk AI is an AI-powered crisis report classification and incident intelligence platform designed to help emergency response teams process incoming crisis reports efficiently.

The system uses AI to classify emergency reports, determine urgency, generate concise summaries, recommend response actions, and detect potentially duplicate reports describing the same real-world incident.

## Problem

During emergencies, multiple people may report the same crisis using different descriptions.

Emergency response teams must manually:

- Review incoming reports
- Identify the type of emergency
- Determine urgency
- Detect duplicate reports
- Prioritize incidents
- Track response status

This can delay critical response operations.

## Solution

CrisisDesk AI automatically transforms unstructured emergency reports into structured operational intelligence.

The platform provides:

- AI-powered crisis classification
- Automatic urgency detection
- AI-generated incident summaries
- AI-suggested response actions
- Semantic duplicate report detection
- Incident clustering
- Linked report intelligence
- Crisis response status tracking
- Activity timeline and audit history
- Real-time analytics
- Advanced search and filtering
- Automatic dashboard refresh

## Core Features

### AI Crisis Classification

Incoming crisis descriptions are analyzed by AI.

The system determines:

- Category
- Urgency
- Summary
- Suggested response action
- Classification confidence

Supported categories include:

- Fire
- Accident
- Medical
- Crime
- Natural Disaster
- Other

### Semantic Duplicate Detection

CrisisDesk AI detects reports that may describe the same real-world incident.

Duplicate detection considers:

- Report description similarity
- Location
- Crisis category

Potential duplicate reports are linked to a shared incident cluster.

This prevents emergency teams from treating multiple reports of the same crisis as unrelated incidents.

### Incident Intelligence

Reports describing the same crisis are grouped using a shared Incident ID.

The dashboard displays:

- Number of linked reports
- Individual reporter information
- Original descriptions
- Duplicate similarity score
- Incident activity timeline

### Crisis Status Management

Emergency operators can update incident status.

Supported statuses:

- Pending
- In Review
- Assigned
- Resolved
- Rejected

Updating an incident synchronizes the status of all linked reports.

### Activity Timeline

The system records important report events including:

- Report creation
- Status changes

Each activity contains timestamps and status transition information.

### Real-Time Analytics

The command dashboard provides operational statistics including:

- Total reports
- Critical reports
- Possible duplicate reports
- Pending reports
- Resolved reports
- Category breakdown
- Response status distribution
- Urgency distribution

### Advanced Search and Filtering

Reports can be searched and filtered using:

- Keyword search
- Category
- Urgency
- Status
- Start date
- End date
- Creation time ordering
- AI confidence ordering

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework

### AI Processing

- AI-powered report classification
- Semantic report similarity analysis

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- SQLite

## System Workflow

1. A citizen submits a crisis report.
2. The backend validates the report.
3. AI analyzes the crisis description.
4. The report is classified by category and urgency.
5. AI generates a concise summary.
6. AI recommends an emergency response action.
7. Duplicate detection compares the report with existing reports.
8. Similar reports are linked to the same incident.
9. The incident appears in the live crisis queue.
10. Emergency operators update the response status.
11. Status changes are recorded in the activity timeline.
12. Real-time analytics update automatically.

## API Endpoints

### Reports

`GET /api/reports`

Retrieve crisis reports with pagination, search, filtering, and ordering.

`POST /api/reports`

Submit a new crisis report for AI processing.

`GET /api/reports/<report_id>`

Retrieve a specific report.

`DELETE /api/reports/<report_id>`

Delete a report.

### Report Status

`PATCH /api/reports/<report_id>/status`

Update the status of an individual report.

### Incident Status

`PATCH /api/incidents/<incident_id>/status`

Update the status of every report linked to an incident.

### Analytics

`GET /api/reports/stats/summary`

Retrieve real-time crisis analytics.

## Example Report Submission

```json
{
    "name": "Karim",
    "contact": "01800000000",
    "location": "Dhaka Mirpur 10",
    "description": "A bus has overturned near Mirpur 10. Several passengers are injured and emergency medical assistance is urgently needed.",
    "language": "en"
}
```

The AI automatically generates the category, urgency, summary, suggested action, and confidence score.

## Search Example

```text
GET /api/reports?search=mirpur
```

## Combined Filtering Example

```text
GET /api/reports?category=accident&search=mirpur&start_date=2026-07-12
```

## Running the Project

Clone the repository:

```bash
git clone <repository-url>
cd CrisisDesk-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure required environment variables in a `.env` file.

Run database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Security

Sensitive configuration and API credentials are stored using environment variables.

The `.env` file is excluded from Git version control.

## Future Scope

Future versions of CrisisDesk AI could integrate:

- Emergency service dispatch systems
- Geographic incident visualization
- SMS and mobile emergency reporting
- Multilingual crisis processing
- Real-time government emergency feeds
- Predictive crisis intelligence
- Role-based emergency operator authentication

## Project Vision

CrisisDesk AI demonstrates how artificial intelligence can convert fragmented emergency reports into structured, actionable crisis intelligence.

The goal is to help response teams identify critical incidents faster, reduce duplicate operational effort, and make better emergency response decisions.