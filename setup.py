import setuptools

setuptools.setup(name='autojira',
                 version='0.2',
                 description='A wrapper library on top of JIRA rest client to automate few jira workflow',
                 url='https://github.com/ramo/autojira',
                 author='Ramachandran Rajagopal',
                 author_email='ramo.phoenix7@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=['jira'],
                 zip_safe=False)
