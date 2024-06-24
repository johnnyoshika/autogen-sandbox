get_flight_data_function = {
    "name": "get_flight_data",
    "description": "Pulls the flight data from the amadeus server and saves it to the neon database.",
    "parameters": {
        "type": "object",
        "properties": {
            "originLocationCode": {
                "type": "string",
                "description": "City/airport IATA code from which the traveler will depart, e.g., BOS for Boston"
            },
            "destinationLocationCode": {
                "type": "string",
                "description": "City/airport IATA code to which the traveler is going, e.g., PAR for Paris"
            },
            "departureDate": {
                "type": "string",
                "description": "The date on which the traveler will depart from the origin to go to the destination, in YYYY-MM-DD format"
            },
            "returnDate": {
                "type": "string",
                "description": "The date on which the traveler will return from the destination to the origin, in YYYY-MM-DD format"
            },
            "adults": {
                "type": "integer",
                "description": "The number of adult travelers (age 12 or older on the date of departure)"
            },
            "children": {
                "type": "integer",
                "description": "The number of child travelers (older than age 2 and younger than age 12 on the date of departure)"
            },
            "infants": {
                "type": "integer",
                "description": "The number of infant travelers (age 2 or younger on the date of departure)"
            },
            "travelClass": {
                "type": "string",
                "description": "Travel class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)"
            },
            "includedAirlineCodes": {
                "type": "string",
                "description": "IATA airline codes to include, comma-separated"
            },
            "excludedAirlineCodes": {
                "type": "string",
                "description": "IATA airline codes to exclude, comma-separated"
            },
            "nonStop": {
                "type": "string",
                "description": "If set to 'true', only non-stop flights are considered"
            },
            "currencyCode": {
                "type": "string",
                "description": "Preferred currency for the flight offers, in ISO 4217 format"
            },
            "maxPrice": {
                "type": "integer",
                "description": "Maximum price per traveler"
            },
            "max": {
                "type": "integer",
                "description": "Maximum number of flight offers to return"
            }
        },
        "required": ["originLocationCode", "destinationLocationCode", "departureDate", "adults"]
    }
}

run_sql_function = {
    "name": "run_sql",
    "description": "Runs a SQL query against the flights_data database",
    "parameters": {
        "type": "object",
        "properties": {
            "sql_query": {
                "type": "string",
                "description": "The sql query required to pull the data needed to answer the initial query"
            }
        },
        "required": ["sql_query"]
    }
}

all_functions = [
    get_flight_data_function,
    run_sql_function
]

get_flight_data_functions = [
    get_flight_data_function
]

run_sql_functions = [
    run_sql_function
]
