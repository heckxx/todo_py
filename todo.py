#!/usr/bin/env python

from enum import Enum
from termcolor import colored
import re, datetime, argparse, colorama
import config

VERSION = '0.101'
## Program starts here

class Task:
    class Type(Enum):
        Exam = 0
        #Ongoing = 1
        Assignment= 1
        Quiz = 2
        Misc = -1
    def __init__(self,task):
        self.task = task
        self.tags = []
    def set_status(self,done):
        if done == config.format_completed:
            self.done = True
        elif done == config.format_upcoming:
            self.done = False
        else:
            raise ValueError
    def set_type(self,itype):
        if itype == 'due': self.itype = Task.Type.Assignment
        elif itype == 'ongoing': self.itype = Task.Type.Ongoing
        elif itype == 'exam': self.itype = Task.Type.Exam
        elif itype == 'quiz': self.itype = Task.Type.Quiz
        else: self.itype = Task.Type.Misc
    def set_date(self,date):
        if date:
            self.date = date
        else: self.date = None
    def set_category(self,cat):
        if cat:
            self.category = cat.lstrip()
        else: self.category = 'Uncategorized'
    def append_tag(self,tag):
        if tag and tag not in ('date','ongoing','exam','quiz'):
            self.tags.append(tag)
    def __repr__(self):
        repr = ''
        if self.itype: repr += 'type: '+self.itype.name
        repr += '\ntask: '+self.task
        if self.category: repr += '\ncategory: '+self.category
        if self.date: repr += '\ndate: '+self.date.ctime()
        if self.tags: repr += '\ntags: '+str(self.tags)
        return '\n\n'+repr
    def print_info(self,verbosity,one_line):
        info = ''
        if not one_line:
            # full-line mode
            if not self.done:
                info += colored('Category: ','white') + colored(self.category,'white',attrs=['bold'])
            else:
                info += colored('X ','grey',attrs=['bold']) + colored('Category: '+self.category,'white',attrs=['dark'])
            info += '\n'+colored(self.itype.name.ljust(10) + ': ','magenta')
            today = datetime.date.today()
            if delta_mode and self.date:
                d = '%d' % (self.date - today).days
                if int(d) > 0: d = '+' + d
            elif self.date and self.date.year == today.year:
                d = self.date.strftime('%m-%d')
            elif self.date and self.date.year != today.year:
                d = self.date.strftime('%Y-%m-%d')
            else: d = 'Undated'
            # Task is urgent
            if self.done:
                info += colored(d,'magenta')
            elif self.itype == Task.Type.Assignment and self.date < today + datetime.timedelta(days=config.assignment_urgency) \
                    or self.itype == Task.Type.Quiz and self.date < today + datetime.timedelta(days=config.quiz_urgency) \
                    or self.itype == Task.Type.Exam and self.date < today + datetime.timedelta(days=config.exam_urgency) \
                    :
                        if self.date <= today:
                            info += colored(d,'red',attrs=['reverse','bold'])
                        else:
                            info += colored(d,'red',attrs=['bold'])
            else: info += colored(d,'magenta')
            info += ' - ' + self.task
            if verbosity >= 3 and self.tags: info += colored('\n'+'Tags: '.rjust(12),'blue') + colored(str(self.tags),'cyan')
        else:
            # one-line mode
            if not self.done:
                info += colored(self.category+": ",'white',attrs=['bold'])
            else:
                info += colored(self.category+": ",'white',attrs=['dark'])
            info += colored(self.itype.name + '(','magenta')
            today = datetime.date.today()
            if delta_mode and self.date:
                d = '%d' % (self.date - today).days
                if int(d) > 0: d = '+' + d
            elif self.date and self.date.year == today.year:
                d = self.date.strftime('%m-%d')
            elif self.date and self.date.year != today.year:
                d = self.date.strftime('%Y-%m-%d')
            else: d = 'n/a'
            # Task is urgent
            if self.done:
                info += colored(d,'magenta')
            elif self.itype == Task.Type.Assignment and self.date < today + datetime.timedelta(days=config.assignment_urgency) \
                    or self.itype == Task.Type.Quiz and self.date < today + datetime.timedelta(days=config.quiz_urgency) \
                    or self.itype == Task.Type.Exam and self.date < today + datetime.timedelta(days=config.exam_urgency) \
                :
                        if self.date <= today:
                            info += colored(d,'red',attrs=['reverse','bold'])
                        else:
                            info += colored(d,'red',attrs=['bold'])
            else: info += colored(d,'magenta')
            info += colored(') ','magenta') + self.task
            if self.done:
                info += colored(' X','grey',attrs=['bold'])
            if verbosity >= 3 and self.tags: info += colored(str(self.tags),'cyan')
        print(info)

