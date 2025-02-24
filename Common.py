from enum import Enum


class MessageType(Enum):
    Exit = 0
    Picture = 1
    AxisX = 2
    AxisY = 3
    AxisZ = 4
    StartSequence = 5
    StopSequence = 6
    Arm = 7
    Disarm = 8
