import sys

orig_stdout = sys.stdout
f = file('out.txt', 'w')
sys.stdout = f

import usefulText as u
url = 'http://insidemovies.ew.com/2014/08/01/lionsgate-sues-online-leakers-expendables-3/'
# TextBlob from that html
tb =  u.HTMLTextBlob()
print tb.extract(url)



sys.stdout = orig_stdout
f.close()