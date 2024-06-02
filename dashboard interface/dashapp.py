import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import requests
import time
import json

# Global variable declaration
FASTAPI_BASE_URL = None

# Set the page to wide mode
st.set_page_config(layout="wide")

logo_path = r"./images/theia_white.png"  # Update the path if you put the logo in a subfolder
st.image(logo_path, width=200)  # Adjust the width as needed


# ------------------------ Handeling servers -------------------------------
def save_servers_to_file():
    with open("servers.json", "w") as file:
        json.dump(available_servers, file)

def load_servers_from_file():
    try:
        with open("servers.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default servers if the file does not exist
        return {
            "aelis": "http://aelis.telecomste.net:8080/",
            # Add other default servers here
        }

@st.cache_data
def load_servers():
    return load_servers_from_file()

available_servers = load_servers()

def save_servers():
    # Clear the cache
    load_servers.clear()
    # Save to file
    save_servers_to_file()
    # Reload the servers to refresh the cache
    global available_servers
    available_servers = load_servers()

def server_configuration():
    global FASTAPI_BASE_URL
    global available_servers  # Ensure available_servers is recognized as global

    st.subheader("Server Configuration")

    with st.form("add_server_form"):
        new_server_name = st.text_input("Enter new server name", key='new_server_name')
        new_server_url = st.text_input("Enter new server URL", key='new_server_url')
        submit_button = st.form_submit_button("Add Server")
        if submit_button:
            if new_server_name and new_server_url:
                # Update the available_servers dictionary
                available_servers[new_server_name] = new_server_url
                st.success(f"Server '{new_server_name}' added successfully.")
                # Set FASTAPI_BASE_URL to the newly added server
                FASTAPI_BASE_URL = new_server_url
                # Save the updated servers list
                save_servers()
            else:
                st.error("Please enter both name and URL for the new server.")

    # Section to select a server for monitoring
    st.subheader("Select Server for Monitoring")
    server_names = list(available_servers.keys())
    selected_server = st.selectbox("Choose a server", server_names, key='unique_server_select')

    # Update FASTAPI_BASE_URL based on the selected server
    FASTAPI_BASE_URL = available_servers[selected_server]
    st.write(f"Selected Server URL: {FASTAPI_BASE_URL}")





# Function to create pie chart for percentages
def create_pie_chart(percentage, label):
    mpl.style.use('dark_background')  # Use a dark theme for the plot
    fig, ax = plt.subplots()
    ax.pie([percentage, 100 - percentage], labels=[label, ''], startangle=90, counterclock=False, colors=['#0f0', 'lightgray'])
    centre_circle = plt.Circle((0, 0), 0.70, fc='#121212')
    fig.gca().add_artist(centre_circle)
    return fig

# DATA FETCHING -------------------------------------------------------------------------------------------------------------------
# ------------------------ CPU Data -------------------------------

def fetch_cpu_usage():
    url = FASTAPI_BASE_URL+"metrics/v1/cpu/usage"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_cpu_core_count():
    url = FASTAPI_BASE_URL+"metrics/v1/cpu/core"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['number']
    else:
        return None

# ------------------------ RAM Data -------------------------------
def fetch_ram_usage():
    url = FASTAPI_BASE_URL+"metrics/v1/ram/usage"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    else:
        return None

# ------------------------ Disk Data -------------------------------
def fetch_disk_info():
    url = FASTAPI_BASE_URL+"metrics/v1/disk/info"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    else:
        return None

# ------------------------ Processes Data -------------------------------
def fetch_process_list():
    url = FASTAPI_BASE_URL+"metrics/v1/process/processes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['processes']
    else:
        return None

def fetch_process_info(pid):
    try:
        pid = int(pid)  # Validate if PID is an integer
    except ValueError:
        return None

    url = f"{FASTAPI_BASE_URL}metrics/v1/process/process/{pid}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# ------------------------ Uptime Data -------------------------------
def fetch_uptime_info():
    url = FASTAPI_BASE_URL+"metrics/v1/uptime/info"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# ------------------------ logs Data -------------------------------
def fetch_and_process_logs_data():
    url = FASTAPI_BASE_URL + "metrics/v1/logs/entries"
    response = requests.get(url)
    data = response.json()['entries']
    df = pd.DataFrame(data)

    # Debugging: Print available columns
    print("Available columns in DataFrame:", df.columns.tolist())

    # Ensure the column exists before processing
    if 'number_of_byte_transferred' in df.columns:
        df['number_of_byte_transferred'] = pd.to_numeric(df['number_of_byte_transferred'], errors='coerce')
    else:
        # Handle the case when the column doesn't exist
        print("Column 'number_of_byte_transferred' not found in the data.")
        # You might want to add an alternative processing step here

    # Rest of the processing
    df = df[df['request_method'].isin(['GET', 'POST'])]
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%b/%Y:%H:%M:%S %z')

    # Group by timestamp and sum the bytes transferred
    df['number_of_byte_transferred'] = pd.to_numeric(df['number_of_byte_transferred'], errors='coerce')
    df_bytes_timeseries = df.groupby(df['timestamp'].dt.to_period('T'))['number_of_byte_transferred'].sum().reset_index()

    # Return processed data
    return df, df_bytes_timeseries

def create_request_method_bar_chart(df):
    request_counts = df['request_method'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(request_counts.index, request_counts.values, color=['blue', 'orange'])
    ax.set_title('Count of GET and POST Requests')
    ax.set_xlabel('Request Method')
    ax.set_ylabel('Count')
    return fig


def create_bytes_transferred_timeseries_chart(df):
    # Convert Period back to datetime for plotting
    df['timestamp'] = df['timestamp'].dt.to_timestamp()

    # Applying the theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots()

    # Plotting
    df.sort_values(by='timestamp', inplace=True)
    timeseries_data = df.groupby('timestamp')['number_of_byte_transferred'].sum()
    ax.plot(timeseries_data.index, timeseries_data.values, color='#0f0')  # Neon green line

    # Setting the title and labels
    ax.set_title('Timeseries of Bytes Transferred', color='#ffffff')  # White text
    ax.set_xlabel('Timestamp', color='#ffffff')
    ax.set_ylabel('Bytes Transferred', color='#ffffff')

    # Setting the background color
    ax.set_facecolor('#121212')  # Slightly lighter black for the plot background
    fig.patch.set_facecolor('#000000')  # Black for the figure background

    # Setting grid color and style
    ax.grid(True, color='lightgray', linestyle='--', linewidth=0.5)

    # Setting the tick colors
    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#ffffff')

    return fig

def fetch_logs():
    url = f"{FASTAPI_BASE_URL}metrics/v1/logs/entries"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Assuming the logs are in JSON format
        else:
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def format_logs(logs):
    formatted_logs = ""
    for entry in logs:
        # Ensure 'entry' is a dictionary and has 'timestamp' and 'message' keys
        if isinstance(entry, dict) and 'timestamp' in entry and 'message' in entry:
            log_line = f"Timestamp: {entry['timestamp']}, Message: {entry['message']}\n"
            formatted_logs += log_line
        else:
            # Handle the case where the entry is not a dictionary or doesn't have the expected keys
            formatted_logs += "Invalid log entry format\n"
    return formatted_logs



# Add a new function for the Logs Analysis page
def logs_analysis():
    st.subheader("Logs Analysis")
    df, df_bytes_timeseries = fetch_and_process_logs_data()  # Extract the two dataframes from the tuple

    # First row with two columns for bar charts
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Count of GETs and POSTs")
        if df is not None:
            fig1 = create_request_method_bar_chart(df)
            st.pyplot(fig1)
        else:
            st.error("Failed to fetch logs data.")

    with col2:
        st.subheader("Number of Bytes Transferred")
        if df_bytes_timeseries is not None:
            fig2 = create_bytes_transferred_timeseries_chart(df_bytes_timeseries)
            st.pyplot(fig2)
        else:
            st.error("Failed to process bytes transferred data.")

    # New row for the text field
    st.subheader("Log Details")
    raw_logs = fetch_logs()  # Assuming fetch_logs returns the raw log data
    if raw_logs:
        # Convert the log entries to a JSON-formatted string
        logs_json_str = json.dumps(raw_logs, indent=2)  # 'indent=2' for pretty printing
        # Create a text area to display the JSON data
        st.text_area("JSON Content", logs_json_str, height=300)  # Adjust height as needed
    else:
        st.error("Failed to fetch log data.")


# Function to create the CPU usage plot
def create_cpu_usage_plot(cpu_data):
    mpl.style.use('dark_background')  # Use a dark theme for the plot
    fig, ax = plt.subplots()
    ids = [item['id'] for item in cpu_data]
    usages = [float(item['usage']) for item in cpu_data]
    ax.bar(ids, usages, color='#0f0')  # Neon green bars
    ax.set_facecolor('#121212')  # Slightly lighter black for secondary elements
    ax.set_title('Real-time CPU Usage per Core', color='#ffffff')  # White text for contrast
    ax.set_xlabel('CPU Core ID', color='#ffffff')
    ax.set_ylabel('Usage (%)', color='#ffffff')
    ax.set_xticks(ids)
    ax.tick_params(colors='#ffffff')  # White ticks for contrast
    ax.grid(axis='y', linestyle='--', alpha=0.7, color='#ffffff')
    return fig
# ------------------------ Add -------------------------------
# Function to  the server overview
def app_overview():
     st.title("Welcome to Theia Server Monitor")

     st.markdown("""
    **Theia Server Monitor** is your comprehensive solution for real-time server management and monitoring. Designed with efficiency and user-friendliness in mind, this tool empowers you to keep a close eye on every critical aspect of your servers. Let's take a quick tour of what Theia offers:

    #### Streamlined Server Configuration
    - **Easily Add and Manage Servers**: Configure new servers with a few clicks. Simply enter the server's name and URL, and you're set to monitor its performance.

    #### Real-Time Monitoring at Your Fingertips
    - **CPU Utilization**: View CPU usage across all cores in real-time, helping you identify and manage the load effectively.
    - **RAM Usage Insights**: Monitor the memory usage, ensuring optimal performance and quick identification of potential issues.
    - **Disk Space Tracker**: Stay informed about your disk utilization with detailed usage statistics.
    - **Server Uptime**: Keep track of server stability with uptime metrics presented in an easily digestible format.

    #### In-depth Process Management
    - **Detailed Process Overview**: Get a comprehensive list of all running processes along with their CPU and memory usage.
    - **Deep Dive into Process Details**: Enter a Process ID to fetch specific data about individual processes, aiding in detailed analysis and troubleshooting.

    #### Advanced Log Analysis
    - **Structured Log Presentation**: Examine server logs in a structured format for efficient troubleshooting.
    - **Visual Data Interpretation**: Analyze GET and POST requests and understand data transfer patterns with intuitive bar charts and time series graphs.
    - **Raw Log Access**: For detailed inspection, view raw logs in their original JSON format.

    #### User-Centric Design
    - **Automatic Data Refresh**: The application refreshes every 10 seconds, ensuring you're viewing the most current data without manual reloads.
    - **Intuitive Navigation**: Easily switch between Overview, Monitoring, Process List, Configuration, and Log Analysis using the streamlined sidebar.

    #### Robust and Reliable
    - **Persistent Configuration**: Server settings are saved in a JSON file, providing consistent and reliable access to your configurations.
    - **Optimized Performance**: Thanks to Streamlit's caching, enjoy a smooth and responsive experience as you navigate through different metrics.

    ### Getting Started
    Dive right into monitoring your servers by selecting the 'Configuration' tab to add and manage your servers. Once set up, explore the various monitoring and analysis features Theia offers.

    **Theia Server Monitor** is more than just a tool; it's your partner in ensuring server health and performance. Enjoy the peace of mind that comes with having a full-scale monitoring solution at your fingertips.
    """)

# Function to display server monitoring
def server_monitoring():
    global FASTAPI_BASE_URL
    if FASTAPI_BASE_URL is None:
        st.error("FASTAPI_BASE_URL is not set")
        return
    st.subheader("Server monitoring")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1.5])

    with col1:
        st.subheader("CPU")
        cpu_core_count = fetch_cpu_core_count()
        if cpu_core_count is not None:
            st.markdown(f"**Number of CPU Cores**: {cpu_core_count}")
        else:
            st.error("Failed to fetch CPU core count.")
        
        cpu_data = fetch_cpu_usage()
        if cpu_data:
            fig = create_cpu_usage_plot(cpu_data)
            st.pyplot(fig)
        else:
            st.error("Failed to fetch CPU usage data.")
    
    with col2:
        st.subheader("RAM")
        ram_data = fetch_ram_usage()
        if ram_data:
            usage_gb = ram_data['usage'] / (1024 ** 3)  # Convert bytes to gigabytes
            capacity_gb = ram_data['capacity'] / (1024 ** 3)
            percent = ram_data['percent']
            st.markdown(f"**RAM Usage**: {usage_gb:.2f} GB / {capacity_gb:.2f} GB")
            pie_chart = create_pie_chart(percent, 'RAM Used (%)')
            st.pyplot(pie_chart)
        else:
            st.error("Failed to fetch RAM usage data.")
    
    with col3:
        st.subheader("Disk")
        disk_data = fetch_disk_info()
        if disk_data:
            total_space_gb = disk_data['total_space'] / (1024 ** 3)
            used_space_gb = disk_data['used_space'] / (1024 ** 3)
            usage_percent = disk_data['usage_percent']
            st.markdown(f"**Disk Information**: {used_space_gb:.2f} GB used of {total_space_gb:.2f} GB total")
            pie_chart = create_pie_chart(usage_percent, 'Disk Used (%)')
            st.pyplot(pie_chart)
        else:
            st.error("Failed to fetch disk information.")
    
    with col4:
        st.subheader("Uptime")
        uptime_info = fetch_uptime_info()
        if uptime_info:
            uptime_seconds = uptime_info.get('seconds', 0)
            hours, remainder = divmod(uptime_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            # Customized HTML for larger and bold uptime display
            uptime_html = f"""
            <div style='text-align: center;'>
                <span style='font-size: 2em; font-weight: bold; color: #0f0;'>
                    {int(hours)}h {int(minutes)}m {int(seconds)}s
                </span>
            </div>
            """
            st.markdown(uptime_html, unsafe_allow_html=True)
        else:
            st.error("Failed to fetch system uptime information.")

    with col5:
        
     st.subheader("Process Details")
     pid = st.text_input("Enter Process ID (PID):", key='process_id')
     if pid:
        process_info = fetch_process_info(pid)
        if process_info:
            cpu_usage = process_info.get('cpu_percent', 0)
            memory_usage = process_info.get('memory_percent', 0)
            st.markdown(f"**CPU Usage**: {cpu_usage:.2f}%")
            st.markdown(f"**Memory Usage**: {memory_usage:.2f}%")
        else:
            st.warning("No data available for the provided PID or the server didn't respond correctly.")
     else:
        st.info("Enter a Process ID to view details.")
    
# Function to display process list
def server_process_list():
    st.subheader("Process list")
    process_list = fetch_process_list()
    if process_list:
        st.markdown("**Process List:**")
        for process in process_list:
            st.text(f"ID: {process['id']}, Name: {process['name']}, CPU: {process['cpu_percent']}%, Memory: {process['memory_percent']*100:.2f}%")
    else:
        st.error("Failed to fetch process list.")

# Add a session state for refresh control
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = time.time()

# Main layout of the app
st.title("THEIA Server Monitoring")

# Set default FASTAPI_BASE_URL when dashboard runs for the first time
if not FASTAPI_BASE_URL and available_servers:
    FASTAPI_BASE_URL = next(iter(available_servers.values()))

# Sidebar navigation
page = st.sidebar.selectbox("Choose a page", ["Overview", "Monitoring", "Process list", "Configuration","Logs Analysis"])

if page == "Overview":
    app_overview()
elif page == "Monitoring":
    server_monitoring()
elif page == "Process list":
    server_process_list()
elif page == "Configuration":
    server_configuration()
elif page == "Logs Analysis":
    logs_analysis()    

# Automatic refresh every 10 seconds for dynamic updates
refresh_interval = 10  # Refresh every 10 seconds
current_time = time.time()
if current_time - st.session_state['last_refresh'] > refresh_interval:
    st.session_state['last_refresh'] = current_time
    st.rerun()

# Display last refresh time
st.sidebar.write(f"Last updated: {time.ctime(current_time)}")
