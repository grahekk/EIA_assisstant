# EIA Assistant
This is an app that automates the reporting of Environmental Impact Assessments (EIA).

## Features
Automates the creation of EIA reports.
Provides an efficient workflow for EIA documentation.
Supports data import and export.

## Installation
Clone the repository:
```
git clone https://github.com/grahekk/EIA_assisstant.git
cd EIA_assisstant
```
Install the required dependencies:

```
pip install -r requirements.txt
```
Set up the environment variables:

```
cp .flaskenv.example .flaskenv
```
Initialize the database:

```
python load_to_local_db.py
```
## Usage
Run the application:
```
flask run
```

## Structure
app/: Contains the main application code.
migrations/: Database migration files.
eia_fast_app/: Contains the EIA specific logic.
config.py: Configuration settings.
EIA_class.py: Defines the EIA class structure.
eia.py: Main entry point for the EIA logic.

## Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.

## License
This project is licensed under the MIT License.
