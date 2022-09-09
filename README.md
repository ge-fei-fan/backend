# 小猫日常记录后端

部署方法
```text
1、修改setting中的数据库配置
2、安装依赖环境
	pip3 install -r requirements.txt
3、 执行迁移命令：
	python3 manage.py makemigrations
	python3 manage.py migrate
4、修改uwsgi.ini文件
        启动: uwsgi --ini uwsgi.ini
        停止: uwsgi --stop uwsgi.pid
```


