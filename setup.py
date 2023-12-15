from setuptools import setup

setup(name='minicv',
  version='1.0.1',
  description='High performance CV',
  author='KateTseng',
  author_email='KateTseng.K@outlook.com',
  url='https://github.com/NakanoSanku/minicv',
  license='MIT',
  keywords='High performance CV',
  project_urls={
   'Documentation': 'https://github.com/NakanoSanku/minicv/README.md',
   'Funding': 'https://donate.pypi.org',
   'Source': 'https://github.com/NakanoSanku/minicv/',
   'Tracker': 'https://github.com/NakanoSanku/minicv/issues',
  },
  packages=['minicv'],
  install_requires=['opencv-python'],
  python_requires='>=3'
  )

