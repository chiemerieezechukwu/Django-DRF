from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import Car
from .services import (
    add_rating_to_car,
    create_save_car_object,
    delete_car_entry,
    retrieve_cars_queryset,
    retrieve_cars_queryset_order_desc,
    retrieve_unique_car_object_to_api,
)


class CarsAPI(APIView):
    class InputSerializer(serializers.Serializer):
        make = serializers.CharField()
        model = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Car
            fields = ["id", "make", "model", "avg_rating"]

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        make, model = serializer.validated_data.values()

        res, status_code = create_save_car_object(make, model)
        if status_code == status.HTTP_201_CREATED:
            res = self.OutputSerializer(res).data
        return Response(data=res, status=status_code)

    def get(self, _):
        queryset = retrieve_cars_queryset()
        res = self.OutputSerializer(queryset, many=True).data
        return Response(data=res, status=status.HTTP_200_OK)


class CarDetailsAPI(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Car
            fields = ["id", "make", "model", "avg_rating"]

    def get(self, _, car_id):
        res, status_code = retrieve_unique_car_object_to_api(car_id)
        res = self.OutputSerializer(res).data
        return Response(data=res, status=status_code)

    def delete(self, _, car_id):
        res, status_code = delete_car_entry(car_id)
        return Response(data=res, status=status_code)


class CarRatingAPI(APIView):
    class InputSerializer(serializers.Serializer):
        car_id = serializers.IntegerField()
        rating = serializers.IntegerField(min_value=1, max_value=5)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car_id, rating = serializer.validated_data.values()

        res, status_code = add_rating_to_car(car_id, rating)
        return Response(data=res, status=status_code)


class PopularCars(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Car
            fields = ["id", "make", "model", "rates_number"]

    def get(self, _):
        queryset = retrieve_cars_queryset_order_desc(order_by="rates_number")
        res = self.OutputSerializer(queryset, many=True).data
        return Response(data=res, status=status.HTTP_200_OK)
