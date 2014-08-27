#!/usr/bin/env python
#coding:utf8

## Coded with python2.7 libraries
## Original idea from http://ai-depot.com/articles/the-easy-way-to-extract-useful-text-from-arbitrary-html/


'''
Tool to extract Text which is informative or main theme of the HTML page.
This code analyses whether the text is informative or not by taking in account the 
density of text to html characters encountered in consecutive line_break

This code only considers text which has p tag


Usage: 

from usefulText import HTMLTextBlob
url = 'http:/website-address/goes/here'
tb = HTMLTextBlob.extract(url)

# methods available
usefulText = tb.extract(url, lower_threshold = 0.5, upper_threshold  = 1)
tb.getHTML # Output : 'String' gives HTML from url
tb.getURL  # Output : 'String' stores the present url
tb.TextObjects  # 'Output : [ Text(),Text() ,Text() ]'returns all the Text objects which stores information about text chunks, density and html_length parsed

Demo:
run from cmd line: # this will automatically open webbrowser

$ python usefulText.py

'''
import formatter, htmllib, StringIO
from formatter import AbstractFormatter
from htmllib import HTMLParser
import requests


# This class stores chunks of text and html parsed (length of html entities) to get the text
class Text(object):

    def __init__(self):
        self.text = ""
        self.html_length =0
        self.density =0
        self.tags = []

class TextWriter(formatter.AbstractWriter):

    def __init__(self, lower_threshold =0.5, upper_threshold = 0.999):
        self.lines = [Text()]
        # self.index will be first initiated through HTMLParser.parse_starttag() in ParsingTracker()
        self.last_index, self.index = 0, 0
        # Forma an instance of AbstractWriter with this class
        formatter.AbstractWriter.__init__(self)
        self.lower_threshold, self.upper_threshold = lower_threshold, upper_threshold
        self.exclude_tags = set(['script','noscript','embed','iframe','style'])
        self.imgs =0

    # This method is called when there are inline '\n'(is not a HTML line_break)
    # Output character data which has already been formatted for display.
    # '\n' evkes this method in writer to write output in sys.stdout
    def send_literal_data(self, data):
        print '\n\n<<%%%;%%%>>\n\n'
        self.writer.lines[-1].text += '<<%%%;%%%>>'
        return self.send_flowing_data(data)

    # This is called whenever there is need to change paragraph
    def send_line_break(self):
        return self.send_paragraph(1)

    def send_flowing_data(self, data):
        # How much text has been processed
        t = len(data)
        # Offset the index position (index now points to start of end_tag)
        self.index += t
        # Compute length of html code processed since last time
        h = self.index - self.last_index
        # Set the last_index to present index
        self.last_index = self.index
        # Store this information in current Text()
        self.lines[-1].text += data
        self.lines[-1].html_length += h

    def send_paragraph(self, blankline =1):
        # if previous Text() does not contain any text no need to create a new object
        if self.lines[-1].text in ["", " "]:
            return
        self.lines[-1].text += '\n'* (blankline)
        self.lines[-1].html_length += 2* (blankline) 
        self.lines.append(Text())

    def compute_density(self):
        self.total = 0.0
        for l in self.lines:
            l.density = len(l.text) / float(l.html_length) if l.html_length else 1.0
            self.total += l.density

        self.average = self.total/float(len(self.lines))

    def output(self):
        self.compute_density()
        output = StringIO.StringIO()
        for l in self.lines:
            print 'density : ',l.density, 'text : ',l.text, 'l.html_length : ', l.html_length, 'tags',l.tags   
            if not (set(l.tags) & self.exclude_tags) and self.lower_threshold <= l.density <= self.upper_threshold :
                output.write(l.text)

        return output.getvalue()

