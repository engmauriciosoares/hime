from abc import ABC, abstractmethod


class Event(ABC):
    """
    These event classes are similar to that of Lavaplayer's
    All business rules should be handled using these and an EventAdapter
    """
    @abstractmethod
    def __init__(self, player):
        self.player = player


class TrackPauseEvent(Event):
    def __init__(self, player):
        super().__init__(player)


class TrackResumeEvent(Event):
    def __init__(self, player):
        super().__init__(player)


class TrackStartEvent(Event):
    def __init__(self, player, track):
        super().__init__(player)
        self.track = track


class TrackEndEvent(Event):
    def __init__(self, player, track, reason):
        super().__init__(player)
        self.track = track
        self.reason = reason


class TrackExceptionEvent(Event):
    def __init__(self, player, track, exception):
        super().__init__(player)
        self.track = track
        self.exception = exception


class TrackStuckEvent(Event):
    def __init__(self, player, track, threshold_ms):
        super().__init__(player)
        self.track = track
        self.threshold_ms = threshold_ms


class AbstractPlayerEventAdapter(ABC):
    """
    This is a base EventAdapter people can inherit to put on their players by doing:

    player.event_adapter = event_adapter
    """
    @abstractmethod
    async def track_pause(self, event: TrackPauseEvent):
        pass

    @abstractmethod
    async def track_resume(self, event: TrackResumeEvent):
        pass

    @abstractmethod
    async def track_start(self, event: TrackStartEvent):
        pass

    @abstractmethod
    async def track_end(self, event: TrackEndEvent):
        pass

    @abstractmethod
    async def track_exception(self, event: TrackExceptionEvent):
        pass

    @abstractmethod
    async def track_stuck(self, event: TrackStuckEvent):
        pass

    async def on_event(self, event):
        if not issubclass(event.__class__, Event):
            raise TypeError
        if isinstance(event, TrackPauseEvent):
            await self.track_pause(event)
        elif isinstance(event, TrackResumeEvent):
            await self.track_resume(event)
        elif isinstance(event, TrackStartEvent):
            await self.track_start(event)
        elif isinstance(event, TrackEndEvent):
            await self.track_end(event)
        elif isinstance(event, TrackExceptionEvent):
            await self.track_exception(event)
        elif isinstance(event, TrackStuckEvent):
            await self.track_stuck(event)


class InternalEventAdapter(AbstractPlayerEventAdapter):
    """
    A default internal EventAdapter that only cares about track_end
    """
    async def track_pause(self, event: TrackPauseEvent):
        event.player.paused = True

    async def track_resume(self, event: TrackResumeEvent):
        event.player.paused = False

    async def track_start(self, event: TrackStartEvent):
        pass

    async def track_end(self, event: TrackEndEvent):
        event.player.reset()

    async def track_exception(self, event: TrackExceptionEvent):
        pass

    async def track_stuck(self, event: TrackStuckEvent):
        pass
