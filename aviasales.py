from datetime import datetime

ALPH = 'abcdefghijklmnopqrstuvwxyz'
SEP_LEN = 30
CHECK_DAY_TIME = {
    "утро": lambda time: 5 <= time.hour < 12,
    "день": lambda time: 12 <= time.hour < 18,
    "вечер": lambda time: 18 <= time.hour < 24,
    "ночь": lambda time: 0 <= time.hour < 5,
    "": lambda time: True,
}


class ServiceLevel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Airport:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Flight:
    def __init__(self, departure: Airport, arrival: Airport, date: datetime, flight_number: str):
        self.departure = departure
        self.arrival = arrival
        self.date = date
        self.flight_number = flight_number
        self.seating_configuration: list[tuple[ServiceLevel, str]] = []
        self.total_seats = 0
        self.booked_seats = set()

    def add_seats(self, service_level: ServiceLevel, rows_count: int, row_scheme: str):  # шаблон "ххх ххх"
        for _ in range(rows_count):
            self.seating_configuration.append((service_level, row_scheme))
            self.total_seats += row_scheme.count("x")

    def book_seat(self, row_num: int, seat_num: str):
        self.booked_seats.add((row_num, seat_num))

    def print_configuration(self):
        print("ПЛАН МЕСТ РЕЙСА:", self.flight_number)
        print("-" * SEP_LEN)
        cur_sl = None
        for i, (sl, scheme) in enumerate(self.seating_configuration):
            if sl != cur_sl:
                print(sl)
                cur_sl = sl
                print("   ", end="")
                seat_idx = 0
                for t in scheme:
                    if t == " ":
                        t = "   "
                    else:
                        t = f" {ALPH[seat_idx]} "
                        seat_idx += 1
                    print(t, end="")
                print()
            print(str(i + 1).rjust(2, ' '), end=" ")
            for s, c in enumerate(scheme):
                if c == " ":
                    c = "   "
                else:
                    c = f"[{'x' if (i + 1, ALPH[s]) in self.booked_seats else ' '}]"
                print(c, end="")
            print()

        print("-" * SEP_LEN)

    def __str__(self):
        return f"{self.flight_number} {self.date:%d.%m.%Y %H:%M} {self.departure} -> {self.arrival}"

    def check_free(self, count: int):
        return self.total_seats - len(self.booked_seats) >= count


class AviaSystem:
    def __init__(self, company_name):
        self.flights = []
        self.airports = []
        self.company_name = company_name

    def add_flight(self, flight: Flight):
        self.flights.append(flight)

    def remove_flight(self, flight: Flight):
        self.flights.remove(flight)

    def add_airport(self, airport: Airport):
        self.airports.append(airport)

    def remove_airport(self, airport: Airport):
        self.airports.remove(airport)

    def find_flights(
            self, departure: Airport, arrival: Airport, date: datetime, count: int, day_part: str = ""
    ) -> list[Flight]:
        res = []
        for flight in self.flights:
            if flight.departure == departure and flight.arrival == arrival and flight.date >= date:
                if CHECK_DAY_TIME[day_part](flight.date) and flight.check_free(count):
                    res.append(flight)
        return res

    def print_flights_list(self, flight_list: list[Flight]):
        if not flight_list:
            print("Рейсы не найдены")
            return
        print("\n".join(map(str, flight_list)))


avia = AviaSystem("S7")
a1 = Airport("Толмочёво")
a2 = Airport("Домодедово")
avia.add_airport(a1)
avia.add_airport(a2)
business = ServiceLevel("Бизнес класс")
economy = ServiceLevel("Эконом класс")
flights = [
    Flight(a1, a2, datetime(2024, 10, 7, 9, 30), "S1310"),
    Flight(a1, a2, datetime(2024, 10, 7, 13, 00), "S4055"),
    Flight(a1, a2, datetime(2024, 10, 7, 16, 00), "S4455"),
    Flight(a1, a2, datetime(2024, 10, 7, 18, 00), "S4035"),
    Flight(a1, a2, datetime(2024, 10, 7, 23, 00), "S4555"),
    Flight(a1, a2, datetime(2024, 10, 7, 1, 00), "S4057"),
    Flight(a2, a1, datetime(2024, 10, 7, 10, 00), "S4047"),
    Flight(a2, a1, datetime(2024, 10, 7, 15, 00), "S6047"),
    Flight(a2, a1, datetime(2024, 10, 7, 3, 00), "S6097"),
]
for fl in flights:
    fl.add_seats(business, 2, "xx xx")
    fl.add_seats(economy, 10, "xxx xxx")

    avia.add_flight(fl)

found = avia.find_flights(a1, a2, datetime.now(), 1, "день")
avia.print_flights_list(found)
found[0].book_seat(1, "a")
found[0].book_seat(9, "f")
found[0].print_configuration()
