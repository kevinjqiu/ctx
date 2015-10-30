from couchdb import design


class CouchView(design.ViewDefinition):
    def __init__(self):
        params = {
            'design': '_design/ctx',
            'name': self.view_name,
            'language': 'python',
        }

        if hasattr(self, 'map_fun'):
            params['map_fun'] = self.map_fun

        if hasattr(self, 'reduce_fun'):
            params['reduce_fun'] = self.reduce_fun

        super().__init__(**params)

    @classmethod
    def uri(self):
        return '_design/ctx/_view/{}'.format(self.view_name)



class GetActiveTask(CouchView):
    view_name = 'get_active_task'

    @staticmethod
    def map_fun(doc):
        if doc.get('is_active', False):
            yield doc['_id'], doc


class GetTasks(CouchView):
    view_name = 'get_tasks'

    @staticmethod
    def map_fun(doc):
        if not doc['_id'].startswith('_design'):
            yield doc['_id'], doc


def sync_views(db):
    GetActiveTask().sync(db)
    GetTasks().sync(db)