class ParsingTracker(htmllib.HTMLParser):

    def __init__(self, writer, *args):
        # writer is an interface with which HTMLParser interacts inorder to 
        # procude printable output
        self.writer = writer
        htmllib.HTMLParser.__init__(self, *args)
        self.imgs = 0
    
    # <style> : this is a start tag and index of '<' represents i 
    # this method overrides the original parse_starttag()
    # returns the same thing
    def parse_starttag(self, i):
        # Parsing returns the index of closing tag i.e '>'
        index = htmllib.HTMLParser.parse_starttag(self,i) 
        # Increment the writer's index to this index
        # to start collecting text
        self.writer.index =index
        return index

    # </style> : this is a closing tag
    # This method is called whenever endtag is encountered in HTMLParser
    # i is the index of '<' 
    def parse_endtag(self,i):
        self.writer.index = i
        return htmllib.HTMLParser.parse_endtag(self,i)

    # This method is called once when <p> tags are encountered
    # if text in Text() is from tags such as p
    def start_p(self, attrs):
        self.writer.lines[-1].tags.append('p')

    def start_div(self, attrs):
        self.writer.lines[-1].tags.append('div')

    def start_li(self, attrs):
        self.writer.lines[-1].tags.append('li')

    def start_ul(self, attrs):
        self.writer.lines[-1].tags.append('ul')

    def start_script(self, attrs):
        self.writer.lines[-1].tags.append('script')

    def start_noscript(self, attrs):
        self.writer.lines[-1].tags.append('noscript')

    def start_embed(self, attrs):
        self.writer.lines[-1].tags.append('embed')

    def start_iframe(self, attrs):
        self.writer.lines[-1].tags.append('iframe')

    def start_style(self, attrs):
        self.writer.lines[-1].tags.append('style')

    def start_img(self, attrs):
        self.writer.imgs +=1

class HTMLTextBlob(object):
   
    def __init__(self):
        pass

    def extract(self, url, lower_threshold =None, upper_threshold =None):
        self.url = url
        response = requests.get(url)
        if response.status_code == 200:
            self.html = response.content
        else:
            print "url can not be accessed. bad request...\n"
            return self.end()
        return self.extract_from_html(self.html, lower_threshold, upper_threshold)

    def extract_from_html(self, html, lower_threshold =None, upper_threshold =None):
        # Create an instance of ParsingTracker and pass TextWriter() to collect approrpiate output
        self.writer = TextWriter()
        formatter = AbstractFormatter(self.writer)
        self.parser = ParsingTracker(self.writer, formatter)

        if lower_threshold: 
            self.writer.lower_threshold = lower_threshold
        if upper_threshold:
            self.writer.upper_threshold = upper_threshold

        self.parser.feed(html)
        self.parser.close()
        return self.writer.output()

    def soup_extract(self, url):
        self.url = url
        response = requests.get(url)
        if response.status_code == 200:
            self.html = response.content
        else:
            print "url can not be accessed. bad request...\n"
            return self.end()

        self.soup = BeautifulSoup(self.html)
        return " ".join([unicode(i.string) for i in self.soup.find_all('p') if i.string != None])

    def getHTML(self):
        return self.html

    def getURL(self):
        return self.url 

    def TextObjects(self):
        return self.writer.lines

    def averageDensity(self):
        return self.writer.average

    def totalDensity(self):
        return self.writer.totalDensity

    def end(self):
        return "exiting...\n"

class DataSet(object):

    def __init__(self):
        self.tb= HTMLTextBlob()
        self.log = open('data_set.txt','w+')
        self.url_log =open('data_set.txt', 'w+')
        self.sample_size =0
        self.input_size =3
        self.output_size =1

    def data(self, url):
        self.url_log.write(url+'\n')
        _ = self.self_learn(url)

        return True

    def end_training(self):
        self.log.seek(0)
        samples = str(self.sample_size) + str(self.input_size) + str(self.output_size)+'\n'
        self.log.write(samples)
        self.log.close() 
        return True

    def self_learn(self, url):
        thresholds =[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        for i in thresholds:
            text = self.tb.extract(url, i, 0.999)
            print '\n\n\n\n\n-----EXTRACTED TEXT----\n\n\n\n'
            print text
            ok = input('Is this ok? [1/0]')
            if ok:
                average = self.tb.averageDensity()
                lines = len(self.tb.writer.lines)
                no_img = self.tb.writer.imgs               
                self.log.write(str(round(average, 4))+' '+ str(lines)+' '+str(no_img)+'\n'+str(i)+'\n')
                self.sample_size +=1
                break
        return False

class NNModel(object):

    def __init__(self):
        pass







if __name__=='__main__':
    url = "http://www.foxnews.com/world/2014/07/29/israel-strikes-symbols-hamas-control-in-gaza-shuts-down-power-plant/"
    url = 'http://insidemovies.ew.com/2014/08/01/lionsgate-sues-online-leakers-expendables-3/'
    # TextBlob from that html
    tb =  HTMLTextBlob()
    print tb.extract(url)

    witness = input('Want to see the webpage?[1/0]')
    if witness == 1:
        # actual article
        import webbrowser
        webbrowser.open(url,new=1)
