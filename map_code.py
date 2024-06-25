import folium
import json

#Starting the map above Florida
m = folium.Map(location=[27.994402, -81.760254], zoom_start=7)

with open("Resources/camera_list.json" , "r") as f:
    data = json.load(f)
    for cam in data:
        camera_lat = cam["latitude"]
        camera_lon = cam["longitude"]
        folium.Marker(
            location=[camera_lat, camera_lon],
            popup=f"{cam['description1']},{cam['description2']}",
            icon=folium.Icon(icon="camera")
                    ).add_to(m)

m.save("Resources/map.html")