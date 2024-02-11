from setuptools import setup

setup(
    # Whatever arguments you need/want
    # Needed to silence warnings (and to be a worthwhile package)
    name='simple_ratelimit',
    author='Anatolii Yakushko',
    author_email='shaddyx@gmail.com',
    # Needed to actually package something
    packages=['simple_ratelimit'],
    package_dir={'simple_ratelimit': 'src/simple_ratelimit'},
    # Needed for dependencies
    install_requires=[
        'pytest',
        'pytest-asyncio'
    ],
    package_data={"": ["*.json"]},
    # *strongly* suggested for sharing
    version='0.01',
    # The license can be anything you like
    license='MIT',
    description='The library to have the rate limit functionality in python',
    include_package_data=True
)
