from setuptools import setup
setup(name='pykairos',
      version='@@VERSION@@',
      description='Python aiohttp server used by Kairos',
      author='Gerard Duval',
      author_email='gerard.duval@gdsoftconsulting.com',
      url='https://github.com/gdsoftconsulting/kairos',
      license='GPL',
      packages=['pykairos'],
      classifiers=[ "Development Status :: 5 - Production/Stable", "Topic :: Utilities", "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)"],
      zip_safe=False)