import random
from datetime import datetime, timedelta


def run_sql(sql_query: str):
    print('Running SQL query:', sql_query)

    # Mocked response
    mocked_response = [
        (1, "John Doe", "john@example.com"),
        (2, "Jane Smith", "jane@example.com"),
        (3, "Bob Johnson", "bob@example.com")
    ]

    # Simulate successful query execution
    return f"query results {mocked_response}"


def get_flight_data(originLocationCode, destinationLocationCode, departureDate,
                    returnDate=None, adults=1, children=None, infants=None, travelClass=None,
                    includedAirlineCodes=None, excludedAirlineCodes=None, nonStop="false",
                    currencyCode="USD", maxPrice=None, max=5):
    print(f"""Requesting flight data (mocked): originLocationCode: {originLocationCode}, 
          destinationLocationCode:{destinationLocationCode}, departureDate:{departureDate},
          returnDate:{returnDate}, adults:{adults}, children:{children}, infants: {infants}, 
          travelClass: {travelClass}, includedAirlineCodes: {includedAirlineCodes}, excludedAirlineCodes:{excludedAirlineCodes},
          nonStop: {nonStop}, currencyCode: {currencyCode}, maxPrice: {maxPrice}""")

    # Helper function to generate random flight data
    def generate_flight_data(dep_code, arr_code, dep_date):
        flight_offer_id = random.randint(1000, 9999)
        price = random.randint(500, 2000)
        duration = timedelta(hours=random.randint(4, 12))
        dep_time = datetime.strptime(
            dep_date, "%Y-%m-%d") + timedelta(hours=random.randint(0, 23))
        arr_time = dep_time + duration
        return {
            "FlightOfferID": flight_offer_id,
            "TotalPrice": price,
            "Currency": currencyCode,
            "ItineraryID": random.randint(10000, 99999),
            "Duration": str(duration),
            "DepartureIATACode": dep_code,
            "ArrivalIATACode": arr_code,
            "DepartureTime": dep_time.isoformat(),
            "ArrivalTime": arr_time.isoformat(),
            "NumberOfStops": random.choice([0, 1]),
            "CarrierCode": random.choice(["QF", "TG", "SQ", "EK"]),
            "FlightNumber": str(random.randint(100, 999)),
            "AircraftCode": random.choice(["788", "789", "350", "777"])
        }

    outbound_flight = generate_flight_data(
        originLocationCode, destinationLocationCode, departureDate)

    if returnDate:
        return_flight = generate_flight_data(
            destinationLocationCode, originLocationCode, returnDate)
        total_trip_price = outbound_flight["TotalPrice"] + \
            return_flight["TotalPrice"]

        return {
            "FlightOfferID": outbound_flight["FlightOfferID"],
            "TotalTripPrice": total_trip_price,
            "Currency": currencyCode,
            "OutboundItineraryID": outbound_flight["ItineraryID"],
            "OutboundDuration": outbound_flight["Duration"],
            "OutboundDepartureIATACode": outbound_flight["DepartureIATACode"],
            "OutboundArrivalIATACode": outbound_flight["ArrivalIATACode"],
            "OutboundDepartureTime": outbound_flight["DepartureTime"],
            "OutboundArrivalTime": outbound_flight["ArrivalTime"],
            "OutboundNumberOfStops": outbound_flight["NumberOfStops"],
            "OutboundCarrierCode": outbound_flight["CarrierCode"],
            "OutboundFlightNumber": outbound_flight["FlightNumber"],
            "OutboundAircraftCode": outbound_flight["AircraftCode"],
            "ReturnItineraryID": return_flight["ItineraryID"],
            "ReturnDuration": return_flight["Duration"],
            "ReturnDepartureIATACode": return_flight["DepartureIATACode"],
            "ReturnArrivalIATACode": return_flight["ArrivalIATACode"],
            "ReturnDepartureTime": return_flight["DepartureTime"],
            "ReturnArrivalTime": return_flight["ArrivalTime"],
            "ReturnNumberOfStops": return_flight["NumberOfStops"],
            "ReturnCarrierCode": return_flight["CarrierCode"],
            "ReturnFlightNumber": return_flight["FlightNumber"],
            "ReturnAircraftCode": return_flight["AircraftCode"]
        }
    else:
        return outbound_flight
