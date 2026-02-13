import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import psycopg2

# CONFIGURATION

BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"

API_KEY = os.getenv("SPORTSRADAR_API_KEY")

if not API_KEY:
    raise ValueError("SPORTSRADAR_API_KEY missing in .env file")

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

ENDPOINTS = {
    "competitions": "/competitions.json",
    "complexes": "/complexes.json",
    "double_rankings": "/double_competitors_rankings.json"
}


# DATABASE CONNECTION


@st.cache_resource
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


# GENERIC API FETCH FUNCTION

def fetch_data(name, endpoint):
    url = BASE_URL + endpoint
    response = requests.get(url, headers=HEADERS, timeout=30)

    print(f"\n Fetching {name}")
    print("Status Code:", response.status_code)

    if response.status_code != 200:
        print(" Error:", response.text[:300])
        return None

    return response.json()

# PARSERS

def parse_competitions(data):
    categories = {}
    competitions = []

    for comp in data.get("competitions", []):
        cat = comp.get("category")

        if cat:
            categories[cat["id"]] = cat["name"]

        competitions.append({
            "competition_id": comp.get("id"),
            "competition_name": comp.get("name"),
            "category_id": cat.get("id") if cat else None,
            "parent_id": comp.get("parent_id"),
            "type": comp.get("type"),
            "gender": comp.get("gender"),
            "level": "top-level" if not comp.get("parent_id") else "lower-level"
        })

    return categories, competitions


def parse_complexes(data):
    complexes = []
    venues = []

    for comp in data.get("complexes", []):
        complex_id = comp.get("id")
        complex_name = comp.get("name")

        venue_list = comp.get("venues", [])

        # ✅ Take location from first venue (if exists)
        first_venue = venue_list[0] if venue_list else {}

        complexes.append({
            "complex_id": complex_id,
            "complex_name": complex_name,
            "city": first_venue.get("city_name"),
            "country": first_venue.get("country_name")
        })

        for venue in venue_list:
            venues.append({
                "venue_id": venue.get("id"),
                "venue_name": venue.get("name"),
                "complex_id": complex_id,
                "surface": venue.get("surface"),
                "capacity": venue.get("capacity"),
                "timezone": venue.get("timezone")  
            })

    return complexes, venues



def parse_rankings(data):
    competitors = {}
    rankings = []

    for ranking in data.get("rankings", []):
        ranking_date = ranking.get("date")

        for entry in ranking.get("competitor_rankings", []):
            comp = entry.get("competitor")

            if comp:
                competitors[comp["id"]] = {
                    "competitor_id": comp.get("id"),
                    "competitor_name": comp.get("name"),
                    "country": comp.get("country"),
                    "abbreviation": comp.get("abbreviation")
                }

            rankings.append({
                "competitor_id": comp.get("id") if comp else None,
                "rank": entry.get("rank"),
                "points": entry.get("points"),
                "movement": entry.get("movement"),
                "ranking_date": ranking_date
            })

    return list(competitors.values()), rankings

def insert_categories(categories):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO categories (category_id, category_name)
        VALUES (%s, %s)
        ON CONFLICT (category_id) DO NOTHING;
    """

    for cid, cname in categories.items():
        cur.execute(query, (cid, cname))

    conn.commit()
    cur.close()
    conn.close()
def insert_competitions(competitions):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO competitions
        (competition_id, competition_name, category_id, parent_id, type, gender, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (competition_id) DO NOTHING;
    """

    for c in competitions:
        cur.execute(query, (
            c["competition_id"],
            c["competition_name"],
            c["category_id"],
            c["parent_id"],
            c["type"],
            c["gender"],
            c["level"]
        ))

    conn.commit()
    cur.close()
    conn.close()
def insert_complexes(complexes):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO complexes (complex_id, complex_name, city, country)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (complex_id) DO NOTHING;
    """

    for c in complexes:
        cur.execute(query, (
            c["complex_id"],
            c["complex_name"],
            c["city"],
            c["country"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def insert_venues(venues):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO venues
        (venue_id, venue_name, complex_id, surface, capacity, timezone)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (venue_id) DO NOTHING;
    """

    for v in venues:
        cur.execute(query, (
            v["venue_id"],
            v["venue_name"],
            v["complex_id"],
            v["surface"],
            v["capacity"],
            v["timezone"]
        ))

    conn.commit()
    cur.close()
    conn.close()
def insert_competitors(competitors):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO competitors
        (competitor_id, competitor_name, country, abbreviation)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (competitor_id) DO NOTHING;
    """

    for c in competitors:
        cur.execute(query, (
            c["competitor_id"],
            c["competitor_name"],
            c["country"],
            c["abbreviation"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def insert_rankings(rankings):
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        INSERT INTO competitor_rankings
        (competitor_id, rank, points, movement, ranking_date)
        VALUES (%s, %s, %s, %s, %s);
    """

    for r in rankings:
        cur.execute(query, (
            r["competitor_id"],
            r["rank"],
            r["points"],
            r["movement"],
            r["ranking_date"]
        ))

    conn.commit()
    cur.close()
    conn.close()



# MAIN PIPELINE

def main():
    raw_data = {}

    # -------- Fetch APIs --------
    for name, endpoint in ENDPOINTS.items():
        data = fetch_data(name, endpoint)
        if data:
            raw_data[name] = data

    # -------- Parse Data --------
    categories, competitions = parse_competitions(raw_data["competitions"])
    complexes, venues = parse_complexes(raw_data["complexes"])
    competitors, rankings = parse_rankings(raw_data["double_rankings"])

    insert_categories(categories)
    insert_competitions(competitions)
    insert_complexes(complexes)
    insert_venues(venues)
    insert_competitors(competitors)
    insert_rankings(rankings)

    # -------- Summary --------
    print("\n📊 PARSED DATA SUMMARY")
    print("Categories:", len(categories))
    print("Competitions:", len(competitions))
    print("Complexes:", len(complexes))
    print("Venues:", len(venues))
    print("Competitors:", len(competitors))
    print("Rankings:", len(rankings))

    print("\nSample Competition:", competitions[0])
    print("Sample Venue:", venues[0])
    print("Sample Ranking:", rankings[0])

    # -------- Save Parsed Output --------
    output = {
        "categories": categories,
        "competitions": competitions,
        "complexes": complexes,
        "venues": venues,
        "competitors": competitors,
        "rankings": rankings
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"parsed_tennis_data_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\nParsed data saved to {filename}")
    print("Pipeline completed successfully")

# RUN

if __name__ == "__main__":
    main()
