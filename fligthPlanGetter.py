import aiohttp

ignore_types = ["LATLON"]


async def fetch_popular_flight_plans(
    from_airport: str, to_airport: str
) -> list[dict[str | list]] | str:
    """
    Asynchronously fetch the most popular flight plans between two airports.

    Parameters:
        from_airport (str): The ICAO code of the departure airport.
        to_airport (str): The ICAO code of the destination airport.

    Returns:
        list: A list of dictionaries containing the fetched flight plan details.
    """

    # Convert airport codes to uppercase
    from_airport, to_airport = from_airport.upper(), to_airport.upper()

    # Initialize fetched plans list
    fetched_plans = []

    async with aiohttp.ClientSession() as session:
        # Step 1: Search for Flight Plans
        print(f"Searching for flight plans from {from_airport} to {to_airport}...")
        search_api_url = "https://api.flightplandatabase.com/search/plans"
        search_params = {
            "fromICAO": from_airport,
            "toICAO": to_airport,
            "sort": "popularity",
            "limit": 5,
        }

        async with session.get(search_api_url, params=search_params) as search_response:
            if search_response.status != 200:
                return f"Search failed. HTTP Status Code: {search_response.status}"
            search_results = await search_response.json()

        if not search_results:
            return "No flight plans found."

        # Step 2: Extract IDs of the found flight plans
        plan_ids = [plan["id"] for plan in search_results]
        print(f"Found plans: {plan_ids}")

        # Step 3: Fetch Details for Each Flight Plan
        fetch_api_url = "https://api.flightplandatabase.com/plan/"

        for plan_id in plan_ids:
            print(f"Fetching details for flight plan ID: {plan_id}...")
            async with session.get(fetch_api_url + str(plan_id)) as fetch_response:
                if fetch_response.status != 200:
                    return f"Fetch failed. HTTP Status Code: {fetch_response.status}"

                fetched_plan_details = await fetch_response.json()
                fetched_plans.append(fetched_plan_details)

    # Extract relevant information
    ifr_routes = []
    for plan in fetched_plans:
        ifr_route = {
            "nodes": [
                node
                for node in plan["route"]["nodes"]
                if node["type"] not in ignore_types
            ],
            "notes": plan["notes"],
        }
        ifr_routes.append(ifr_route)

    return ifr_routes
