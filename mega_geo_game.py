# -*- coding:utf-8 -*-
'''
Created on 03.04.2014

@author: Ausleihe
This modules holds the whole logic for a megageogame,
right now somewhat hardcoded for the event that took place on the
4.6.14, but it should be easily updatable such that it can get generic
game-instructions from a database
'''
from flask import (Flask, render_template, request, jsonify)
import os
import psycopg2
import urlparse
from operator import itemgetter
from math import floor, fabs
from arcgis_scraper import ArcgisScraper
from geometry_calculator import GeometryHandler
import traceback

APP = Flask(__name__)

SCRAPER = ArcgisScraper()
GEOMETRYHANDLER = GeometryHandler()
DATABASE_URL = (
    '''postgres://dgibhwjhbemyxu:rFqJwYnsX48PtWyR8LUgVHH0bE@ec2-54-228-219-2.eu-west-1.compute.amazonaws.com:5432/d6ln3gnquqodqq'''
    )
urlparse.uses_netloc.append("postgres")
URL = urlparse.urlparse(os.environ['DATABASE_URL'])

CONNECTION = psycopg2.connect(
    database=URL.path[1:],
    user=URL.username,
    password=URL.password,
    host=URL.hostname,
    port=URL.port
    )

CURSOR = CONNECTION.cursor()

QUERY_GET_LEVEL = []
QUERY_GET_LEVEL.append(
    "http://services1.arcgis.com/6RDtDcH"
    "z3yZdtEVu/ArcGIS/rest/services/MegaGeoGame_Level"
    )
QUERY_GET_LEVEL.append(
    "_State/FeatureServer/0/query?where"
    "=1%3D1&outFields=GeoGameState&f=pjson"
    )

QUERY_LEVEL_2 = []
QUERY_LEVEL_2.append(
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/"
    "MegaGeoGame_Level2_Distanzen/FeatureServer/0/query?where=Klasse+%3D+"
    )
QUERY_LEVEL_2.append('''&units=esriSRUnit_Meter&returnGeometry=true&f=pjson''')

QUERY_LEVEL_3 = []
QUERY_LEVEL_3.append(
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/Mega"
    "GeoGame_Level3_L%C3%A4rmmessung/FeatureServer/0/query?where=Klasse+%3D+"
    )
QUERY_LEVEL_3.append('''&units=esriSRUnit_Meter&returnGeometry=true&f=pjson''')
QUERY_LEVEL_4 = []
QUERY_LEVEL_4.append(
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/"
    "MegaGeoGame_Level4_WeisseSocken/FeatureServer/0/query?where=Klasse+%3D+"
    )
QUERY_LEVEL_4.append('''&units=esriSRUnit_Meter&returnGeometry=true&f=pjson''')

QUERY_POINTS = "SELECT points FROM classes WHERE number = %s"

UPDATE_POINTS_QUERY = (
    '''UPDATE classes SET points = %s WHERE number = %s'''
    )
POINTS_FOR_LEVEL_1 = [980, 1080, 1230, 1200, 1010, 970]
CLASSES_IN_ORDER = [
    'Burggraben',
    'Kirchenfeld',
    'Beromünster',
    'Solothurn',
    'Wil',
    'Alpenquai'
    ]

VALID_LEVELS = [1, 2, 3, 4, 5, 6]
VALID_STATES = [1, 2]
TREND_HTML = []
TREND_HTML.append(
    "<img style=\"float:right; margin-top: -5px;\" "
    + "alt=\"trend\" src=\"static/images/")
TREND_HTML.append(".png\" />")

LEGEND_HTML = []
LEGEND_HTML.append("<img alt=\"Legend\" src=\"static/images/legend")
LEGEND_HTML.append(".png\" />")

STATISTICS_CELL = []
STATISTICS_CELL.append('''<li class="list-group-item list-stat">''')
STATISTICS_CELL.append('''</li>''')

STATISTICS_COLUMN = []
STATISTICS_COLUMN.append(
    '''<div class="col-xs-6 stat-col"><ul class="list-group">''')
STATISTICS_COLUMN.append('''</ul></div>''')

STATISTICS_PANEL = []
STATISTICS_PANEL.append(
    '''<div id="level1-stat"><div class="row sub-row" id="stat-row">''')
STATISTICS_PANEL.append('''</div></div>''')
UPDATE_TREND = "UPDATE classes SET trend = %s WHERE number = %s"
@APP.route('/')
def show_site():
    '''
    Renders the infopanel
    '''
    return render_template('content.html')


