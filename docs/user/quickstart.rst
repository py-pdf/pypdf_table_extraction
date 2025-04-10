.. _quickstart:

Quickstart
==========

In a hurry to extract tables from PDFs?
This document gives a good introduction to help you get started with pypdf_table_extraction.
Or checkout the quickstart-notebook.

.. image:: https://colab.research.google.com/assets/colab-badge.svg
    :target: https://colab.research.google.com/github/py-pdf/pypdf_table_extraction/blob/quickstart-notebook/examples/pypdf_table_extraction_quick_start_notebook.ipynb


Read the PDF
------------

Reading a PDF to extract tables with pypdf_table_extraction is very simple.

Begin by importing the pypdf_table_extraction module

.. code-block:: pycon

    >>> import pypdf_table_extraction

Now, let's try to read a PDF. (You can check out the PDF used in this example `here`_.) Since the PDF has a table with clearly demarcated lines, we will use the :ref:`Lattice <lattice>` method here.

.. note:: :ref:`Lattice <lattice>` is used by default. You can use :ref:`Stream <stream>` with ``flavor='stream'``.

.. _here: ../_static/pdf/foo.pdf

.. code-block:: pycon

    >>> tables = pypdf_table_extraction.read_pdf('foo.pdf')
    >>> tables
    <TableList n=1>

Now, we have a :class:`TableList <pypdf_table_extraction.core.TableList>` object called ``tables``, which is a list of :class:`Table <pypdf_table_extraction.core.Table>` objects. We can get everything we need from this object.

We can access each table using its index. From the code snippet above, we can see that the ``tables`` object has only one table, since ``n=1``. Let's access the table using the index ``0`` and take a look at its ``shape``.

.. code-block:: pycon

    >>> tables[0]
    <Table shape=(7, 7)>

Let's print the parsing report.

.. code-block:: pycon

    >>> print tables[0].parsing_report
    {
        'accuracy': 99.02,
        'whitespace': 12.24,
        'order': 1,
        'page': 1
    }

Woah! The accuracy is top-notch and there is less whitespace, which means the table was most likely extracted correctly. You can access the table as a pandas DataFrame by using the :class:`table <pypdf_table_extraction.core.Table>` object's ``df`` property.

.. code-block:: pycon

    >>> tables[0].df

.. csv-table::
  :file: ../_static/csv/foo.csv

Looks good! You can now export the table as a CSV file using its :meth:`to_csv() <pypdf_table_extraction.core.Table.to_csv>` method. Alternatively you can use :meth:`to_json() <pypdf_table_extraction.core.Table.to_json>`, :meth:`to_excel() <pypdf_table_extraction.core.Table.to_excel>` :meth:`to_html() <pypdf_table_extraction.core.Table.to_html>` :meth:`to_markdown() <pypdf_table_extraction.core.Table.to_markdown>` or :meth:`to_sqlite() <pypdf_table_extraction.core.Table.to_sqlite>` methods to export the table as JSON, Excel, HTML files or a sqlite database respectively.

.. code-block:: pycon

    >>> tables[0].to_csv('foo.csv')

This will export the table as a CSV file at the path specified. In this case, it is ``foo.csv`` in the current directory.

You can also export all tables at once, using the :class:`tables <pypdf_table_extraction.core.TableList>` object's :meth:`export() <pypdf_table_extraction.core.TableList.export>` method.

.. code-block:: pycon

    >>> tables.export('foo.csv', f='csv')

.. tip::
    Here's how you can do the same with the :ref:`command-line interface <cli>`.

    .. code-block:: console

        $ pypdf_table_extraction --format csv --output foo.csv lattice foo.pdf

This will export all tables as CSV files at the path specified. Alternatively, you can use ``f='json'``, ``f='excel'``, ``f='html'``, ``f='markdown'`` or ``f='sqlite'``.

.. note:: The :meth:`export() <pypdf_table_extraction.core.TableList.export>` method exports files with a ``page-*-table-*`` suffix. In the example above, the single table in the list will be exported to ``foo-page-1-table-1.csv``. If the list contains multiple tables, multiple CSV files will be created. To avoid filling up your path with multiple files, you can use ``compress=True``, which will create a single ZIP file at your path with all the CSV files.

.. note:: pypdf_table_extraction handles rotated PDF pages automatically. As an exercise, try to extract the table out of `this PDF`_.

.. _this PDF: ../_static/pdf/rotated.pdf

Specify page numbers
--------------------

By default, pypdf_table_extraction only uses the first page of the PDF to extract tables. To specify multiple pages, you can use the ``pages`` keyword argument::

    >>> pypdf_table_extraction.read_pdf('your.pdf', pages='1,2,3')

.. tip::
    Here's how you can do the same with the :ref:`command-line interface <cli>`.

    .. code-block:: console

        $ pypdf_table_extraction --pages 1,2,3 lattice your.pdf

The ``pages`` keyword argument accepts pages as comma-separated string of page numbers. You can also specify page ranges — for example, ``pages=1,4-10,20-30`` or ``pages=1,4-10,20-end``.

Extract tables in parallel
--------------------------

pypdf_table_extraction supports extracting tables in parrallel using all the available CPU cores.

.. code-block:: pycon

    >>> tables = pypdf_table_extraction.read_pdf('foo.pdf', page='all', parallel=True)
    >>> tables
    <TableList n=1>

.. tip::
    Here's how you can do the same with the :ref:`command-line interface <cli>`.

    .. code-block:: console

        $ pypdf_table_extraction --pages all --parallel lattice foo.pdf

.. note:: The reading of the PDF document is parallelized by processing pages by different CPU core.
    Therefore, a document with a low page count could be slower to process in parallel.

Reading encrypted PDFs
----------------------

To extract tables from encrypted PDF files you must provide a password when calling :meth:`read_pdf() <pypdf_table_extraction.read_pdf>`.

.. code-block:: pycon

    >>> tables = pypdf_table_extraction.read_pdf('foo.pdf', password='userpass')
    >>> tables
    <TableList n=1>

.. tip::
    Here's how you can do the same with the :ref:`command-line interface <cli>`.

    .. code-block:: console

        $ pypdf_table_extraction --password userpass lattice foo.pdf

pypdf_table_extraction supports PDFs with all encryption types supported by `pypdf`_. This might require installing PyCryptodome. An exception is thrown if the PDF cannot be read. This may be due to no password being provided, an incorrect password, or an unsupported encryption algorithm.

Further encryption support may be added in future, however in the meantime if your PDF files are using unsupported encryption algorithms you are advised to remove encryption before calling :meth:`read_pdf() <pypdf_table_extraction.read_pdf>`. This can been successfully achieved with third-party tools such as `QPDF`_.

.. code-block:: console

    $ qpdf --password=<PASSWORD> --decrypt input.pdf output.pdf

.. _pypdf: https://pypdf.readthedocs.io/en/latest/user/pdf-version-support.html
.. _QPDF: https://www.github.com/qpdf/qpdf

----

Ready for more? Check out the :ref:`advanced <advanced>` section.
