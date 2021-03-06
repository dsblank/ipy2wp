# -*- coding: utf-8 -*-

## Based on the script originally published on
## http://www.jansipke.nl/using-python-to-add-new-posts-in-wordpress/

import datetime
import argparse
try:
    import xmlrpc.client as xmlrpclib #python3
except:
    import xmlrpclib # python2

import IPython.nbconvert as nbc

#options
parser = argparse.ArgumentParser(description='Publish ipynb to wp')
parser.add_argument('--xmlrpc-url', 
                    help="The XML-RPC server/path url")
parser.add_argument('--user', 
                    help="The wordpress user")
parser.add_argument('--password', 
                    help="The wordpress user password")
parser.add_argument('--nb', 
                    help="The path and notebook filename")
parser.add_argument('--title', 
                    help="The title for the post in the site")
parser.add_argument('--categories', nargs='+', 
                    help="A list of categories separated by space")
parser.add_argument('--tags', nargs='+', 
                    help="A list of tags separated by space")
args = parser.parse_args()

err_msg = "You should provide a value for the option --{}"

if args.xmlrpc_url:
    server = xmlrpclib.ServerProxy(args.xmlrpc_url)
else:
    raise Exception(err_msg.format('xmlrpc-url'))

if args.user:
    user = args.user
else:
    raise Exception(err_msg.format('user'))

if args.password:
    password = args.password
else:
    raise Exception(err_msg.format('password'))
    
if args.nb:
    post = nbc.export_html(nb = args.nb, template_file="basic")[0]
else:
    raise Exception(err_msg.format('nb'))

if args.title:
    title = args.title
else:
    raise Exception(err_msg.format('title'))

if args.categories:
    categories = args.categories
else:
    categories = ['Uncategorized']

if args.tags:
    tags = args.tags
else:
    tags = ''

if __name__ == '__main__':
    ## Publishing the post
    date_created = xmlrpclib.DateTime(datetime.datetime.now())
    status_published = 0
    wp_blogid = ""
    data = {'title': title, 
            'description': post,
            'post_type': 'post',
            'dateCreated': date_created,
            'mt_allow_comments': 'open',
            'mt_allow_pings': 'open',
            'post_status': 'draft',
            'categories': categories, 
            'mt_keywords': tags}
    post_id = server.metaWeblog.newPost(wp_blogid, 
                                        user, 
                                        password, 
                                        data, 
                                        status_published)
