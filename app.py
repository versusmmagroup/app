from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, DateField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_moment import Moment

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'flask'
app.config['MYSQL_DB'] = 'versusmma'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

@app.route('/chart1/')
def chart1():
    'hi'
    return render_template('chart1.html')

@app.route('/chart/<string:fig_name>/')
def chart(fig_name):
    cur = mysql.connection.cursor()
    history = cur.execute("SELECT * FROM histories WHERE fig_name = %s ORDER BY date_ DESC", [fig_name])
    history = cur.fetchall()

    tfs = cur.execute("SELECT COUNT(fig_name) as tfs from histories where fig_name = %s", [fig_name])
    tfs = cur.fetchone()
    tw = cur.execute("SELECT COUNT(fig_name) as tw from histories where result = 'win' and fig_name = %s", [fig_name])
    tw = cur.fetchone()
    tl = cur.execute("SELECT COUNT(fig_name) as tl from histories where result = 'loss' and fig_name = %s", [fig_name])
    tl = cur.fetchone()
    draws = cur.execute("SELECT COUNT(fig_name) as draws from histories where result = 'draw' and fig_name = %s", [fig_name])
    draws = cur.fetchone()
    nc = cur.execute("SELECT COUNT(fig_name) as nc from histories where result = 'NC' and fig_name = %s", [fig_name])
    nc = cur.fetchone()


    tkow = cur.execute("SELECT COUNT(fig_name) as tkow FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkow = cur.fetchone()
    tsubw = cur.execute("SELECT COUNT(fig_name) as tsubw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubw = cur.fetchone()
    tdecw = cur.execute("SELECT COUNT(fig_name) as tdecw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecw = cur.fetchone()
    tkol = cur.execute("SELECT COUNT(fig_name) as tkol FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkol = cur.fetchone()
    tsubl = cur.execute("SELECT COUNT(fig_name) as tsubl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubl = cur.fetchone()
    tdecl = cur.execute("SELECT COUNT(fig_name) as tdecl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecl = cur.fetchone()


    ssla = cur.execute("SELECT SUM(ssl_) as ssla from stats where fig_name = %s", [fig_name])
    ssla = cur.fetchone()

    ssat = cur.execute("SELECT SUM(ssa_) as ssat from stats where fig_name = %s", [fig_name])
    ssat = cur.fetchone()
    ssacc = cur.execute("SELECT IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0) as ssacc from stats where fig_name = %s", [fig_name])
    ssacc = cur.fetchone()


    tsl = cur.execute("SELECT SUM(tsl_) as tsl from stats where fig_name = %s", [fig_name])
    tsl = cur.fetchone()
    tsat = cur.execute("SELECT SUM(tsa_) as tsat from stats where fig_name = %s", [fig_name])
    tsat = cur.fetchone()
    tsacc = cur.execute("SELECT IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0) as tsacc from stats where fig_name = %s", [fig_name])
    tsacc = cur.fetchone()


    tdl = cur.execute("SELECT SUM(tdl_) as tdl from stats where fig_name = %s", [fig_name])
    tdl = cur.fetchone()
    tdat = cur.execute("SELECT SUM(tda_) as tdat from stats where fig_name = %s", [fig_name])
    tdat = cur.fetchone()
    tdacc = cur.execute("SELECT IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0) as tdacc from stats where fig_name = %s", [fig_name])
    tdacc = cur.fetchone()


    subs = cur.execute("SELECT SUM(sub_) as subs from stats where fig_name = %s", [fig_name])
    subs = cur.fetchone()
    passes = cur.execute("SELECT SUM(pass_) as passes from stats where fig_name = %s", [fig_name])
    passes = cur.fetchone()
    rev = cur.execute("SELECT SUM(rev) as rev from stats where fig_name = %s", [fig_name])
    rev = cur.fetchone()


    hsl = cur.execute("SELECT SUM(headl_) as hsl from stats where fig_name = %s", [fig_name])
    hsl = cur.fetchone()
    hsat = cur.execute("SELECT SUM(heada_) as hsat from stats where fig_name = %s", [fig_name])
    hsat = cur.fetchone()
    hsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as hsacc from stats where fig_name = %s", [fig_name])
    hsacc = cur.fetchone()


    bsl = cur.execute("SELECT SUM(bodyl_) as bsl from stats where fig_name = %s", [fig_name])
    bsl = cur.fetchone()
    bsat = cur.execute("SELECT SUM(bodya_) as bsat from stats where fig_name = %s", [fig_name])
    bsat = cur.fetchone()
    bsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as bsacc from stats where fig_name = %s", [fig_name])
    bsacc = cur.fetchone()


    lsl = cur.execute("SELECT SUM(legl_) as lsl from stats where fig_name = %s", [fig_name])
    lsl = cur.fetchone()
    lsat = cur.execute("SELECT SUM(lega_) as lsat from stats where fig_name = %s", [fig_name])
    lsat = cur.fetchone()
    lsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as lsacc from stats where fig_name = %s", [fig_name])
    lsacc = cur.fetchone()


    dsl = cur.execute("SELECT SUM(distl_) as dsl from stats where fig_name = %s", [fig_name])
    dsl = cur.fetchone()
    dsat = cur.execute("SELECT SUM(dista_) as dsat from stats where fig_name = %s", [fig_name])
    dsat = cur.fetchone()
    dsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as dsacc from stats where fig_name = %s", [fig_name])
    dsacc = cur.fetchone()


    csl = cur.execute("SELECT SUM(clinchl_) as csl from stats where fig_name = %s", [fig_name])
    csl = cur.fetchone()
    csat = cur.execute("SELECT SUM(clincha_) as csat from stats where fig_name = %s", [fig_name])
    csat = cur.fetchone()
    csacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as csacc from stats where fig_name = %s", [fig_name])
    csacc = cur.fetchone()


    gsl = cur.execute("SELECT SUM(groundl_) as gsl from stats where fig_name = %s", [fig_name])
    gsl = cur.fetchone()
    gsat = cur.execute("SELECT SUM(grounda_) as gsat from stats where fig_name = %s", [fig_name])
    gsat = cur.fetchone()
    gsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as gsacc from stats where fig_name = %s", [fig_name])
    gsacc = cur.fetchone()



    dkd = cur.execute("SELECT SUM(kd) as dkd from stats where opponent = %s", [fig_name])
    dkd = cur.fetchone()


    dssla = cur.execute("SELECT SUM(ssl_) as dssla from stats where opponent = %s", [fig_name])
    dssla = cur.fetchone()

    dssat = cur.execute("SELECT SUM(ssa_) as dssat from stats where opponent = %s", [fig_name])
    dssat = cur.fetchone()


    dssacc = cur.execute("SELECT IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0) as dssacc from stats where opponent = %s", [fig_name])
    dssacc = cur.fetchone()


    dtsl = cur.execute("SELECT SUM(tsl_) as dtsl from stats where opponent = %s", [fig_name])
    dtsl = cur.fetchone()
    dtsat = cur.execute("SELECT SUM(tsa_) as dtsat from stats where opponent = %s", [fig_name])
    dtsat = cur.fetchone()
    dtsacc = cur.execute("SELECT IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0) as dtsacc from stats where opponent = %s", [fig_name])
    dtsacc = cur.fetchone()


    dtdl = cur.execute("SELECT SUM(tdl_) as dtdl from stats where opponent = %s", [fig_name])
    dtdl = cur.fetchone()
    dtdat = cur.execute("SELECT SUM(tda_) as dtdat from stats where opponent = %s", [fig_name])
    dtdat = cur.fetchone()
    dtdacc = cur.execute("SELECT IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0) as dtdacc from stats where opponent = %s", [fig_name])
    dtdacc = cur.fetchone()


    dsubs = cur.execute("SELECT SUM(sub_) as dsubs from stats where opponent = %s", [fig_name])
    dsubs = cur.fetchone()
    dpasses = cur.execute("SELECT SUM(pass_) as dpasses from stats where opponent = %s", [fig_name])
    dpasses = cur.fetchone()
    drev = cur.execute("SELECT SUM(rev) as drev from stats where opponent = %s", [fig_name])
    drev = cur.fetchone()


    dhsl = cur.execute("SELECT SUM(headl_) as dhsl from stats where opponent = %s", [fig_name])
    dhsl = cur.fetchone()
    dhsat = cur.execute("SELECT SUM(heada_) as dhsat from stats where opponent = %s", [fig_name])
    dhsat = cur.fetchone()
    dhsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as dhsacc from stats where opponent = %s", [fig_name])
    dhsacc = cur.fetchone()


    dbsl = cur.execute("SELECT SUM(bodyl_) as dbsl from stats where opponent = %s", [fig_name])
    dbsl = cur.fetchone()
    dbsat = cur.execute("SELECT SUM(bodya_) as dbsat from stats where opponent = %s", [fig_name])
    dbsat = cur.fetchone()
    dbsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as dbsacc from stats where opponent = %s", [fig_name])
    dbsacc = cur.fetchone()


    dlsl = cur.execute("SELECT SUM(legl_) as dlsl from stats where opponent = %s", [fig_name])
    dlsl = cur.fetchone()
    dlsat = cur.execute("SELECT SUM(lega_) as dlsat from stats where opponent = %s", [fig_name])
    dlsat = cur.fetchone()
    dlsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as dlsacc from stats where opponent = %s", [fig_name])
    dlsacc = cur.fetchone()


    ddsl = cur.execute("SELECT SUM(distl_) as ddsl from stats where opponent = %s", [fig_name])
    ddsl = cur.fetchone()
    ddsat = cur.execute("SELECT SUM(dista_) as ddsat from stats where opponent = %s", [fig_name])
    ddsat = cur.fetchone()
    ddsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as ddsacc from stats where opponent = %s", [fig_name])
    ddsacc = cur.fetchone()


    dcsl = cur.execute("SELECT SUM(clinchl_) as dcsl from stats where opponent = %s", [fig_name])
    dcsl = cur.fetchone()
    dcsat = cur.execute("SELECT SUM(clincha_) as dcsat from stats where opponent = %s", [fig_name])
    dcsat = cur.fetchone()
    dcsacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as dcsacc from stats where opponent = %s", [fig_name])
    dcsacc = cur.fetchone()


    dgsl = cur.execute("SELECT SUM(groundl_) as dgsl from stats where opponent = %s", [fig_name])
    dgsl = cur.fetchone()
    dgsat = cur.execute("SELECT SUM(grounda_) as dgsat from stats where opponent = %s", [fig_name])
    dgsat = cur.fetchone()
    dgsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as dgsacc from stats where opponent = %s", [fig_name])
    dgsacc = cur.fetchone()


    ranks = cur.execute("SELECT * FROM ranks where fig_name = %s", [fig_name])
    ranks = cur.fetchone()

    ssm = cur.execute("SELECT SUM(ssm_) as ssm from stats where fig_name = %s", [fig_name])
    ssm = cur.fetchone()

    tsm = cur.execute("SELECT SUM(tsm_) as tsm from stats where fig_name = %s", [fig_name])
    tsm = cur.fetchone()

    tdm = cur.execute("SELECT SUM(tdm_) as tdm from stats where fig_name = %s", [fig_name])
    tdm = cur.fetchone()

    hsm = cur.execute("SELECT SUM(headm_) as hsm from stats where fig_name = %s", [fig_name])
    hsm = cur.fetchone()

    bsm = cur.execute("SELECT SUM(bodym_) as bsm from stats where fig_name = %s", [fig_name])
    bsm = cur.fetchone()

    lsm = cur.execute("SELECT SUM(legm_) as lsm from stats where fig_name = %s", [fig_name])
    lsm = cur.fetchone()

    dsm = cur.execute("SELECT SUM(distm_) as dsm from stats where fig_name = %s", [fig_name])
    dsm = cur.fetchone()

    csm = cur.execute("SELECT SUM(clinchm_) as csm from stats where fig_name = %s", [fig_name])
    csm = cur.fetchone()
    
    gsm = cur.execute("SELECT SUM(groundm_) as gsm from stats where fig_name = %s", [fig_name])
    gsm = cur.fetchone()

    history = cur.execute("SELECT * FROM histories WHERE fig_name = %s ORDER BY date_ asc", [fig_name])
    history = cur.fetchall()

    result = cur.execute("SELECT result FROM histories WHERE fig_name = %s ORDER BY date_ asc", [fig_name])
    result = cur.fetchall()

    historywins = cur.execute("SELECT * FROM histories WHERE result = 'win' and fig_name = %s ORDER BY date_ asc", [fig_name])
    historywins = cur.fetchall()

    historylosses = cur.execute("SELECT * FROM histories as historylosses WHERE result = 'loss' and fig_name = %s ORDER BY date_ asc", [fig_name])
    historylosses = cur.fetchall()

    historydraw = cur.execute("SELECT * FROM histories as historydraw WHERE result = 'draw' and fig_name = %s ORDER BY date_ asc", [fig_name])
    historydraw = cur.fetchall()


    historync = cur.execute("SELECT * FROM histories as historync WHERE result = 'No Contest' and fig_name = %s ORDER BY date_ asc", [fig_name])
    historync = cur.fetchall()


    return render_template('chart.html', fig_name=fig_name, tfs=tfs, tw=tw, tl=tl, draws=draws, nc=nc, tkow=tkow,tsubw=tsubw,tdecw=tdecw,tkol=tkol,tsubl=tsubl,tdecl=tdecl, ssla=ssla, ssat=ssat, ssacc=ssacc, tsl=tsl, tsat=tsat, tsacc=tsacc, tdl=tdl, tdat=tdat, tdacc=tdacc, subs=subs, passes=passes, rev=rev, hsl=hsl, hsat=hsat, hsacc=hsacc, bsl=bsl, bsat=bsat, bsacc=bsacc, lsl=lsl, lsat=lsat, lsacc=lsacc, dsl=dsl, dsat=dsat, dsacc=dsacc, csl=csl, csat=csat, csacc=csacc, gsl=gsl, gsat=gsat, gsacc=gsacc, dkd=dkd, dssla=dssla, dssat=dssat, dssacc=dssacc, dtsl=dtsl, dtsat=dtsat, dtsacc=dtsacc, dtdl=dtdl, dtdat=dtdat, dtdacc=dtdacc, dsubs=dsubs, dpasses=dpasses, drev=drev, dhsl=dhsl, dhsat=dhsat, dhsacc=dhsacc, dbsl=dbsl, dbsat=dbsat, dbsacc=dbsacc, dlsl=dlsl, dlsat=dlsat, dlsacc=dlsacc, ddsl=ddsl, ddsat=ddsat, ddsacc=ddsacc, dcsl=dcsl, dcsat=dcsat, dcsacc=dcsacc, dgsl=dgsl, dgsat=dgsat, dgsacc=dgsacc, ranks=ranks, ssm=ssm, tsm=tsm, tdm=tdm, hsm=hsm, bsm=bsm, lsm=lsm, dsm=dsm, csm=csm, gsm=gsm, history=history, historywins=historywins, historylosses=historylosses, historydraw=historydraw, historync=historync, result=result)


#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        fighter = request.form['fighter']
        # search by author or book
        cur = mysql.connection.cursor()
        data = cur.execute("SELECT * from roster WHERE fig_name LIKE %s OR weightclass LIKE %s", ("%" + (fighter) + "%", fighter))
        mysql.connection.commit()
        data = cur.fetchall()
        # all in the search box will return all the tuples
        if len(data) == 0 and fighter == 'all':
            cur = mysql.connection.cursor()
            data = cur.execute("SELECT * from roster")
            mysql.connection.commit()
            data = cur.fetchall()
        return render_template('search.html', data=data)
    return render_template('search.html')


@app.route('/events')
def events():
    cur = mysql.connection.cursor()
    event = cur.execute("SELECT * FROM events where status = 'upcoming' ORDER BY date asc")
    event = cur.fetchall()
    p_event = cur.execute("SELECT * FROM events where attendance >0 ORDER BY date DESC")
    p_event = cur.fetchall()

    return render_template('events.html', event=event, p_event=p_event)


@app.route('/cards/<string:event_name>/')
def cards(event_name):
    cur = mysql.connection.cursor()
    cards = cur.execute("SELECT * FROM upcoming WHERE event_name = %s ORDER BY date DESC", [event_name])
    cards = cur.fetchall()

    p_cards = cur.execute("SELECT * FROM histories WHERE event = %s ORDER BY date DESC", [event_name])
    p_cards = cur.fetchall()

    eventcard = cur.execute("SELECT * FROM events WHERE event_name = %s", [event_name])
    eventcard = cur.fetchone()

    return render_template('cards.html', cards=cards, p_cards=p_cards, event_name=event_name, eventcard=eventcard)


@app.route('/versus/<string:fig_name>/<string:opponent>/')
def versus(fig_name, opponent):

    cur = mysql.connection.cursor()
    
    bio = cur.execute("SELECT * FROM roster WHERE fig_name = %s", [fig_name])
    bio = cur.fetchone()

    history = cur.execute("SELECT * FROM histories WHERE fig_name = %s ORDER BY date asc", [fig_name])
    history = cur.fetchall()

    stats_o = cur.execute("SELECT * FROM stats WHERE fig_name = %s ORDER BY date DESC", [fig_name])
    stats_o = cur.fetchall()

    stats_d = cur.execute("SELECT * FROM stats WHERE opponent = %s ORDER BY date DESC", [fig_name])
    stats_d = cur.fetchall()

    tfs = cur.execute("SELECT COUNT(fig_name) as tfs from histories where fig_name = %s", [fig_name])
    tfs = cur.fetchone()

    tw = cur.execute("SELECT COUNT(fig_name) as tw from histories where result = 'win' and fig_name = %s", [fig_name])
    tw = cur.fetchone()

    tl = cur.execute("SELECT COUNT(fig_name) as tl from histories where result = 'loss' and fig_name = %s", [fig_name])
    tl = cur.fetchone()

    tkow = cur.execute("SELECT COUNT(fig_name) as tkow FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkow = cur.fetchone()

    tsubw = cur.execute("SELECT COUNT(fig_name) as tsubw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubw = cur.fetchone()

    tdecw = cur.execute("SELECT COUNT(fig_name) as tdecw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecw = cur.fetchone()

    tkol = cur.execute("SELECT COUNT(fig_name) as tkol FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkol = cur.fetchone()

    tsubl = cur.execute("SELECT COUNT(fig_name) as tsubl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubl = cur.fetchone()

    tdecl = cur.execute("SELECT COUNT(fig_name) as tdecl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecl = cur.fetchone()

    draws = cur.execute("SELECT COUNT(fig_name) as draws from histories where result = 'draw' and fig_name = %s", [fig_name])
    draws = cur.fetchone()

    nc = cur.execute("SELECT COUNT(fig_name) as nc from histories where result = 'NC' and fig_name = %s", [fig_name])
    nc = cur.fetchone()

    frf = cur.execute("SELECT COUNT(fig_name) as frf from histories where result = 'win' and round_ = '1' and fig_name = %s", [fig_name])
    frf = cur.fetchone()

    potn = cur.execute("SELECT COUNT(fig_name) as potn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Performance of the Night' + "%", [fig_name]))
    potn = cur.fetchone()

    fotn = cur.execute("SELECT COUNT(fig_name) as fotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Fight of the Night' + "%", [fig_name]))
    fotn = cur.fetchone()

    kootn = cur.execute("SELECT COUNT(fig_name) as kootn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Knockout of the Night' + "%", [fig_name]))
    kootn = cur.fetchone()

    sotn = cur.execute("SELECT COUNT(fig_name) as sotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Submission of the Night' + "%", [fig_name]))
    sotn = cur.fetchone()

    bonuses = cur.execute("SELECT COUNT(fig_name) as bonuses FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'f the Night' + "%", [fig_name]))
    bonuses = cur.fetchone()

    tft = cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(total_fight_time))) as tft FROM histories WHERE fig_name = %s", [fig_name])
    tft = cur.fetchone()

    scalc = cur.execute("SELECT fig_name from histories WHERE fig_name = %s", [fig_name])
    scalc = cur.fetchone()

    kd = cur.execute("SELECT SUM(kd) as kd from stats where fig_name = %s", [fig_name])
    kd = cur.fetchone()


    ssla = cur.execute("SELECT SUM(ssl_) as ssla from stats where fig_name = %s", [fig_name])
    ssla = cur.fetchone()
    ssat = cur.execute("SELECT SUM(ssa_) as ssat from stats where fig_name = %s", [fig_name])
    ssat = cur.fetchone()
    ssacc = cur.execute("SELECT IFNULL(IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0),0.0) as ssacc from stats where fig_name = %s", [fig_name])
    ssacc = cur.fetchone()


    tsl = cur.execute("SELECT SUM(tsl_) as tsl from stats where fig_name = %s", [fig_name])
    tsl = cur.fetchone()
    tsat = cur.execute("SELECT SUM(tsa_) as tsat from stats where fig_name = %s", [fig_name])
    tsat = cur.fetchone()
    tsacc = cur.execute("SELECT IFNULL(IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0),0.0) as tsacc from stats where fig_name = %s", [fig_name])
    tsacc = cur.fetchone()


    tdl = cur.execute("SELECT SUM(tdl_) as tdl from stats where fig_name = %s", [fig_name])
    tdl = cur.fetchone()
    tdat = cur.execute("SELECT SUM(tda_) as tdat from stats where fig_name = %s", [fig_name])
    tdat = cur.fetchone()
    tdacc = cur.execute("SELECT IFNULL(IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0),0.0) as tdacc from stats where fig_name = %s", [fig_name])
    tdacc = cur.fetchone()


    subs = cur.execute("SELECT SUM(sub_) as subs from stats where fig_name = %s", [fig_name])
    subs = cur.fetchone()
    passes = cur.execute("SELECT SUM(pass_) as passes from stats where fig_name = %s", [fig_name])
    passes = cur.fetchone()
    rev = cur.execute("SELECT SUM(rev) as rev from stats where fig_name = %s", [fig_name])
    rev = cur.fetchone()


    hsl = cur.execute("SELECT SUM(headl_) as hsl from stats where fig_name = %s", [fig_name])
    hsl = cur.fetchone()
    hsat = cur.execute("SELECT SUM(heada_) as hsat from stats where fig_name = %s", [fig_name])
    hsat = cur.fetchone()
    hsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as hsacc from stats where fig_name = %s", [fig_name])
    hsacc = cur.fetchone()


    bsl = cur.execute("SELECT SUM(bodyl_) as bsl from stats where fig_name = %s", [fig_name])
    bsl = cur.fetchone()
    bsat = cur.execute("SELECT SUM(bodya_) as bsat from stats where fig_name = %s", [fig_name])
    bsat = cur.fetchone()
    bsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as bsacc from stats where fig_name = %s", [fig_name])
    bsacc = cur.fetchone()


    lsl = cur.execute("SELECT SUM(legl_) as lsl from stats where fig_name = %s", [fig_name])
    lsl = cur.fetchone()
    lsat = cur.execute("SELECT SUM(lega_) as lsat from stats where fig_name = %s", [fig_name])
    lsat = cur.fetchone()
    lsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as lsacc from stats where fig_name = %s", [fig_name])
    lsacc = cur.fetchone()


    dsl = cur.execute("SELECT SUM(distl_) as dsl from stats where fig_name = %s", [fig_name])
    dsl = cur.fetchone()
    dsat = cur.execute("SELECT SUM(dista_) as dsat from stats where fig_name = %s", [fig_name])
    dsat = cur.fetchone()
    dsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as dsacc from stats where fig_name = %s", [fig_name])
    dsacc = cur.fetchone()


    csl = cur.execute("SELECT SUM(clinchl_) as csl from stats where fig_name = %s", [fig_name])
    csl = cur.fetchone()
    csat = cur.execute("SELECT SUM(clincha_) as csat from stats where fig_name = %s", [fig_name])
    csat = cur.fetchone()
    csacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as csacc from stats where fig_name = %s", [fig_name])
    csacc = cur.fetchone()


    gsl = cur.execute("SELECT SUM(groundl_) as gsl from stats where fig_name = %s", [fig_name])
    gsl = cur.fetchone()
    gsat = cur.execute("SELECT SUM(grounda_) as gsat from stats where fig_name = %s", [fig_name])
    gsat = cur.fetchone()
    gsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as gsacc from stats where fig_name = %s", [fig_name])
    gsacc = cur.fetchone()


#DEFENSE---------------------------------------
    dkd = cur.execute("SELECT SUM(kd) as dkd from stats where opponent = %s", [fig_name])
    dkd = cur.fetchone()
    dsubs = cur.execute("SELECT SUM(sub_) as dsubs from stats where opponent = %s", [fig_name])
    dsubs = cur.fetchone()
    dpasses = cur.execute("SELECT SUM(pass_) as dpasses from stats where opponent = %s", [fig_name])
    dpasses = cur.fetchone()
    drev = cur.execute("SELECT SUM(rev) as drev from stats where opponent = %s", [fig_name])
    drev = cur.fetchone()

    dtsl = cur.execute("SELECT SUM(tsl_) as dtsl from stats where opponent = %s", [fig_name])
    dtsl = cur.fetchone()
    dtsat = cur.execute("SELECT SUM(tsa_) as dtsat from stats where opponent = %s", [fig_name])
    dtsat = cur.fetchone()
    dtsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0)-100) as dtsacc from stats where opponent = %s", [fig_name])
    dtsacc = cur.fetchone()

    dssla = cur.execute("SELECT SUM(ssl_) as dssla from stats where opponent = %s", [fig_name])
    dssla = cur.fetchone()
    dssat = cur.execute("SELECT SUM(ssa_) as dssat from stats where opponent = %s", [fig_name])
    dssat = cur.fetchone()
    dssacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0)-100) as dssacc from stats where opponent = %s", [fig_name])
    dssacc = cur.fetchone()

    dhsl = cur.execute("SELECT SUM(headl_) as dhsl from stats where opponent = %s", [fig_name])
    dhsl = cur.fetchone()
    dhsat = cur.execute("SELECT SUM(heada_) as dhsat from stats where opponent = %s", [fig_name])
    dhsat = cur.fetchone()
    dhsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0)-100) as dhsacc from stats where opponent = %s", [fig_name])
    dhsacc = cur.fetchone()


    dbsl = cur.execute("SELECT SUM(bodyl_) as dbsl from stats where opponent = %s", [fig_name])
    dbsl = cur.fetchone()
    dbsat = cur.execute("SELECT SUM(bodya_) as dbsat from stats where opponent = %s", [fig_name])
    dbsat = cur.fetchone()
    dbsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0)-100) as dbsacc from stats where opponent = %s", [fig_name])
    dbsacc = cur.fetchone()


    dlsl = cur.execute("SELECT SUM(legl_) as dlsl from stats where opponent = %s", [fig_name])
    dlsl = cur.fetchone()
    dlsat = cur.execute("SELECT SUM(lega_) as dlsat from stats where opponent = %s", [fig_name])
    dlsat = cur.fetchone()
    dlsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0)-100) as dlsacc from stats where opponent = %s", [fig_name])
    dlsacc = cur.fetchone()


    ddsl = cur.execute("SELECT SUM(distl_) as ddsl from stats where opponent = %s", [fig_name])
    ddsl = cur.fetchone()
    ddsat = cur.execute("SELECT SUM(dista_) as ddsat from stats where opponent = %s", [fig_name])
    ddsat = cur.fetchone()
    ddsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0)-100) as ddsacc from stats where opponent = %s", [fig_name])
    ddsacc = cur.fetchone()


    dcsl = cur.execute("SELECT SUM(clinchl_) as dcsl from stats where opponent = %s", [fig_name])
    dcsl = cur.fetchone()
    dcsat = cur.execute("SELECT SUM(clincha_) as dcsat from stats where opponent = %s", [fig_name])
    dcsat = cur.fetchone()
    dcsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0)-100) as dcsacc from stats where opponent = %s", [fig_name])
    dcsacc = cur.fetchone()


    dgsl = cur.execute("SELECT SUM(groundl_) as dgsl from stats where opponent = %s", [fig_name])
    dgsl = cur.fetchone()
    dgsat = cur.execute("SELECT SUM(grounda_) as dgsat from stats where opponent = %s", [fig_name])
    dgsat = cur.fetchone()
    dgsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0)-100) as dgsacc from stats where opponent = %s", [fig_name])
    dgsacc = cur.fetchone()

    dtdl = cur.execute("SELECT SUM(tdl_) as dtdl from stats where opponent = %s", [fig_name])
    dtdl = cur.fetchone()
    dtdat = cur.execute("SELECT SUM(tda_) as dtdat from stats where opponent = %s", [fig_name])
    dtdat = cur.fetchone()
    dtdacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0)-100) as dtdacc from stats where opponent = %s", [fig_name])
    dtdacc = cur.fetchone()



    ranks = cur.execute("SELECT * FROM ranks as ranks where fig_name = %s", [fig_name])
    ranks = cur.fetchone()

    opp_bio = cur.execute("SELECT * FROM roster WHERE fig_name = %s", [opponent])
    opp_bio = cur.fetchone()

    opp_history = cur.execute("SELECT * FROM histories WHERE fig_name = %s ORDER BY date ASC", [opponent])
    opp_history = cur.fetchall()

    opp_stats_o = cur.execute("SELECT * FROM stats WHERE fig_name = %s ORDER BY date DESC", [opponent])
    opp_stats_o = cur.fetchall()

    opp_stats_d = cur.execute("SELECT * FROM stats WHERE opponent = %s ORDER BY date DESC", [opponent])
    opp_stats_d = cur.fetchall()

    opp_tfs = cur.execute("SELECT COUNT(fig_name) as opp_tfs from histories where fig_name = %s", [opponent])
    opp_tfs = cur.fetchone()

    opp_tw = cur.execute("SELECT COUNT(fig_name) as opp_tw from histories where result = 'win' and fig_name = %s", [opponent])
    opp_tw = cur.fetchone()

    opp_tl = cur.execute("SELECT COUNT(fig_name) as opp_tl from histories where result = 'loss' and fig_name = %s", [opponent])
    opp_tl = cur.fetchone()

    opp_tkow = cur.execute("SELECT COUNT(fig_name) as opp_tkow FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [opponent]))
    opp_tkow = cur.fetchone()

    opp_tsubw = cur.execute("SELECT COUNT(fig_name) as opp_tsubw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [opponent]))
    opp_tsubw = cur.fetchone()

    opp_tdecw = cur.execute("SELECT COUNT(fig_name) as opp_tdecw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [opponent]))
    opp_tdecw = cur.fetchone()

    opp_tkol = cur.execute("SELECT COUNT(fig_name) as opp_tkol FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [opponent]))
    opp_tkol = cur.fetchone()

    opp_tsubl = cur.execute("SELECT COUNT(fig_name) as opp_tsubl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [opponent]))
    opp_tsubl = cur.fetchone()

    opp_tdecl = cur.execute("SELECT COUNT(fig_name) as opp_tdecl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [opponent]))
    opp_tdecl = cur.fetchone()

    opp_draws = cur.execute("SELECT COUNT(fig_name) as opp_draws from histories where result = 'draw' and fig_name = %s", [opponent])
    opp_draws = cur.fetchone()

    opp_nc = cur.execute("SELECT COUNT(fig_name) as opp_nc from histories where result = 'NC' and fig_name = %s", [opponent])
    opp_nc = cur.fetchone()

    opp_frf = cur.execute("SELECT COUNT(fig_name) as opp_frf from histories where result = 'win' and round_ = '1' and fig_name = %s", [opponent])
    opp_frf = cur.fetchone()

    opp_potn = cur.execute("SELECT COUNT(fig_name) as opp_potn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Performance of the Night' + "%", [opponent]))
    opp_potn = cur.fetchone()

    opp_fotn = cur.execute("SELECT COUNT(fig_name) as opp_fotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Fight of the Night' + "%", [opponent]))
    opp_fotn = cur.fetchone()

    opp_kootn = cur.execute("SELECT COUNT(fig_name) as opp_kootn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Knockout of the Night' + "%", [opponent]))
    opp_kootn = cur.fetchone()

    opp_sotn = cur.execute("SELECT COUNT(fig_name) as opp_sotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Submission of the Night' + "%", [opponent]))
    opp_sotn = cur.fetchone()

    opp_bonuses = cur.execute("SELECT COUNT(fig_name) as opp_bonuses FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'f the Night' + "%", [opponent]))
    opp_bonuses = cur.fetchone()

    opp_tft = cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(total_fight_time))) as opp_tft FROM histories WHERE fig_name = %s", [opponent])
    opp_tft = cur.fetchone()

    opp_scalc = cur.execute("SELECT fig_name from histories WHERE fig_name = %s", [opponent])
    opp_scalc = cur.fetchone()

    opp_kd = cur.execute("SELECT SUM(kd) as opp_kd from stats where fig_name = %s", [opponent])
    opp_kd = cur.fetchone()


    opp_ssla = cur.execute("SELECT SUM(ssl_) as opp_ssla from stats where fig_name = %s", [opponent])
    opp_ssla = cur.fetchone()

    opp_ssat = cur.execute("SELECT SUM(ssa_) as opp_ssat from stats where fig_name = %s", [opponent])
    opp_ssat = cur.fetchone()
    opp_ssacc = cur.execute("SELECT IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0) as opp_ssacc from stats where fig_name = %s", [opponent])
    opp_ssacc = cur.fetchone()


    opp_tsl = cur.execute("SELECT SUM(tsl_) as opp_tsl from stats where fig_name = %s", [opponent])
    opp_tsl = cur.fetchone()
    opp_tsat = cur.execute("SELECT SUM(tsa_) as opp_tsat from stats where fig_name = %s", [opponent])
    opp_tsat = cur.fetchone()
    opp_tsacc = cur.execute("SELECT IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0) as opp_tsacc from stats where fig_name = %s", [opponent])
    opp_tsacc = cur.fetchone()


    opp_tdl = cur.execute("SELECT SUM(tdl_) as opp_tdl from stats where fig_name = %s", [opponent])
    opp_tdl = cur.fetchone()
    opp_tdat = cur.execute("SELECT SUM(tda_) as opp_tdat from stats where fig_name = %s", [opponent])
    opp_tdat = cur.fetchone()
    opp_tdacc = cur.execute("SELECT IFNULL(IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0),0.0) as opp_tdacc from stats where fig_name = %s", [opponent])
    opp_tdacc = cur.fetchone()


    opp_subs = cur.execute("SELECT SUM(sub_) as opp_subs from stats where fig_name = %s", [opponent])
    opp_subs = cur.fetchone()
    opp_passes = cur.execute("SELECT SUM(pass_) as opp_passes from stats where fig_name = %s", [opponent])
    opp_passes = cur.fetchone()
    opp_rev = cur.execute("SELECT SUM(rev) as opp_rev from stats where fig_name = %s", [opponent])
    opp_rev = cur.fetchone()


    opp_hsl = cur.execute("SELECT SUM(headl_) as opp_hsl from stats where fig_name = %s", [opponent])
    opp_hsl = cur.fetchone()
    opp_hsat = cur.execute("SELECT SUM(heada_) as opp_hsat from stats where fig_name = %s", [opponent])
    opp_hsat = cur.fetchone()
    opp_hsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as opp_hsacc from stats where fig_name = %s", [opponent])
    opp_hsacc = cur.fetchone()


    opp_bsl = cur.execute("SELECT SUM(bodyl_) as opp_bsl from stats where fig_name = %s", [opponent])
    opp_bsl = cur.fetchone()
    opp_bsat = cur.execute("SELECT SUM(bodya_) as opp_bsat from stats where fig_name = %s", [opponent])
    opp_bsat = cur.fetchone()
    opp_bsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as opp_bsacc from stats where fig_name = %s", [opponent])
    opp_bsacc = cur.fetchone()


    opp_lsl = cur.execute("SELECT SUM(legl_) as opp_lsl from stats where fig_name = %s", [opponent])
    opp_lsl = cur.fetchone()
    opp_lsat = cur.execute("SELECT SUM(lega_) as opp_lsat from stats where fig_name = %s", [opponent])
    opp_lsat = cur.fetchone()
    opp_lsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as opp_lsacc from stats where fig_name = %s", [opponent])
    opp_lsacc = cur.fetchone()


    opp_dsl = cur.execute("SELECT SUM(distl_) as opp_dsl from stats where fig_name = %s", [opponent])
    opp_dsl = cur.fetchone()
    opp_dsat = cur.execute("SELECT SUM(dista_) as opp_dsat from stats where fig_name = %s", [opponent])
    opp_dsat = cur.fetchone()
    opp_dsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as opp_dsacc from stats where fig_name = %s", [opponent])
    opp_dsacc = cur.fetchone()


    opp_csl = cur.execute("SELECT SUM(clinchl_) as opp_csl from stats where fig_name = %s", [opponent])
    opp_csl = cur.fetchone()
    opp_csat = cur.execute("SELECT SUM(clincha_) as opp_csat from stats where fig_name = %s", [opponent])
    opp_csat = cur.fetchone()
    opp_csacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as opp_csacc from stats where fig_name = %s", [opponent])
    opp_csacc = cur.fetchone()


    opp_gsl = cur.execute("SELECT SUM(groundl_) as opp_gsl from stats where fig_name = %s", [opponent])
    opp_gsl = cur.fetchone()
    opp_gsat = cur.execute("SELECT SUM(grounda_) as opp_gsat from stats where fig_name = %s", [opponent])
    opp_gsat = cur.fetchone()
    opp_gsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as opp_gsacc from stats where fig_name = %s", [opponent])
    opp_gsacc = cur.fetchone()


#OPPONENT DEFENSE--------------------------------------------
    opp_dkd = cur.execute("SELECT SUM(kd) as opp_dkd from stats where opponent = %s", [opponent])
    opp_dkd = cur.fetchone()
    opp_dsubs = cur.execute("SELECT SUM(sub_) as opp_dsubs from stats where opponent = %s", [opponent])
    opp_dsubs = cur.fetchone()
    opp_dpasses = cur.execute("SELECT SUM(pass_) as opp_dpasses from stats where opponent = %s", [opponent])
    opp_dpasses = cur.fetchone()
    opp_drev = cur.execute("SELECT SUM(rev) as opp_drev from stats where opponent = %s", [opponent])
    opp_drev = cur.fetchone()


    opp_dtsl = cur.execute("SELECT SUM(tsl_) as opp_dtsl from stats where opponent = %s", [opponent])
    opp_dtsl = cur.fetchone()
    opp_dtsat = cur.execute("SELECT SUM(tsa_) as opp_dtsat from stats where opponent = %s", [opponent])
    opp_dtsat = cur.fetchone()
    opp_dtsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0)-100) as opp_dtsacc from stats where opponent = %s", [opponent])
    opp_dtsacc = cur.fetchone()


    opp_dssla = cur.execute("SELECT SUM(ssl_) as opp_dssla from stats where opponent = %s", [opponent])
    opp_dssla = cur.fetchone()
    opp_dssat = cur.execute("SELECT SUM(ssa_) as opp_dssat from stats where opponent = %s", [opponent])
    opp_dssat = cur.fetchone()
    opp_dssacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0)-100) as opp_dssacc from stats where opponent = %s", [opponent])
    opp_dssacc = cur.fetchone()


    opp_dhsl = cur.execute("SELECT SUM(headl_) as opp_dhsl from stats where opponent = %s", [opponent])
    opp_dhsl = cur.fetchone()
    opp_dhsat = cur.execute("SELECT SUM(heada_) as opp_dhsat from stats where opponent = %s", [opponent])
    opp_dhsat = cur.fetchone()
    opp_dhsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0)-100) as opp_dhsacc from stats where opponent = %s", [opponent])
    opp_dhsacc = cur.fetchone()


    opp_dbsl = cur.execute("SELECT SUM(bodyl_) as opp_dbsl from stats where opponent = %s", [opponent])
    opp_dbsl = cur.fetchone()
    opp_dbsat = cur.execute("SELECT SUM(bodya_) as opp_dbsat from stats where opponent = %s", [opponent])
    opp_dbsat = cur.fetchone()
    opp_dbsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0)-100) as opp_dbsacc from stats where opponent = %s", [opponent])
    opp_dbsacc = cur.fetchone()


    opp_dlsl = cur.execute("SELECT SUM(legl_) as opp_dlsl from stats where opponent = %s", [opponent])
    opp_dlsl = cur.fetchone()
    opp_dlsat = cur.execute("SELECT SUM(lega_) as opp_dlsat from stats where opponent = %s", [opponent])
    opp_dlsat = cur.fetchone()
    opp_dlsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0)-100) as opp_dlsacc from stats where opponent = %s", [opponent])
    opp_dlsacc = cur.fetchone()


    opp_ddsl = cur.execute("SELECT SUM(distl_) as opp_ddsl from stats where opponent = %s", [opponent])
    opp_ddsl = cur.fetchone()
    opp_ddsat = cur.execute("SELECT SUM(dista_) as opp_ddsat from stats where opponent = %s", [opponent])
    opp_ddsat = cur.fetchone()
    opp_ddsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0)-100) as opp_ddsacc from stats where opponent = %s", [opponent])
    opp_ddsacc = cur.fetchone()


    opp_dcsl = cur.execute("SELECT SUM(clinchl_) as opp_dcsl from stats where opponent = %s", [opponent])
    opp_dcsl = cur.fetchone()
    opp_dcsat = cur.execute("SELECT SUM(clincha_) as opp_dcsat from stats where opponent = %s", [opponent])
    opp_dcsat = cur.fetchone()
    opp_dcsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0)-100) as opp_dcsacc from stats where opponent = %s", [opponent])
    opp_dcsacc = cur.fetchone()


    opp_dgsl = cur.execute("SELECT SUM(groundl_) as opp_dgsl from stats where opponent = %s", [opponent])
    opp_dgsl = cur.fetchone()
    opp_dgsat = cur.execute("SELECT SUM(grounda_) as opp_dgsat from stats where opponent = %s", [opponent])
    opp_dgsat = cur.fetchone()
    opp_dgsacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0)-100) as opp_dgsacc from stats where opponent = %s", [opponent])
    opp_dgsacc = cur.fetchone()


    opp_dtdl = cur.execute("SELECT SUM(tdl_) as opp_dtdl from stats where opponent = %s", [opponent])
    opp_dtdl = cur.fetchone()
    opp_dtdat = cur.execute("SELECT SUM(tda_) as opp_dtdat from stats where opponent = %s", [opponent])
    opp_dtdat = cur.fetchone()
    opp_dtdacc = cur.execute("SELECT ABS(IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0)-100) as opp_dtdacc from stats where opponent = %s", [opponent])
    opp_dtdacc = cur.fetchone()


    opp_ranks = cur.execute("SELECT * FROM ranks where fig_name = %s", [opponent])
    opp_ranks = cur.fetchone()

    odds = cur.execute("SELECT odds from upcoming where fig_name = %s", [fig_name])
    odds = cur.fetchone()

    opp_odds = cur.execute("SELECT opp_odds from upcoming where opponent = %s", [opponent])
    opp_odds = cur.fetchone()

    opp_avgtft = cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(total_fight_time))) as opp_avgtft FROM histories WHERE fig_name = %s", [fig_name])
    opp_avgtft = cur.fetchone()

    avgtft = cur.execute("SELECT SUBSTRING(SEC_TO_TIME((SUM(TIME_TO_SEC(total_fight_time)))/COUNT(fig_name)),2,7) as avgtft from histories where fig_name = %s", [fig_name])
    avgtft = cur.fetchone()

    opp_avgtft = cur.execute("SELECT SUBSTRING(SEC_TO_TIME((SUM(TIME_TO_SEC(total_fight_time)))/COUNT(fig_name)),2,7) as opp_avgtft from histories where fig_name = %s", [opponent])
    opp_avgtft = cur.fetchone()

    ssm = cur.execute("SELECT SUM(ssm_) as ssm from stats where fig_name = %s", [fig_name])
    ssm = cur.fetchone()

    tsm = cur.execute("SELECT SUM(tsm_) as tsm from stats where fig_name = %s", [fig_name])
    tsm = cur.fetchone()

    tdm = cur.execute("SELECT SUM(tdm_) as tdm from stats where fig_name = %s", [fig_name])
    tdm = cur.fetchone()

    hsm = cur.execute("SELECT SUM(headm_) as hsm from stats where fig_name = %s", [fig_name])
    hsm = cur.fetchone()

    bsm = cur.execute("SELECT SUM(bodym_) as bsm from stats where fig_name = %s", [fig_name])
    bsm = cur.fetchone()

    lsm = cur.execute("SELECT SUM(legm_) as lsm from stats where fig_name = %s", [fig_name])
    lsm = cur.fetchone()

    dsm = cur.execute("SELECT SUM(distm_) as dsm from stats where fig_name = %s", [fig_name])
    dsm = cur.fetchone()

    csm = cur.execute("SELECT SUM(clinchm_) as csm from stats where fig_name = %s", [fig_name])
    csm = cur.fetchone()
    
    gsm = cur.execute("SELECT SUM(groundm_) as gsm from stats where fig_name = %s", [fig_name])
    gsm = cur.fetchone()

    opp_ssm = cur.execute("SELECT SUM(ssm_) as opp_ssm from stats where fig_name = %s", [opponent])
    opp_ssm = cur.fetchone()

    opp_tsm = cur.execute("SELECT SUM(tsm_) as opp_tsm from stats where fig_name = %s", [opponent])
    opp_tsm = cur.fetchone()

    opp_tdm = cur.execute("SELECT SUM(tdm_) as opp_tdm from stats where fig_name = %s", [opponent])
    opp_tdm = cur.fetchone()

    opp_hsm = cur.execute("SELECT SUM(headm_) as opp_hsm from stats where fig_name = %s", [opponent])
    opp_hsm = cur.fetchone()

    opp_bsm = cur.execute("SELECT SUM(bodym_) as opp_bsm from stats where fig_name = %s", [opponent])
    opp_bsm = cur.fetchone()

    opp_lsm = cur.execute("SELECT SUM(legm_) as opp_lsm from stats where fig_name = %s", [opponent])
    opp_lsm = cur.fetchone()

    opp_dsm = cur.execute("SELECT SUM(distm_) as opp_dsm from stats where fig_name = %s", [opponent])
    opp_dsm = cur.fetchone()

    opp_csm = cur.execute("SELECT SUM(clinchm_) as opp_csm from stats where fig_name = %s", [opponent])
    opp_csm = cur.fetchone()

    opp_gsm = cur.execute("SELECT SUM(groundm_) as opp_gsm from stats where fig_name = %s", [opponent])
    opp_gsm = cur.fetchone()

    dssm = cur.execute("SELECT SUM(ssm_) as dssm from stats where opponent = %s", [fig_name])
    dssm = cur.fetchone()

    dtsm = cur.execute("SELECT SUM(tsm_) as dtsm from stats where opponent = %s", [fig_name])
    dtsm = cur.fetchone()

    dtdm = cur.execute("SELECT SUM(tdm_) as dtdm from stats where opponent = %s", [fig_name])
    dtdm = cur.fetchone()

    dhsm = cur.execute("SELECT SUM(headm_) as dhsm from stats where opponent = %s", [fig_name])
    dhsm = cur.fetchone()

    dbsm = cur.execute("SELECT SUM(bodym_) as dbsm from stats where opponent = %s", [fig_name])
    dbsm = cur.fetchone()

    dlsm = cur.execute("SELECT SUM(legm_) as dlsm from stats where opponent = %s", [fig_name])
    dlsm = cur.fetchone()

    ddsm = cur.execute("SELECT SUM(distm_) as ddsm from stats where opponent = %s", [fig_name])
    ddsm = cur.fetchone()

    dcsm = cur.execute("SELECT SUM(clinchm_) as dcsm from stats where opponent = %s", [fig_name])
    dcsm = cur.fetchone()

    dgsm = cur.execute("SELECT SUM(groundm_) as dgsm from stats where opponent = %s", [fig_name])
    dgsm = cur.fetchone()

    opp_dssm = cur.execute("SELECT SUM(ssm_) as opp_dssm from stats where opponent = %s", [opponent])
    opp_dssm = cur.fetchone()

    opp_dtsm = cur.execute("SELECT SUM(tsm_) as opp_dtsm from stats where opponent = %s", [opponent])
    opp_dtsm = cur.fetchone()

    opp_dtdm = cur.execute("SELECT SUM(tdm_) as opp_dtdm from stats where opponent = %s", [opponent])
    opp_dtdm = cur.fetchone()

    opp_dhsm = cur.execute("SELECT SUM(headm_) as opp_dhsm from stats where opponent = %s", [opponent])
    opp_dhsm = cur.fetchone()

    opp_dbsm = cur.execute("SELECT SUM(bodym_) as opp_dbsm from stats where opponent = %s", [opponent])
    opp_dbsm = cur.fetchone()

    opp_dlsm = cur.execute("SELECT SUM(legm_) as opp_dlsm from stats where opponent = %s", [opponent])
    opp_dlsm = cur.fetchone()

    opp_ddsm = cur.execute("SELECT SUM(distm_) as opp_ddsm from stats where opponent = %s", [opponent])
    opp_ddsm = cur.fetchone()

    opp_dcsm = cur.execute("SELECT SUM(clinchm_) as opp_dcsm from stats where opponent = %s", [opponent])
    opp_dcsm = cur.fetchone()

    opp_dgsm = cur.execute("SELECT SUM(groundm_) as opp_dgsm from stats where opponent = %s", [opponent])
    opp_dgsm = cur.fetchone()

    historywins = cur.execute("SELECT * FROM histories WHERE result = 'win' and fig_name = %s ORDER BY date asc", [fig_name])
    historywins = cur.fetchall()

    historylosses = cur.execute("SELECT * FROM histories as historylosses WHERE result = 'loss' and fig_name = %s ORDER BY date asc", [fig_name])
    historylosses = cur.fetchall()

    opp_historywins = cur.execute("SELECT * FROM histories WHERE result = 'win' and fig_name = %s ORDER BY date asc", [opponent])
    opp_historywins = cur.fetchall()

    opp_historylosses = cur.execute("SELECT * FROM histories as opp_historylosses WHERE result = 'loss' and fig_name = %s ORDER BY date asc", [opponent])
    opp_historylosses = cur.fetchall()



    return render_template('versus.html', bio=bio, history=history, stats_o=stats_o, stats_d=stats_d, tfs=tfs, tw=tw, tl=tl, tkow=tkow, tsubw=tsubw, tdecw=tdecw, tkol=tkol, tsubl=tsubl, tdecl=tdecl, draws=draws, nc=nc, frf=frf, potn=potn, fotn=fotn, kootn=kootn, sotn=sotn, bonuses=bonuses, tft=tft, kd=kd, ssla=ssla, ssat=ssat, ssacc=ssacc, tsl=tsl, tsat=tsat, tsacc=tsacc, tdl=tdl, tdat=tdat, tdacc=tdacc, subs=subs, passes=passes, rev=rev, hsl=hsl, hsat=hsat, hsacc=hsacc, bsl=bsl, bsat=bsat, bsacc=bsacc, lsl=lsl, lsat=lsat, lsacc=lsacc, dsl=dsl, dsat=dsat, dsacc=dsacc, csl=csl, csat=csat, csacc=csacc, gsl=gsl, gsat=gsat, gsacc=gsacc, dkd=dkd, dssla=dssla, dssat=dssat, dssacc=dssacc, dtsl=dtsl, dtsat=dtsat, dtsacc=dtsacc, dtdl=dtdl, dtdat=dtdat, dtdacc=dtdacc, dsubs=dsubs, dpasses=dpasses, drev=drev, dhsl=dhsl, dhsat=dhsat, dhsacc=dhsacc, dbsl=dbsl, dbsat=dbsat, dbsacc=dbsacc, dlsl=dlsl, dlsat=dlsat, dlsacc=dlsacc, ddsl=ddsl, ddsat=ddsat, ddsacc=ddsacc, dcsl=dcsl, dcsat=dcsat, dcsacc=dcsacc, dgsl=dgsl, dgsat=dgsat, dgsacc=dgsacc, ranks=ranks, opp_bio=opp_bio, opp_history=opp_history, opp_stats_o=opp_stats_o, opp_stats_d=opp_stats_d, opp_tfs=opp_tfs, opp_tw=opp_tw, opp_tl=opp_tl, opp_tkow=opp_tkow, opp_tsubw=opp_tsubw, opp_tdecw=opp_tdecw, opp_tkol=opp_tkol, opp_tsubl=opp_tsubl, opp_tdecl=opp_tdecl, opp_draws=opp_draws, opp_nc=opp_nc, opp_frf=opp_frf, opp_potn=opp_potn, opp_fotn=opp_fotn, opp_kootn=opp_kootn, opp_sotn=opp_sotn, opp_bonuses=opp_bonuses, opp_tft=opp_tft, opp_kd=opp_kd, opp_ssla=opp_ssla, opp_ssat=opp_ssat, opp_ssacc=opp_ssacc, opp_tsl=opp_tsl, opp_tsat=opp_tsat, opp_tsacc=opp_tsacc, opp_tdl=opp_tdl, opp_tdat=opp_tdat, opp_tdacc=opp_tdacc, opp_subs=opp_subs, opp_passes=opp_passes, opp_rev=opp_rev, opp_hsl=opp_hsl, opp_hsat=opp_hsat, opp_hsacc=opp_hsacc, opp_bsl=opp_bsl, opp_bsat=opp_bsat, opp_bsacc=opp_bsacc, opp_lsl=opp_lsl, opp_lsat=opp_lsat, opp_lsacc=opp_lsacc, opp_dsl=opp_dsl, opp_dsat=opp_dsat, opp_dsacc=opp_dsacc, opp_csl=opp_csl, opp_csat=opp_csat, opp_csacc=opp_csacc, opp_gsl=opp_gsl, opp_gsat=opp_gsat, opp_gsacc=opp_gsacc, opp_dkd=opp_dkd, opp_dssla=opp_dssla, opp_dssat=opp_dssat, opp_dssacc=opp_dssacc, opp_dtsl=opp_dtsl, opp_dtsat=opp_dtsat, opp_dtsacc=opp_dtsacc, opp_dtdl=opp_dtdl, opp_dtdat=opp_dtdat, opp_dtdacc=opp_dtdacc, opp_dsubs=opp_dsubs, opp_dpasses=opp_dpasses, opp_drev=opp_drev, opp_dhsl=opp_dhsl, opp_dhsat=opp_dhsat, opp_dhsacc=opp_dhsacc, opp_dbsl=opp_dbsl, opp_dbsat=opp_dbsat, opp_dbsacc=opp_dbsacc, opp_dlsl=opp_dlsl, opp_dlsat=opp_dlsat, opp_dlsacc=opp_dlsacc, opp_ddsl=opp_ddsl, opp_ddsat=opp_ddsat, opp_ddsacc=opp_ddsacc, opp_dcsl=opp_dcsl, opp_dcsat=opp_dcsat, opp_dcsacc=opp_dcsacc, opp_dgsl=opp_dgsl, opp_dgsat=opp_dgsat, opp_dgsacc=opp_dgsacc, opp_ranks=opp_ranks, odds=odds, opp_odds=opp_odds, avgtft=avgtft, opp_avgtft=opp_avgtft, ssm=ssm, tsm=tsm, tdm=tdm, hsm=hsm, bsm=bsm, lsm=lsm, dsm=dsm, csm=csm, gsm=gsm, opp_ssm=opp_ssm, opp_tsm=opp_tsm, opp_tdm=opp_tdm, opp_hsm=opp_hsm, opp_bsm=opp_bsm, opp_lsm=opp_lsm, opp_dsm=opp_dsm, opp_csm=opp_csm, opp_gsm=opp_gsm, dssm=dssm, dtsm=dtsm, dtdm=dtdm, dhsm=dhsm, dbsm=dbsm, dlsm=dlsm, ddsm=ddsm, dcsm=dcsm, dgsm=dgsm, opp_dssm=opp_dssm, opp_dtsm=opp_dtsm, opp_dtdm=opp_dtdm, opp_dhsm=opp_dhsm, opp_dbsm=opp_dbsm, opp_dlsm=opp_dlsm, opp_ddsm=opp_ddsm, opp_dcsm=opp_dcsm, opp_dgsm=opp_dgsm, historywins=historywins, historylosses=historylosses, opp_historywins=opp_historywins, opp_historylosses=opp_historylosses)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/fighters')
