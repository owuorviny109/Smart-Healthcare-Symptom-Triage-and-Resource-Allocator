# TriageAI: A Serverless Healthcare Operations Platform

A professional-grade, end-to-end patient triage and resource allocation system designed to solve operational bottlenecks in high-volume hospitals like Mama Lucy Kibaki Hospital in Nairobi, Kenya. This project was built for the AWS Lambda Hackathon.

The platform provides a real-time **Operational Command Center** for hospital administrators, powered by a robust, serverless backend built entirely on the **AWS Free Tier**. It automates patient prioritization and intelligently assigns staff, turning a chaotic intake process into an efficient, data-driven workflow.

---

## Core Features & Services

Our platform is a complete clinical operating system, providing four key services:

1.  **Patient Intake & AI Triage:** A professional, multi-step workflow allows administrators to register new patients or find existing ones. A rule-based AI engine then instantly analyzes symptoms to assign a clear, actionable urgency score.
2.  **Intelligent Resource Allocation:** A serverless function runs automatically every minute, assigning queued patients to the least busy, available staff member (Doctors for high-urgency, Nurses for medium) based on real-time workload data.
3.  **Unified Command Center:** A live, single-page dashboard (`staff-portal.html`) provides a bird's-eye view of the entire hospital operation, including:
    *   Live-updating KPI cards (Patients Waiting, Available Staff, etc.).
    *   A real-time patient queue, color-coded by urgency.
    *   A D3.js-powered staff workload heatmap.
    *   Integrated forms for both patient intake and staff management.
4.  **Actionable Analytics:** An automated data pipeline generates daily operational reports in CSV format and stores them in Amazon S3. This data can be queried with **Amazon Athena** and visualized in **Amazon QuickSight** for strategic analysis and long-term planning.

## Architecture Overview

The entire system is built on a serverless, event-driven architecture using the AWS Free Tier.

*   **Frontend:** A static HTML/CSS/JavaScript single-page application (`staff-portal.html`) acts as the user interface. It uses TailwindCSS for styling, D3.js for visualizations, and GSAP for animations.
*   **API Layer:** **Amazon API Gateway** (`httpApi`) provides secure, public endpoints (`/triage`, `/staff`, `/patients`, `/dashboard`) for the frontend to communicate with the backend.
*   **Compute Layer:** **AWS Lambda** powers all business logic with six distinct microservices written in Python:
    *   `processTriage`: Calculates urgency scores.
    *   `assignWorker`: Assigns patients to staff on a 1-minute schedule.
    *   `getDashboardData`: Gathers real-time data for the command center.
    *   `manageStaff`: Handles creating and listing staff members.
    *   `managePatient`: Handles creating and searching for patient records.
    *   `generateReport`: Runs daily to create analytics reports.
*   **Database Layer:** **Amazon DynamoDB** provides three core NoSQL tables:
    *   `PatientsTable`: A permanent registry of all patients.
    *   `WorkerScheduleTable`: A real-time roster and workload tracker for all staff.
    *   `TriageQueueTable`: A temporary queue for patients awaiting assignment.
*   **Analytics & Data Lake:**
    *   **Amazon S3:** Stores daily CSV reports, forming a simple data lake.
    *   **(Optional Extension)** **AWS Glue & Amazon Athena:** Can be used to query the S3 data using standard SQL.
    *   **(Optional Extension)** **Amazon QuickSight:** Can be used to build strategic BI dashboards from the Athena data source.

## How to Run the Application

1.  **Deploy the Backend:**
    *   Ensure you have the [Serverless Framework](https://www.serverless.com/framework/docs/getting-started) and configured AWS credentials.
    *   Navigate to the project's root directory.
    *   Run `serverless deploy`. This will create all the necessary AWS resources.
2.  **Configure the Frontend:**
    *   After deployment, the terminal will output the API endpoints. Copy the base URL (e.g., `https://<id>.execute-api.us-east-1.amazonaws.com`).
    *   Open `staff-portal.html` and paste this URL into the `API_BASE_URL` constant in the `<script>` section.
3.  **Seed Initial Data (First Time Only):**
    *   Open `staff-portal.html` in your browser.
    *   Navigate to the "Manage Staff" tab and add at least one "Doctor" and one "Nurse".
4.  **Use the Command Center:**
    *   Navigate to the "Patient Intake" tab.
    *   Use the "Register New Patient" or "Find Existing Patient" buttons to start the intake workflow.
    *   After triaging a patient, watch the "Live Patient Queue" and dashboard metrics update in near real-time.

## Project Evolution & Key Milestones

*   **Initial Setup:** Configured AWS account, IAM user, and billing alerts for a secure, cost-controlled environment.
*   **Core Backend Deployment:** Deployed initial Lambda functions and DynamoDB tables using the Serverless Framework.
*   **Professional Frontend:** Developed a polished, animated Staff Command Center UI (`staff-portal.html`).
*   **CORS Debugging:** Solved critical "Failed to fetch" errors by implementing a robust CORS strategy using `httpApi: cors: true` in `serverless.yml` and correct header handling.
*   **Patient Management System:** Evolved the application from a simple triage form to a professional multi-step patient intake system, including a permanent `Patients` database table and a search/registration workflow.
*   **Full System Integration:** Successfully connected all frontend components to the backend API, achieving a complete, end-to-end functional application.
*   **CORS Support & Workflow Enhancements:** Implemented full CORS support with explicit OPTIONS handling for all Lambda functions. Improved patient and staff intake workflows, enhanced error handling, and updated documentation.

## Dependencies

*   **Backend:** Serverless Framework, Python 3.9, Boto3
*   **Frontend:** TailwindCSS, GSAP, D3.js

---

## Commit message for today

Implement full CORS support and production-ready patient/staff intake workflow

- Added explicit OPTIONS handling to all Lambda functions (manageStaff, managePatient) for CORS preflight.
- Updated serverless.yml with explicit httpApi.cors configuration for all methods and headers.
- Fixed frontend/backend JSON key mismatches for staff and patient creation.
- Improved error handling in staff-portal.html to display backend error messages.
- Enhanced patient intake workflow and staff management UI.
- Updated documentation to reflect CORS and deployment steps.