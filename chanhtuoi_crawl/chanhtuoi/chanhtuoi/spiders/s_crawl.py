from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from crawl_chanhtuoi import JobSpider
from time import gmtime, strftime
from scrapy.utils.log import configure_logging

def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    settings = get_project_settings()
    configure_logging()
    runner = CrawlerRunner(settings)
    return runner.crawl(JobSpider)

def schedule_next_crawl(null, sleep_time):
    """
    Schedule the next crawl
    """
    reactor.callLater(sleep_time, crawl)

def crawl():
    """
    A "recursive" function that schedules a crawl 30 seconds after
    each successful crawl.
    """
    # crawl_job() returns a Deferred
    d = crawl_job()
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    d.addCallback(schedule_next_crawl, 60 * 60 * 6)
    d.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)

if __name__=="__main__":
    print('Chanhtuoi')
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    crawl()
    reactor.run()


# import datetime as dt

# def schedule_next_crawl(null, hour, minute):
#     tomorrow = (
#         dt.datetime.now() + dt.timedelta(days=1)
#         ).replace(hour=hour, minute=minute, second=0, microsecond=0)
#     sleep_time = (tomorrow - dt.datetime.now()).total_seconds()
#     reactor.callLater(sleep_time, crawl)

# def crawl():
#     d = crawl_job()
#     # crawl everyday at 1pm
#     d.addCallback(schedule_next_crawl, hour=13, minute=30)
