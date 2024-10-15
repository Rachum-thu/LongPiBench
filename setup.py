import setuptools

setuptools.setup(
    name="dense_toolkit",
    version="0.0.1",
    author="Runchu Tian",
    author_email="runchutian@gmail.com",
    description="A python tool kit for this repo only.",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
)