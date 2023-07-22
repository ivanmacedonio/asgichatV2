from django.shortcuts import render
from .models import Box
from django.http import JsonResponse

#view necesaria para traer la data de la consulta de las cajas 
def boxdump(request):

    boxes = Box.objects.all()

    box_data = []

    for box in boxes:
        box_data.append({
            'title': box.title,
            'color': box.color,
            'id': box.id
        })
    
    return JsonResponse(box_data, safe=False)





