"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from collections import Counter

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if title in self.events or capacity < 1:
            raise ValueError
        n_event = Event(title, capacity)
        self.events[title] = n_event
        return n_event
        
    def event(self, title: str) -> Event:
        try:
            return self.events[title]
        except:
            raise UnknownEventError(title)

    def handle(self, line: str) -> str:
        parts = [part.strip() for part in line.split(",")]
        
        if len(parts) < 3 or not parts[0] in ['join', 'leave']:
            return f'Sorry, I don\'t understand {line!r}.'

        command, title, member = parts
        
        try:
            event = self.event(title)

            if command == "join":
                result = event.sign_up(member)

                if result == "seat":
                    return f"{member} has a seat at {title}."

                return f"{member} is on the waitlist for {title}."

            old_seats = list(event.seats)
            event.cancel(member)

            promoted = [
                person for person in event.seats
                if person not in old_seats
            ]

            if promoted:
                return (
                    f"{member} left {title}. "
                    f"{promoted[0]} gets the seat."
                )

            return f"{member} left {title}."

        except SignupError as error:
            return f"Sorry, {error}."
        

    def attendance(self) -> dict[str, int]:
        counts = Counter()

        for event in self.events.values():
            counts.update(event.seats)

        return dict(counts)

if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
