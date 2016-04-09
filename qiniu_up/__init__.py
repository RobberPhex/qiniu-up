import argparse
import configparser
import logging
import os
from os.path import getsize, join, relpath

from qiniu import Auth, BucketManager, etag, put_file


def list_file(base_path):
    for root, dirs, files in os.walk(base_path):
        for f in files:
            yield relpath(join(root, f), base_path)


def upload(q, bucket_name, local_path, remote_path):
    bucket = BucketManager(q)
    assert bucket.stat(bucket_name, '')[1].status_code != 401
    for rel_path in list_file(local_path):
        key = join(remote_path, rel_path)
        stat, _ = bucket.stat(bucket_name, key)
        if not stat:
            token = q.upload_token(bucket_name, key, 3600)
            logging.info('uploading new file %s' % rel_path)
            put_file(token, key, join(local_path, rel_path))
        elif stat['fsize'] != getsize(join(local_path, rel_path)) \
                or stat['hash'] != etag(join(local_path, rel_path)):
            token = q.upload_token(bucket_name, key, 3600)
            logging.info('uploading diff file %s' % rel_path)
            put_file(token, key, join(local_path, rel_path))
        else:
            logging.debug('file %s is identical' % rel_path)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='upload local file to qiniu.')
    parser.add_argument('--config', '-c', dest='config_file', help='config file')
    parser.add_argument('--local-path', '-l', dest='local_path', required=True, help='which local path to upload')
    parser.add_argument('--remote-path', '-r', default='', dest='remote_path', help='which remote path to upload to')
    args = parser.parse_args()

    if args.config_file:
        config = configparser.ConfigParser()
        config.read(args.config_file)
        access_key = config['default']['AccessKey']
        secret_key = config['default']['SecretKey']
        bucket_name = config['default']['BucketName']
    else:
        access_key = os.getenv('QINIU_ACCESS_KEY')
        secret_key = os.getenv('QINIU_SECRET_KEY')
        bucket_name = os.getenv('QINIU_BUCKET_NAME')

    q = Auth(access_key, secret_key)
    upload(q, bucket_name, args.local_path, args.remote_path)


if __name__ == '__main__':
    main()
