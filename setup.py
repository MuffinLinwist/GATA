from setuptools import setup


setup(
    name='cldfbench_gata',
    py_modules=['cldfbench_gata'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'gata=cldfbench_gata:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
