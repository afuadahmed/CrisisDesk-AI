# CrisisDesk AI

CrisisDesk AI is an AI-powered crisis report classification and incident intelligence platform designed to help emergency response teams process incoming crisis reports efficiently.

The system transforms unstructured emergency reports into structured operational intelligence by classifying emergencies, determining urgency, generating summaries, recommending response actions, detecting similar reports, and clustering reports describing the same real-world incident.

## Live Demo

CrisisDesk AI is publicly deployed as a live web application.

### Application Links

- Live Crisis Command Dashboard: https://crisisdesk-ai-24hg.onrender.com/
- Submit Crisis Report: https://crisisdesk-ai-24hg.onrender.com/report/
- Interactive Swagger API Documentation: https://crisisdesk-ai-24hg.onrender.com/api/docs/
- OpenAPI Schema: https://crisisdesk-ai-24hg.onrender.com/api/schema/

> Note: The application is hosted on a free cloud instance. The first request may take additional time if the service is waking from inactivity.

## Problem

During emergencies, multiple people may report the same crisis using different descriptions, languages, or location formats.

Emergency response teams may need to manually:

- Review incoming reports
- Identify the emergency category
- Determine urgency
- Detect similar or duplicate reports
- Prioritize critical incidents
- Track response status
- Analyze incoming crisis trends

This manual process can delay critical response operations.

## Solution

CrisisDesk AI automatically converts unstructured emergency reports into structured crisis intelligence.

The platform provides:

- AI-powered crisis classification
- Automatic urgency detection
- AI-generated incident summaries
- AI-suggested response actions
- Classification confidence scoring
- Bangla and English crisis report processing
- Duplicate and similar report detection
- Incident clustering
- Linked report intelligence
- Crisis response status tracking
- Activity timeline and audit history
- Real-time operational analytics
- Advanced search and filtering
- Automatic dashboard refresh
- Interactive Swagger/OpenAPI documentation

## Core Features

### AI Crisis Classification

Incoming crisis descriptions are analyzed by an AI processing service.

The system determines:

- Crisis category
- Urgency level
- Concise incident summary
- Suggested emergency response action
- Classification confidence

Supported categories are:

- `medical`
- `fire`
- `accident`
- `crime`
- `flood`
- `utility`
- `public_service`
- `infrastructure`
- `other`

Supported urgency levels are:

- `low`
- `medium`
- `high`
- `critical`

### Multilingual Crisis Processing

CrisisDesk AI supports crisis reports written in both Bangla and English.

Users can submit emergency descriptions using natural language.

The AI processing layer converts the submitted description into structured crisis information regardless of whether the original report is written in Bangla or English.

### Duplicate and Similar Report Detection

During a major emergency, multiple citizens may report the same real-world incident using different descriptions.

CrisisDesk AI compares incoming reports with existing reports using:

- Report description similarity
- Location similarity
- Crisis category

A weighted similarity score is calculated.

Reports exceeding the configured similarity threshold are marked as possible duplicates and linked to the same incident cluster.

This reduces duplicate operational effort and allows emergency teams to understand how many independent reports are associated with a crisis.

### Incident Intelligence

Reports describing the same crisis are grouped using a shared Incident ID.

The incident intelligence interface displays:

- Number of linked reports
- Incident ID
- Individual reporter information
- Reporter contact information
- Original crisis descriptions
- Duplicate similarity score
- Primary report identification
- Incident activity timeline

This allows emergency operators to inspect individual citizen reports while managing them as one operational incident.

### Crisis Status Management

Emergency operators can update the response status of a crisis.

Supported statuses are:

- `pending`
- `in_review`
- `assigned`
- `resolved`
- `rejected`

Updating an incident status synchronizes the status of reports linked to the same incident.

### Activity Timeline

The system records important report events.

Tracked activities include:

- Report creation
- Status changes

Activity records contain:

- Action type
- Previous status
- New status
- Timestamp

This creates an operational audit history for crisis reports.

### Real-Time Analytics

The CrisisDesk AI command dashboard provides live operational intelligence.

Dashboard statistics include:

- Total reports
- Critical reports
- Possible duplicate reports
- Pending reports
- Resolved reports

Analytics visualizations include:

- Category breakdown
- Response status distribution
- Urgency distribution

