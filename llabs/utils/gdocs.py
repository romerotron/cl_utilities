from bs4 import BeautifulSoup
import requests

HTML_EXPORT_URL = u'https://docs.google.com/feeds/download/documents/export/Export?id={0}&exportFormat=html'


class GoogleDoc(object):
    """ A Google Doc object """

    def __init__(self, gdoc_url):
        """ Initialize the object with the passed thru URL """
        self.url = gdoc_url
        self.doc_id = self.get_doc_id()
        self.html_url = self.get_html_url()
        self.html = self.fetch_html()
        self.html_body = self.get_html_body()

    def get_doc_id(self):
        """ Return the doc_id of the doc from the url """
        if self.url:
            return self.url.split('/')[5]
        return None

    def get_html_body(self):
        """ Return the html_body of the doc """
        if self.html:
            soup = BeautifulSoup(self.html, 'html.parser')
            return soup.body.contents[0]
        return None

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
