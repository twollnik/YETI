How to update the documentation
===============================

The documentation for YETI is written in `reStructuredText <https://en.wikipedia.org/wiki/ReStructuredText/>`_ (rst)
using `Sphinx <http://www.sphinx-doc.org/en/master/>`_. Please familiarize yourself with the basics of rst and Sphinx
before updating the docs.

Each page of the documentation corresponds to one rst file in the folder ``docs/``.
You can look at the rst sourcecode of existing documentation pages by clicking on "View page source"
in the top right corner of the page.

When writing documentation, you will want to **look at what you created** and see if it renders the way you
want it to. To see what the documentation website will look like with your changes follow these steps:

1. Run ``make html`` on the command line from the folder ``docs/``.
2. Open the file ``docs/_build/index.html`` in your favourite browser.

If you have firefox installed, you can alternatively run ``make open`` on the command
line from the folder ``docs/``.

Update an existing page
-----------------------
To update an existing page, find the rst file that contains the content of the page. You can find
the rst files for the user documentation in ``docs/user/`` and the rst files for the developer documentation
in ``docs/developer/``.

Once you have found the right file, make you changes. Then commit them to git and push to GitHub.
Make sure to merge the changes into the master branch, otherwise they won't be added to the
documentation website.


Add a new page
--------------
1. Create an rst file in ``docs/``
''''''''''''''''''''''''''''''''''
Create an rst file in the folder ``docs/`` or one of its subfolders. You can also create your own subfolder.

2. Add content to the rst file
''''''''''''''''''''''''''''''
Add the desired content to the rst file you created. Follow this template:

.. code-block:: rst

    Page Title
    ==========
    Description of docs page

    Major section 1
    ---------------
    Some text and/or images

    Paragraph 1.1
    ^^^^^^^^^^^^^
    Some text and/or images

    Major section 2
    ---------------
    ...

3. Add the new file to index.rst
''''''''''''''''''''''''''''''''
To add your documentation page to the docs, you need to add it to the file ``docs/index.rst``.

Add the path to your rst file to a ``toctree`` in ``docs/index.rst``. The documentation
page will be displayed in the documentation subsection that corresponds to the chosen ``toctree``
("User documentation" or "Developer documentation").
Note that the path to your rst file needs to be relative to ``docs/index.rst``
and you should omit the ``.rst`` postfix in the path to your rst file.

If you want to create a new documentation subsection, you can add a new ``toctree`` to ``docs/index.rst``.
Follow this template:

.. code-block:: rst

    .. toctree::
       :maxdepth: 1
       :caption: Name of the new subsection

       path/to/pageA
       path/to/pageB
       ...


4. Commit and Push
''''''''''''''''''
When you are happy with the new documentation page, commit your changes to git and push them to GitHub.
Make sure to merge the changes into the master branch, otherwise they won't be added to the
documentation website.
