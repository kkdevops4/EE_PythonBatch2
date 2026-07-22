import requests


class OSRMService:

    BASE_URL = "https://router.project-osrm.org/route/v1/driving"

    def get_route(self, start, end):
        """
        Fetch driving route between two GPS coordinates.

        Parameters:
            start = (latitude, longitude)
            end = (latitude, longitude)

        Returns:
            List of (latitude, longitude) coordinates.
        """

        start_lat, start_lon = start
        end_lat, end_lon = end

        url = (
            f"{self.BASE_URL}/"
            f"{start_lon},{start_lat};"
            f"{end_lon},{end_lat}"
            f"?overview=full&geometries=geojson"
        )

        response = requests.get(url)

        if response.status_code != 200:
            return []

        data = response.json()

        routes = data.get("routes")

        if not routes:
            return []

        geometry = routes[0]["geometry"]["coordinates"]

        # Convert (longitude, latitude) → (latitude, longitude)
        route = []

        for lon, lat in geometry:
            route.append((lat, lon))

        return route