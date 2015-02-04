#!/usr/bin/env python3
import os
import argparse
import logging
import threading

from string import ascii_lowercase, ascii_uppercase
from urllib import request, error


def create_directory(path):
    if path is not None:
        directory = path
    else:
        directory = os.path.join(os.path.curdir + '/files/')

    if not os.path.exists(directory):
        logging.info('Directory', directory, 'does not exist. Creating it.')
        os.makedirs(directory)

    return directory


def create_links(var_link, iterations):

    variables = ['{I}', '{a}', '{A}']

    int_count = str.count(var_link, variables[0])
    lowercase_count = str.count(var_link, variables[1])
    uppercase_count = str.count(var_link, variables[2])

    links = replace_integer(var_link, iterations)
    for i in range(int_count - 1):
        for j in range(len(links)):
            links.extend(replace_integer(links.pop(i), iterations))

    for i in range(lowercase_count):
        for j in range(len(links)):
            links.extend(replace_lowercase(links.pop(i)))

    for i in range(uppercase_count):
        for j in range(len(links)):
            links.extend(replace_uppercase(links.pop(i)))

    return links


def thread_download(i, link, directory):
    try:
        file_ext = os.path.splitext(link)
        filename = os.path.join(directory, str(i) + file_ext[1])
        request.urlretrieve(link, filename)
        print('\nSUCCESS:', link, '\nDownloaded to:', filename)
    except error.URLError:
        increment_failed()


def download(links, directory):
    global failed
    failed = 0

    thread_list = []
    print('\n-\tDOWNLOADS\t-\n')

    for i, link in enumerate(links):
        t = threading.Thread(target=thread_download, args=(i, link, directory))
        thread_list.append(t)
        t.start()

    for thread in thread_list:
        thread.join()
    logging.info('\nFinished running ' + str(len(thread_list)) + ' threads')
    print('\nNumber of links failed:', failed)


def increment_failed():
    global failed
    failed += 1


def replace_integer(var_link, iterations):

    temp_list = []

    for i in range(iterations):
        temp_list.append(str.replace(var_link, '{I}', str(i), 1))

    return temp_list


def replace_lowercase(var_link):

    temp_list = []

    for l in ascii_lowercase:
        temp_list.append(str.replace(var_link, '{a}', l, 1))

    return temp_list


def replace_uppercase(var_link):

    temp_list = []

    for u in ascii_uppercase:
        temp_list.append(str.replace(var_link, '{A}', u, 1))

    return temp_list


def main():
    args = init()

    links = create_links(args.link, args.iterations + 1)
    if not args.urls:
        print('#########################')
        print('#\tPYDL v0.0.1\t#')
        print('#########################\n')
        logging.basicConfig(level=args.verbose, format='%(message)s')
        directory = create_directory(args.path)

        if args.verbose == logging.INFO:
            print('-\tLINKS\t-\n')
            for link in links:
                print(link)

        download(links, directory)
    else:
        for link in links:
            print(link)


def init():
    parser = argparse.ArgumentParser(
        description='pydl is a tool to download sets of files with '
                    'incrementable occurences of integers and/or characters')

    parser.add_argument('link', metavar='link', type=str,
                        help='Use {I}, {a} or {A} for variable increments,'
                             ' where I is integer and a/A is alphabetical variables.\n'
                             'E.g http://somewebsite.com/Picture{I}.jpg'
                             'Gives http://somewebsite.com/Picture1.jpg'
                             ', http://somewebsite.com/Picture2.jpg and so on.'
                        )

    parser.add_argument('-i', '--iterations', dest='iterations',
                        type=int, default=10,
                        help='Specify max integer for link creation.')

    parser.add_argument('-u', '--urls', dest='urls',
                        action='store_const', const=True,
                        help='Return ONLY the list of URLs')

    parser.add_argument('-v', dest='verbose', action='store_const',
                        const=logging.INFO, help='Shows some extra information')

    parser.add_argument('-p', '--path', type=str, dest='path',
                        help='Specify FULL path, otherwise it will '
                             'create a /files/ in your current directory')

    return parser.parse_args()


if __name__ == '__main__':
    main()
