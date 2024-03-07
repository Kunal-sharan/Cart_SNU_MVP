import streamlit as st
import streamlit.components.v1 as components
import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

print("Screen width:", screen_width)

st.header("Cart_EXPO")
source_code="""<html>
  <head>
    <script src="https://api.tiles.mapbox.com/mapbox-gl-js/v3.1.0/mapbox-gl.js"></script>
    <link
      href="https://api.tiles.mapbox.com/mapbox-gl-js/v3.1.0/mapbox-gl.css"
      rel="stylesheet"
    />
    
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v3.1.2/mapbox-gl.css"
      rel="stylesheet"
    />
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.1.2/mapbox-gl.js"></script>
  </head>
  <body>
    <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.2.0/mapbox-gl-directions.js"></script>
    <!-- Include fingerprint.js library -->
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fingerprintjs2/2.1.0/fingerprint2.min.js"></script>
    <link
      rel="stylesheet"
      href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.2.0/mapbox-gl-directions.css"
      type="text/css"
    />
    <p>Click the button to get your coordinates:</p>

    <button onclick="getLocation()">Try It</button>

    <p id="demo"></p>
    <p id="distance"></p>
    <p id="mapbox_dist"></p>
    <p id="speed"></p>
    <p id="travelTime"></p>
    <button onclick="getID()">GetID</button>
    <p id="mylocid"></p>
    <button onclick="stop()">Stop</button>
    
    <div
      id="map"
      style="width: 100%; height: 60%; float: left; margin-right: 20px"
    ></div>

    <script>
      var x = document.getElementById("demo");
      var j=document.getElementById("jainamLATLONG");
      var d = document.getElementById("distance");
      var m = document.getElementById("mapbox_dist");
      var spd = document.getElementById("speed");
      var time = document.getElementById("travelTime");
      var i = document.getElementById("mylocid");
      let watchID = null; //watchId for Geolocation API
      let ID_loc = null;
      // Generate a fingerprint
      // Initialize the agent on page load.

      function getID() {
        const fpPromise = import(
          "https://fpjscdn.net/v3/7z2gqZnHm9vyCMwMDeH9"
        ).then((FingerprintJS) =>
          FingerprintJS.load({
            region: "ap",
          })
        );

        // Get the visitorId when you need it.
        fpPromise
          .then((fp) => fp.get())
          .then((result) => {
            const visitorId = result.visitorId;
            console.log(visitorId);
            ID_loc = visitorId;
            i.innerHTML = "MY ID: " + ID_loc;
          });
      }

      function degreesToRadians(degrees) {
        return (degrees * Math.PI) / 180;
      }
      // Function to calculate the distance between two points
      function calculateDistance(lat1, lon1, lat2, lon2) {
        var earthRadiusKm = 6371;

        var dLat = degreesToRadians(lat2 - lat1);
        var dLon = degreesToRadians(lon2 - lon1);

        lat1 = degreesToRadians(lat1);
        lat2 = degreesToRadians(lat2);

        var a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.sin(dLon / 2) *
            Math.sin(dLon / 2) *
            Math.cos(lat1) *
            Math.cos(lat2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return earthRadiusKm * c;
      }
      mapboxgl.accessToken =
        "pk.eyJ1IjoiZHJhc3RpY2MxbmsiLCJhIjoiY2xtcXJpZzJmMDBkODJzbXloajQzdXd4NyJ9.xKoQBVmU8LiaOy0WJ2sHsg"; // Replace with your Mapbox access token // Replace with your Mapbox access token // Replace with your Mapbox access token // Replace with your Mapbox access token
      const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/satellite-streets-v12",
        center: [77.5709, 28.5253307], // starting position in [longitude, latitude] format
        zoom: 17,
      });

      // an arbitrary start will always be the same
      // only the end or destination will change
      const start = [77.5709, 28.5253307]; // in [longitude, latitude] format
      let endCoords = start; // initialize end coordinates with start coordinates

      async function getRoute(start, end) {
        // make a directions request using cycling profile
        const query = await fetch(
          `https://api.mapbox.com/directions/v5/mapbox/walking/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
          { method: "GET" }
        );
        const json = await query.json();
        const data = json.routes[0];
        const route = data.geometry.coordinates;
        const geojson = {
          type: "Feature",
          properties: {},
          geometry: {
            type: "LineString",
            coordinates: route,
          },
        };
        // if the route already exists on the map, we'll reset it using setData
        if (map.getSource("route")) {
          map.getSource("route").setData(geojson);
        }
        // otherwise, we'll make a new request
        else {
          map.addLayer({
            id: "route",
            type: "line",
            source: {
              type: "geojson",
              data: geojson,
            },
            layout: {
              "line-join": "round",
              "line-cap": "round",
            },
            paint: {
              "line-color": "#3887be",
              "line-width": 5,
              "line-opacity": 1,
            },
          });
        }

        // Add marker for end point
        new mapboxgl.Marker({ color: "#ff0000" })
          .setLngLat(end)
          .addTo(map)
          .setPopup(new mapboxgl.Popup().setHTML("<h3>You</h3>"));
      }

      map.on("load", () => {
        // make an initial directions request that
        // starts and ends at the same location
        getRoute(start, start);

        // Add marker for start point
        new mapboxgl.Marker()
          .setLngLat(start)
          .addTo(map)
          .setPopup(new mapboxgl.Popup().setHTML("<h1>GIR 3A</h1>"));
      });
        
      // Use the Geolocation API to get the current position
     
      function getLocation() {
        if (navigator.geolocation) {
          if (watchID !== null) {
            navigator.geolocation.clearWatch(watchID);
          }
          watchID = navigator.geolocation.watchPosition(showPosition);
        } else {
          x.innerHTML = "Geolocation is not supported by this browser.";
        }
      }
      

      function stop() {
        if (watchID !== null) {
          navigator.geolocation.clearWatch(watchID);
          d.innerHTML = "Stopped";
          m.innerHTML = "Stopped";
          spd.innerHTML = "Stopped";
          time.innerHTML = "N/A";
          watchID = null;
          ID_loc = JSON.stringify(navigator.geolocation);
          i.innerHTML = ID_loc;
          ID_loc = null;

        }
      }

      function showPosition(position) {
        let s = null;
        let e = null;
        let coords = [position.coords.longitude, position.coords.latitude];
        x.innerHTML =
          "Latitude: " +
          position.coords.latitude +
          "<br>Longitude: " +
          position.coords.longitude;
        dist = calculateDistance(
          start[1],
          start[0],
          position.coords.latitude,
          position.coords.longitude
        );
        s = new mapboxgl.LngLat(start[0], start[1]);
        e = new mapboxgl.LngLat(
          position.coords.longitude,
          position.coords.latitude
        );
        disMapbox = s.distanceTo(e);
        i.innerHTML = "MY ID: " + ID_loc;
        d.innerHTML = "distance(from GIR 3A HOSTEL) : " + dist * 1000 + " m";
        m.innerHTML = "distance(mapBox): " + disMapbox + " meters";
        spd.innerHTML = "Speed:" + position.coords.speed + " m/s";
        if (position.coords.speed !== null || position.coords.speed !== 0) {
          time.innerHTML =
            "Time(Mapbox): " + (dist * 1000) / position.coords.speed + " sec";
        }
        endCoords = coords; // update the end coordinates
        getRoute(start, endCoords); // update the route
      }
    </script>
  </body>
</html>
"""
components.html(source_code,width=screen_width,height=screen_height)