from flask import url_for


def external_url_for(view, **kwargs):
    """ Takes a view function name, like `flask.url_for`,
        and returns that view function's URL prefixed
        with the full & correct scheme and domain. """
    return url_for(view, _external=True, **kwargs)
