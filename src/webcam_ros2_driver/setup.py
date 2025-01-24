from setuptools import setup

package_name = 'webcam_ros2_driver'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Marcus Wong',
    maintainer_email='wongherseng.@gmail.com',
    description='start and recieve input image from picamera',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_script = webcam_ros2_driver.my_script:main',
        ],
    },
)
