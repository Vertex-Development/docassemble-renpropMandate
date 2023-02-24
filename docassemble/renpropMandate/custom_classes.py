from docassemble.base.util import IndividualName, Individual

# Import any DAObject classes that you will need
from docassemble.base.util import Individual, Person, DAObject

class IndividualNameSA(IndividualName):
    """The name of a South African Individual."""

    def init(self, *pargs, **kwargs):
        if 'uses_parts' not in kwargs:
            self.uses_parts = True
        super().init(*pargs, **kwargs)  

    def defined(self):
        """Returns True if the name has been defined.  Otherwise, returns False."""
        if not self.uses_parts:
            return super().defined()
        return hasattr(self, 'names')    

    def familiar(self):
        """Returns the familiar name."""
        if not self.uses_parts: 
            return self.full()  
        return self._extract_first() 

    def full(self, use_suffix=True):  # pylint: disable=arguments-differ
        """Returns the full name.  Has optional keyword arguments middle
        and use_suffix."""
        if not self.uses_parts:
            return super().full()
        names = [self._extract_first()]
        if self._extract_middle() != "NA":
            names.append(self._extract_middle())
        if hasattr(self, 'last') and len(self.last.strip()):
            names.append(self.last.strip())
        else:
            if hasattr(self, 'paternal_surname') and len(self.paternal_surname.strip()):
                names.append(self.paternal_surname.strip())
            if hasattr(self, 'maternal_surname') and len(self.maternal_surname.strip()):
                names.append(self.maternal_surname.strip())
        if hasattr(self, 'suffix') and use_suffix and len(self.suffix.strip()):
            names.append(self.suffix.strip())
        return " ".join(names)

    def firstlast(self):
        """Returns the first name followed by the last name."""
        if not self.uses_parts:
            return super().firstlast()
        return self._extract_first() + " " + self.last

    def lastfirst(self):
        """Returns the last name followed by a comma, followed by the
        last name, followed by the suffix (if a suffix exists)."""
        if not self.uses_parts:
            return super().lastfirst()
        output = self.last
        if hasattr(self, 'suffix') and self.suffix and len(self.suffix.strip()):
            output += " " + self.suffix
        output += ", " + self._extract_first()
        if hasattr(self, 'middle'):
            initial = self.middle_initial()
            if initial:
                output += " " + initial
        return output

    def middle_initial(self, with_period=True):
        """Returns the middle initial, or the empty string if the name does not have a middle component."""
        return ''

    def _extract_first(self):
        """Returns the first name."""
        names_list = self.names.split()
        return names_list[0]

    def _extract_middle(self):
        """Returns middle name or NA"""
        names_list = self.names.split()
        if len(names_list) > 1:
            return ' '.join(names_list[1:])
        else:
            return "NA"


class IndividualSA(Individual):
    """Represents a natural person."""
    NameClass = IndividualNameSA

    def init(self, *pargs, **kwargs):
        if 'name' not in kwargs and not hasattr(self, 'name'):
            self.initializeAttribute('name', self.NameClass)
        if (not hasattr(self, 'name')) and 'name' in kwargs and isinstance(kwargs['name'], str):
            self.initializeAttribute('name', self.NameClass)
            self.name.uses_parts = False
            self.name.text = kwargs['name']
        super().init(*pargs, **kwargs) 


        

            

