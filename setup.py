from setuptools import setup, find_packages
import sys, os

version = '0.0.3'

setup(
      name='django-survey',
      version=version,
      description='A simple extensible survey application for django sites',
      long_description="""\
""",
      author='Yann Malet, Doug Napoleone',
      author_email='yann.malet@gmail.com',
      url='http://code.google.com/p/django-survey/',
      keywords='django',
      license='GPL',
      include_package_data=True,
      zip_safe=False,
      classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Framework :: Django',
      ],
      packages=find_packages(exclude=['ez_setup', 'examples', 'test_project']),
      package_data={
          'survey': ['templates/', 'locale/*/LC_MESSAGES/*', 'static/*'],
      },
      )
