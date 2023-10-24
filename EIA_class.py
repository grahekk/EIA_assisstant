from abc import ABC, abstractmethod


class Project(ABC):
    def __init__(self, name, description, location, geometry, project_type, project_category, start_date, end_date, report):
        self.name = name
        self.description = description
        self.location = location
        self.geometry = geometry
        self.project_type = project_type
        self.project_category = project_category
        self.start_date = start_date
        self.end_date = end_date
        self.report = report

    @abstractmethod
    def plan(self):
        """Abstract method to outline the project plan."""

    @abstractmethod
    def execute(self):
        """Abstract method to execute the project activities."""

    @abstractmethod
    def monitor(self):
        """Abstract method to monitor the project's progress and impacts."""

    @abstractmethod
    def close(self):
        """Abstract method to close the project and finalize activities."""


# class EnvironmentalImpactAssessment(ABC):
#     def __init__(self, project, environmental_factors):
#         self.project = project
#         self.environmental_factors = EnvironmentalFactor

#     @abstractmethod
#     def scoping(self):
#         """Abstract method to define the scope and objectives of the EIA."""
    
#     @abstractmethod
#     def assess_impacts(self):
#         """Abstract method to assess the environmental impacts of the project."""

#     @abstractmethod
#     def propose_mitigation(self):
#         """Abstract method to propose mitigation measures for the identified impacts."""

#     @abstractmethod
#     def prepare_report(self):
#         """Abstract method to prepare the final EIA report."""

#     def submit_report(self):
#         """A method to submit the EIA report to relevant authorities or stakeholders."""
#         # Implement submission logic here
#         pass


class EnvironmentalImpactAssessmentProject(Project):
    def __init__(self, name, description, location, geometry, project_type, project_category, start_date, end_date, report):
        super().__init__(name, description, location, geometry, project_type, project_category, start_date, end_date, report)
        self.environmental_factors = EnvironmentalFactor

class ScopingProject(Project):
    def __init__(self, name, description, location, geometry, project_type, project_category, start_date, end_date, report):
        super().__init__(name, description, location, geometry, project_type, project_category, start_date, end_date, report)
        self.environmental_factors = EnvironmentalFactor

class BiologyReportProject(Project):
    def __init__(self, name, description, location, geometry, project_type, project_category, start_date, end_date, report):
        super().__init__(name, description, location, geometry, project_type, project_category, start_date, end_date, report)
        self.biology_factor = BiodiversityFactor


class EnvironmentalFactor():
    def __init__(self, name, description, expert_person, literature, data_source, legislative):
        self.name = name
        self.description = description
        self.expert_person = expert_person
        self.literature = literature
        self.data_source = data_source
        self.legislative = legislative

    def describe(self):
        """Common method to assess the environmental impact of the factor."""
        # get data and make text here

    def assess(self):
        """Common method to assess the environmental impact of the factor."""
        # Implement assessment logic here

    def propose_mitigation(self):
        """Common method to propose mitigation measures for the factor."""
        # Implement mitigation logic here


class HydrologyFactor(EnvironmentalFactor):
    def __init__(self, name, description, expert_person, literature, data_source, legislative, water_source_quality,potential_contamination, water_bodies):
        super().__init__(name, description, expert_person, literature, data_source, legislative)
        self.water_source_quality = water_source_quality
        self.potential_contamination = potential_contamination
        self.water_bodies = water_bodies

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement water quality assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to water quality
        pass

class BiodiversityFactor(EnvironmentalFactor):
    def __init__(self, name, description, species_diversity, habitat_disruption, conservation_status):
        super().__init__(name, description)
        self.species_diversity = species_diversity
        self.habitat_disruption = habitat_disruption
        self.conservation_status = conservation_status

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement biodiversity assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to biodiversity
        pass

class LandUseFactor(EnvironmentalFactor):
    def __init__(self, name, description, land_type, land_cover_change, urban_development):
        super().__init__(name, description)
        self.land_type = land_type
        self.land_cover_change = land_cover_change
        self.urban_development = urban_development

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement land use assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to land use
        pass

class GeologyFactor(EnvironmentalFactor):
    def __init__(self, name, description, geological_features, soil_composition, potential_geological_hazards):
        super().__init__(name, description)
        self.geological_features = geological_features
        self.soil_composition = soil_composition
        self.potential_geological_hazards = potential_geological_hazards

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement geology assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to geology
        pass

class ClimateFactor(EnvironmentalFactor):
    def __init__(self, name, description, expert_person, literature, data_source, legislative, 
                 climate_classification, air_quality, climate_patterns, extreme_weather_events, climate_change_resilience):
        super().__init__(name, description, expert_person, literature, data_source, legislative)
        self.climate_classification = climate_classification
        self.air_quality = air_quality
        self.climate_patterns = climate_patterns
        self.extreme_weather_events = extreme_weather_events
        self.climate_change_resilience = climate_change_resilience

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement climate assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to climate
        pass


class SocialFactor(EnvironmentalFactor):
    def __init__(self, name, description, expert_person, literature, data_source, legislative, 
                 settlements, population_density, demographics, social_impacts, local_economy, cultural_heritage):
        super().__init__(name, description, expert_person, literature, data_source, legislative)
        self.settlements = settlements
        self.population_density = population_density
        self.demographics = demographics
        self.social_impacts = social_impacts
        self.local_economy = local_economy
        self.cultural_heritage = cultural_heritage

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement population assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to population
        pass

class TransportationFactor(EnvironmentalFactor):
    def __init__(self, name, description, transportation_network, traffic_impact, accessibility):
        super().__init__(name, description)
        self.transportation_network = transportation_network
        self.traffic_impact = traffic_impact
        self.accessibility = accessibility

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement transportation assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to transportation
        pass

class ForestryFactor(EnvironmentalFactor):
    def __init__(self, name, description, forest_type, deforestation_risk, impact_on_wildlife_habitat):
        super().__init__(name, description)
        self.forest_type = forest_type
        self.deforestation_risk = deforestation_risk
        self.impact_on_wildlife_habitat = impact_on_wildlife_habitat

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement forestry assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to forestry
        pass

class SpatialPlanningFactor(EnvironmentalFactor):
    def __init__(self, name, description, land_use_planning, zoning, urban_growth_impact):
        super().__init__(name, description)
        self.land_use_planning = land_use_planning
        self.zoning = zoning
        self.urban_growth_impact = urban_growth_impact

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement spatial planning assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to spatial planning
        pass

class NoiseFactor(EnvironmentalFactor):
    def __init__(self, name, description, expert_person, literature, data_source, legislative, noise_increase):
        super().__init__(name, description, expert_person, literature, data_source, legislative)
        self.noise_increase = noise_increase

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement spatial planning assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to spatial planning
        pass

class WasteManagementFactor(EnvironmentalFactor):
    def __init__(self, name, description, expert_person, literature, data_source, legislative, waste_increase):
        super().__init__(name, description, expert_person, literature, data_source, legislative)
        self.waste_increase = waste_increase 

    def describe(self):
        # get data and make text here
        pass

    def assess(self):
        # Implement spatial planning assessment specific to this factor
        pass

    def propose_mitigation(self):
        # Implement mitigation measures specific to spatial planning
        pass