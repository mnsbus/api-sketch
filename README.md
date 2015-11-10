Trending
----------------------------------------------------------


Note: sample **output** can be found in output_minute_intervals.txt

Toprisers data flow:

* domains.py - harvests available domains for processing every 60 seconds & pings pages
* pages.py - gets the page data per domain & writes to db & pings accelerands
* accelerands.py - calculates the accelerating pages & updates the current toprisers

domains.py refreshes the domains once a minue, triggering
page.py to hit the pages server, triggering
accelerands.py to refresh the accelerating-pages-per-domain.

It runs but TODO:

* verify that the top risers are actually the top risers
* api server (flask/gunicorn)
* tests (!)
* server should also serve a page of available domains



