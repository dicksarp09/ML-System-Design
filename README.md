**StudentPass: Predicting Student Performance (Pass/Fail)**

StudentPass is an ML-based web application that predicts whether a student will pass or fail based on academic and demographic data. It helps educators and institutions quickly identify at-risk students and take timely interventions. StudentPass reduces manual effort, speeds up performance evaluation, and provides actionable insights using predictive machine learning models.

Here’s a walkthrough of what I built:

**Phase 1 – Data Collection**

End goal (business perspective):

1. Automate student performance prediction using machine learning.
2. Reduce manual effort for educators while providing actionable insights.
3.Collect student data with a binary target variable (pass/fail) and understand feature importance.
4. Understand requirements for an API and batch prediction workflow.

**Phase 2 – Data Ingestion with MongoDB**

Goal: Store and manage collected data in a NoSQL database.

Tools Used:

1. MongoDB for data persistence

2. PyMongo for Python–MongoDB interaction

Key Steps:

Create database and collection in MongoDB

Insert raw or cleaned data for later access

**Phase 3 – Model Development**

Goal: Train and evaluate a machine learning model.

Tools Used:

1. scikit-learn for ML

2. pandas and numpy for preprocessing

Outcome: A trained logistic regression model stored as logreg.pkl.

**Phase 4 – Flask API**

Goal: Serve the ML model through a REST API.

Tools Used:

1. Flask for API endpoints

2. Flask-PyMongo to fetch input data from MongoDB

Features:

Single predictions via JSON input

Batch predictions via CSV input/output

**Phase 5 – Dockerization**

Goal: Containerize the application for consistent deployment.

Tools Used:

1. Docker for containerization

2. docker-compose to run multiple services

Key Files:

Dockerfile

docker-compose.yml

**Phase 6 – Monitoring with Prometheus**

Goal: Collect application and system metrics.

Tools Used:

Prometheus for metrics scraping and storage

node-exporter for host CPU/memory metrics

cAdvisor for container-level metrics

**Phase 7 – Visualization with Grafana**

Goal: Visualize metrics and build dashboards.

Tools Used:

Grafana for visualization

Imported Prometheus as a data source

Dashboards: CPU, memory, and API request metrics

**Key Takeaways**

Built an end-to-end ML pipeline from scratch

Supported batch predictions, a common real-world requirement<img width="1536" height="1024" alt="StudentPass Logo Design" src="https://github.com/user-attachments/assets/dfce31cb-566d-4133-97ff-93e631479f93" />


Containerized services for consistent deployment

Implemented monitoring and visualization for production readiness

Learned how modern ML engineering combines coding, DevOps, and system observability

**Tech Stack**

| Tool/Library  | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Data processing, model training |
| pandas, numpy | Data wrangling                  |
| scikit-learn  | ML model training               |
| MongoDB       | Data storage                    |
| PyMongo       | Python–MongoDB connection       |
| Flask         | Serve model as API              |
| Docker        | Containerization                |
| Prometheus    | Metrics collection              |
| node-exporter | Host system metrics             |
| cAdvisor      | Container-level metrics         |
| Grafana       | Visualization dashboards        |
