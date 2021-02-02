from setuptools import setup

setup(
    name="licensecheck",
    version='0.1',
    py_modules=['license_check'],
    install_requires=[
        'click',
        'requests',
        'python-dateutil',
        'datetime'
    ],
    entry_points='''
        [console_scripts]
        licensecheck=license_check:lc_check
    ''',
)