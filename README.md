# CrisisDesk AI

CrisisDesk AI is an AI-powered crisis report classification and incident intelligence platform designed to help emergency response teams process incoming crisis reports efficiently.

The system transforms unstructured emergency reports into structured operational intelligence by classifying emergencies, determining urgency, generating summaries, recommending response actions, detecting similar reports, and clustering reports describing the same real-world incident.

## Live Deployment

CrisisDesk AI is publicly deployed as a live web application.

Live Application:

https://crisisdesk-ai-24hg.onrender.com

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
