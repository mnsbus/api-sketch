Toprisers: Chartbeat BE Engineering Architecture Challenge
----------------------------------------------------------
*Michael Scharf*

Note: sampple **output** can be found in output_minute_intervals.txt

Toprisers data flow:

* domains.py - harvests available domains for processing every 60 seconds & pings toppages
* toppages.py - gets the toppage data per domain & writes to db & pings accelerands
* accelerands.py - calculates the accelerating pages & updates the current toprisers

domains.py refreshes the domains once a minue, triggering
toppage.py to hit the toppages server, triggering
accelerands.py to refresh the accelerating-pages-per-domain.

It runs but TODO:

* verify that the top risers are actually the top risers
* api server (flask/gunicorn)
* tests (!)
* server should also serve a page of available domains

I can continue to clean it up, but, as discussed, it took me a full day
(plus much pre-thinking) to get to up to the pre-calculation piece. On that,
I have now worked a full two days (it's been two years since I've done SQL,
and pandas fail), and it's still not close to where it should be.

Thank you for the opportunity to think this through, and to work with a piece of
the toppages API.

Best,
Mike


