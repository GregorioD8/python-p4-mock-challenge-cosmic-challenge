
from app import app
from models import db, Planet, Scientist, Mission
import os

def create_scientists():
    scientists = [
        Scientist(name="Alice Smith", field_of_study="Chemistry"),
        Scientist(name="Bob Johnson", field_of_study="Computer Science"),
        Scientist(name="Charlie Brown", field_of_study="Botany"),
        Scientist(name="David Wilson", field_of_study="Marine Biology"),
        Scientist(name="Eva Green", field_of_study="Physics"),
        Scientist(name="Marcus Aldrin", field_of_study="Astrophysics"),
    ] 
    return scientists

def create_planets():
    planets = [
        Planet(name="Proxima Centauri b", distance_from_earth=3, nearest_star="Proxima Centauri"),
        Planet(name="Epsilon Eridani b", distance_from_earth=7, nearest_star="Epsilon Eridani"),
        Planet(name="Ross 128 b", distance_from_earth=5, nearest_star="Ross 128"),
        Planet(name="61 Virginis b", distance_from_earth=12, nearest_star="61 Virginis"),
        Planet(name="Wolf 1069 b", distance_from_earth=31, nearest_star="Wolf 1069"),
        Planet(name="Kepler 186 f", distance_from_earth=31, nearest_star="Kepler 186"),
    ]
    return planets

def create_missions(scientists, planets):
    missions = []
    missions.append(Mission(name="Mission 1", scientist_id=scientists[0].id, planet_id=planets[0].id))
    missions.append(Mission(name="Mission 2", scientist_id=scientists[1].id, planet_id=planets[1].id))
    missions.append(Mission(name="Mission 3", scientist_id=scientists[2].id, planet_id=planets[2].id))
    missions.append(Mission(name="Mission 4", scientist_id=scientists[3].id, planet_id=planets[3].id))
    missions.append(Mission(name="Mission 5", scientist_id=scientists[4].id, planet_id=planets[4].id))
    missions.append(Mission(name="Mission 6", scientist_id=scientists[5].id, planet_id=planets[5].id))
    return missions

if __name__ == '__main__':
    if os.path.exists('app.db'):
        os.remove('app.db')

    with app.app_context():
        print('Creating a new database...')
        db.create_all()

        print("Seeding scientists...")
        scientists = create_scientists()
        db.session.add_all(scientists)
        db.session.commit()

        print("Seeding planets...")
        planets = create_planets()
        db.session.add_all(planets)
        db.session.commit()

        print("Seeding missions...")
        planets = Planet.query.all()
        scientists = Scientist.query.all()
        missions = create_missions(planets, scientists)
        db.session.add_all(missions)
        db.session.commit()

        print("Done seeding!")
