from __future__ import print_function
import sys
import io
import json
from datetime import datetime
from flask import render_template, request, send_file

from sight import app, SightEngine


if not hasattr(app, 'se_instance'):
    sys.stdout.write('Processing catalog file... ')
    sys.stdout.flush()
    app.se_instance = SightEngine.SightEngine(app.config["lib_location"])
    sys.stdout.write("[OK]\n")
else:
    print('loaded SE from app')
se = app.se_instance


@app.template_filter('secondstohms')
def secondstohms(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)


# Use this for json.dumps() calls that may contain datetime values,
# because JSON chokes on them unless we serialize them manually.
def jsondefault(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime):
        import calendar

        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis
    else:
        return obj



@app.route('/')
def dashboard_view():
    return render_template('layout.html', se=se)


@app.route('/persistentid/<pid>/artwork')
def getArtwork(pid):
    artwork = se.getArtwork(pid)
    
    return send_file(io.BytesIO(artwork), mimetype='image/jpeg', cache_timeout=0) if artwork else ''


