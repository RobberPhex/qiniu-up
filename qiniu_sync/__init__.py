import os
from os.path import join, relpath, getsize
import configparser
from qiniu import Auth, BucketManager, put_file, etag
import argparse


def list_file(base_path):
    for root, dirs, files in os.walk(base_path):
        for f in files:
            yield relpath(join(root, f), base_path)


def upload(q, bucket_name, local_path, remote_path):
    bucket = BucketManager(q)
    for rel_path in list_file(local_path):
        key = join(remote_path, rel_path)
        s, _ = bucket.stat(bucket_name, key)
        if not s:
            token = q.upload_token(bucket_name, key, 3600)
            print('uploading %s' % (rel_path))
            put_file(token, key, join(local_path, rel_path))
        elif s['fsize'] != getsize(join(local_path, rel_path)) \
                or s['hash'] != etag(join(local_path, rel_path)):
            token = q.upload_token(bucket_name, key, 3600)
            print('uploading %s' % (rel_path))
            put_file(token, key, join(local_path, rel_path))
        else:
            print('file %s' % (rel_path))


def main():
    parser = argparse.ArgumentParser(description='upload local file to qiniu.')
    parser.add_argument('--config', '-c', default='config.ini', dest='config_file', help='config file')
    parser.add_argument('--local-path', '-l', dest='local_path', required=True, help='which local path to upload')
    parser.add_argument('--remote-path', '-r', default='', dest='remote_path', help='which remote path to upload to')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config_file)
    access_key = config['default']['AccessKey']
    secret_key = config['default']['SecretKey']
    bucket_name = config['default']['BucketName']
    q = Auth(access_key, secret_key)

    upload(q, bucket_name, args.local_path, args.remote_path)


if __name__ == '__main__':
    main()
