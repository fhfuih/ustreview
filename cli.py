import atexit

import click

click.echo("""UST Review
A tool to look up HKUST instructors' ratings based on ust.space
Please wait when it's loading up...""")

import spider
#from . import spider

atexit.register(spider.quit)

def formatted_course_info(name, ratings):
    return '\n'.join(("",
                "Rating of {course}:",
                "Content:\t{0}",
                "Teaching:\t{1}",
                "Grading:\t{2}",
                "Workload:\t{3}",
                "")).format(*ratings, course=name)

def formatted_instructor_info(name, ratings):
    return '\n'.join(("",
                "Average rating of {instructor}:",
                "Content:\t{0[0]} ({1[0]})",
                "Teaching:\t{0[1]} ({1[1]})",
                "Grading:\t{0[2]} ({1[2]})",
                "Workload:\t{0[3]} ({1[3]})",
                "Variance of the ratings (the smaller the better):",
                "Content:\t{2[0]}",
                "Teaching:\t{2[1]}",
                "Grading:\t{2[2]}",
                "Workload:\t{2[3]}",
                "")).format(*ratings, instructor=name)

def formatted_limited_info(name, data):
    return '\n'.join(("",
                "Accessible rating of {course}:",
                "Instructor:\t{2}"
                "Content:\t{0[0]} ({1[0]})",
                "Teaching:\t{0[1]} ({1[1]})",
                "Grading:\t{0[2]} ({1[2]})",
                "Workload:\t{0[3]} ({1[3]})",
                "")).format(*data, course=name)

while True:
    click.clear()
    username = click.prompt("Enter your username")
    password = click.prompt("Enter your password\n(Your input won't show up on the screen)", hide_input=True)
    click.echo("\nLogging you in...\n")
    try:
        spider.login(username, password)
    except (ValueError, RuntimeError) as e:
        click.echo(e)
    else:
        break


while True:
    click.clear()
    while True:
        course = click.prompt("Enter a course code (Case insensitive)").upper()
        click.echo("\nAcquiring course page...\n")
        try:
            overall_soup, has_full_access = spider.request_review_page_soup(course)
        except ValueError as e:
            click.echo(e)
        else:
            break
    course_rating = spider.get_course_rating(overall_soup)
    click.echo(formatted_course_info(course, course_rating))

    if has_full_access:
        click.echo("Found reviews of the following instructors:")
        instructors = spider.get_instructor_list(overall_soup)
        for i, name in enumerate(instructors):
            click.echo("{0:<2}: {1}".format(i, name))


        instructor_no = click.prompt("Enter a instructor's No. Enter 'back' to go back.").lower()
        while instructor_no != "back":
            while True:
                try:
                    instructor_no = int(instructor_no)
                    selected_instructor = instructors[instructor_no]
                except ValueError:
                    click.echo("This is not a number.")
                except IndexError:
                    click.echo("Invalid number.")
                else:
                    break
                instructor_no = click.prompt("Enter a instructor's No. Enter 'back' to go back.")

            instructor_soup = spider.request_instructor_page_soup(selected_instructor)
            ratings_data = spider.get_instructor_review(instructor_soup)
            click.echo(formatted_instructor_info(selected_instructor, ratings_data))
            instructor_no = click.prompt("Enter a instructor's No. Enter 'back' to go back.")
    else:
        click.echo('You can only read the latest review of this course.')
        ratings_data = spider.get_limited_review(overall_soup)
