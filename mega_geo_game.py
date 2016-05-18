# -*- coding:utf-8 -*-
from flask import (Flask, render_template, request, jsonify)
import os
import psycopg2
import urlparse
from operator import itemgetter
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
# urlparse.uses_netloc.append("postgres")
# # URL = urlparse.urlparse(os.environ['DATABASE_URL'])
#
# CONNECTION = psycopg2.connect(
#     database="d6ln3gnquqodqq",
#     user="dgibhwjhbemyxu",
#     password="rFqJwYnsX48PtWyR8LUgVHH0bE",
#     host="ec2-54-228-219-2.eu-west-1.compute.amazonaws.com",
#     port="5432"
# )

CURSOR = CONNECTION.cursor()
QUERY_GET_LEVEL = ["http://services1.arcgis.com/6RDtDcHz3yZdtEVu/ArcGIS/rest/services/mgg2016_gamestate_m", "_sek1/FeatureServer/0/query?where"
                                                                       "=1%3D1&outFields=Status&f=pjson"]

QUERY_LEVEL_1 = [
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/mgg2016_m1_sek1/FeatureServer/0/query?where=Gruppe%3D%27",
    '''%27&units=esriSRUnit_Meter&returnGeometry=true&outFields=Flaeche&f=pjson''']

QUERY_LEVEL_2 = [
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/mgg2016_m2_sek1/FeatureServer/0/query?where=Gruppe%3D%27",
    '''%27&outFields=Nummer_Eingabe%2C+Nummer_Loesung&f=pjson&''']

QUERY_LEVEL_3 = [
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/mgg2016_m3_sek1/FeatureServer/0/query?where=Gruppe%3D%27",
    '''%27&units=esriSRUnit_Meter&returnGeometry=true&f=pjson''']

QUERY_LEVEL_4 = [
    "http://services1.arcgis.com/6RDtDcHz3yZdtEVu/arcgis/rest/services/mgg2016_m4_sek1/FeatureServer/0/query?where=Gruppe%3D%27",
    '''%27&units=esriSRUnit_Meter&returnGeometry=true&f=pjson''']

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
    'Alpenquai',
    'Test1',
    'Test2',
    'Test3',
    'Test4'
]
PLAYER_IDS = [
    'A1',
    'B1',
    'C1',
    'D1',
    'E1',
    'F1',
    'G1',
    'H1',
    'I1',
    'J1'
]
VALID_LEVELS = [1, 2, 3, 4, 5, 6]
VALID_STATES = ['weiss', 'schwarz']
TREND_HTML = ["<img style=\"float:right; margin-top: -5px;\" " +
              "alt=\"trend\" src=\"static/images/", ".png\" />"]

LEGEND_HTML = ["<img alt=\"Legend\" src=\"static/images/legend", ".png\" />"]

STATISTICS_CELL = ['''<li class="list-group-item list-stat">''', '''</li>''']

STATISTICS_COLUMN = ['''<div class="col-xs-6 stat-col"><ul class="list-group">''', '''</ul></div>''']

STATISTICS_PANEL = ['''<div id="level1-stat"><div class="row sub-row" id="stat-row">''', '''</div></div>''']
UPDATE_TREND = "UPDATE classes SET trend = %s WHERE number = %s"

NUMBER_OF_PLAYERS = 10


@APP.route('/')
def show_site():
    return render_template('content.html')


@APP.route('/instruction')
def instructions():
    return render_template('instruction.html')


@APP.route('/input-level1')
def input_level1():
    classes = get_classes()
    return render_template('input-level1.html', classes=classes)


@APP.route('/test')
def tester():
    pass


@APP.route('/input-level2')
def input_level2():
    return render_template('input-level2.html')


@APP.route('/input-level3')
def input_level3():
    return render_template('input-level3.html')


@APP.route('/input-level4')
def input_level4():
    return render_template('input-level4.html' )


@APP.route('/input-level5')
def input_level5():
    return render_template('input-level5.html')


@APP.route('/input-level6')
def input_level6():
    classes = get_classes()
    return render_template('input-level6.html', classes=classes)


