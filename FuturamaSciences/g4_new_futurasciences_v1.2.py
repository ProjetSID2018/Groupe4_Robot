﻿""" -*- coding: utf-8 -*-
 Groupe 4
 MOTHES Céline
 HERVE Pierrick
 V1 : create code
 V1.1 : create function
 V1.2 : code optimization
"""
import unidecode
import re
import g4_utils_v40 as utils
import datetime as date


def recovery_information_fusc(url):
    """
        Arguments:
            url : string
        Return :
            article : dictionary
        It retrieve for each article the title, newspaper, author, date, theme
    """
    soup = utils.recovery_flux_url_rss(url)

    # retrieve title
    title = ''
    title = unidecode.unidecode(soup.title.string)
    indice = title.find('|')
    if indice != -1:
        title = title[:indice-1]
    # retrieve the author
    author = []
    tag_author = soup.find('h3', attrs={'itemprop': 'author'})
    author.append(tag_author.get_text())

    # retrieve date
    publi_date = ''
    regex_date = re. search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', soup.time.string)
    publi_date = regex_date.group(0)
    publi_date = str(date.datetime.strptime(publi_date, '%d/%m/%Y').date())

    # retrieve content
    content = ''
    for p in soup.find_all('p'):
        for p2 in re.finditer('py0p5', p.get('class')[-1]):
            content += p.get_text()
    content = unidecode.unidecode(content)

    # retrieve theme
    delimiter = url.split('/')
    theme = delimiter[3]

    article = utils.recovery_article(title, 'FuturaSciences', author,
                                     publi_date, content, theme)
    return(article)


def recovery_link_new_articles(url_rss):
    """
        Argument:
            url_rss : string
        Return:
            retrieving links of new articles thanks to the rss feed
    """
    soup = utils.recovery_flux_url_rss(url_rss)
    list_link = []
    for link in soup.find_all('a', attrs={'class': 'first-capitalize'}):
        list_link.append('https://www.futura-sciences.com' + link.get('href'))
    return(list_link)


def recovery_new_articles_fusc():
    """
        it create a json for each new article
    """
    links = recovery_link_new_articles('https://www.futura-sciences.com/' +
                                       'flux-rss/')
    list_articles = []
    file_target = '/var/www/html/projet2018/data/clean/robot/'
    for article in links:
        new_article = recovery_information_fusc(article)
        if not utils.is_empty(new_article):
            list_articles.append(new_article)
    utils.create_json(file_target, list_articles, 'FuturaSciences', 'fusc')


if __name__ == '__main__':
    recovery_new_articles_fusc()
