import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peer_reply_project.settings')
from peer_reply.models import Course, School, Level, University
import django
django.setup()




def populate():
    python_university = add_university('University of Glasgow', 'Glasgow')

    # Read Schools, levels and courses from file

    txt_file = open('schools_and_courses.txt', 'r')
    python_school = 0;
    python_level = 0;
    count = 0
    school_count = 0
    # loop through each line in schools and courses file
    for line in txt_file:
        line = line.strip()
        # if line starts with ';' then it is a school name so create new school
        if line.startswith(';'):
            python_school = add_school(line[1:], python_university)
            school_count = school_count + 1
        elif line.startswith('Level') and school_count <= 15:
            count = 0
            python_level = add_level(line, python_school)
        elif count < 12 and school_count <= 15:
            add_course(line, python_level)
            count = count + 1

    txt_file.close()


def add_university(name, location):
    u = University.objects.get_or_create(name=name, location=location)[0]
    return u


def add_school(name, university):
    s = School.objects.get_or_create(name=name, university=university)[0]
    return s

#
# def add_school_level(school, level):
#     sl = School_Level.objects.get_or_create(school=school, level=level)[0]
#     return sl


def add_level(name, school):
    l = Level.objects.get_or_create(name=name, school=school)[0]
    return l


def add_course(name, level):
    c = Course.objects.get_or_create(name=name, level=level)[0]
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()

