
import mako.lookup
import mako.template
import tornado.web

#route
class Route(object):
    urls = []
    def __call__(self, url):
        def _(cls):
            self.urls.append((url, cls))
            return cls
        return _
route = Route()


#模板
lookup = mako.lookup.TemplateLookup(
        directories=['./static/html', './static/css'],
        module_directory='/tmp/mako',
        input_encoding='utf-8',
)


class View(tornado.web.RequestHandler):
    def render(self, filename=None, **kwargs):
        if not filename:
            filename = '/%s/%s.html' % ('/'.join(self.__module__.split('.')[1:-1]), self.__class__.__name__.lower())

        tmpl = lookup.get_template(filename.replace(r'//', r'/'))
        self.finish(tmpl.render(req=self, **kwargs))
