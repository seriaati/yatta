from __future__ import annotations

from enum import StrEnum

__all__ = ("CombatType", "Language", "PathType")


class Language(StrEnum):
    """Enumerate supported languages for the API."""

    CHT = "cht"
    """Traditional Chinese"""
    CN = "cn"
    """Simplified Chinese"""
    DE = "de"
    """German"""
    EN = "en"
    """English"""
    ES = "es"
    """Spanish"""
    FR = "fr"
    """French"""
    ID = "id"
    """Indonesian"""
    JP = "jp"
    """Japanese"""
    KR = "kr"
    """Korean"""
    PT = "pt"
    """Portuguese"""
    RU = "ru"
    """Russian"""
    TH = "th"
    """Thai"""
    VI = "vi"
    """Vietnamese"""


class PathType(StrEnum):
    """Represent the Path types in Honkai: Star Rail."""

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
    MEMORY = "Memory"
    """Remembrance"""
    ELATION = "Elation"
    """Elation"""


class CombatType(StrEnum):
    """Represent the Combat Types (Elements) in Honkai: Star Rail."""

    ICE = "Ice"
    FIRE = "Fire"
    QUANTUM = "Quantum"
    IMAGINARY = "Imaginary"
    WIND = "Wind"
    THUNDER = "Thunder"
    PHYSICAL = "Physical"
