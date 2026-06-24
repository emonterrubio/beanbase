"""
Seed canonical coffee origin rows into the origins table.
Run from the project root with the api venv active:

    source api/.venv/bin/activate
    python db/seeds/seed_origins.py
"""

import os
import sys
from pathlib import Path

# Allow imports from api/
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "api"))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

load_dotenv(Path(__file__).parent.parent.parent / "api" / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/beanbase")

ORIGINS = [
    # (country, region, lat, lon, alt_min, alt_max, harvest_start, harvest_end, varietals, flavor_tags, notes)
    ("Ethiopia", None, 9.1, 40.5, 1700, 2200, 10, 2, ["Heirloom", "JARC varieties"], ["Blueberry", "Jasmine", "Citrus", "Floral"], "Birthplace of Arabica. Yirgacheffe and Sidama are the prestige subregions."),
    ("Ethiopia", "Yirgacheffe", 6.1, 38.2, 1800, 2200, 10, 1, ["Heirloom"], ["Blueberry", "Bergamot", "Jasmine", "Lemon"], "Yirgacheffe produces some of the world's most floral washed coffees."),
    ("Ethiopia", "Sidama", 6.7, 38.4, 1550, 2200, 10, 1, ["Heirloom"], ["Peach", "Apricot", "Jasmine", "Berry"], None),
    ("Ethiopia", "Guji", 5.6, 38.5, 1700, 2100, 10, 1, ["Heirloom"], ["Blueberry", "Dark Chocolate", "Tropical Fruit"], None),
    ("Kenya", None, -0.02, 37.9, 1500, 2100, 10, 12, ["SL28", "SL34", "Ruiru 11", "Batian"], ["Blackcurrant", "Tomato", "Citrus", "Winey"], "Kenya's auction system (Nairobi Coffee Exchange) is world-renowned."),
    ("Kenya", "Nyeri", -0.4, 36.9, 1700, 2000, 10, 12, ["SL28", "SL34"], ["Blackcurrant", "Grapefruit", "Winey", "Complex"], "Nyeri is Kenya's most prestigious subregion."),
    ("Colombia", None, 4.6, -74.1, 1200, 2000, 3, 12, ["Castillo", "Caturra", "Colombia", "Geisha"], ["Caramel", "Red Apple", "Citrus", "Milk Chocolate"], "Two harvest seasons (main Oct-Feb, fly crop Apr-Jun) in many regions."),
    ("Colombia", "Huila", 2.5, -75.5, 1500, 2000, 9, 12, ["Castillo", "Caturra", "Geisha"], ["Stone Fruit", "Brown Sugar", "Caramel", "Citrus"], "Huila is Colombia's top auction-performing subregion."),
    ("Colombia", "Nariño", 1.2, -77.3, 1800, 2300, 5, 8, ["Castillo", "Caturra"], ["Citrus", "Panela", "Floral"], None),
    ("Guatemala", None, 15.8, -90.2, 1200, 2000, 11, 4, ["Bourbon", "Caturra", "Catuai", "Geisha"], ["Chocolate", "Brown Sugar", "Dried Fruit", "Caramel"], None),
    ("Guatemala", "Antigua", 14.6, -90.7, 1500, 1700, 11, 2, ["Bourbon", "Caturra", "Catuai"], ["Spice", "Dark Chocolate", "Tobacco", "Caramel"], "Antigua's volcanic soil produces classic heavy-bodied coffees."),
    ("Guatemala", "Huehuetenango", 15.3, -91.5, 1500, 2100, 11, 4, ["Bourbon", "Caturra", "Catuai", "Geisha"], ["Peach", "Citrus", "Brown Sugar", "Wine"], None),
    ("Panama", None, 8.9, -79.5, 1200, 1800, 11, 3, ["Geisha", "Bourbon", "Caturra", "Typica"], ["Jasmine", "Bergamot", "Citrus", "Tropical"], "Home of Geisha variety and Best of Panama auction."),
    ("Panama", "Boquete", 8.8, -82.4, 1400, 1800, 11, 3, ["Geisha", "Bourbon"], ["Jasmine", "Bergamot", "Peach", "Orange Blossom"], "Boquete produces the world's most expensive auction coffees."),
    ("Costa Rica", None, 9.7, -83.8, 1200, 1800, 10, 3, ["Caturra", "Catuai", "Geisha", "Villa Sarchi"], ["Citrus", "Brown Sugar", "Honey", "Clean"], "Strict quality regulations make Costa Rica consistently clean."),
    ("Honduras", None, 15.2, -86.2, 1000, 1800, 11, 4, ["Catuai", "Lempira", "IHCAFE 90", "Caturra"], ["Citrus", "Caramel", "Brown Sugar", "Tropical"], None),
    ("El Salvador", None, 13.8, -88.9, 1100, 1800, 11, 3, ["Bourbon", "Pacas", "Pacamara", "Catuai"], ["Brown Sugar", "Peach", "Milk Chocolate", "Floral"], "Known for Bourbon and the unique Pacamara varietal."),
    ("Mexico", None, 23.6, -102.5, 900, 1800, 11, 4, ["Typica", "Bourbon", "Caturra", "Maragogype"], ["Chocolate", "Nut", "Citrus", "Brown Sugar"], None),
    ("Peru", None, -9.2, -75.0, 1200, 2000, 6, 9, ["Typica", "Caturra", "Bourbon", "Geisha"], ["Caramel", "Citrus", "Milk Chocolate", "Clean"], None),
    ("Bolivia", None, -16.3, -63.6, 1200, 2000, 5, 8, ["Caturra", "Typica", "Catuai"], ["Citrus", "Chocolate", "Brown Sugar"], "High altitude potential but limited infrastructure."),
    ("Brazil", None, -14.2, -51.9, 800, 1400, 5, 9, ["Yellow Bourbon", "Catuai", "Mundo Novo", "Red Bourbon"], ["Chocolate", "Nut", "Caramel", "Low Acid"], "World's largest coffee producer. Natural process dominates."),
    ("Brazil", "Cerrado Mineiro", -18.5, -46.0, 850, 1100, 5, 9, ["Yellow Bourbon", "Catuai", "Acaiá"], ["Caramel", "Chocolate", "Almond", "Full Body"], "Brazil's first coffee region with a denomination of origin."),
    ("Brazil", "Sul de Minas", -21.5, -45.5, 800, 1300, 5, 9, ["Red Bourbon", "Catuai", "Mundo Novo"], ["Chocolate", "Brown Sugar", "Vanilla"], None),
    ("Indonesia", None, -0.8, 113.9, 1000, 1700, 10, 3, ["Typica", "Catimor", "Linie S"], ["Earthy", "Cedar", "Tobacco", "Dark Chocolate"], "Wet-hulled (Giling Basah) process gives distinctive earthy character."),
    ("Indonesia", "Sumatra", 0.5, 101.4, 1000, 1600, 10, 3, ["Typica", "Catimor"], ["Earthy", "Mushroom", "Cedar", "Dark Chocolate", "Full Body"], "Sumatra Mandheling and Gayo are the most recognized subregions."),
    ("Yemen", None, 15.6, 48.5, 1400, 2600, 10, 2, ["Udaini", "Dawairi", "Ismaili"], ["Dried Fruit", "Spice", "Wine", "Dark Chocolate"], "Ancient coffee cultivation. Rare, expensive, naturally processed."),
    ("Rwanda", None, -1.9, 29.9, 1700, 2000, 3, 6, ["Red Bourbon"], ["Black Tea", "Hibiscus", "Citrus", "Stone Fruit"], "Bourbon dominant. Cup of Excellence program has elevated quality."),
    ("Burundi", None, -3.4, 29.9, 1500, 2000, 3, 6, ["Red Bourbon"], ["Citrus", "Black Tea", "Peach", "Juicy"], None),
    ("Uganda", None, 1.4, 32.3, 1200, 2000, 10, 2, ["SL14", "SL28", "Drago"], ["Chocolate", "Black Pepper", "Fruity"], "Mt. Elgon and Rwenzori regions produce notable specialty lots."),
    ("Tanzania", None, -6.4, 34.9, 1400, 2000, 7, 10, ["SL28", "N39", "Kent", "Bourbon"], ["Black Tea", "Citrus", "Winey", "Dark Chocolate"], None),
]


def run():
    engine = create_engine(DATABASE_URL)

    with Session(engine) as session:
        existing = session.execute(text("SELECT COUNT(*) FROM origins")).scalar()
        if existing > 0:
            print(f"origins table already has {existing} rows — skipping seed.")
            return

        rows_inserted = 0
        for (country, region, lat, lon, alt_min, alt_max, h_start, h_end, varietals, flavor_tags, notes) in ORIGINS:
            session.execute(
                text("""
                    INSERT INTO origins
                        (country, region, latitude, longitude, altitude_min_m, altitude_max_m,
                         harvest_start_month, harvest_end_month, dominant_varietals, flavor_tags, notes)
                    VALUES
                        (:country, :region, :lat, :lon, :alt_min, :alt_max,
                         :h_start, :h_end, :varietals, :flavor_tags, :notes)
                """),
                {
                    "country": country, "region": region, "lat": lat, "lon": lon,
                    "alt_min": alt_min, "alt_max": alt_max, "h_start": h_start, "h_end": h_end,
                    "varietals": varietals, "flavor_tags": flavor_tags, "notes": notes,
                }
            )
            rows_inserted += 1

        session.commit()
        print(f"Seeded {rows_inserted} origin rows.")


if __name__ == "__main__":
    run()
