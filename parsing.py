# from _typeshed import FileDescriptor, Self
import requests
from bs4 import BeautifulSoup

def get_post():
    response = requests.get('https://habr.com/ru/all/')

    soup = BeautifulSoup(response.content, 'lxml')

    posts = soup.find(
        'h2', class_="tm-article-snippet__title tm-article-snippet__title_h2")
    postname = posts.find('a').find('span').contents[0]          # название поста
    # span  потом уберу
    postlink = posts.find('a').get('href')      # сслыка на пост

print(postlink)
print(postname)

class Comment:
    text: str
    comments: list[object]
    director: str

class Post:
    title: str
    comments: list[Comment]
	director: str
	tags: list[]

def get_posts(n):
    pass

def get_tree_comment(tree):
    result = {}
    for index, comment in enumerate(tree):
        text = '\n'.join([str(p.contents[0]) for p in comment.find_all('p')])
        result[index] = {'title' : text, 'comments' : []}
        if comment.find('div', class_='tm-comment-thread__children'):
            comments = comment.find('div', class_='tm-comment-thread__children').find_all('section', recursive=False)
            result[index]['comments'] = get_tree_comment(comments)
    return result

response = requests.get('https://habr.com' + postlink)        

soup = BeautifulSoup(response.content, 'lxml')

tree = soup.find('div', class_="tm-comments__tree")
Comment_tree = get_tree_comment(tree)
print(len(tree))




