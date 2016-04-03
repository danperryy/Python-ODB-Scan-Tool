Testing
=======

To test python-OBD, you will need to `pip install pytest` and install the module (preferably in a virtualenv) by running `python setup.py install`. The end-to-end tests will also require [obdsim](http://icculus.org/obdgpslogger/obdsim.html) to be running in the background. When starting obdsim, note the "SimPort name" that it creates, and pass it as an argument to py.test.

To run all tests, run the following command:

	$ py.test --port=/dev/pts/<num>

For more information on pytest with virtualenvs, [read more here](https://pytest.org/dev/goodpractises.html)