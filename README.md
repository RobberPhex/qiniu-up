# qiniu-up

将本地文件夹上传到七牛.

- 若本地文件和七牛上的文件内容相同,则不上传
- 不删除七牛上的文件

## 使用方式

````
qiniu-up [--config CONFIG_FILE] --local-path LOCAL_PATH
                [--remote-path REMOTE_PATH]
````

- --config CONFIG_FILE, -c CONFIG_FILE

配置文件路径,若无,则直接从环境变量中读取

- --local-path LOCAL_PATH, -l LOCAL_PATH

本地文件夹路径

- --remote-path REMOTE_PATH, -r REMOTE_PATH

远端文件夹路径
