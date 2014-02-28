import falcon


class VideoCollection(object):

    def on_get(self):
        # TODO(kgriffs): List videos

    def on_post(self):
        # TODO(kgriffs): Stream into Swift
        # TODO(kgriffs): On successful stream, create video document in mongo


app = falcon.API()

app.add_route('/videos', VideoCollection())
