from django.shortcuts import render
import math

from parks.models import Park, Comment


def contact(request):
    return render(request, 'main/contact.html')


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)


def home(request):
    parks = Park.objects.all()
    parks_list = []

    location_input = request.GET.get("location") or ''
    search_res = search_output(location_input)

    myLocation = [40.4075421676875, 49.86160992233112]

    for park in parks:
        comments = Comment.objects.filter(park=park)
        parks_list.append([park, distance(myLocation, [park.lat, park.lng]), comments])

    context = {
        "parks": parks_list,
        "search_res": search_res,
    }

    print(search_res)
    
    return render(request, "main/home.html", context)


def distance(coord1, coord2):
    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    R = 6371.0

    # Calculate the result
    distance = R * c
    return round(distance, 2)


def search_output(location_input):
    if location_input:
        results = Park.objects.filter(city__icontains=location_input)
        if len(results) > 0:
            return results
        
    return []    
