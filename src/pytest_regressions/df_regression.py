from functools import partial

import yaml

from pytest_regressions.common import Path, check_text_files, perform_df_regression_check


class DataFrameRegressionFixture:
    """
    Implementation of `data_regression` fixture.
    """

    def __init__(self, datadir, original_datadir, request):
        """
        :type datadir: Path
        :type original_datadir: Path
        :type request: FixtureRequest
        """
        self.request = request
        self.datadir = datadir
        self.original_datadir = original_datadir
        self.force_regen = False

    def check(self, data_df, basename=None, fullpath=None):
        """
        Checks the given dict against a previously recorded version, or generate a new file.

        :param dict data_dict: any yaml serializable dict.

        :param str basename: basename of the file to test/record. If not given the name
            of the test is used.
            Use either `basename` or `fullpath`.

        :param str fullpath: complete path to use as a reference file. This option
            will ignore ``datadir`` fixture when reading *expected* files but will still use it to
            write *obtained* files. Useful if a reference file is located in the session data dir for example.

        ``basename`` and ``fullpath`` are exclusive.
        """
        __tracebackhide__ = True

        def dump(filename):
            """Dump df contents to the given parquet filename"""

            with filename.open("wb") as f:
                data_df.to_parquet(f)

        perform_df_regression_check(
            datadir=self.datadir,
            original_datadir=self.original_datadir,
            request=self.request,
            check_fn=partial(check_text_files, encoding="UTF-8"),
            dump_fn=dump,
            extension=".parquet",
            basename=basename,
            fullpath=fullpath,
            force_regen=self.force_regen,
        )

    # non-PEP 8 alias used internally at ESSS
    Check = check


