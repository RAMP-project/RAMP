# How to contribute

*(this section is freely adapted from the [calliope](https://github.com/calliope-project/calliope/blob/master/CONTRIBUTING.md) project)*

We're really glad you're reading this, because we need volunteer developers to help this project come to fruition.

Some of the resources to look at if you're interested in contributing:

* [Join us on Gitter to chat!](https://gitter.im/RAMP-project/community)
* Look at [open issues](https://github.com/RAMP-project/RAMP/issues)

## Licensing

By contributing to RAMP, e.g. through opening a pull request or submitting a patch, you represent that your contributions are your own original work and that you have the right to license them, and you agree that your contributions are licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2.

## Open an issue

[Open an issue](https://github.com/RAMP-project/RAMP/issues) to report a bug or for a feature request, please try to provide the information summarized below

- OS: *your_operating_system*, *your_distribution*
- RAMP version or Branch: *RAMP version* or *branch_name*, updated on *update_date*
- If applicable: Attach full error message
- If applicable: Share screenshots/images of your problem
- If applicable: Share used input data

## Submitting changes

To contribute changes:
- Fork the project on GitHub
- Follow the "Setup" steps below
- Create a feature branch (e.g. named "add-this-new-feature") to work on in your fork
- Add your name to the [AUTHORS](AUTHORS) file
- Commit your changes to the feature branch
- Push the branch to GitHub
- On GitHub, create a new pull request from the feature branch

### Setup

1. Create a virtual environment and install the dev dependencies with

        pip install -r dev_requirements.txt

2. Install the pre-commit hooks with

        pre-commit install

   This will mainly make sure you can't commit if your code is not linted with black.
   The pre-commit hook will check if your code is linted and if it is not it will simply lint it for you, you then only need to stage the changes made by the linter and commit again, as simple as that :)

### Pull requests

Before submitting a pull request, check whether you have:

* Added your changes to ``CHANGELOG.md``
* Added or updated documentation for your changes
* Passed qualitative tests if you implemented new functionality

When opening a pull request, please provide a clear summary of your changes!

### Commit messages

Please try to write clear commit messages. One-line messages are fine for small changes, but bigger changes should look like this:

    A brief summary of the commit

    A paragraph or bullet-point list describing what changed and its impact,
    covering as many lines as needed.

## Testing

Testing is used by RAMP developers to make sure their new feature/bug fix is not breaking existing code. As RAMP is stochastic some tests are only qualitative, other unit tests are ran by GitHub Actions.

Before running the tests locally, you need to install the testing dependencies

```
pip install -r tests/requirements.txt
```

### Qualitative testing

The qualitative testing functionality allows to compare the results arising from a modified version of the code against default ones, for the 3 reference input files provided within the code itself.

To run the qualitative test, you'll have to run
 ```
 python ramp/test/test_run.py
 ```
from the root level of this repository.

If you already ran this script, you will be asked if you want to overwrite the results files (if you decide not to, the results are not going to be regenerated from your latest code version). You should compare the results of your code and those saved from the latest stable version thanks to the image which is displayed after the script ran.

Ideally, the difference between reference and new results should be minimal and just due to the stochastic nature of the code. If more pronounced, it should be fully explainable based on the changes made to the code and aligned to the expectations of the developers (i.e. it should reflect a change in the output *wanted* and precisely *sought* with the commit in question).

### Unit tests

Run `pytest tests/` form the root of the repository to run the unit tests.

## Attribution

The layout and content of this document is partially based on [calliope](https://github.com/calliope-project/calliope/blob/master/CONTRIBUTING.md)'s equivalent document.
