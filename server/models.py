from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship with Missions model 
    # Since a Mission belongs to a Scientist and a Planet, configure the model to cascade deletes.
    missions = db.relationship('Mission', cascade='all,delete', backref='planet')
    
    # Add serialization rules
    serialize_rules = ('-missions.planet',)

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship with Missions model
    missions = db.relationship('Mission', cascade='all,delete', backref='scientist')
    

    # Add serialization rules
    serialize_rules = ('-missions.scientist',)

    # Add validation for the name field
    @validates('name')
    def validate_name(self, key, name):
        print('Inside teh name validation')
        if not name or len(name) < 1:
            raise ValueError('Name must exist')
        return name
    
    # Add validation for the field_of_study
    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        print('Inside the field_of_study validation')
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError('must enter a field_of_study')
        return field_of_study
    
    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}, field: {self.field_of_study}'



class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships with Planet and Scientist using ForeignKeys (plural)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)

    # Add serialization rules
    serialize_rules = ('-scientist.missions', '-planet.missions')
    
    # Add validation for name
    @validates('name')
    def validate_name(self, key, name):
        print('Inside the name validation')
        if not name or len(name) < 1:
            raise ValueError('must enter a name')
        return name
    
    # Add validation for scientist_id
    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        print('Inside the scientist_id validation')
        if not scientist_id:
            raise ValueError('must enter a scientist_id')
        return scientist_id
    
    # Add validation for planet_id
    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        print('Inside the planet_id validation')
        if not planet_id:
            raise ValueError('must enter a planet_id')
        return planet_id
    
    def __repr__(self):
        return f'Mission {self.id} {self.name} {self.scientist_id} {self.planet_id}'

# add any models you may need.
