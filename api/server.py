import cgi
from wsgiref import simple_server

import falcon


class VideoCollection(object):

    def on_get(self, req, resp):
        # TODO(kgriffs): List videos
        pass

    def on_post(self, req, resp):
        form = cgi.FieldStorage(fp=req.stream, environ=req.env)
        title, video = form['title'].value, form['video'].file

        # if video_field.file:
        #     pass

        data = video.read()

        # TODO(kgriffs): Stream into Swift
        # TODO(kgriffs): On successful stream, create video document in mongo


app = application = falcon.API()

app.add_route('/videos', VideoCollection())

if __name__ == '__main__' :
    httpd = simple_server.make_server('localhost', 8000, app)
    print 'Serving on localhost:8000'
    httpd.serve_forever()
