from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

HTML_EXPORT_URL = u'https://docs.google.com/feeds/download/documents/export/Export?id={0}&exportFormat=html'


class GoogleDoc(object):
    """ A Google Doc object """

    @classmethod
    def clean_header_tag(cls, tag):
        return u'<{0}>{1}</{2}>'.format(tag.name, tag.contents[0].string, tag.name)

    @classmethod
    def is_header_tag(cls, tag):
        """ Return True if header tag, else False

        Args:
            tag: A BeautifulSoup Tag object
        """
        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return True
        return False

    @classmethod
    def is_anchor_tag(cls, tag):
        """ Return True if header tag, else False

        Args:
            tag: A BeautifulSoup Tag object
        """
        if isinstance(tag, Tag) and tag.name == 'a':
            return True
        return False

    @classmethod
    def tag_as_a(cls, tag):
        """ Return the tag as an anchor stripping the Google redirect

        Args:
            tag: A BeautifulSoup Tag object
        """
        link = tag['href'].split('google.com/url?q=')[1]
        link = link.split('&sa=D&u')[0]
        return u'<a href="{0}">{1}</a>'.format(link, tag.string)

    @classmethod
    def tag_as_p(cls, tag):
        """ Return the tag as a <p>

        Args:
            tag: A BeautifulSoup Tag object
        """
        return u'<p>{0}</p>'.format(tag.string)

    def __init__(self, gdoc_url, **kwargs):
        """ Initialize the object with the passed thru URL """
        self.url = gdoc_url
        self.doc_id = self.get_doc_id()
        self.html_url = self.get_html_url()
        self.html = self.fetch_html()
        self.html_body = self.get_html_body(**kwargs)

    def get_doc_id(self):
        """ Return the doc_id of the doc from the url """
        if self.url:
            return self.url.split('/')[5]
        return None

    def get_html_body(self, **kwargs):
        """ Return the html_body of the doc """
        if self.html:
            soup = BeautifulSoup(self.html, 'html.parser')
            return ''.join(['%s' % x for x in soup.body.contents])
        return None

    def get_cleaned_html_body(self, **kwargs):
        """ Return the html_body of the doc cleaned of classes
        """
        if self.html_body:
            soup = BeautifulSoup(self.html, 'html.parser')
            body = [x for x in soup.body.contents]
            html = u''

            for tag in body:
                if GoogleDoc.is_header_tag(tag):
                    html += self.cleanded_header_tag(tag)

                elif (tag.name == 'p' and len(tag.contents) == 1 and
                      len(tag.contents[0]) == 0):
                    continue

                elif tag.name == 'p' and tag.string:
                    html += GoogleDoc.tag_as_p(tag)

                elif ((tag.name == 'p' and len(tag.contents) == 1)
                      and len(tag.find_all('img')) == 1):
                    html += u'<p><img class="gdoc" src="{0}"></p>'.format(tag.find_all('img')[0]['src'])

                elif len(tag.contents) > 1:
                    contents_html = u''
                    for child in tag.contents:
                        if GoogleDoc.is_anchor_tag(child.contents[0]):
                            contents_html += GoogleDoc.tag_as_a(child.contents[0])
                        else:
                            contents_html += child.contents[0].string
                    html += u'<p>{0}</p>'.format(contents_html)

            return html

    def get_html_url(self):
        """ Return the html_url of the doc """
        if self.url and self.doc_id:
            return HTML_EXPORT_URL.format(self.doc_id)
        return None

    def fetch_html(self):
        """ fetch the Google doc html """
        try:
            r = requests.get(self.html_url)
            if r.status_code == 200 and r.content:
                return r.content
        except:
            pass
        return None
