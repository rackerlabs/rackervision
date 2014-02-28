import cgi
import time
import json
import uuid
from wsgiref import simple_server

import falcon
import pymongo
import pyrax


def _generate_id():
    return str(uuid.uuid1())


def _now():
    return time.time()


class VideoCollection(object):

    def __init__(self, db):
        self.db = db

        pyrax.set_setting('identity_type', 'rackspace')
        pyrax.keyring_auth('rackervision')
        pyrax.queues.client_id = _generate_id()

        self.unprocessed_container = pyrax.cloudfiles.get_container("unprocessed")
        self.processed_container = pyrax.cloudfiles.get_container("processed")
        self.queue = pyrax.queues.get("unprocessed")

    def on_get(self, req, resp):
        sort = [('uploaded_at', pymongo.DESCENDING)]
        cursor = self.db.videos.find({}, fields={'_id': False}, sort=sort)

        doc = list(cursor)
        resp.body = json.dumps(doc)

    def on_post(self, req, resp):
        form = cgi.FieldStorage(fp=req.stream, environ=req.env)
        title, video = form['title'].value, form['video'].file

        # if video_field.file:
        #     pass

        # Stream into Swift
        uuid = _generate_id()
        self.unprocessed_container.upload_file(video, uuid)
        self.queue.post_message(uuid, 1209599)

        # On successful stream, create video document in mongo
        doc = {
            'title': title,
            'uuid': uuid,
            'href': None,
            'uploaded_at': _now(),
        }

        self.db.videos.insert(doc)

# ---------------------------------------------------------------------------


app = application = falcon.API()

mongo_client = pymongo.MongoClient()
app.add_route('/videos', VideoCollection(mongo_client['rackervision']))


if __name__ == '__main__' :
    httpd = simple_server.make_server('localhost', 8000, app)
    print 'Serving on localhost:8000'
    httpd.serve_forever()
