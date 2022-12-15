import enum

class StatusContainer(enum.Enum):
    empty = 'empty'
    filling = 'filling'
    full = 'full'

class StatusRoute(enum.Enum):
    opened = 'opened'
    closed = 'closed'
