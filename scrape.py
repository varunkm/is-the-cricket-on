from datetime import datetime
from datetime import timedelta
import requests
import sys
from lxml import html


def parse_time(time):
    t, dur = time.split(', ')
    h, m = t.split(':')
    ap = m[2:]
    m = m[:2]
    h, m = int(h), int(m)
    dur = int(dur.split(' ')[0])
    if ap == 'pm':
        h += 12

    start = datetime.now()
    start = start.replace(hour=h)
    start = start.replace(minute=m)
    start = start.replace(second=0)
    delta = timedelta(seconds=(dur*60))
    end = start + delta
    return start, end


def now(start, end):
    timenow = datetime.now()
    return timenow >= start and timenow < end


def signal_on():
    print("on")


def signal_off():
    print("off")

def main(argv):
    URL = 'http://www.skysports.com/watch/tv-guide'
    resp = requests.get(URL)
    source = resp.content
    doc = html.document_fromstring(source)

    p_name = doc.xpath("//div[@class='row-table'][4]/div/a/h4")
    p_time = doc.xpath("//div[@class='row-table'][4]/div/a/p")

    for name, time in list(zip(p_name, p_time)):
        name = str(name.text_content()).strip()
        time = str(time.text_content()).strip()
        if 'Live' in name:
            start, end = parse_time(time)
            if now(start, end):
                signal_on()
                return
    signal_off()
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