The dashboard automatically refreshes to display updated crisis intelligence.

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

These tools allow emergency operators to quickly identify relevant reports during high-volume crisis situations.

### Swagger and OpenAPI Documentation

CrisisDesk AI provides interactive REST API documentation using Swagger UI and an automatically generated OpenAPI schema.

Swagger UI allows developers and evaluators to inspect the available API endpoints, request formats, parameters, and response schemas.

Interactive API documentation:

`/api/docs/`

OpenAPI schema:

`/api/schema/`

## System Architecture

CrisisDesk AI follows a modular service-oriented Django backend architecture.

```text
Citizen / Crisis Reporter
            |
            v
     Crisis Report UI
            |
            v
      Django REST API
            |
            v
     Request Validation
            |
            v
    AI Processing Service
            |
            +---------------------------+
            |                           |
            v                           v
 Crisis Classification          Urgency Detection
 Summary Generation             Suggested Action
            |
            v
 Duplicate Detection Service
            |
            v
    Incident Clustering
            |
            v
      Persistent Database
            |
            +---------------------------+
            |                           |
            v                           v
      Analytics API             Crisis Queue API
            |                           |
            +-------------+-------------+
                          |
                          v
              Crisis Command Dashboard
```

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework

### AI Processing

- External AI-powered crisis classification service
- Natural-language crisis analysis
- Multilingual report processing

### Duplicate Detection

- Weighted text similarity analysis
- Description similarity
- Location similarity
- Category matching
- Incident clustering

### API Documentation

- drf-spectacular
- OpenAPI
- Swagger UI

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- SQLite

### Deployment

- Render
- Gunicorn
- WhiteNoise

## System Workflow

1. A citizen submits a crisis report.
2. The backend validates the request.
3. The AI processing service analyzes the crisis description.
4. The report is classified by category and urgency.
5. AI generates a concise incident summary.
6. AI recommends an emergency response action.
7. Duplicate detection compares the report with existing reports.
8. Similar reports are linked to the same incident.
9. The incident appears in the live crisis queue.
10. Emergency operators inspect incident intelligence.
11. Operators update the response status.
12. Status changes are recorded in the activity timeline.
13. Real-time analytics update automatically.

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

`GET /api/analytics/summary`

Retrieve crisis analytics summary data.

### API Documentation

`GET /api/docs/`

Open the interactive Swagger API documentation.

`GET /api/schema/`

Retrieve the generated OpenAPI schema.

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

The AI processing layer automatically generates the category, urgency, summary, suggested action, and confidence score.

## Bangla Report Example

```json
{
    "name": "Rahim",
    "contact": "01800000000",
    "location": "মিরপুর ১০, ঢাকা",
    "description": "মিরপুর ১০ এর একটি আবাসিক ভবনে ভয়াবহ আগুন লেগেছে। প্রচুর ধোঁয়া হচ্ছে এবং কয়েকজন মানুষ ভবনের ভিতরে আটকা পড়েছে।",
    "language": "bn"
}
```

The report is processed into structured crisis intelligence and can be compared with English reports describing the same incident.

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
git clone https://github.com/afuadahmed/CrisisDesk-AI.git
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

Configure the required environment variables in a `.env` file.

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

## Testing

Run the automated test suite:

```bash
python manage.py test
```

Run Django system checks:

```bash
python manage.py check
```

## Security

Sensitive configuration and API credentials are stored using environment variables.

The `.env` file is excluded from Git version control.

Production secrets are configured through deployment environment variables.

## Deployment

The application is deployed on Render using Gunicorn as the production WSGI server.

Static assets are served using WhiteNoise.

The deployed service automatically builds from the main GitHub branch.

## Future Scope

Future versions of CrisisDesk AI could integrate:

- Emergency service dispatch systems
- Geographic incident visualization
- SMS and mobile emergency reporting
- Additional multilingual crisis processing
- Real-time government emergency feeds
- Predictive crisis intelligence
- Role-based emergency operator authentication

## Project Vision

CrisisDesk AI demonstrates how artificial intelligence can convert fragmented emergency reports into structured, actionable crisis intelligence.

The goal is to help response teams identify critical incidents faster, reduce duplicate operational effort, and make better emergency response decisions.