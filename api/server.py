import cgi
from wsgiref import simple_server

import falcon
import uuid
import pyrax

class VideoCollection(object):

    def __init__(self):
        pyrax.keyring_auth("rackervision")
        pyrax.queues.client_id = _generate_id()
        self.unprocessed_container = pyrax.cloudfiles.get_container("unprocessed")
        self.processed_container = pyrax.cloudfiles.get_container("processed")
        self.queue = pyrax.queues.get("unprocessed")

    def on_get(self, req, resp):
        # TODO(kgriffs): List videos
        pass

    def on_post(self, req, resp):
        form = cgi.FieldStorage(fp=req.stream, environ=req.env)
        title, video = form['title'].value, form['video'].file

        # if video_field.file:
        #     pass

        #data = video
        uuid = _generate_id()
        self.unprocessed_container.upload_file(video, uuid)
        self.queue.post_message(uuid, 1209599)
        

        # TODO(kgriffs): Stream into Swift
        # TODO(kgriffs): On successful stream, create video document in mongo


def _generate_id():
    return str(uuid.uuid1())


app = application = falcon.API()

app.add_route('/videos', VideoCollection())

if __name__ == '__main__' :
    httpd = simple_server.make_server('localhost', 8000, app)
    print 'Serving on localhost:8000'
    httpd.serve_forever()
