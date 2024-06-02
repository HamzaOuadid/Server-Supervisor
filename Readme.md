# Server Supervisor

## Project Overview
This project is about an agent that fetches server data and exposes it through an API. The gathered data is later visualized on a dashboard. The main goal is to monitor and analyze the health and performance of individual servers within the network, providing an intuitive and graphical overview of the data for effective monitoring and management.

## Dashboard
The dashboard is designed to visually represent the extracted metrics, such as CPU usage, RAM utilization, and disk performance, obtained from each connected server. Its purpose is to provide an intuitive and graphical overview of the data, enabling users to monitor and analyze the health and performance of individual servers within the network.

## Agent
The agent operates on each monitored machine, capturing and transmitting key system metrics to a central dashboard for monitoring purposes. The primary focus includes gathering data on **RAM**, **CPU**, and **disk** usage, as well as information about active **processes**, system **uptime**, and **logs**. The objective is to provide a comprehensive overview of the machine's performance and health for effective monitoring and management.

## Running the Project

### Dashboard
Follow these steps to access the dashboard:

1. Pull the project:
    ```sh
    docker pull devops.telecomste.fr:5050/printerfaceadmin/2023-24/group8/dashboardinterface:latest
    ```
2. Go to the dashboard interface:
    ```sh
    docker run -p {any port you like}:8501 devops.telecomste.fr:5050/printerfaceadmin/2023-24/group8/dashboardinterface:latest
    ```
3. Open the dashboard by going to your preferred browser and navigating to:
    ```sh
    localhost:{the port you selected}
    ```
    or
    ```sh
    127.0.0.1:{the port you selected}
    ```

### Agent
Follow these steps to deploy the agent on your server:

1. Pull the project:
    ```sh
    docker pull devops.telecomste.fr:5050/printerfaceadmin/2023-24/group8/agent:latest
    ```
2. Run the agent:
    ```sh
    docker run devops.telecomste.fr:5050/printerfaceadmin/2023-24/group8/agent:latest
    ```

## Links
- **Agent**: [Agent](https://devops.telecomste.fr/printerfaceadmin/2023-24/group8/agent)
- **Dashboard**: [Dashboard](https://devops.telecomste.fr/printerfaceadmin/2023-24/group8/dashboardinterface)

[![coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)](https://devops.telecomste.fr/printerfaceadmin/2023-24/group8/agent/-/commits/main)
