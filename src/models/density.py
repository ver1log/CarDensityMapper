def define_density_table(db):
    class DensityTable(db.Model):
        zipcode = db.Column(db.Integer, primary_key=True)
        x = db.Column(db.Float)
        y = db.Column(db.Float)
        area = db.Column(db.Float)
        number_of_vehicles = db.Column(db.Integer)
        color = db.Column(db.String(20))
        city_name = db.Column(db.String(20))
        jsonboundries = db.Column(db.String)

    return DensityTable