@APP.route('/admin')
def tryLogin():
    return render_template('login.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    name = request.json['name']
    password = request.json['password']
    classes = get_classes()
    if name == 'geo' and password == '22322':
        return render_template('admin-board.html', classes=classes)


@APP.route('/_level_1_submit')
def data_submitted():
    return data_submit(1)


@APP.route('/_admin_relative_submit')
def relative_submit():
    class_name = request.args.get('class_num', 0, type=int)
    estimate = request.args.get('points')
    if class_name == 0:
        return jsonify(result="Bitte wähle eine Klasse aus")
    try:
        estimate = int(estimate)
    except ValueError:
        return jsonify(result="Deine Eingabe war keine Zahl")
    CURSOR.execute(
        QUERY_POINTS,
        (PLAYER_IDS[class_name-1],)
    )
    points = CURSOR.fetchone()[0]
    CURSOR.execute(
        UPDATE_POINTS_QUERY,
        (estimate + points, PLAYER_IDS[class_name-1])
    )
    CONNECTION.commit()
    return jsonify(result="Deine Eingabe war erfolgreich")


@APP.route('/_level_6_submit')
def data_submitted6():
    return data_submit(6)


@APP.route('/seed_classes')
def seed():
    x = os.getcwd()
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, 'classes.txt')) as f:
        content = f.readlines()
        for line in content:
            CURSOR.execute(line.rstrip())
        CONNECTION.commit()
    return jsonify(result='''Super''')


@APP.route('/match_submit')
def match_submitted():
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
    classes = get_classes()
    return render_template('matching.html', classes=classes)


@APP.route('/_level1_selected')
def level_1_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 1)


@APP.route('/_level2_selected')
def level2_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 2)


@APP.route('/_level3_selected')
def level3_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 3)


@APP.route('/_level4_selected')
def level4_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 4)


@APP.route('/_level5_selected')
def level5_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 5)


@APP.route('/_level6_selected')
def level6_selected():
    curr_level = int(request.args.get('current_level'))
    return elements_for_manual_mode(curr_level, 6)


def elements_for_manual_mode(curr_level, clicked_level):
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
    curr_level = int(request.args.get('current_level'))
    curr_state = request.args.get('current_state')
    if not curr_level in VALID_LEVELS:
        curr_level = 0
    instruction_panel_text = get_instruction(curr_level)
    instruction_panel_heading = ''
    if curr_level == 0:
        map_iframe = get_map(1)
        instruction_panel_heading = 'A game with 6 levels'
        image_html = get_legend(0)
    elif curr_level == 1 and (curr_state == 'weiss' or curr_state == 'schwarz'):
        map_iframe = get_map(1)
        image_html = get_legend(1.1)
    else:
        map_iframe = get_map(curr_level)
    if curr_level == 1 and (curr_state == 'schwarz'):
        image_html = get_legend(1.3)
    elif curr_level < 7 and curr_level > 1:
        image_html = get_legend(curr_level)
    return jsonify(
        instruction_panel_heading=instruction_panel_heading,
        instruction=instruction_panel_text,
        map=map_iframe,
        image=image_html
    )



@APP.route('/_get_current_ranking')
def update_ranking():
    curr_level = int(request.args.get('current_level'))
    curr_state = request.args.get('current_state')
    stats = get_classes_in_statistics(curr_level, curr_state)
    ranking = get_ranking()
    return jsonify(
        ranking=ranking,
        instruction=stats
    )


@APP.route('/_get_current_level')
def get_current_level():
    curr_level = int(request.args.get('current_level'))
    if not curr_level == 0:
        pre_query = str(curr_level).join(QUERY_GET_LEVEL)
        curr_layer = SCRAPER.get_json(pre_query)
        state = curr_layer['features'][0]['attributes']['Status']
        if state != 'schwarz' and state in VALID_STATES:
            return jsonify(level=curr_level, state=state)
    for i in range(1, 7):
        if i != curr_level:
            query = str(i).join(QUERY_GET_LEVEL)
            curr_layer = SCRAPER.get_json(query)
            state = curr_layer['features'][0]['attributes']['Status']
            if state != 'schwarz' and state in VALID_STATES:
                return jsonify(level=i, state=state)
    if curr_level in VALID_LEVELS:
        return jsonify(level=curr_level, state=3)
    else:
        return jsonify(level=0, state=0)


