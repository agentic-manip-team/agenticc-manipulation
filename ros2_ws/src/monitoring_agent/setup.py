from setuptools import find_packages, setup

# package ka naam — ROS2 isi naam se pehchanta hai
package_name = 'monitoring_agent'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),   # python files khud dhoond lo
    data_files=[
        # ROS2 ke registry files — inhe mat chherna
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eeman',
    maintainer_email='eeman@todo.todo',
    description='M5: Monitoring + Recovery agents with mock robot for testing',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    # yahan har naya node register hota hai:
    # 'command_name = package.file_name:main'
    entry_points={
        'console_scripts': [
            'monitoring_node = monitoring_agent.monitoring_node:main',  # quality inspector
            'mock_robot = monitoring_agent.mock_robot:main',            # fake robot (demo/testing)
            'recovery_node = monitoring_agent.recovery_node:main',      # problem solver
        ],
    },
)