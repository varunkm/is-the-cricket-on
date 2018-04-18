from datetime import datetime
from datetime import timedelta
import requests
import sys
from lxml import html
import wiringpi as wiringpi

pin = 1
URL = 'http://www.skysports.com/watch/tv-guide'

# time looks like: "(h)h:mm(am/pm), [duration] mins"
# e.g. 7:30pm, 120 mins or 11:15am, 45 mins
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
    wiringpi.digitalWrite(pin, 1)


def signal_off():
    wiringpi.digitalWrite(pin, 0)


def main(argv):
    wiringpi.wiringPiSetup()
    wiringpi.pinMode(pin, 1)
    
    resp = requests.get(URL)
    source = resp.content
    doc = html.document_fromstring(source)
    
    # the cricket channel is the fourth row in the tv guide table
    names = doc.xpath("//div[@class='row-table'][4]/div/a/h4")
    times = doc.xpath("//div[@class='row-table'][4]/div/a/p")

    for name, time in list(zip(names, times)):
        name = str(name.text_content()).strip()
        time = str(time.text_content()).strip()
        if 'Live' in name:
            start, end = parse_time(time)
            if now(start, end):
                signal_on()
                return
    signal_off()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
