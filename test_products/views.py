from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from test_products.models import Product
from test_products.serializers import ProductSerializer
from rest_framework.decorators import api_view

import redis

redis_client = redis.StrictRedis(host='localhost',
                                port=6379,
                                db=0)

def validate(product_data):
  if not product_data.get('name') or not product_data.get('price') or product_data['price'] < 0 or not product_data.get('stock') or product_data['stock'] < 0 or isinstance(product_data['stock'], float):
    return False
  return True

@api_view(['GET', 'POST'])
def tutorial_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        name = request.GET.get('name', None)
        if name is not None:
            products = products.filter(title__icontains=name)
        products_serializer = ProductSerializer(products, many=True)
        result = []
        for i in range(len(products)):
          redis_result = redis_client.hgetall(products[i].id)
          result.append({
            "name": products[i].name,
            "price": redis_result[b'price'].decode(),
            "stock": redis_result[b'stock'].decode()
          })
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
      product_data = JSONParser().parse(request)
      product_serializer = ProductSerializer(data=product_data)
      if product_serializer.is_valid():
        if not validate(product_data):
          return JsonResponse({'message': 'Invalid data sent!'}, status=status.HTTP_400_BAD_REQUEST)
        product_serializer.save()
        redis_client.hmset(product_serializer.data['id'], { "price": product_data['price'], "stock": product_data['stock'] })
        return JsonResponse({"name": product_serializer.data['name'], "price": product_data['price'], "stock": product_data['stock']}, status=status.HTTP_201_CREATED)
      return JsonResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def tutorial_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return JsonResponse({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        product_serializer = ProductSerializer(product)
        redis_result=redis_client.hgetall(product_serializer.data['id'])
        # return {'price': redis_result[b'']}
        if redis_result:
          return JsonResponse({"name": product_serializer.data['name'],
                            "price": redis_result[b'price'].decode(),
                            "stock": redis_result[b'stock'].decode()})
        return JsonResponse({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND) 