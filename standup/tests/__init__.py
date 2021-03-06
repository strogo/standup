from functools import wraps
from standup.app import db
from standup.apps.status.models import Project, Status
from standup.apps.users.models import User

def with_save(func):
    """Decorate a model maker to add a `save` kwarg.

    If save=True, the model maker will save the object before returning it.

    """
    @wraps(func)
    def saving_func(*args, **kwargs):
        save = kwargs.pop('save', False)
        ret = func(*args, **kwargs)
        if save:
            db.session.add(ret)
            db.session.commit()
        return ret

    return saving_func

@with_save
def project(**kwargs):
    defaults = dict(name='Test Project',
                    slug='test-project')
    defaults.update(kwargs)

    return Project(**defaults)

@with_save
def user(**kwargs):
    defaults = dict(username='jdoe',
                    name='John Doe',
                    email='john@doe.com',
                    slug='jdoe')
    defaults.update(kwargs)

    return User(**defaults)

@with_save
def status(**kwargs):
    defaults = dict(content='This is a status update.')
    defaults.update(kwargs)

    if 'user' not in kwargs and 'user_id' not in kwargs:
        defaults['user'] = user(save=True)

    if 'project' not in kwargs and 'project_id' not in kwargs:
        defaults['project'] = project(save=True)

    return Status(**defaults)