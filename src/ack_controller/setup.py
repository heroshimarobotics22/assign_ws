from setuptools import setup

package_name = 'ack_controller'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jagadeswar',
    maintainer_email='pssjagadeswar22@gmail.com',
    description='Ackermann visual servoing control node',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'control_node = ack_controller.control_node:main',
        ],
    },
)