import os
import logging
from csci_utils.canvas import (
    get_canvas,
    get_courses,
    get_adv_python_course,
    get_assignment,
    submit_assignment,
)
from git import Repo
from canvasapi.assignment import Assignment
from typing import Dict
import json


os.environ["TZ"] = "US/Eastern"
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y %I:%M:%S %p %Z",
)


def submit():
    logging.info("Final project assignment submission begin!")
    get_courses(get_canvas())
    adv_python_course = get_adv_python_course(get_canvas())
    assignment_fp = get_assignment(adv_python_course, "Final Project")
    submit_assignment(assignment_fp)
    logging.info("Final project assignment submission end!")


def submit_assignment(assignment: Assignment):
    """Submit the supplied assignment

    :param assignment: assignment to be submitted
    :return: nothing return
    """
    # Begin submissions
    repo = Repo(".")
    logging.info("Repo Untracked Files: ")
    logging.info(repo.untracked_files)
    url = "https://github.com/devfulcrum/{}/commit/{}".format(
        os.path.basename(repo.working_dir), repo.head.commit.hexsha
    )
    # url = repo.remotes.origin.url[:-4] + "/commit/{}".format(
    #     repo.head.commit.hexsha
    # )  # you MUST push to the classroom org, even if CI/CD runs
    # elsewhere (you can push anytime before peer review begins)
    assignment.submit(
        dict(
            submission_type="online_url",
            url=url,
        ),
        comment=dict(text_comment=json.dumps(get_submission_comments(repo))),
    )


def get_submission_comments(repo: Repo) -> Dict:  # pylint: disable=W0621
    """Get some info about this submission

    :param repo: repo location information
    :return: return the comments as Dict
    """
    return dict(
        gh_pages_sphinx_docs="https://devfulcrum.github.io/2021sp-final-project-devfulcrum/",
        read_the_docs="https://2021sp-final-project-devfulcrum.readthedocs.io/en/latest/",
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(index=False, working_tree=False),
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
    )


if __name__ == "__main__":
    submit()
