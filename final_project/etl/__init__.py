# from pkg_resources import get_distribution, DistributionNotFound

# code included from csci_utils pset and Professor's lecture slides

try:
    from setuptools_scm import get_version

    __version__ = get_version(root="../..", relative_to=__file__)
except:  # package is not installed  # noqa: E722
    from setuptools_scm import get_version

    __version__ = get_version(root="../..", relative_to=__file__)
