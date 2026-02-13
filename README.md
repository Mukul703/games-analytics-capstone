# Games Analytics Capstone Project

## Project Overview
The **Games Analytics Capstone Project** delivers an enterprise-style analytics solution for structured exploration and analysis of professional tennis competition data. Built on top of the SportRadar API, the project transforms raw, nested JSON event data into a relational analytics layer and an interactive dashboard, enabling clear visibility into competition hierarchies, venues, and competitor performance. The solution is designed to support analytical discovery, benchmarking, and decision-making in sports analytics environments.

---

## Business Context & Objective
In sports analytics, stakeholders require structured, reliable, and easily explorable data to understand competition formats, participant performance, and event distribution across regions and levels. Raw API data alone is insufficient for analysis due to its nested and unstructured nature.

**Business need addressed:**
- Convert complex sports event data into an analytics-ready format  
- Enable interactive exploration of tournaments, venues, and competitors  
- Support analytical questions around rankings, participation, and competition structure  

**Primary Objective:**  
Build an **end-to-end tennis analytics platform** that extracts SportRadar competition data, stores it in a relational database, applies analytical logic via SQL, and delivers insights through an interactive Streamlit dashboard.

---

## Dataset Summary
- **Source:** SportRadar API  
- **Domain:** Tennis / Sports Analytics  
- **Scope:**  
  - Competition hierarchy (parent and sub-competitions)  
  - Venues, complexes, cities, and countries  
  - Competitor profiles, rankings, and points  

- **Data Characteristics:**  
  - Raw nested JSON responses  
  - Parsed and normalized into structured relational tables  
  - Designed to support hierarchical and comparative analysis  

- **Constraints:**  
  - Data availability limited to SportRadar free trial API scope  

---

## Analytical Approach
The project follows a production-style analytics workflow focused on clarity, scalability, and analytical usability:

- Designed an automated **data ingestion pipeline** to fetch competition data from the SportRadar API  
- Parsed and normalized raw JSON into structured entities reflecting real-world sports hierarchies  
- Modeled relational tables to support joins across competitions, venues, and competitors  
- Applied **SQL-driven analysis** to derive rankings, category distributions, and hierarchy insights  
- Built a **Streamlit dashboard** to surface insights through interactive filters and visual summaries  

The approach prioritizes **decision support and structured exploration** rather than exploratory experimentation.

---

## Tools & Technologies
- **Python:** API integration, JSON parsing, and data transformation  
- **PostgreSQL:** Relational data modeling and structured storage  
- **SQL:** Analytical querying, aggregations, and hierarchy analysis  
- **Pandas:** Data manipulation and preprocessing  
- **Streamlit:** Interactive analytics dashboard  
- **Plotly:** Dynamic, business-friendly visualizations  

---

## Key Insights
- Major venue hubs include **Buenos Aires Lawn Tennis Club (30 venues)**, **National Tennis Center Kazakhstan (25)**, and **Melbourne Park Australia (25)**.  
- **Top-ranked competitor:** Katerina Siniakova (#1, Czechia, 9,530 points).  
- Dataset captures **~1,000 competitors across 78 countries**, reflecting strong global participation.  
- **ITF Men (2,198)** and **ITF Women (2,032)** are the most active competition categories.  
- Parent-to-sub competition mapping enables structured analysis of event formats (e.g., Singles vs Doubles).  
- Venue data is normalized across complex, city, and country levels, enabling location-based analytics.

---

## Business Impact & Use Cases
This solution enables:
- Interactive exploration of competitions across hierarchical levels  
- Trend analysis by competition type, category, and gender  
- Player participation and ranking analysis across events  
- Decision support for event organizers, federations, and sports analytics teams  

The analytical framework can be extended to other sports domains and event-based analytics use cases.

---

## Limitations & Future Enhancements
**Current Limitations:**
- Data restricted to SportRadar free trial API endpoints  

**Planned Enhancements:**
- Integration of additional SportRadar endpoints (matches, player profiles)  
- Automated data refresh through scheduled pipelines  
- Enhanced dashboard filters and cross-dimensional analysis  
- Automated ranking and competition update workflows  

---

## Repository Structure


