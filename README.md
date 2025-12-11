# PI Cadence Calculator - Agile Release Train

A comprehensive Streamlit application for planning and managing PI (Program Increment) events for Agile Release Trains with support for multiple trains, holidays, and custom configurations.

## Features

- 📅 Automatic PI Planning and Iteration scheduling
- 🚂 Support for multiple trains with custom names and colors
- 🎯 Hackathon event planning
- 🚫 Canada statutory holidays + custom blocked periods
- 💾 Save/Load configurations as JSON
- 🌐 Bilingual support (English/French)
- 📊 Visual calendar and detailed event views
- ✏️ Editable event dates with automatic recalculation

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Installation Guide

### Step 1: Extract the Files

Extract this ZIP file to a folder on your computer.

### Step 2: Create a Virtual Environment (Recommended)

#### On Windows:
```bash
# Open Command Prompt or PowerShell in the extracted folder
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Open Terminal in the extracted folder
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Dependencies

With your virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This will install:
- **streamlit**: The web app framework
- **pandas**: Data manipulation
- **streamlit-calendar**: Interactive calendar component
- **holidays**: Canada statutory holidays

### Step 4: Verify Installation

Check that all packages are installed:

```bash
pip list
```

You should see all the packages from requirements.txt listed.

## Running the Application

### Start the App

With your virtual environment activated:

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at:
```
http://localhost:8501
```

### Access from Mobile/Other Devices (Same Network)

To access from your phone or another device on the same network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then open on your mobile browser:
```
http://YOUR_COMPUTER_IP:8501
```

(Replace YOUR_COMPUTER_IP with your computer's local IP address)

## How to Use

### 1. Configure Your Trains
- Set train names (default: Train A, Train B)
- Choose colors for each train
- Set the offset between trains (-7, 0, or +7 days)

### 2. Set Up Blocked Days
- ✅ Include Canada statutory holidays (automatic)
- Add custom blocked periods (e.g., Dec 15 - Jan 3)
- Add manual holidays with custom names and dates

### 3. Configure Hackathon
- **Automatic mode**: Select iteration and week
- **Custom dates**: Specify exact start and end dates

### 4. Generate Calendar
- Click "🔄 Generate Calendar" in the sidebar
- View events in interactive calendar
- Filter by train, PI, or event type

### 5. Edit Dates (Optional)
- Click "✏️ Edit Dates" button
- Modify any event dates
- Subsequent events recalculate automatically

### 6. Save Configuration
- Configure all your settings
- Click "📥 Download Configuration"
- Saves as JSON file with timestamp
- Upload later with "📤 Upload Configuration"

### 7. Export Data
- Download calendar as CSV
- Import into Jira, Excel, or other tools

## Configuration File Format

Saved configurations are JSON files containing:
```json
{
  "version": "2.2",
  "language": "en",
  "year": 2026,
  "train_a_name": "Train A",
  "train_a_color": "#3788d8",
  "custom_blocks": [...],
  "manual_holidays": [...]
}
```

## Troubleshooting

### Issue: `streamlit: command not found`
**Solution**: Make sure your virtual environment is activated and streamlit is installed:
```bash
pip install streamlit
```

### Issue: `ModuleNotFoundError: No module named 'holidays'`
**Solution**: Install the missing package:
```bash
pip install holidays
```

### Issue: Calendar not displaying
**Solution**: Clear Streamlit cache and restart:
```bash
streamlit cache clear
streamlit run app.py
```

### Issue: Port already in use
**Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Updating the Application

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Deactivating Virtual Environment

When you're done working:
```bash
deactivate
```

## File Structure

```
pi-cadence-calculator/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
├── README.md              # This guide
├── QUICKSTART.md          # Quick setup guide
├── .gitignore             # Git ignore file
└── venv/                  # Virtual environment (created by you)
```

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed
3. Make sure you're using Python 3.8+
4. Check that your virtual environment is activated

## Version

Current Version: 2.2

## License

This application is provided as-is for PI planning purposes.
