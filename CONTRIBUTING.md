# How to contribute

*(this section is freely adapted from the [calliope](https://github.com/calliope-project/calliope/blob/master/CONTRIBUTING.md) project)*

We're really glad you're reading this, because we need volunteer developers to help this project come to fruition.

Some of the resources to look at if you're interested in contributing:

* [Join us on Gitter to chat!](https://gitter.im/RAMP-project/community)
* Look at [open issues](https://github.com/RAMP-project/RAMP/issues)

## Licensing

By contributing to RAMP, e.g. through opening a pull request or submitting a patch, you represent that your contributions are your own original work and that you have the right to license them, and you agree that your contributions are licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2.

## Submitting changes

To contribute changes:
- Fork the project on GitHub
- Create a feature branch (e.g. named "add-this-new-feature") to work on in your fork
- Add your name to the [AUTHORS](AUTHORS) file
- Commit your changes to the feature branch
- Push the branch to GitHub
- On GitHub, create a new pull request from the feature branch

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

We have a qualitative testing functionality that allows to compare the results arising from a modified version of the code against default ones, for the 3 reference input files provided within the code itself.

This functionality is accessible via `test/test_run.py`. To run the qualitative test, you'll have to go through the following steps:
   1. run your modified code for the 3 reference input files for 30 days each. This will create 3 corresponding output files in the `results` folder
   2. run `test/test_run.py` and visualise the comparison between the results of your code and those obtainable with the latest stable version
   
Ideally, the difference between reference and new results should be minimal and just due to the stochastic nature of the code. If more pronounced, it should be fully explainable based on the changes made to the code and aligned to the expectations of the developers (i.e. it should reflect a change in the output *wanted* and precisely *sought* with the commit in question).

## Attribution

The layout and content of this document is partially based on [calliope](https://github.com/calliope-project/calliope/blob/master/CONTRIBUTING.md)'s equivalent document.