from setuptools import find_packages, setup


with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="church_platform",
    version="1.0.0",
    description="Comprehensive hierarchical content management and engagement system for church organizations",
    author="Church Platform Team",
    author_email="support@churchplatform.local",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