def fighters():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM roster ORDER BY ufc_debut desc")
    fighters = cur.fetchall()
    if result > 0:
        return render_template('fighters.html', fighters=fighters)
    else:
        msg = 'No fighters Found'
        return render_template('fighters.html', msg=msg)
    cur.close()


@app.route('/bouts')
def bouts():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM histories ORDER BY date DESC")
    bouts = cur.fetchmany(100)
    if result > 0:
        return render_template('bouts.html', bouts=bouts)
    else:
        msg = 'No Bouts Found'
        return render_template('bouts.html', msg=msg)
    cur.close()


@app.route('/stats')
def stats():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM stats ORDER BY stat_id DESC")
    stats = cur.fetchmany(25)
    if result > 0:
        return render_template('stats.html', stats=stats)
    else:
        msg = 'No stats Found'
        return render_template('stats.html', msg=msg)
    cur.close()


@app.route('/hcalcs')
def hcalcs():
    cur = mysql.connection.cursor()
    hcalcs = cur.execute("SELECT fig_name from histories group by fig_name")
    hcalcs = cur.fetchall()    

    return render_template('hcalcs.html', hcalcs=hcalcs)


@app.route('/hcalc/<string:fig_name>/')
def hcalc(fig_name):
    cur = mysql.connection.cursor()
    hcalc = cur.execute("SELECT fig_name from histories WHERE fig_name = %s", [fig_name])
    hcalc = cur.fetchone()

    tfs = cur.execute("SELECT COUNT(fig_name) as tfs from histories where fig_name = %s", [fig_name])
    tfs = cur.fetchone()

    tw = cur.execute("SELECT COUNT(fig_name) as tw from histories where result = 'win' and fig_name = %s", [fig_name])
    tw = cur.fetchone()

    tl = cur.execute("SELECT COUNT(fig_name) as tl from histories where result = 'loss' and fig_name = %s", [fig_name])
    tl = cur.fetchone()

    tkow = cur.execute("SELECT COUNT(fig_name) as tkow FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkow = cur.fetchone()

    tsubw = cur.execute("SELECT COUNT(fig_name) as tsubw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubw = cur.fetchone()

    tdecw = cur.execute("SELECT COUNT(fig_name) as tdecw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecw = cur.fetchone()

    tkol = cur.execute("SELECT COUNT(fig_name) as tkol FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkol = cur.fetchone()

    tsubl = cur.execute("SELECT COUNT(fig_name) as tsubl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubl = cur.fetchone()

    tdecl = cur.execute("SELECT COUNT(fig_name) as tdecl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecl = cur.fetchone()

    draws = cur.execute("SELECT COUNT(fig_name) as draws from histories where result = 'draw' and fig_name = %s", [fig_name])
    draws = cur.fetchone()

    nc = cur.execute("SELECT COUNT(fig_name) as nc from histories where result = 'NC' and fig_name = %s", [fig_name])
    nc = cur.fetchone()

    frf = cur.execute("SELECT COUNT(fig_name) as frf from histories where result = 'win' and round_ = '1' and fig_name = %s", [fig_name])
    frf = cur.fetchone()

    potn = cur.execute("SELECT COUNT(fig_name) as potn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Performance of the Night' + "%", [fig_name]))
    potn = cur.fetchone()

    fotn = cur.execute("SELECT COUNT(fig_name) as fotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Fight of the Night' + "%", [fig_name]))
    fotn = cur.fetchone()

    kootn = cur.execute("SELECT COUNT(fig_name) as kootn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Knockout of the Night' + "%", [fig_name]))
    kootn = cur.fetchone()

    sotn = cur.execute("SELECT COUNT(fig_name) as sotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Submission of the Night' + "%", [fig_name]))
    sotn = cur.fetchone()

    bonuses = cur.execute("SELECT COUNT(fig_name) as bonuses FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'f the Night' + "%", [fig_name]))
    bonuses = cur.fetchone()

    tft = cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(total_fight_time))) as tft FROM histories WHERE fig_name = %s", [fig_name])
    tft = cur.fetchone()
 
    return render_template('hcalc.html', fig_name=fig_name, hcalc=hcalc, tfs=tfs, tw=tw, tl=tl, tkow=tkow, tsubw=tsubw, tdecw=tdecw, tkol=tkol, tsubl=tsubl, tdecl=tdecl, draws=draws, nc=nc, frf=frf, potn=potn, fotn=fotn, kootn=kootn, sotn=sotn, bonuses=bonuses, tft=tft)



@app.route('/scalc/<string:fig_name>/')
def scalc(fig_name):
    cur = mysql.connection.cursor()
    scalc = cur.execute("SELECT fig_name from histories WHERE fig_name = %s", [fig_name])
    scalc = cur.fetchone()

    kd = cur.execute("SELECT SUM(kd) as kd from stats where fig_name = %s", [fig_name])
    kd = cur.fetchone()


    ssla = cur.execute("SELECT SUM(ssl_) as ssla from stats where fig_name = %s", [fig_name])
    ssla = cur.fetchone()

    ssat = cur.execute("SELECT SUM(ssa_) as ssat from stats where fig_name = %s", [fig_name])
    ssat = cur.fetchone()
    ssacc = cur.execute("SELECT AVG(ROUND(ssac_, 1)) as ssacc from stats where fig_name = %s", [fig_name])
    ssacc = cur.fetchone()


    tsl = cur.execute("SELECT SUM(tsl_) as tsl from stats where fig_name = %s", [fig_name])
    tsl = cur.fetchone()
    tsat = cur.execute("SELECT SUM(tsa_) as tsat from stats where fig_name = %s", [fig_name])
    tsat = cur.fetchone()
    tsacc = cur.execute("SELECT AVG(ROUND(tsac_)) as tsacc from stats where fig_name = %s", [fig_name])
    tsacc = cur.fetchone()


    tdl = cur.execute("SELECT SUM(tdl_) as tdl from stats where fig_name = %s", [fig_name])
    tdl = cur.fetchone()
    tdat = cur.execute("SELECT SUM(tda_) as tdat from stats where fig_name = %s", [fig_name])
    tdat = cur.fetchone()
    tdacc = cur.execute("SELECT AVG(ROUND(tdac_)) as tdacc from stats where fig_name = %s", [fig_name])
    tdacc = cur.fetchone()


    subs = cur.execute("SELECT SUM(sub_) as subs from stats where fig_name = %s", [fig_name])
    subs = cur.fetchone()
    passes = cur.execute("SELECT SUM(pass_) as passes from stats where fig_name = %s", [fig_name])
    passes = cur.fetchone()
    rev = cur.execute("SELECT SUM(rev) as rev from stats where fig_name = %s", [fig_name])
    rev = cur.fetchone()


    hsl = cur.execute("SELECT SUM(headl_) as hsl from stats where fig_name = %s", [fig_name])
    hsl = cur.fetchone()
    hsat = cur.execute("SELECT SUM(heada_) as hsat from stats where fig_name = %s", [fig_name])
    hsat = cur.fetchone()
    hsacc = cur.execute("SELECT AVG(ROUND(headac_)) as hsacc from stats where fig_name = %s", [fig_name])
    hsacc = cur.fetchone()


    bsl = cur.execute("SELECT SUM(bodyl_) as bsl from stats where fig_name = %s", [fig_name])
    bsl = cur.fetchone()
    bsat = cur.execute("SELECT SUM(bodya_) as bsat from stats where fig_name = %s", [fig_name])
    bsat = cur.fetchone()
    bsacc = cur.execute("SELECT AVG(ROUND(bodyac_)) as bsacc from stats where fig_name = %s", [fig_name])
    bsacc = cur.fetchone()


    lsl = cur.execute("SELECT SUM(legl_) as lsl from stats where fig_name = %s", [fig_name])
    lsl = cur.fetchone()
    lsat = cur.execute("SELECT SUM(lega_) as lsat from stats where fig_name = %s", [fig_name])
    lsat = cur.fetchone()
    lsacc = cur.execute("SELECT AVG(ROUND(legac_)) as lsacc from stats where fig_name = %s", [fig_name])
    lsacc = cur.fetchone()


    dsl = cur.execute("SELECT SUM(distl_) as dsl from stats where fig_name = %s", [fig_name])
    dsl = cur.fetchone()
    dsat = cur.execute("SELECT SUM(dista_) as dsat from stats where fig_name = %s", [fig_name])
    dsat = cur.fetchone()
    dsacc = cur.execute("SELECT AVG(ROUND(distac_)) as dsacc from stats where fig_name = %s", [fig_name])
    dsacc = cur.fetchone()


    csl = cur.execute("SELECT SUM(clinchl_) as csl from stats where fig_name = %s", [fig_name])
    csl = cur.fetchone()
    csat = cur.execute("SELECT SUM(clincha_) as csat from stats where fig_name = %s", [fig_name])
    csat = cur.fetchone()
    csacc = cur.execute("SELECT AVG(ROUND(clinchac_)) as csacc from stats where fig_name = %s", [fig_name])
    csacc = cur.fetchone()


    gsl = cur.execute("SELECT SUM(groundl_) as gsl from stats where fig_name = %s", [fig_name])
    gsl = cur.fetchone()
    gsat = cur.execute("SELECT SUM(grounda_) as gsat from stats where fig_name = %s", [fig_name])
    gsat = cur.fetchone()
    gsacc = cur.execute("SELECT AVG(ROUND(groundac_)) as gsacc from stats where fig_name = %s", [fig_name])
    gsacc = cur.fetchone()



    dkd = cur.execute("SELECT SUM(kd) as dkd from stats where opponent = %s", [fig_name])
    dkd = cur.fetchone()


    dssla = cur.execute("SELECT SUM(ssl_) as dssla from stats where opponent = %s", [fig_name])
    dssla = cur.fetchone()

    dssat = cur.execute("SELECT SUM(ssa_) as dssat from stats where opponent = %s", [fig_name])
    dssat = cur.fetchone()


    dssacc = cur.execute("SELECT AVG(ROUND(ssac_, 1)) as dssacc from stats where opponent = %s", [fig_name])
    dssacc = cur.fetchone()


    dtsl = cur.execute("SELECT SUM(tsl_) as dtsl from stats where opponent = %s", [fig_name])
    dtsl = cur.fetchone()
    dtsat = cur.execute("SELECT SUM(tsa_) as dtsat from stats where opponent = %s", [fig_name])
    dtsat = cur.fetchone()
    dtsacc = cur.execute("SELECT ABS(AVG(ROUND(tsac_)-100)) as dtsacc from stats where opponent = %s", [fig_name])
    dtsacc = cur.fetchone()


    dtdl = cur.execute("SELECT SUM(tdl_) as dtdl from stats where opponent = %s", [fig_name])
    dtdl = cur.fetchone()
    dtdat = cur.execute("SELECT SUM(tda_) as dtdat from stats where opponent = %s", [fig_name])
    dtdat = cur.fetchone()
    dtdacc = cur.execute("SELECT AVG(ROUND(tdac_)) as dtdacc from stats where opponent = %s", [fig_name])
    dtdacc = cur.fetchone()


    dsubs = cur.execute("SELECT SUM(sub_) as dsubs from stats where opponent = %s", [fig_name])
    dsubs = cur.fetchone()
    dpasses = cur.execute("SELECT SUM(pass_) as dpasses from stats where opponent = %s", [fig_name])
    dpasses = cur.fetchone()
    drev = cur.execute("SELECT SUM(rev) as drev from stats where opponent = %s", [fig_name])
    drev = cur.fetchone()


    dhsl = cur.execute("SELECT SUM(headl_) as dhsl from stats where opponent = %s", [fig_name])
    dhsl = cur.fetchone()
    dhsat = cur.execute("SELECT SUM(heada_) as dhsat from stats where opponent = %s", [fig_name])
    dhsat = cur.fetchone()
    dhsacc = cur.execute("SELECT AVG(ROUND(headac_)) as dhsacc from stats where opponent = %s", [fig_name])
    dhsacc = cur.fetchone()


    dbsl = cur.execute("SELECT SUM(bodyl_) as dbsl from stats where opponent = %s", [fig_name])
    dbsl = cur.fetchone()
    dbsat = cur.execute("SELECT SUM(bodya_) as dbsat from stats where opponent = %s", [fig_name])
    dbsat = cur.fetchone()
    dbsacc = cur.execute("SELECT AVG(ROUND(bodyac_)) as dbsacc from stats where opponent = %s", [fig_name])
    dbsacc = cur.fetchone()


    dlsl = cur.execute("SELECT SUM(legl_) as dlsl from stats where opponent = %s", [fig_name])
    dlsl = cur.fetchone()
    dlsat = cur.execute("SELECT SUM(lega_) as dlsat from stats where opponent = %s", [fig_name])
    dlsat = cur.fetchone()
    dlsacc = cur.execute("SELECT AVG(ROUND(legac_)) as dlsacc from stats where opponent = %s", [fig_name])
    dlsacc = cur.fetchone()


    ddsl = cur.execute("SELECT SUM(distl_) as ddsl from stats where opponent = %s", [fig_name])
    ddsl = cur.fetchone()
    ddsat = cur.execute("SELECT SUM(dista_) as ddsat from stats where opponent = %s", [fig_name])
    ddsat = cur.fetchone()
    ddsacc = cur.execute("SELECT AVG(ROUND(distac_)) as ddsacc from stats where opponent = %s", [fig_name])
    ddsacc = cur.fetchone()


    dcsl = cur.execute("SELECT SUM(clinchl_) as dcsl from stats where opponent = %s", [fig_name])
    dcsl = cur.fetchone()
    dcsat = cur.execute("SELECT SUM(clincha_) as dcsat from stats where opponent = %s", [fig_name])
    dcsat = cur.fetchone()
    dcsacc = cur.execute("SELECT AVG(ROUND(clinchac_)) as dcsacc from stats where opponent = %s", [fig_name])
    dcsacc = cur.fetchone()


    dgsl = cur.execute("SELECT SUM(groundl_) as dgsl from stats where opponent = %s", [fig_name])
    dgsl = cur.fetchone()
    dgsat = cur.execute("SELECT SUM(grounda_) as dgsat from stats where opponent = %s", [fig_name])
    dgsat = cur.fetchone()
    dgsacc = cur.execute("SELECT AVG(ROUND(groundac_)) as dgsacc from stats where opponent = %s", [fig_name])
    dgsacc = cur.fetchone()

    return render_template('scalc.html', scalc=scalc, fig_name=fig_name, kd=kd, ssla=ssla, ssat=ssat, ssacc=ssacc, tsl=tsl, tsat=tsat, tsacc=tsacc, tdl=tdl, tdat=tdat, tdacc=tdacc, subs=subs, passes=passes, rev=rev, hsl=hsl, hsat=hsat, hsacc=hsacc, bsl=bsl, bsat=bsat, bsacc=bsacc, lsl=lsl, lsat=lsat, lsacc=lsacc, dsl=dsl, dsat=dsat, dsacc=dsacc, csl=csl, csat=csat, csacc=csacc, gsl=gsl, gsat=gsat, gsacc=gsacc, dkd=dkd, dssla=dssla, dssat=dssat, dssacc=dssacc, dtsl=dtsl, dtsat=dtsat, dtsacc=dtsacc, dtdl=dtdl, dtdat=dtdat, dtdacc=dtdacc, dsubs=dsubs, dpasses=dpasses, drev=drev, dhsl=dhsl, dhsat=dhsat, dhsacc=dhsacc, dbsl=dbsl, dbsat=dbsat, dbsacc=dbsacc, dlsl=dlsl, dlsat=dlsat, dlsacc=dlsacc, ddsl=ddsl, ddsat=ddsat, ddsacc=ddsacc, dcsl=dcsl, dcsat=dcsat, dcsacc=dcsacc, dgsl=dgsl, dgsat=dgsat, dgsacc=dgsacc)



@app.route('/fighter/<string:fig_name>/')
def fighter(fig_name):
    cur = mysql.connection.cursor()
    bio = cur.execute("SELECT * FROM roster WHERE fig_name = %s", [fig_name])
    bio = cur.fetchone()

    result = cur.execute("SELECT * FROM histories WHERE fig_name = %s", [fig_name])
    history = cur.fetchall()

    result = cur.execute("SELECT * FROM stats WHERE fig_name = %s", [fig_name])
    stats_o = cur.fetchall()

    result = cur.execute("SELECT * FROM stats WHERE opponent = %s", [fig_name])
    stats_d = cur.fetchall()

    cur.close()

    return render_template('fighter.html', bio=bio, history=history, stats_o=stats_o, stats_d=stats_d)



@app.route('/fighterpage/<string:fig_name>/')
def fighterpage(fig_name):
    cur = mysql.connection.cursor()

    bio = cur.execute("SELECT * FROM roster WHERE fig_name = %s", [fig_name])
    bio = cur.fetchone()

    history = cur.execute("SELECT * FROM histories WHERE fig_name = %s ORDER BY date DESC", [fig_name])
    history = cur.fetchall()

    stats_o = cur.execute("SELECT * FROM stats WHERE fig_name = %s ORDER BY date DESC", [fig_name])
    stats_o = cur.fetchall()

    stats_d = cur.execute("SELECT * FROM stats WHERE opponent = %s ORDER BY date DESC", [fig_name])
    stats_d = cur.fetchall()

    tfs = cur.execute("SELECT COUNT(fig_name) as tfs from histories where fig_name = %s", [fig_name])
    tfs = cur.fetchone()

    tw = cur.execute("SELECT COUNT(fig_name) as tw from histories where result = 'win' and fig_name = %s", [fig_name])
    tw = cur.fetchone()

    tl = cur.execute("SELECT COUNT(fig_name) as tl from histories where result = 'loss' and fig_name = %s", [fig_name])
    tl = cur.fetchone()

    tkow = cur.execute("SELECT COUNT(fig_name) as tkow FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkow = cur.fetchone()

    tsubw = cur.execute("SELECT COUNT(fig_name) as tsubw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubw = cur.fetchone()

    tdecw = cur.execute("SELECT COUNT(fig_name) as tdecw FROM histories WHERE result = 'win' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecw = cur.fetchone()

    tkol = cur.execute("SELECT COUNT(fig_name) as tkol FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'KO' + "%", [fig_name]))
    tkol = cur.fetchone()

    tsubl = cur.execute("SELECT COUNT(fig_name) as tsubl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'sub' + "%", [fig_name]))
    tsubl = cur.fetchone()

    tdecl = cur.execute("SELECT COUNT(fig_name) as tdecl FROM histories WHERE result = 'loss' AND method_ LIKE %s and fig_name = %s", ("%" + 'dec' + "%", [fig_name]))
    tdecl = cur.fetchone()

    draws = cur.execute("SELECT COUNT(fig_name) as draws from histories where result = 'draw' and fig_name = %s", [fig_name])
    draws = cur.fetchone()

    nc = cur.execute("SELECT COUNT(fig_name) as nc from histories where result = 'NC' and fig_name = %s", [fig_name])
    nc = cur.fetchone()

    frf = cur.execute("SELECT COUNT(fig_name) as frf from histories where result = 'win' and round_ = '1' and fig_name = %s", [fig_name])
    frf = cur.fetchone()

    potn = cur.execute("SELECT COUNT(fig_name) as potn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Performance of the Night' + "%", [fig_name]))
    potn = cur.fetchone()

    fotn = cur.execute("SELECT COUNT(fig_name) as fotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Fight of the Night' + "%", [fig_name]))
    fotn = cur.fetchone()

    kootn = cur.execute("SELECT COUNT(fig_name) as kootn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Knockout of the Night' + "%", [fig_name]))
    kootn = cur.fetchone()

    sotn = cur.execute("SELECT COUNT(fig_name) as sotn FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'Submission of the Night' + "%", [fig_name]))
    sotn = cur.fetchone()

    bonuses = cur.execute("SELECT COUNT(fig_name) as bonuses FROM histories WHERE notes LIKE %s and fig_name = %s", ("%" + 'f the Night' + "%", [fig_name]))
    bonuses = cur.fetchone()

    tft = cur.execute("SELECT SEC_TO_TIME(SUM(TIME_TO_SEC(total_fight_time))) as tft FROM histories WHERE fig_name = %s", [fig_name])
    tft = cur.fetchone()

    scalc = cur.execute("SELECT fig_name from histories WHERE fig_name = %s", [fig_name])
    scalc = cur.fetchone()

    kd = cur.execute("SELECT SUM(kd) as kd from stats where fig_name = %s", [fig_name])
    kd = cur.fetchone()


    ssla = cur.execute("SELECT SUM(ssl_) as ssla from stats where fig_name = %s", [fig_name])
    ssla = cur.fetchone()

    ssat = cur.execute("SELECT SUM(ssa_) as ssat from stats where fig_name = %s", [fig_name])
    ssat = cur.fetchone()
    ssacc = cur.execute("SELECT IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0) as ssacc from stats where fig_name = %s", [fig_name])
    ssacc = cur.fetchone()


    tsl = cur.execute("SELECT SUM(tsl_) as tsl from stats where fig_name = %s", [fig_name])
    tsl = cur.fetchone()
    tsat = cur.execute("SELECT SUM(tsa_) as tsat from stats where fig_name = %s", [fig_name])
    tsat = cur.fetchone()
    tsacc = cur.execute("SELECT IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0) as tsacc from stats where fig_name = %s", [fig_name])
    tsacc = cur.fetchone()


    tdl = cur.execute("SELECT SUM(tdl_) as tdl from stats where fig_name = %s", [fig_name])
    tdl = cur.fetchone()
    tdat = cur.execute("SELECT SUM(tda_) as tdat from stats where fig_name = %s", [fig_name])
    tdat = cur.fetchone()
    tdacc = cur.execute("SELECT IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0) as tdacc from stats where fig_name = %s", [fig_name])
    tdacc = cur.fetchone()


    subs = cur.execute("SELECT SUM(sub_) as subs from stats where fig_name = %s", [fig_name])
    subs = cur.fetchone()
    passes = cur.execute("SELECT SUM(pass_) as passes from stats where fig_name = %s", [fig_name])
    passes = cur.fetchone()
    rev = cur.execute("SELECT SUM(rev) as rev from stats where fig_name = %s", [fig_name])
    rev = cur.fetchone()


    hsl = cur.execute("SELECT SUM(headl_) as hsl from stats where fig_name = %s", [fig_name])
    hsl = cur.fetchone()
    hsat = cur.execute("SELECT SUM(heada_) as hsat from stats where fig_name = %s", [fig_name])
    hsat = cur.fetchone()
    hsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as hsacc from stats where fig_name = %s", [fig_name])
    hsacc = cur.fetchone()


    bsl = cur.execute("SELECT SUM(bodyl_) as bsl from stats where fig_name = %s", [fig_name])
    bsl = cur.fetchone()
    bsat = cur.execute("SELECT SUM(bodya_) as bsat from stats where fig_name = %s", [fig_name])
    bsat = cur.fetchone()
    bsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as bsacc from stats where fig_name = %s", [fig_name])
    bsacc = cur.fetchone()


    lsl = cur.execute("SELECT SUM(legl_) as lsl from stats where fig_name = %s", [fig_name])
    lsl = cur.fetchone()
    lsat = cur.execute("SELECT SUM(lega_) as lsat from stats where fig_name = %s", [fig_name])
    lsat = cur.fetchone()
    lsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as lsacc from stats where fig_name = %s", [fig_name])
    lsacc = cur.fetchone()


    dsl = cur.execute("SELECT SUM(distl_) as dsl from stats where fig_name = %s", [fig_name])
    dsl = cur.fetchone()
    dsat = cur.execute("SELECT SUM(dista_) as dsat from stats where fig_name = %s", [fig_name])
    dsat = cur.fetchone()
    dsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as dsacc from stats where fig_name = %s", [fig_name])
    dsacc = cur.fetchone()


    csl = cur.execute("SELECT SUM(clinchl_) as csl from stats where fig_name = %s", [fig_name])
    csl = cur.fetchone()
    csat = cur.execute("SELECT SUM(clincha_) as csat from stats where fig_name = %s", [fig_name])
    csat = cur.fetchone()
    csacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as csacc from stats where fig_name = %s", [fig_name])
    csacc = cur.fetchone()


    gsl = cur.execute("SELECT SUM(groundl_) as gsl from stats where fig_name = %s", [fig_name])
    gsl = cur.fetchone()
    gsat = cur.execute("SELECT SUM(grounda_) as gsat from stats where fig_name = %s", [fig_name])
    gsat = cur.fetchone()
    gsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as gsacc from stats where fig_name = %s", [fig_name])
    gsacc = cur.fetchone()



    dkd = cur.execute("SELECT SUM(kd) as dkd from stats where opponent = %s", [fig_name])
    dkd = cur.fetchone()


    dssla = cur.execute("SELECT SUM(ssl_) as dssla from stats where opponent = %s", [fig_name])
    dssla = cur.fetchone()

    dssat = cur.execute("SELECT SUM(ssa_) as dssat from stats where opponent = %s", [fig_name])
    dssat = cur.fetchone()


    dssacc = cur.execute("SELECT IFNULL(ROUND(SUM(ssl_)/SUM(ssa_)*100,2),0.0) as dssacc from stats where opponent = %s", [fig_name])
    dssacc = cur.fetchone()


    dtsl = cur.execute("SELECT SUM(tsl_) as dtsl from stats where opponent = %s", [fig_name])
    dtsl = cur.fetchone()
    dtsat = cur.execute("SELECT SUM(tsa_) as dtsat from stats where opponent = %s", [fig_name])
    dtsat = cur.fetchone()
    dtsacc = cur.execute("SELECT IFNULL(ROUND(SUM(tsl_)/SUM(tsa_)*100,2),0.0) as dtsacc from stats where opponent = %s", [fig_name])
    dtsacc = cur.fetchone()


    dtdl = cur.execute("SELECT SUM(tdl_) as dtdl from stats where opponent = %s", [fig_name])
    dtdl = cur.fetchone()
    dtdat = cur.execute("SELECT SUM(tda_) as dtdat from stats where opponent = %s", [fig_name])
    dtdat = cur.fetchone()
    dtdacc = cur.execute("SELECT IFNULL(ROUND(SUM(tdl_)/SUM(tda_)*100,2),0.0) as dtdacc from stats where opponent = %s", [fig_name])
    dtdacc = cur.fetchone()


    dsubs = cur.execute("SELECT SUM(sub_) as dsubs from stats where opponent = %s", [fig_name])
    dsubs = cur.fetchone()
    dpasses = cur.execute("SELECT SUM(pass_) as dpasses from stats where opponent = %s", [fig_name])
    dpasses = cur.fetchone()
    drev = cur.execute("SELECT SUM(rev) as drev from stats where opponent = %s", [fig_name])
    drev = cur.fetchone()


    dhsl = cur.execute("SELECT SUM(headl_) as dhsl from stats where opponent = %s", [fig_name])
    dhsl = cur.fetchone()
    dhsat = cur.execute("SELECT SUM(heada_) as dhsat from stats where opponent = %s", [fig_name])
    dhsat = cur.fetchone()
    dhsacc = cur.execute("SELECT IFNULL(ROUND(SUM(headl_)/SUM(heada_)*100,2),0.0) as dhsacc from stats where opponent = %s", [fig_name])
    dhsacc = cur.fetchone()


    dbsl = cur.execute("SELECT SUM(bodyl_) as dbsl from stats where opponent = %s", [fig_name])
    dbsl = cur.fetchone()
    dbsat = cur.execute("SELECT SUM(bodya_) as dbsat from stats where opponent = %s", [fig_name])
    dbsat = cur.fetchone()
    dbsacc = cur.execute("SELECT IFNULL(ROUND(SUM(bodyl_)/SUM(bodya_)*100,2),0.0) as dbsacc from stats where opponent = %s", [fig_name])
    dbsacc = cur.fetchone()


    dlsl = cur.execute("SELECT SUM(legl_) as dlsl from stats where opponent = %s", [fig_name])
    dlsl = cur.fetchone()
    dlsat = cur.execute("SELECT SUM(lega_) as dlsat from stats where opponent = %s", [fig_name])
    dlsat = cur.fetchone()
    dlsacc = cur.execute("SELECT IFNULL(ROUND(SUM(legl_)/SUM(lega_)*100,2),0.0) as dlsacc from stats where opponent = %s", [fig_name])
    dlsacc = cur.fetchone()


    ddsl = cur.execute("SELECT SUM(distl_) as ddsl from stats where opponent = %s", [fig_name])
    ddsl = cur.fetchone()
    ddsat = cur.execute("SELECT SUM(dista_) as ddsat from stats where opponent = %s", [fig_name])
    ddsat = cur.fetchone()
    ddsacc = cur.execute("SELECT IFNULL(ROUND(SUM(distl_)/SUM(dista_)*100,2),0.0) as ddsacc from stats where opponent = %s", [fig_name])
    ddsacc = cur.fetchone()


    dcsl = cur.execute("SELECT SUM(clinchl_) as dcsl from stats where opponent = %s", [fig_name])
    dcsl = cur.fetchone()
    dcsat = cur.execute("SELECT SUM(clincha_) as dcsat from stats where opponent = %s", [fig_name])
    dcsat = cur.fetchone()
    dcsacc = cur.execute("SELECT IFNULL(ROUND(SUM(clinchl_)/SUM(clincha_)*100,2),0.0) as dcsacc from stats where opponent = %s", [fig_name])
    dcsacc = cur.fetchone()


    dgsl = cur.execute("SELECT SUM(groundl_) as dgsl from stats where opponent = %s", [fig_name])
    dgsl = cur.fetchone()
    dgsat = cur.execute("SELECT SUM(grounda_) as dgsat from stats where opponent = %s", [fig_name])
    dgsat = cur.fetchone()
    dgsacc = cur.execute("SELECT IFNULL(ROUND(SUM(groundl_)/SUM(grounda_)*100,2),0.0) as dgsacc from stats where opponent = %s", [fig_name])
    dgsacc = cur.fetchone()

    ranks = cur.execute("SELECT * FROM ranks")
    ranks = cur.fetchone()

    cur.close()

    return render_template('fighterpage.html', bio=bio, history=history, stats_o=stats_o, stats_d=stats_d, tfs=tfs, tw=tw, tl=tl, tkow=tkow, tsubw=tsubw, tdecw=tdecw, tkol=tkol, tsubl=tsubl, tdecl=tdecl, draws=draws, nc=nc, frf=frf, potn=potn, fotn=fotn, kootn=kootn, sotn=sotn, bonuses=bonuses, tft=tft, kd=kd, ssla=ssla, ssat=ssat, ssacc=ssacc, tsl=tsl, tsat=tsat, tsacc=tsacc, tdl=tdl, tdat=tdat, tdacc=tdacc, subs=subs, passes=passes, rev=rev, hsl=hsl, hsat=hsat, hsacc=hsacc, bsl=bsl, bsat=bsat, bsacc=bsacc, lsl=lsl, lsat=lsat, lsacc=lsacc, dsl=dsl, dsat=dsat, dsacc=dsacc, csl=csl, csat=csat, csacc=csacc, gsl=gsl, gsat=gsat, gsacc=gsacc, dkd=dkd, dssla=dssla, dssat=dssat, dssacc=dssacc, dtsl=dtsl, dtsat=dtsat, dtsacc=dtsacc, dtdl=dtdl, dtdat=dtdat, dtdacc=dtdacc, dsubs=dsubs, dpasses=dpasses, drev=drev, dhsl=dhsl, dhsat=dhsat, dhsacc=dhsacc, dbsl=dbsl, dbsat=dbsat, dbsacc=dbsacc, dlsl=dlsl, dlsat=dlsat, dlsacc=dlsacc, ddsl=ddsl, ddsat=ddsat, ddsacc=ddsacc, dcsl=dcsl, dcsat=dcsat, dcsacc=dcsacc, dgsl=dgsl, dgsat=dgsat, dgsacc=dgsacc, ranks=ranks)



# Single bout
@app.route('/bout/<string:fig_name>/')
def bout(fig_name):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM histories WHERE fig_name = %s", [fig_name])
    bouts = cur.fetchmany(25)
    return render_template('bout.html', bouts=bouts, fig_name=fig_name)


# Single stat
@app.route('/stat/<string:fig_name>/')
def stat(fig_name):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM stats WHERE fig_name = %s", [fig_name])
    stats = cur.fetchall()
    return render_template('stat.html', stats=stats)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('events'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM roster")
    fighters = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', fighters=fighters)
    else:
        msg = 'No Fighters Found'
        return render_template('dashboard.html', msg=msg)
    cur.close()


# Fighter Form Class
class FighterForm(Form):
    fig_name = StringField('Fighter Name', [validators.Length(min=1, max=40)])
    nickname = StringField('Nickname', [validators.Length(max=40)])
    rank_ = StringField('Rank', [validators.Length(max=40)])
    weightclass = StringField('Weightclass', [validators.Length(max=40)])
    country = StringField('Country', [validators.Length(max=40)])
    height = StringField('Height', [validators.Length(max=40)])
    status = StringField('Status', [validators.Length(max=40)])
    age = IntegerField('Age', [validators.Length(max=40)])
    weight = StringField('Weight', [validators.Length(max=40)])
    arm_length = StringField('Arm Length', [validators.Length(max=40)])
    leg_length = StringField('Leg Length', [validators.Length(max=40)])
    stance = StringField('Stance', [validators.Length(max=40)])
    ufc_debut = StringField('UFC Debut', [validators.Length(max=40)])
    camp = StringField('Camp', [validators.Length(max=300)])
    birthday = StringField('Birthday', [validators.Length(max=40)])
    twitter = StringField('Twitter', [validators.Length(max=40)])
    instagram = StringField('Instagram', [validators.Length(max=40)])
    ufc_link = StringField('UFC Link', [validators.Length(max=100)])
    ufc_stats_link = StringField('UFC Stats Link', [validators.Length(max=100)])
    espn_link = StringField('ESPN Link', [validators.Length(max=100)])
    other_links = TextAreaField('Other Links', [validators.Length(max=500)])
    strengths = TextAreaField('Strengths', [validators.Length(max=500)])
    keys_ = TextAreaField('Keys', [validators.Length(max=500)])
    xfactors = TextAreaField('XFactors', [validators.Length(max=500)])
    analyst_notes = TextAreaField('Analyst Notes', [validators.Length(max=1000)])
    accolades = TextAreaField('Accolades', [validators.Length(max=1000)])
    other_info = TextAreaField('Other Info', [validators.Length(max=2000)])
    notable_wins = StringField('Notable Wins', [validators.Length(max=40)])    


# Add fighter
@app.route('/add_fighter', methods=['GET', 'POST'])
@is_logged_in
def add_fighter():
    form = FighterForm(request.form)
    if request.method == 'POST':
        fig_name = form.fig_name.data
        nickname = form.nickname.data
        rank_ = form.rank_.data
        weightclass = form.weightclass.data
        country = form.country.data
        height = form.height.data
        status = form.status.data
        weight = form.weight.data
        arm_length = form.arm_length.data
        leg_length = form.leg_length.data
        stance = form.stance.data
        ufc_debut = form.ufc_debut.data
        camp = form.camp.data
        birthday = form.birthday.data
        twitter = form.twitter.data
        instagram = form.instagram.data
        ufc_link = form.ufc_link.data
        ufc_stats_link = form.ufc_stats_link.data
        espn_link = form.espn_link.data
        other_links = form.other_links.data
        strengths = form.strengths.data
        keys_ = form.keys_.data
        xfactors = form.xfactors.data
        analyst_notes = form.analyst_notes.data
        accolades = form.accolades.data
        other_info = form.other_info.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO roster(fig_name, nickname, rank_, weightclass, country, height, status, weight, arm_length, leg_length, stance, ufc_debut, camp, birthday, twitter, instagram, ufc_link, ufc_stats_link, espn_link, other_links, strengths, keys_, xfactors, analyst_notes, accolades, other_info, author) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (fig_name, nickname, rank_, weightclass, country, height, status, weight, arm_length, leg_length, stance, ufc_debut, camp, birthday, twitter, instagram, ufc_link, ufc_stats_link, espn_link, other_links, strengths, keys_, xfactors, analyst_notes, accolades, other_info, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Fighter Created', 'success')
        return redirect(url_for('fighters'))
    return render_template('add_fighter.html', form=form)


# Edit fighter
@app.route('/edit_fighter/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_fighter(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM roster WHERE fig_name = %s", [id])
    edit_bio = cur.fetchone()
    cur.close()
    # Get form
    form = FighterForm(request.form)
    # Populate fighter form fields
    form.fig_name.data = edit_bio['fig_name']
    form.nickname.data = edit_bio['nickname']
    form.rank_.data = edit_bio['rank_']
    form.weightclass.data = edit_bio['weightclass']
    form.country.data = edit_bio['country']
    form.height.data = edit_bio['height']
    form.status.data = edit_bio['status']
    form.weight.data = edit_bio['weight']
    form.arm_length.data = edit_bio['arm_length']
    form.leg_length.data = edit_bio['leg_length']
    form.stance.data = edit_bio['stance']
    form.ufc_debut.data = edit_bio['ufc_debut']
    form.camp.data = edit_bio['camp']
    form.birthday.data = edit_bio['birthday']
    form.twitter.data = edit_bio['twitter']
    form.instagram.data = edit_bio['instagram']
    form.ufc_link.data = edit_bio['ufc_link']
    form.ufc_stats_link.data = edit_bio['ufc_stats_link']
    form.espn_link.data = edit_bio['espn_link']
    form.other_links.data = edit_bio['other_links']
    form.strengths.data = edit_bio['strengths']
    form.keys_.data = edit_bio['keys_']
    form.xfactors.data = edit_bio['xfactors']
    form.analyst_notes.data = edit_bio['analyst_notes']
    form.accolades.data = edit_bio['accolades']
    form.other_info.data = edit_bio['other_info']

    if request.method == 'POST':
        fig_name = request.form['fig_name']
        nickname = request.form['nickname']
        rank_ = request.form['rank_']
        weightclass = request.form['weightclass']
        country = request.form['country']
        height = request.form['height']
        status = request.form['status']
        weight = request.form['weight']
        arm_length = request.form['arm_length']
        leg_length = request.form['leg_length']
        stance = request.form['stance']
        ufc_debut = request.form['ufc_debut']
        camp = request.form['camp']
        birthday = request.form['birthday']
        twitter = request.form['twitter']
        instagram = request.form['instagram']
        ufc_link = request.form['ufc_link']
        ufc_stats_link = request.form['ufc_stats_link']
        espn_link = request.form['espn_link']
        other_links = request.form['other_links']
        strengths = request.form['strengths']
        keys_ = request.form['keys_']
        xfactors = request.form['xfactors']
        analyst_notes = request.form['analyst_notes']
        accolades = request.form['accolades']
        other_info = request.form['other_info']
        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(fig_name)
        cur.execute("UPDATE roster SET fig_name=%s, nickname=%s, rank_=%s, weightclass=%s, country=%s, height=%s, status=%s, weight=%s, arm_length=%s, leg_length=%s, stance=%s, ufc_debut=%s, camp=%s, birthday=%s, twitter=%s, instagram=%s, ufc_link=%s, ufc_stats_link=%s, espn_link=%s, other_links=%s, strengths=%s, keys_=%s, xfactors=%s, analyst_notes=%s, accolades=%s, other_info=%s WHERE fig_name=%s", (fig_name, nickname, rank_, weightclass, country, height, status, weight, arm_length, leg_length, stance, ufc_debut, camp, birthday, twitter, instagram, ufc_link, ufc_stats_link, espn_link, other_links, strengths, keys_, xfactors, analyst_notes, accolades, other_info, id))

        mysql.connection.commit()
        cur.close()
        flash('Fighter Updated', 'success')
        return redirect(url_for('fighters'))
    return render_template('edit_fighter.html', form=form)


# Delete fighter
@app.route('/delete_fighter/<string:id>', methods=['POST'])
@is_logged_in
def delete_fighter(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM roster WHERE fig_name = %s", [id])
    # Commit to DB
    mysql.connection.commit()
    # Close connection
    cur.close()
    flash('Fighter Deleted', 'success')
    return redirect(url_for('fighters'))


# FighterBout Form Class
class FighterBout(Form):
    hist_id = StringField('Hist ID', [validators.Length(min=1, max=40)])
    fig_name = StringField('Fighter Name', [validators.Length(min=1, max=40)])
    date = StringField('Date', [validators.Length(max=40)])
    event = StringField('Event', [validators.Length(max=40)])
    opponent = StringField('Opponent', [validators.Length(max=40)])
    result = StringField('Result', [validators.Length(max=40)])
    method_ = StringField('Method', [validators.Length(max=40)])
    round_ = StringField('Round', [validators.Length(max=40)])
    time_ = StringField('Time', [validators.Length(max=40)])
    notes = TextAreaField('Notes', [validators.Length(max=40)])
    total_fight_time = StringField('Total Fight Time', [validators.Length(max=40)])
    record = StringField('Record', [validators.Length(max=40)])
    location = StringField('Location', [validators.Length(max=40)])


# Add bout
@app.route('/add_bout', methods=['GET', 'POST'])
@is_logged_in
def add_bout():
    form = FighterBout(request.form)
    if request.method == 'POST':
        fig_name = form.fig_name.data
        date = form.date.data
        event = form.event.data
        opponent = form.opponent.data
        result = form.result.data
        method_ = form.method_.data
        round_ = form.round_.data
        time_ = form.time_.data
        notes = form.notes.data
        total_fight_time = form.total_fight_time.data
        record = form.record.data
        location = form.location.data
        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute("INSERT INTO histories(fig_name, date, event, opponent, result, method_, round_, time_, notes, total_fight_time, record, location, author) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 (fig_name, date, event, opponent, result, method_, round_, time_, notes, total_fight_time, record, location, session['username']))
        mysql.connection.commit()
        cur.close()
        flash('Bout Created', 'success')
        return redirect(url_for('bouts'))
    return render_template('add_bout.html', form=form)


# Edit bout
@app.route('/edit_bout/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_bout(id):
    # Create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM histories WHERE hist_id = %s", [id])
    edit_bout = cur.fetchone()
    cur.close()
    # Get form
    form = FighterBout(request.form)
    # Populate bout form fields
    form.fig_name.data = edit_bout['fig_name']
    form.date.data = edit_bout['date']
    form.event.data = edit_bout['event']
    form.opponent.data = edit_bout['opponent']
    form.result.data = edit_bout['result']
    form.method_.data = edit_bout['method_']
    form.round_.data = edit_bout['round_']
    form.time_.data = edit_bout['time_']
    form.notes.data = edit_bout['notes']
    form.total_fight_time.data = edit_bout['total_fight_time']
    form.record.data = edit_bout['record']
    form.location.data = edit_bout['location']

    if request.method == 'POST':
        fig_name = request.form['fig_name']
        date = request.form['date']
        event = request.form['event']
        opponent = request.form['opponent']
        result = request.form['result']
        method_ = request.form['method_']
        round_ = request.form['round_']
        time_ = request.form['time_']
        notes = request.form['notes']
        total_fight_time = request.form['total_fight_time']
        record = request.form['record']
        location = request.form['location']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE histories SET fig_name=%s, date=%s, event=%s, opponent=%s, result=%s, method_=%s, round_=%s, time_=%s, notes=%s, total_fight_time=%s, record=%s, location=%s WHERE hist_id=%s", (fig_name, date, event, opponent, result, method_, round_, time_, notes, total_fight_time, record, location, id))
        mysql.connection.commit()
        cur.close()
        flash('Bout Updated', 'success')
        return redirect(url_for('bouts'))
    return render_template('edit_bout.html', form=form)


# Delete bout
@app.route('/delete_bout/<string:id>', methods=['POST'])
@is_logged_in
def delete_bout(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM histories WHERE hist_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Bout Deleted', 'success')
    return redirect(url_for('bouts'))


# FighterStat Form Class
class FighterStat(Form):
    stat_id = StringField('Stat ID', [validators.Length(min=1, max=150)])
    fig_name = StringField('Fig Name', [validators.Length(min=1, max=50)])
    opponent = StringField('Opponent', [validators.Length(min=1, max=50)])
    kd = IntegerField('Kd')
    ssl_ = IntegerField('Significant Strikes Landed')
    ssa_ = IntegerField('Significant Strike Attempted')
    tsl_ = IntegerField('Total Strikes Landed')
    tsa_ = IntegerField('Total Strikes Attempted')
    tdl_ = IntegerField('Takedowns Landed')
    tda_ = IntegerField('Takedowns Attempted')
    sub_ = IntegerField('Sub Attempts')
    pass_ = IntegerField('Pass')
    rev = IntegerField('Rev')
    headl_ = IntegerField('Head Landed')
    heada_ = IntegerField('Head Attempted')
    bodyl_ = IntegerField('Body Landed')
    bodya_ = IntegerField('Body Attempted')
    legl_ = IntegerField('Leg Landed')
    lega_ = IntegerField('Leg Attempted')
    distl_ = IntegerField('Distance Landed')
    dista_ = IntegerField('Distance Attempted')
    clinchl_ = IntegerField('Clinch Landed')
    clincha_ = IntegerField('Clinch Attempted')
    groundl_ = IntegerField('Ground Landed')
    grounda_ = IntegerField('Ground Attempted')
    event = StringField('Event')
    date = StringField('Date')


# Add stat
@app.route('/add_stat', methods=['GET', 'POST'])
@is_logged_in
def add_stat():
    form = FighterStat(request.form)
    if request.method == 'POST':
        fig_name = form.fig_name.data
        opponent = form.opponent.data
        kd = form.kd.data
        ssl_ = form.ssl_.data
        ssa_ = form.ssa_.data
        tsl_ = form.tsl_.data
        tsa_ = form.tsa_.data
        tdl_ = form.tdl_.data
        tda_ = form.tda_.data
        sub_ = form.sub_.data
        pass_ = form.pass_.data
        rev = form.rev.data
        headl_ = form.headl_.data
        heada_ = form.heada_.data
        bodyl_ = form.bodyl_.data
        bodya_ = form.bodya_.data
        legl_ = form.legl_.data
        lega_ = form.lega_.data
        distl_ = form.distl_.data
        dista_ = form.dista_.data
        clinchl_ = form.clinchl_.data
        clincha_ = form.clincha_.data
        groundl_ = form.groundl_.data
        grounda_ = form.grounda_.data
        event = form.event.data
        date = form.date.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stats(fig_name, opponent, kd, ssl_, ssa_, tsl_, tsa_, tdl_, tda_, sub_, pass_, rev, headl_, heada_, bodyl_, bodya_, legl_, lega_, distl_, dista_, clinchl_, clincha_, groundl_, grounda_, event, date, author) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                     (fig_name, opponent, kd, ssl_, ssa_, tsl_, tsa_, tdl_, tda_, sub_, pass_, rev, headl_, heada_, bodyl_, bodya_, legl_, lega_, distl_, dista_, clinchl_, clincha_, groundl_, grounda_, event, date, session['username']))

        mysql.connection.commit()
        cur.close()
        flash('Stat Created', 'success')
        return redirect(url_for('stats'))
    return render_template('add_stat.html', form=form)


# Edit stat
@app.route('/edit_stat/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_stat(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM stats WHERE stat_id = %s", [id])
    edit_stat = cur.fetchone()
    cur.close()

    form = FighterStat(request.form)
    # Populate stat form fields
    form.fig_name.data = edit_stat['fig_name']
    form.opponent.data = edit_stat['opponent']
    form.kd.data = edit_stat['kd']
    form.ssl_.data = edit_stat['ssl_']
    form.ssa_.data = edit_stat['ssa_']
    form.tsl_.data = edit_stat['tsl_']
    form.tsa_.data = edit_stat['tsa_']
    form.tdl_.data = edit_stat['tdl_']
    form.tda_.data = edit_stat['tda_']
    form.sub_.data = edit_stat['sub_']
    form.pass_.data = edit_stat['pass_']
    form.rev.data = edit_stat['rev']
    form.headl_.data = edit_stat['headl_']
    form.heada_.data = edit_stat['heada_']
    form.bodyl_.data = edit_stat['bodyl_']
    form.bodya_.data = edit_stat['bodya_']
    form.legl_.data = edit_stat['legl_']
    form.lega_.data = edit_stat['lega_']
    form.distl_.data = edit_stat['distl_']
    form.dista_.data = edit_stat['dista_']
    form.clinchl_.data = edit_stat['clinchl_']
    form.clincha_.data = edit_stat['clincha_']
    form.groundl_.data = edit_stat['groundl_']
    form.grounda_.data = edit_stat['grounda_']
    form.event.data = edit_stat['event']
    form.date.data = edit_stat['date']

    if request.method == 'POST':
        fig_name = request.form['fig_name']
        opponent = request.form['opponent']
        kd = request.form['kd']
        ssl_ = request.form['ssl_']
        ssa_ = request.form['ssa_']
        tsl_ = request.form['tsl_']
        tsa_ = request.form['tsa_']
        tdl_ = request.form['tdl_']
        tda_ = request.form['tda_']
        sub_ = request.form['sub_']
        pass_ = request.form['pass_']
        rev = request.form['rev']
        headl_ = request.form['headl_']
        heada_ = request.form['heada_']
        bodyl_ = request.form['bodyl_']
        bodya_ = request.form['bodya_']
        legl_ = request.form['legl_']
        lega_ = request.form['lega_']
        distl_ = request.form['distl_']
        dista_ = request.form['dista_']
        clinchl_ = request.form['clinchl_']
        clincha_ = request.form['clincha_']
        groundl_ = request.form['groundl_']
        grounda_ = request.form['grounda_']
        event = request.form['event']
        date = request.form['date']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE stats SET fig_name=%s, opponent=%s, kd=%s, ssl_=%s, ssa_=%s, tsl_=%s, tsa_=%s, tdl_=%s, tda_=%s, sub_=%s, pass_=%s, rev=%s, headl_=%s, heada_=%s, bodyl_=%s, bodya_=%s, legl_=%s, lega_=%s, distl_=%s, dista_=%s, clinchl_=%s, clincha_=%s, groundl_=%s, grounda_=%s, event=%s, date=%s WHERE stat_id=%s", (fig_name, opponent, kd, ssl_, ssa_, tsl_, tsa_, tdl_, tda_, sub_, pass_, rev, headl_, heada_, bodyl_, bodya_, legl_, lega_, distl_, dista_, clinchl_, clincha_, groundl_, grounda_, event, date, id))
        mysql.connection.commit()
        cur.close()
        flash('Stat Updated', 'success')
        return redirect(url_for('stats'))
    return render_template('edit_stat.html', form=form)


# Delete stat
@app.route('/delete_stat/<string:id>', methods=['POST'])
@is_logged_in
def delete_stat(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stats WHERE stat_id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Stat Deleted', 'success')
    return redirect(url_for('stats'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)