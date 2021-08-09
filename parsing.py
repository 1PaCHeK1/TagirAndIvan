# from _typeshed import FileDescriptor, Self
import requests
from typing import List
from bs4 import BeautifulSoup

class Comment:
    text: str
    comments: List[object]
    director: str

class Post:
    title: str
    comments: List[Comment]
    director: str
    tags: List[str]
    url: str

def get_posts():
    response = requests.get('https://habr.com/ru/all/')
    soup = BeautifulSoup(response.content, 'lxml')
    posts = soup.find_all('article')
    for post in posts:
        postname = post.find('h2', class_="tm-article-snippet__title tm-article-snippet__title_h2").find('span').contents[0]          # название поста
        postlink = post.find('h2', class_="tm-article-snippet__title tm-article-snippet__title_h2").find('a').get('href')      # сслыка на пост


        print(postlink)
        print(postname)

    # return postlink, postname


def get_tree_comment(tree):
    result = {}
    for index, comment in enumerate(tree):
        text = '\n'.join([str(p.contents[0]) for p in comment.find_all('p')])
        result[index] = {'title' : text, 'comments' : []}
        if comment.find('div', class_='tm-comment-thread__children'):
            comments = comment.find('div', class_='tm-comment-thread__children').find_all('section', recursive=False)
            result[index]['comments'] = get_tree_comment(comments)
    return result



get_posts()