def get_classes_in_statistics(curr_level, curr_state):
    data_array = []

    if curr_level == 1:
        scrape_query = QUERY_LEVEL_1
        select_old_points = "SELECT points FROM level1 WHERE class = %s"
        update_level_score = "UPDATE level1 SET points = %s WHERE class = %s"
        for player_id in PLAYER_IDS:
            features = SCRAPER.get_json(player_id.join(scrape_query))['features']
            level_points = 0
            if len(features) > 0:
                level_points = features[0]['attributes']['Flaeche']
            CURSOR.execute(select_old_points, (player_id,))
            old_points = CURSOR.fetchone()[0]
            CURSOR.execute(QUERY_POINTS, (player_id,))
            curr_points = CURSOR.fetchone()[0]
            new_points = level_points - old_points + curr_points
            if old_points < level_points:
                CURSOR.execute(UPDATE_POINTS_QUERY, (new_points, player_id))
                CURSOR.execute(update_level_score, (level_points, player_id))
            data_array.append({"name": player_id, "points": level_points})

    elif curr_level == 2:
        scrape_query = QUERY_LEVEL_2
        select_old_points = "SELECT points FROM level2 WHERE class = %s"
        update_level_score = "UPDATE level2 SET points = %s WHERE class = %s"
        for i in range(0, NUMBER_OF_PLAYERS):
            features = SCRAPER.get_json(
                str(PLAYER_IDS[i]).join(scrape_query))['features']
            level_points = 0
            if len(features) > 0:
                for feature in features:
                    number_given = int(feature['attributes']['Nummer_Eingabe'])
                    number_searched = int(feature['attributes']['Nummer_Loesung'])
                    if number_given == number_searched:
                        level_points += 1
            CURSOR.execute(select_old_points, (PLAYER_IDS[i],))
            old_points = CURSOR.fetchone()[0]
            CURSOR.execute(QUERY_POINTS, (PLAYER_IDS[i],))
            curr_points = CURSOR.fetchone()[0]
            new_points = level_points - old_points + curr_points
            point_data = str(level_points)
            if old_points < level_points:
                CURSOR.execute(UPDATE_POINTS_QUERY, (new_points, PLAYER_IDS[i]))
                CURSOR.execute(update_level_score, (level_points, PLAYER_IDS[i]))
            #data_array.append(point_data)

    elif curr_level == 3 or curr_level == 4:
        if curr_level == 3:
            scrape_query = QUERY_LEVEL_3
            select_old_points = "SELECT numb FROM level3 WHERE class = %s"
            update_level_score = "UPDATE level3 SET numb = %s WHERE class = %s"
        if curr_level == 4:
            scrape_query = QUERY_LEVEL_4
            select_old_points = "SELECT socks FROM level4 WHERE class = %s"
            update_level_score = "UPDATE level4 SET socks = %s WHERE class = %s"
        for player_id in PLAYER_IDS:
            features = SCRAPER.get_json(
                str(player_id).join(scrape_query))['features']
            level_points = len(features)
            CURSOR.execute(select_old_points, (player_id,))
            old_points = CURSOR.fetchone()[0]
            CURSOR.execute(QUERY_POINTS, (player_id,))
            curr_points = CURSOR.fetchone()[0]
            new_points = level_points - old_points + curr_points
            if old_points < level_points:
                CURSOR.execute(UPDATE_POINTS_QUERY, (new_points, player_id))
                CURSOR.execute(update_level_score, (level_points, player_id))
            data_array.append({"name": player_id, "points": level_points})

    else:
        for player_id in PLAYER_IDS:
            CURSOR.execute(QUERY_POINTS, (player_id,))
            points = CURSOR.fetchone()[0]
            data_array.append({"name": player_id, "points": points})
    CONNECTION.commit()

    # for i in range(0, NUMBER_OF_PLAYERS):
    #     classes_html.append(
    #         class_array[i] +
    #         '<br>' +
    #         data_array[i])
    if len(data_array) > 0:
        return data_array #get_statistics_html(classes_html)
    else:
        return ''


