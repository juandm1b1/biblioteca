from rest_framework import serializers
from apps.libro.models import Autor, Libro


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','nombre','apellido']
        model = Autor

class LibroSerializer(serializers.ModelSerializer):
    autor_id = AutorSerializer(many=True)
    class Meta:
        fields = ['titulo','autor_id']
        model = Libro

    # def listar(self,validated_data):
    #     autores_data = validated_data.pop('autor_id')
    #     libro = Libro.objects.filter(**validated_data)
    #     for autor_data in autores_data:
    #         Autor.objects.filter(libro=libro,**autor_data)
    #         return libro