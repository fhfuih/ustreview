import atexit

import click

import ustreview
#from . import ustreview

atexit.register(ustreview.quit)

click.echo('''UST Review
A tool to look up HKUST instructors' ratings based on ust.space''')

while True:
    username = click.prompt('Enter your username')
    password = click.prompt('Enter your password\n(Your input won\'t show up on the screen)', hide_input=True)
    click.echo('\nLogging you in...\n')
    try:
        ustreview.login(username, password)
    except ValueError as e:
        click.echo(e)
    else:
        break
    click.clear()


while True:
    click.clear()

    while True:
        course = click.prompt('Enter a course code (Case insensitive)').upper()
        click.echo('\nAcquiring course page...\n')
        try:
            overall_soup = ustreview.request_review_page_soup(course)
        except ValueError as e:
            click.echo(e)
        else:
            break
    course_rating = ustreview.get_course_rating(overall_soup)
    click.echo((""
                "Rating of {course}:"
                "Content:\t{0}"
                "Teaching:\t{1}"
                "Grading:\t{2}"
                "Workload:\t{3}"
                "").format(*course_rating, course=course))
    click.echo('Found reviews of the following instructors:')
    instructors = ustreview.get_instructor_list(overall_soup)
    for i, name in enumerate(instructors):
        click.echo('{0:<2}: {1}'.format(i, name))


    instructor_no = click.prompt('Enter a instructor\'s No. Enter \'back\' to go back.').lower()
    while instructor_no != 'back':
        while True:
            try:
                instructor_no = int(instructor_no)
                selected_instructor = instructors[instructor_no]
            except ValueError:
                click.echo('This is not a number.')
            except IndexError:
                click.echo('Invalid number.')
            else:
                break
            instructor_no = click.prompt('Enter a instructor\'s No. Enter \'back\' to go back.')

        instructor_soup = ustreview.request_instructor_page_soup(selected_instructor)
        ratings = ustreview.get_instructor_review(instructor_soup)
        click.echo((""
                    "Average rating of {instructor}:"
                    "Content:\t{0[0]} ({1[0]})"
                    "Teaching:\t{0[1]} ({1[1]})"
                    "Grading:\t{0[2]} ({1[2]})"
                    "Workload:\t{0[3]} ({1[3]})"
                    "Variance of the ratings (the smaller the better):"
                    "Content:\t{2[0]}"
                    "Teaching:\t{2[1]}"
                    "Grading:\t{2[2]}"
                    "Workload:\t{2[3]}"
                    "").format(*ratings, instructor=selected_instructor))
        instructor_no = click.prompt('Enter a instructor\'s No. Enter \'back\' to go back.')
