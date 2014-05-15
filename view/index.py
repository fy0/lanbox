
import os
import config
from os.path import join
from view import View, route

@route('/')
class index(View):
    def get(self):
        prefix_path = self.get_argument('p', '')
        data_path = join(config.REAL_PATH, prefix_path)
        data = []
        for i in os.listdir(data_path):
            path = join(data_path, i)
            stat = os.stat(path)
            info = {
                'name': i,
                'ext': os.path.splitext(path)[1], #获取扩展名
                'is_dir': os.path.isdir(path), #是否为目录
                'atime': stat.st_atime, #访问时间
                'mtime': stat.st_mtime, #修改时间
                'ctime': stat.st_ctime, #创建时间
                'size': stat.st_size, #文件大小
                'source': join(prefix_path, i), #相对路径
            }
            data.append(info)
        self.render(data=data, prefix_path=prefix_path)

@route('/vplay')
class vplay(View):
    def get(self):
        v = self.get_argument('v')
        self.render(vsource=v)