@APP.route('/instruction')
def instructions():
    '''
    Renders the instruction page
    '''
    return render_template('instruction.html')


@APP.route('/input-level1')
def input_level1():
    '''
    Renders instructions for level 1
    '''
    classes = get_classes()
    return render_template('input-level1.html', classes=classes)


@APP.route('/test')
def tester():
    '''
    page-location available for testing
    '''
    pass


@APP.route('/input-level2')
def input_level2():
    '''
    Renders instructions for level 2
    '''
    return render_template('input-level2.html')


@APP.route('/input-level3')
def input_level3():
    '''
    Renders instructions for level 3
    '''
    return render_template('input-level3.html')


@APP.route('/input-level4')
def input_level4():
    '''
    Renders instructions for level 4
    '''
    return render_template('input-level4.html',)


@APP.route('/input-level5')
def input_level5():
    '''
    Renders instructions for level 5
    '''
    return render_template('input-level5.html')


@APP.route('/input-level6')
def input_level6():
    '''
    Renders instructions for level 6
    '''
    classes = get_classes()
    return render_template('input-level6.html', classes=classes)


@APP.route('/_level_1_submit')
def data_submitted():
    '''
    Ajax function for input of level 1
    '''
    return data_submit(1)


@APP.route('/_level_6_submit')
def data_submitted6():
    '''
    Ajax function for input of level 6
    '''
    return data_submit(6)


@APP.route('/match_submit')
def match_submitted():
    '''
    Ajax function for matching input
    '''
    class_number = int(request.args.get('class_num'))
    match = int(request.args.get('match')) + 1
    if class_number == 0:
        return jsonify(result="Please select a class")
    CURSOR.execute(
        "SELECT match, number FROM classes"
        )
    match_entries = CURSOR.fetchall()
    for row in match_entries:
        if row[0] == match and row[1] != class_number:
            return jsonify(
                result="This startpoint is already chosen by somebody")
    CURSOR.execute(
        "SELECT match, points FROM classes WHERE number = %s",
        (class_number,)
        )
    query_results = CURSOR.fetchone()
    old_match = query_results[0]
    old_points = query_results[1]
    CURSOR.execute(
        "UPDATE classes SET match = %s WHERE number = %s ",
        (match, class_number)
        )
    if old_match == 0:
        new_points = old_points + POINTS_FOR_LEVEL_1[class_number - 1]
        CURSOR.execute(
            UPDATE_POINTS_QUERY,
            (new_points, class_number)
            )
    CONNECTION.commit()
    return jsonify(result='''Your submission has been recorded''')


@APP.route('/matching')
def show_match():
    '''
    Backend for matching
    '''
    classes = get_classes()
    return render_template('matching.html', classes=classes)


@APP.route('/_level1_selected')
def level_1_selected():
    '''
    Ajax function for manual display of level 1
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 1)


@APP.route('/_level2_selected')
def level2_selected():
    '''
    Ajax function for manual display of level 2
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 2)


@APP.route('/_level3_selected')
def level3_selected():
    '''
    Ajax function for manual display of level 3
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 3)


@APP.route('/_level4_selected')
def level4_selected():
    '''
    Ajax function for manual display of level 4
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 4)