def get_classes():
    classes = []
    CURSOR.execute("SELECT name FROM classes ORDER BY number")
    for current_class in CURSOR.fetchall():
        classes.append(current_class[0])
    return classes


def get_ranking():
    classes = []
    for i in PLAYER_IDS:
        CURSOR.execute(
            '''SELECT points, name,
            match, state, former_place,
            trend
             from classes
            WHERE number = %s''',
            (i,)
        )
        result = CURSOR.fetchone()
        curr_class = {
            'class_id': i,
            'points': result[0],
            'class_name': result[1],
            'match': result[2],
            'state': result[5],
            'former_place': result[3],
            'old_trend': result[4]
        }
        classes.append(curr_class)
    classes = sorted(classes, key=itemgetter('points'))
    classes.reverse()
    curr_places = []
    dirty = False
    dirties = ['', '', '', '', '', '', '', '', '', '']

    for i in range(0, NUMBER_OF_PLAYERS):
        result_array = get_class_html(classes[i], i, dirties)
        curr_places.append(result_array[0])
        if not dirty:
            dirty = result_array[1]
        dirties = result_array[2]
    if dirty:
        for i in range(0, NUMBER_OF_PLAYERS):
            if dirties[i] == '':
                dirties[i] = (
                    get_match_color(classes[i]['match']) +
                    str(classes[i]['class_name']) +
                    ' (' +
                    str(classes[i]['state']) +
                    ')' +
                    get_image_trend(0) +
                    '<div class="points_ranking" style="float: right;" >' +
                    str(classes[i]['points']) +
                    ' points' +
                    '</div>'
                )
                CURSOR.execute(
                    UPDATE_TREND,
                    (0, classes[i]['class_id'],)
                )
                CONNECTION.commit()
        curr_places = dirties
    return curr_places


def get_instruction(level):
    CURSOR.execute(
        "SELECT instruction FROM instructions WHERE level = %s",
        (level,))
    return CURSOR.fetchone()[0]


def get_map(level):
    CURSOR.execute(
        "SELECT map_link FROM maps WHERE level = %s",
        (level,))
    return CURSOR.fetchone()[0]


def data_submit(level):
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
    if current_level > level:
        return 'Passed'
    elif current_level < level:
        return 'Not Started'
    else:
        return 'Playing'


def get_match_color(match):
    if match != 0:
        match_color = (
            "<img style=\"margin-right: 15px;\"" +
            " alt=\"Color\" src=\"static/images/" +
            str(match) + ".png\" />"
        )
    else:
        match_color = ''
    return match_color


def get_class_html(class_dict, index, dirties):
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
        get_match_color(class_dict['match']) +
        class_dict['class_name'] +
        ' (' +
        str(class_dict['state']) +
        ') ' +
        image +
        '<div class="points_ranking" style="float: right;" >' +
        str(class_dict['points']) +
        ' points' +
        '</div>'
    )
    if dirty:
        dirties[index] = class_text
    return [class_text, dirty, dirties]


def get_statistics_html(class_html_array):
    html = (
        (
            (
                class_html_array[0].join(STATISTICS_CELL) +
                class_html_array[1].join(STATISTICS_CELL) +
                class_html_array[2].join(STATISTICS_CELL)
            ).join(STATISTICS_COLUMN) +
            (
                class_html_array[3].join(STATISTICS_CELL) +
                class_html_array[4].join(STATISTICS_CELL) +
                class_html_array[5].join(STATISTICS_CELL)
            ).join(STATISTICS_COLUMN)
        ).join(STATISTICS_PANEL)
    )
    return html


def get_image_trend(trend):
    if trend == 1:
        return 'up'.join(TREND_HTML)
    elif trend == -1:
        return 'down'.join(TREND_HTML)
    else:
        return 'same'.join(TREND_HTML)


def get_legend(level):
    if level == 1.1 or level == 1.2:
        return '1-1'.join(LEGEND_HTML)
    elif level == 1.3 or level == 1:
        return '1-2'.join(LEGEND_HTML)
    elif 7 > level > 1:
        return str(level).join(LEGEND_HTML)
    else:
        return ''


#if __name__ == '__main__':
#    APP.run()
