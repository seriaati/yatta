from enum import StrEnum

__all__ = ("PathType", "CombatType")


class PathType(StrEnum):
    KNIGHT = "Knight"
    """Preservation"""
    ROGUE = "Rogue"
    """The Hunt"""
    MAGE = "Mage"
    """Erudition"""
    WARLOCK = "Warlock"
    """Nihility"""
    WARRIOR = "Warrior"
    """Destruction"""
    SHAMAN = "Shaman"
    """Harmony"""
    PRIEST = "Priest"
    """Abundance"""


class CombatType(StrEnum):
    ICE = "Ice"
    FIRE = "Fire"
    QUANTUM = "Quantum"
    IMAGINARY = "Imaginary"
    WIND = "Wind"
    THUNDER = "Thunder"
    PHYSICAL = "Physical"
