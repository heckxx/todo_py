import os
### todo program configuration
# Defaults are shown between description and configuration line
# See todo --help and README.md for more details

# The .todo file to open (~/tasks.todo)
# (-f --file) [Default: os.path.join(os.environ['HOME'], 'tasks.todo')]
todo_file = os.path.join(os.environ['HOME'], 'tasks.todo')

# Example task format:
#   [prefix] [tagsymbol][type]([date]) [task] [optional tags]
#    ✔ #due(10-31) get holloween costume #spooky
#    ☐ #due(12-25) get christmas gift #hohoho

# Prefix for tasks
format_upcoming = '☐'
format_completed = '✔'
format_tagsymbol = '#'

# Number of days an unfinished task will be in the past for todo
# to consider it to be due next year
# [Default = 180]
days_max = 180

# Task types and days to due date until todo considers an unfinished task urgent
# [Default = Assignment:2, Quiz:3, Exam:5, Project:5, Misc/Untyped:-1]
task_type = {'assignment': 2,
             'quiz': 3,
             'exam': 5,
             'project': 5,
             'misc': -1}

# Number of days of future unfinished tasks prompt will show
# (-p --prompt) [Default: 1]
prompt_days = 2;

# The amount of days todo shows
# (-d --days --weeks --months) [Default: 1 week]
days = 7;

# The level of verbosity (0-3)
# (-v --verbosity --quiet) [Default: 1]
# verbosity = ['quiet','default','extrainfo','debug']
verbosity = 1;

# Whether to show tasks in minimal, one line mode
# (--full-view --minimal-view) [Default = False]
minimal_view = True

# Whether to show dates in days until (+1, +2, etc)
# (--delta-mode) [Default = False]
delta_mode = True

# Whether to show certain tasks
# (-a --all) [Default: False]
# (--archived) [Default: False]
# (--completed) [Default: True]
# (--undated) [Default: True]
show_archive = False;
show_completed = False;
show_undated = False;
