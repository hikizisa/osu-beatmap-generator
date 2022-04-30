import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hikizisa",
    version="1.0.0",
    author="hikizisa",

    author_email="32244151+hikizisa@users.noreply.github.com",

    description="osu! automatic mapping assistant tool",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="<https://github.com/hikizisa/osu-auto-mapper>",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    install_requires=[
        'spleeter >= 2.3.0'
    ],

    python_requires='>=3.6',

)