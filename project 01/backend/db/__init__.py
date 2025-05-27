# from .engine import Base, engine
# from .models import User


"""
The __all__ variable should be a list of strings containing those names
that you want to export from your package when someone uses a wildcard
import. By defining the __all__ variable in the __init__.py file,
you establish the module names that a wildcard import will bring into
your namespace.

instead of importing like below:
===> from db.engine import Base
we can import it like this:
===> from db import Base

"""
# __all__ = ["Base", "User"]


# for sync codes
# Base.metadata.create_all(bind=engine)
