from flask_marshmallow import Marshmallow

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user', 'password')


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'year', 'director',
                  'repart', 'genre', 'trailer')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)