# EIA Assistant
This is an app that automates the reporting of Environmental Impact Assessments (EIA). Built with Flask, it is a full-stack application designed to simplify and streamline the entire EIA process. The app supports the inclusion of data from various domains such as biology, Natura 2000, protected areas, forestry, geology, hydrology, and more. It features a Leaflet map in the frontend for interactive data visualization. User management is fully functional and scalable, ensuring secure and efficient handling of user accounts.


## Features
- Automates the creation of EIA reports.
- Provides an efficient workflow for EIA documentation.
- Supports data import and export from various environmental domains.
- Includes a Leaflet map for interactive data visualization.
- Fully functional and scalable user management.

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
- app/: Contains the main application code written in flask. Contains flask templates and app logic.
- migrations/: Database migration files.
- eia_fast_app/: Contains the EIA specific logic. Uses FastAPI framework as alternative.
- config.py: Configuration settings.
- EIA_class.py: Defines the EIA class structure.
- eia.py: Main entry point for the EIA logic.

## Contributing
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a Pull Request.

## License
This project is licensed under the MIT License.