def main():
    global delta_mode
    colorama.init()
    def log(string,loglevel=2,end='\n'):
        if loglevel <= verbosity:
            print(string,end=end)
    # take care of arguments
    parser = argparse.ArgumentParser(prog='todo')
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    days_group = parser.add_mutually_exclusive_group()
    days_group.add_argument('-d','--days', action='store', dest='days', default=config.days, metavar='N',
            help='show N days of tasks')
    days_group.add_argument('--weeks', action='store', dest='weeks', default=0, metavar='N',
            help='show N weeks of tasks')
    days_group.add_argument('--months', action='store', dest='months', default=0, metavar='N',
            help='show N months of tasks')
    days_group.add_argument('-p','--prompt', type=int, dest='prompt_days', metavar='D', default=-1, const=config.prompt_days, nargs='?',
            help='prompt mode, show tasks due in the next D days')
    parser.add_argument('-a','--all', action='store_true', dest='show_all', default=(config.show_completed and config.show_archive and config.show_undated),
            help='show all tasks, including completed/archived')
    parser.add_argument('--archived', action='store_true', dest='show_archive', default=config.show_archive,
            help='show archived tasks')
    parser.add_argument('--completed', action='store_true', dest='show_completed', default=config.show_completed,
            help='show completed tasks')
    parser.add_argument('--undated', action='store_true', dest='show_undated', default=config.show_undated,
            help='show undated tasks')
    view_group = parser.add_mutually_exclusive_group()
    view_group.add_argument('--full-view', action='store_false', dest='one_line', default=config.minimal_view,
            help='show tasks in full view')
    view_group.add_argument('--minimal-view', action='store_true', dest='one_line', default=config.minimal_view,
            help='show tasks in minimal view')
    date_group = parser.add_mutually_exclusive_group()
    date_group.add_argument('--date-mode', action='store_false', dest='delta_mode', default=config.delta_mode,
            help='show dates as absolute dates')
    date_group.add_argument('--delta-mode', action='store_true', dest='delta_mode', default=config.delta_mode,
            help='show dates as days until')
    parser.add_argument('-f','--file', default=config.todo_file, dest='todo_file', metavar='FILE',
            help='file to parse')
    verbose_group = parser.add_mutually_exclusive_group()
    verbose_group.add_argument('-v', '--verbosity', type=int, action='store', default=config.verbosity, metavar='N',
            help='change the verbosity (0-3)')
    verbose_group.add_argument('-q', '--quiet', action='store_const', const=0, dest='verbosity', default=config.verbosity,
            help='quiet mode, same as -v 0')
    args = parser.parse_args()
    verbosity = args.verbosity
    log('args: %r' % args, 3)
    if args.show_all:
        show_archive = True
        show_completed = True
        show_undated = True
    else:
        show_archive = args.show_archive
        show_completed = args.show_completed
        show_undated = args.show_undated
    one_line_tasks = args.one_line
    delta_mode = args.delta_mode
    todo_file = args.todo_file
    prompt_days = args.prompt_days
    prompt = (prompt_days!=-1)
    if args.days: delta = datetime.timedelta(days=int(args.days))
    if args.weeks: delta = datetime.timedelta(weeks=int(args.weeks))
    if args.months: delta = datetime.timedelta(weeks=int(args.months)*4)

    today = datetime.date.today()
    # program start
    tasks = []
    log('opening %r' % todo_file, 3)
    try:
        todo = open(todo_file)
    except FileNotFoundError:
        print('File \''+ todo_file + '\' not found.')
        return
    category = None
    for line in todo.readlines():
        r = re.search('Archive:', line)
        if r and not show_archive: break;
        r = re.search('([.]*):$', line)
        if r:
            log('Header %r found' % line[:r.start()],3)
            if not prompt: log(colored(line,attrs=['bold']),2,end='')
            category = line[:r.start()]
            continue
        r = re.search('(?P<status>[%(u)r%(c)r]) ([%(t)r](?P<type>due|exam|quiz)\((?P<month>([0-9]){1,2})-(?P<date>([0-9]){1,2})\) )?(?P<task>[\w,-./\+\(\) ]+)' % {'u':config.format_upcoming,'c':config.format_completed,'t':config.format_tagsymbol},line)
        if r:
            log(r.group('status')+'Task found: ' + r.group('task'),3)
            i = Task(r.group('task'))
            i.set_category(category)
            i.set_status(r.group('status'))
            i.set_type(r.group('type'))
            if r.group('date'):
                i.set_date(datetime.date(2015,int(r.group('month')),int(r.group('date'))))
            else:
                i.set_date(None)
            r = re.finditer('( %(t)r(?P<tag>[\w]+))*$'%{'t':config.format_tagsymbol},line)
            for t in r:
                i.append_tag(t.group(0).replace('@','').split())
            tasks.append(i)
            if not prompt: log('\r'+line,2,end='')
            continue
    tasks.sort(key=lambda t: t.date if (t and t.date)
            else datetime.date.max)
    log(tasks,3)
    # Prompt mode
    if prompt:
        due = []
        count = 0
        for t in tasks:
            if t.date and t.date < (today+datetime.timedelta(days=prompt_days)):
                if not t.done or show_completed:
                    due.append(t)
                    log('Found task due ' + str(t.date) + ': ' + t.task)
        print('['+str(len(due))+']')
        return
    # Normal mode
    else:
        log('Today is: %r' % today.isoformat(),1)
        for t in tasks:
            if (t.date and t.date < (today+delta)) or (show_undated and not t.date):
                if not t.done or show_completed:
                    t.print_info(3,one_line_tasks)

if __name__ == '__main__':
    main();
