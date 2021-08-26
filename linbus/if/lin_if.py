#!/usr/bin/env python
# Copyright (c) 2021 Timothy Rule


"""LIN Bus Frame Interface.
"""


from abc import ABC
from dataclasses import dataclass, field
from typing import Any, List, Callable


@dataclass
class LinFrame:
    """LIN Frame

    Attributes
    ----------
    identifier : int
        Frame header identifier field, 0 to 63 (6 bits).
            * 0 to 59 (0x3b) are used for signal-carrying frames (Unconditional/Event triggered/Sporadic).
            * 60 (0x3c) and 61 (0x3d) are used to carry diagnostic data.
            * 62 (0x3e) is reserved for user-defined extensions.
            * 63 (0x3f) is reserved for future protocol enhancements.
    parity : int
        Frame header parity, 2 bits, calculated at transmission. Info only.
        P0 = ID0 ⊕ ID1 ⊕ ID2 ⊕ ID4 (1)
        P1 = ¬ (ID1 ⊕ ID3 ⊕ ID4 ⊕ ID5)
    length : int
        When set indicates the expected length of the received data payload. If
        not set then transmit length is determined by the length of the data field.
    data : [int]
        Frame payload data, 1 to 8 bytes.
    checksum : int
        Frame response checksum, 1 byte, calculated at transmission (inverted eight bit sum with carry6).
        LIN 1.3 "classic checksum" based on frame data only.
        LIN 2.0 "enhanced checksum" based on frame data and identifier.
        Identifier 60 .. 63 always use "classic checksum".
    """
    # Header
    identifier: int
    parity: int = field(default=None, init=False)
    # Payload
    length: int = field(default=None)
    data: [int] = field(default=[])
    checksum: int = field(default=None, init=False)
    # Functions
    checksum_func: Callable[[LinFrame], int] = field(default=None)


class LinIf(ABC):
    """LIN Interface

    """

    @staticmethod
    def checksum__lin_1_3(frame: LinFrame) -> int:
        """
        LIN 1.3 "classic checksum" based on frame data only.
        """
        pass

    @staticmethod
    def checksum__lin_2_0(frame: LinFrame) -> int:
        """
        LIN 2.0 "enhanced checksum" based on frame data and identifier.
        """
        pass

    @abstractmethod
    def send(self, frame: LinFrame) -> None:
        """
        Send a frame header.

        If len(frame.data) then send the data payload, otherwise read
        frame.length bytes.

        Note
        ----
        Called by a LIN Master.

        Example
        -------
        lin_if = SerialLinIf(device='/dev/serial0')
        lin_frame = LinFrame(identifier=42)
        lin_if.send(lin_frame)
        print(lin_frame)
        """
        pass

    @abstractmethod
    async def wait(self) -> LinFrame:
        """
        Wait for a frame header, return the LIN Frame to the caller.

        Note
        ----
        Called by LIN Slave.

        Example
        -------
        lin_if = SerialLinIf(device='/dev/serial0')
        lin_frame = await asyncio.wait_for(lin_if.wait(), timeout=3.0)
        # Frame header received.
        if lin_frame.identifier == 42:
            lin_frame.length = 4 # Indicate receive (4 bytes).
        elif lin_frame.identifier == 24:
            lin_frame.data = b'foobar'  # Indicate transmit.
        else:
            pass  # NOP, slave drops the frame.
        lin_if.complete(lin_frame)
        """
        while True:
            yield None
            return None

    @abstractmethod
    def complete(self, frame: LinFrame) -> None:
        """
        Send or receive the frame payload.

        If len(frame.data) then send the data payload, otherwise read
        frame.length bytes.

        Note
        ----
        Called by LIN Slave.
        """
        pass

    @abstractmethod
    def wake_up(self) -> None:
        """Network Management - WAKE UP

        The wake-up request is issued by forcing the bus to the dominant state
        for 250 μs to 5 ms. Every slave node must be ready to listen to bus
        commands within 100 ms, measured from the ending edge of the dominant pulse.
        """
        pass

    @abstractmethod
    def goto_sleep(self) -> None:
        """Network Management - GOTO SLEEP

        Send diagnostic command (identifier=0x3c) with first databyte set to 0.

        Slave nodes automatically enter sleep mode after 4 seconds of LIN Bus inactivity.
        """
        pass
