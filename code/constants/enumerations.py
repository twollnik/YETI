from enum import Enum


class MyEnum(Enum):

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.value == other.value
        return NotImplemented

    def __gt__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, self.__class__):
            return self.value > other.value
        return NotImplemented

    @classmethod
    def from_val(cls, value):
        """ Convert input value to enumeration object. """

        try:
            return cls(str(value))
        except ValueError:
            pass

        try:
            return cls[str(value)]
        except KeyError:
            pass

        try:
            return eval(str(value))
        except:
            pass

        return None

class VehicleCategory(MyEnum):

    PC = "PC"
    LCV = "LCV"
    HDV = "HDV"
    COACH = "Coach"
    UBUS = "Ubus"
    MOPED = "Moped"
    MC = "MC"


class DayType(MyEnum):

    MONtoTHU = "1"
    FRI = "2"
    SAT = "3"
    SUN = "7"


class PollutantType(MyEnum):

    # The pollutant values need to match the names in the
    # berlin_format emission factors file
    NOx = "NOx"
    CO = "CO"
    NH3 = "NH3"
    VOC = "VOC"
    PM_Exhaust = "PM Exhaust"


class LOSType(MyEnum):

    LOS1 = "1"  # Freeflow
    LOS2 = "2"  # Heavy
    LOS3 = "3"  # Saturated
    LOS4 = "4"  # Stop+Go


class Dir(MyEnum):

    # The values assigned to L and R need to match the values
    # used in the link data input file.
    L = "0"
    R = "1"


class AreaType(MyEnum):

    # The values assigned to L and R need to match the values
    # used in the links data input file.
    Urban = "1"
    Rural = "0"


class RoadType(MyEnum):

    # The values assigned to L and R need to match the values
    # used in the links data input file.
    Access = "0"
    Distr = "1"
    Local = "3"
    MW_City = "5"
    MW_Nat = "6"
    Trunk_City = "8"
    Trunk_Nat = "9"