@APP.route('/_level5_selected')
def level5_selected():
    '''
    Ajax function for manual display of level 5
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 5)

@APP.route('/_level6_selected')
def level6_selected():
    '''
    Ajax function for manual display of level 6
    '''
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 6)

def elements_for_manual_mode(curr_level, clicked_level):
    '''
    Generic function for returning all elements that change
    dynamically when in manual mode
    '''
    stats = get_classes_in_statistics(clicked_level, 3)
    header = get_instruction_header(curr_level, clicked_level)
    instruction_panel_text = get_instruction(clicked_level)
    legend = get_legend(clicked_level)
    map_iframe = get_map(clicked_level)
    return jsonify(
        stats=stats,
        header=header,
        instruction=instruction_panel_text,
        legend=legend,
        map=map_iframe
        )


@APP.route('/_update_level')
def update():
    '''
    Ajax function for updating the level displayed
    '''
    try:
        curr_level = int(request.args.get('current_level'))
        curr_state = int(request.args.get('current_state'))
        if not curr_level in VALID_LEVELS:
            curr_level = 0
        instruction_panel_text = get_instruction(curr_level)
        instruction_panel_heading = ''
        if curr_level == 0:
            map_iframe = get_map(1)
            instruction_panel_heading = 'A game with 6 levels'
            image_html = get_legend(0)
        elif curr_level == 1 and (curr_state == 1 or curr_state == 2):
            map_iframe = get_map(10)
            image_html = get_legend(1.1)
        else:
            map_iframe = get_map(curr_level)
        if curr_level == 1 and (curr_state == 3 or curr_state == 3):
            image_html = get_legend(1.3)
        elif curr_level < 7 and curr_level > 1:
            image_html = get_legend(curr_level)
        return jsonify(
            instruction_panel_heading=instruction_panel_heading,
            instruction=instruction_panel_text,
            map=map_iframe,
            image=image_html
            )
    except Exception:
        return jsonify(
            result=traceback.format_exc())

@APP.route('/_get_current_ranking')
def update_ranking():
    '''
    Ajax function for updating ranking
    '''
    curr_level = int(request.args.get('current_level'))
    curr_state = int(request.args.get('current_state'))
    stats = get_classes_in_statistics(curr_level, curr_state)
    ranking = get_ranking()
    return jsonify(
        place1=ranking[0],
        place2=ranking[1],
        place3=ranking[2],
        place4=ranking[3],
        place5=ranking[4],
        place6=ranking[5],
        instruction=stats
        )


@APP.route('/_get_current_level')
def get_current_level():
    '''
    Ajax function for getting current level
    '''
    curr_level = int(request.args.get('current_level'))
    if not curr_level == 0:
        pre_query = str(curr_level).join(QUERY_GET_LEVEL)
        curr_layer = SCRAPER.get_json(pre_query)
        state = int(
            curr_layer['features'][0]['attributes']['GeoGameState']
            )
        if state != 3 and state in VALID_STATES:
            return jsonify(level=curr_level, state=state)
    for i in range(1, 7):
        if i != curr_level:
            query = str(i).join(QUERY_GET_LEVEL)
            curr_layer = SCRAPER.get_json(query)
            state = int(
                curr_layer['features'][0]['attributes']['GeoGameState']
                )
            if state != 3 and state in VALID_STATES:
                return jsonify(level=i, state=state)
    if curr_level in VALID_LEVELS:
        return jsonify(level=curr_level, state=3)
    else:
        return jsonify(level=0, state=0)

def get_classes_in_statistics(curr_level, curr_state):
    '''
    Return the whole html for the statistics panel
    '''
    classes_html = []
    data_array = []
    class_array = CLASSES_IN_ORDER


    if curr_level == 1:
        query_count = "SELECT count(*) FROM estimate_class_%s"
        select_querry = "SELECT estimate FROM estimate_class_%s"
        correct_answer = 1574
    elif curr_level == 6:
        query_count = "SELECT count(*) from estimate_6_class_%s"
        select_querry = "SELECT estimate FROM estimate_6_class_%s"
        correct_answer = 8797

    if curr_level == 1 or curr_level == 6:
        if curr_state == 1 or curr_state == 2:
            for i in range(1, 7):
                CURSOR.execute(query_count, (i,))
                data_array.append(
                    str(CURSOR.fetchone()[0])
                    + ' submissions'
                    )
        elif curr_state == 3:
            numbs = []
            class_array = []
            for i in range(1, 7):
                CURSOR.execute(query_count, (i,))
                row_count = CURSOR.fetchone()[0]
                CURSOR.execute(
                    "SELECT name from classes WHERE number = %s",
                    (i,)
                    )
                current_class = CURSOR.fetchone()[0]
                estimate_difference = 0
                if int(row_count) > 0:
                    estimate = 0
                    CURSOR.execute(select_querry, (i,))
                    for row in CURSOR.fetchall():
                        estimate += row[0]
                    estimate = int(estimate / row_count)
                    if curr_level == 6:
                        CURSOR.execute(
                            "UPDATE level6 SET estimate = %s WHERE class = %s",
                            (estimate, str(i))
                            )
                        CURSOR.execute(
                            "SELECT has_guessed FROM level6 WHERE class = %s",
                            (str(i), )
                            )
                        if int(CURSOR.fetchone()[0]) == 0:
                            CURSOR.execute(QUERY_POINTS, (str(i), ))
                            old_points = CURSOR.fetchone()[0]
                            new_points = int(
                                10000
                                - fabs(correct_answer - estimate)
                                )
                            if new_points < 0:
                                new_points = 0
                            new_points = old_points + new_points
                            CURSOR.execute(
                                UPDATE_POINTS_QUERY,
                                (new_points, str(i))
                                )
                            CURSOR.execute(
                                "UPDATE level6 SET has_guessed = 1 WHERE class = %s",
                                (str(i), )
                                )
                    estimate_difference = int(fabs(correct_answer - estimate))
                numbs.append(
                    {"class": current_class,
                     "estimate_difference": estimate_difference}
                    )
            numbs = sorted(
                numbs,
                key=itemgetter('estimate_difference')
                )
            for i in range(0, 6):
                class_array.append(str(numbs[i]["class"]))
                data_array.append(str(numbs[i]["estimate_difference"]))


    elif curr_level == 2 or curr_level == 3 or curr_level == 4:
        if curr_level == 2:
            scrape_query = QUERY_LEVEL_2
            select_old_points = "SELECT meter FROM level2 WHERE class = %s"
            update_level_score = "UPDATE level2 SET meter = %s WHERE class = %s"
        if curr_level == 3:
            scrape_query = QUERY_LEVEL_3
            select_old_points = "SELECT numb FROM level3 WHERE class = %s"
            update_level_score = "UPDATE level3 SET numb = %s WHERE class = %s"
        if curr_level == 4:
            scrape_query = QUERY_LEVEL_4
            select_old_points = "SELECT socks FROM level4 WHERE class = %s"
            update_level_score = "UPDATE level4 SET socks = %s WHERE class = %s"
        for i in range(0, 6):
            features = SCRAPER.get_json(
                str(i + 1).join(scrape_query))['features']
            level_points = len(features)
            CURSOR.execute(select_old_points, (i + 1,))
            old_points = CURSOR.fetchone()[0]
            CURSOR.execute(QUERY_POINTS, (i + 1,))
            curr_points = CURSOR.fetchone()[0]
            new_points = (level_points - old_points) * 100 + curr_points
            point_data = str(level_points)
            if curr_level == 2:
                if level_points > 0:
                    point1 = features[0]['geometry']['paths'][0][0]
                    point2 = features[0]['geometry']['paths'][0][1]
                    level_points = int(
                        floor(GEOMETRYHANDLER.get_distance(point1, point2))
                        / 1000
                        )
                new_points = level_points  - old_points + curr_points
                point_data = 'Length: ' +  str(level_points) + ' km'
            elif curr_level == 3:
                point_data += ' objects'
            elif curr_level == 4:
                point_data += ' socks'
            if old_points < level_points:
                CURSOR.execute(UPDATE_POINTS_QUERY, (new_points, i + 1))
                CURSOR.execute(update_level_score, (level_points, i + 1))
            data_array.append(point_data)
    CONNECTION.commit()
    for i in range(0, 6):
        classes_html.append(
            class_array[i]
            + '<br>'
            + data_array[i])
    if len(classes_html) < 0:
        return get_statistics_html(classes_html)
    else:
        return ''

def get_classes():
    '''
    Returns all classes
    '''
    classes = []
    CURSOR.execute("SELECT name FROM classes ORDER BY number")
    for current_class in CURSOR.fetchall():
        classes.append(current_class[0])
    return classes

def get_ranking():
    '''
    Returns the current ranking
    '''
    classes = []
    for i in range(1, 7):
        CURSOR.execute(
            '''SELECT points, name,
            match, state, former_place,
            trend
             from classes
            WHERE number = %s''',
            (i, )
            )
        result = CURSOR.fetchone()
        curr_class = {
            'class_id': i,
            'points': result[0],
            'class_name': result[1],
            'match': result[2],
            'state': result[3],
            'former_place': result[4],
            'old_trend': result[5]
            }
        classes.append(curr_class)
    classes = sorted(classes, key=itemgetter('points'))
    classes.reverse()
    curr_places = []
    dirty = False
    dirties = ['', '', '', '', '', '']

    for i in range(0, 6):
        result_array = get_class_html(classes[i], i, dirties)
        curr_places.append(result_array[0])
        if not dirty:
            dirty = result_array[1]
        dirties = result_array[2]
    if dirty:
        for i in range(0, 6):
            if dirties[i] == '':
                dirties[i] = (
                    get_match_color(classes[i]['match'])
                    + str(classes[i]['class_name'])
                    + ' ('
                    + str(classes[i]['state'])
                    + ')'
                    + get_image_trend(0)
                    + '<div class="points_ranking" style="float: right;" >'
                    + str(classes[i]['points'])
                    + ' points'
                    + '</div>'
                    )
                CURSOR.execute(
                    UPDATE_TREND,
                    (0, classes[i]['class_id'],)
                    )
                CONNECTION.commit()
        curr_places = dirties
    return curr_places

def get_instruction(level):
    '''
    Gets the instruction text for the level
    '''
    CURSOR.execute(
        "SELECT instruction FROM instructions WHERE level = %s",
        (level,))
    return CURSOR.fetchone()[0]

def get_map(level):
    '''
    Gets the map for the level
    '''
    CURSOR.execute(
        "SELECT map_link FROM maps WHERE id = %s",
        (level,))
    return CURSOR.fetchone()[0]

def data_submit(level):
    '''
    Handles the submit of estimates in level 1 and 6
    '''
    class_name = request.args.get('class_num', 0, type=int)
    estimate = request.args.get('estimate')
    if class_name == 0:
        return jsonify(result="Bitte wähle eine Klasse aus")
    try:
        estimate = int(estimate)
    except ValueError:
        return jsonify(result="Deine Eingabe war keine Zahl")
    if level == 1:
        count_query = '''SELECT count(*) FROM estimate_class_%s'''
        insert_query = '''INSERT INTO estimate_class_%s VALUES ( %s )'''
    elif level == 6:
        count_query = '''SELECT count(*) FROM estimate_6_class_%s'''
        insert_query = '''INSERT INTO estimate_6_class_%s VALUES ( %s )'''
    CURSOR.execute(
        count_query,
        (class_name,)
        )
    estimate_count = CURSOR.fetchone()[0]
    if estimate_count >= 25:
        return jsonify(result="Diese Klasse hat schon 25 Eingaben gemacht.")
    else:
        CURSOR.execute(
            insert_query,
            (class_name, estimate)
            )
        CONNECTION.commit()
        return jsonify(result="Deine Eingabe war erfolgreich")

def get_instruction_header(current_level, level):
    '''
    Returns the header to be displayed in manual mode
    '''
    if current_level > level:
        return 'Passed'
    elif current_level < level:
        return 'Not Started'
    else:
        return 'Playing'

def get_match_color(match):
    '''
    Returns html representing the match color
    '''
    if match != 0:
        match_color = (
            "<img style=\"margin-right: 15px;\""
            + " alt=\"Color\" src=\"static/images/"
            + str(match) + ".png\" />"
            )
    else:
        match_color = ''
    return match_color

def get_class_html(class_dict, index, dirties):
    '''
    Returns html for classes in ranking panel and some flags used for
    determining if ranking has changed
    '''
    dirty = False
    if class_dict['former_place'] != index + 1:
        dirty = True
        CURSOR.execute(
            "UPDATE classes SET former_place = %s WHERE number = %s",
            (index + 1, class_dict['class_id'])
            )
        if class_dict['former_place'] < index + 1:
            image = get_image_trend(-1)
            CURSOR.execute(
                UPDATE_TREND,
                (-1, class_dict['class_id'],)
                )
            CONNECTION.commit()
        elif class_dict['former_place'] > index + 1:
            image = get_image_trend(1)
            CURSOR.execute(
                UPDATE_TREND,
                (1, class_dict['class_id'],)
                )
        CONNECTION.commit()
    else:
        image = get_image_trend(class_dict['old_trend'])

    class_text = (
        get_match_color(class_dict['match'])
        + class_dict['class_name']
        + ' ('
        + class_dict['state']
        + ') '
        + image
        + '<div class="points_ranking" style="float: right;" >'
        + str(class_dict['points'])
        + ' points'
        + '</div>'
        )
    if dirty:
        dirties[index] = class_text
    return [class_text, dirty, dirties]

def get_statistics_html(class_html_array):
    '''
    Return the html used in the statistics panel
    '''
    html = (
        (
            (
                class_html_array[0].join(STATISTICS_CELL)
                + class_html_array[1].join(STATISTICS_CELL)
                + class_html_array[2].join(STATISTICS_CELL)
                ).join(STATISTICS_COLUMN)
            + (
                class_html_array[3].join(STATISTICS_CELL)
                + class_html_array[4].join(STATISTICS_CELL)
                + class_html_array[5].join(STATISTICS_CELL)
                ).join(STATISTICS_COLUMN)
            ).join(STATISTICS_PANEL)
        )
    return html

def get_image_trend(trend):
    '''
    Returns the image-html representing the trend
    '''
    if trend == 1:
        return 'up'.join(TREND_HTML)
    elif trend == -1:
        return 'down'.join(TREND_HTML)
    else:
        return 'same'.join(TREND_HTML)

def get_legend(level):
    '''
    Returns image-html for the legend-panel
    '''
    if level == 1.1 or level == 1.2:
        return '1-1'.join(LEGEND_HTML)
    elif level == 1.3 or level == 1:
        return '1-2'.join(LEGEND_HTML)
    elif level < 7 and level > 1:
        return str(level).join(LEGEND_HTML)
    else:
        return ''
