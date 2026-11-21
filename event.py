"""HW2 · event.py: one club event with limited seats. Practises Session 4 (a dataclass with
its own lists) and Session 6 (raising the club's exceptions)."""

from dataclasses import dataclass, field

from errors import AlreadySignedUpError, NotSignedUpError


@dataclass
class Event:
    """One event. Members in `seats` have a place; members in `waitlist` wait, first come first."""

    def __init__(self, event: str, wait_list: int):
        self.title = event
        self.capacity = wait_list
        self.seats = []
        self.waitlist = []
    
    def seats_left(self) -> int:
        """Provided: how many seats are still free."""
        return self.capacity - len(self.seats)

    def sign_up(self, member: str) -> str:
        if member in self.seats or member in self.waitlist:
            raise AlreadySignedUpError(member,self.title)
        
        if len(self.seats) < self.capacity:
            self.seats.append(member)
            return 'seat'
        else:
            self.waitlist.append(member)
            return 'waitlist'

    def cancel(self, member: str) -> str | None:
        if member in self.seats:
            self.seats.remove(member)
            if self.waitlist:
                self.seats.append(self.waitlist[0])
                self.waitlist.remove(self.waitlist[0])
                return self.seats[-1]
            else:
                return None
        elif member in self.waitlist:
            self.waitlist.remove(member)
        else:
            raise NotSignedUpError(member,self.title)

    def place(self, member: str) -> int:
        """0 for a member with a seat, or their number on the waitlist, counting from 1."""
        if member in self.seats:
            return 0
        elif member in self.waitlist:
            return self.waitlist.index(member)+1
        else:
            raise NotSignedUpError(member,self.title)