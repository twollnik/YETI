.. _add-validation-function:

Change how data is validated
============================

Data validation is done by the ``validation_function``, as specified in the config. This docs page covers how to
write your own ``validation_function``.

How is a ``validation_function`` called?
------------------------------------

A validation function is called with the single argument ``kwargs``:

.. code-block:: python

    def validation_function(**kwargs)

        ...

``kwargs`` is a Python dictionary that contains all arguments from the config file. For example if the config
file contains the line ``input_link_data:     path/to/link_data.csv`` the ``kwargs`` dictionary will contain the
key-value pair ``"input_link_data": "path/to/link_data.csv"``.

``kwargs`` lets you access the input files that are specified in the config file.
You can access these input files and do whatever you want with them. For example you can check if
an input file contains all necessary columns.

Example
-------

.. code-block:: python

    import pandas as pd
    import logging

    def validation_function(**kwargs)

        # validate the link data
        # 1. Load link data from file
        link_data_file = kwargs["input_link_data"]
        link_data = pd.read_csv(link_data)

        # 2. Check that link data has the column 'LinkID', 'Length_m', 'MaxSpeed_kmh', 'AreaCat', and 'RoadCat'.
        for colname in ["LinkID", "Length_m", "MaxSpeed", "AreaCat", "RoadCat"]:
            if colname not in link_data.columns:
                logging.warning(f"link data is missing the column {colname}")

        # 3. perform other validation operations on the link data
        ...

        # validate other datasets
        ...

Output of the validation_function
---------------------------------

What you want the ``validation_function`` to output is up to you.

The ``validation_function``s that we provide print warnings whenever a validation check fails. This means
that YETI will keep running even if the validation fails.
You can print warnings with ``logging.warning("..")``, as shown in the example above.

If you want to stop the YETI run when a validation check fails, you should raise an Error. For example:

.. code-block:: python

    def validation_function(**kwargs):

        if some_validation_check_does_not_pass():
            raise RuntimeError("validation failed")