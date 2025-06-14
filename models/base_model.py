import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """
    BaseModel class
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialization method for BaseModel.
        Public instance attributes:
            id: a unique identifier generated by uuid
            created_at: the datetime at which the object is instantiated
            updated_at: the datetime at which the object is instantiated and updated
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
    
    def __str__(self):
        """
        Returns a string representation of the BaseModel instance, including
        the class name, unique id, and dictionary of all instance attributes.
        """

        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime.
        """
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        return instance_dict