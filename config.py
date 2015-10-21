import os
### todo program configuration
# Defaults are shown between description and configuration line
# See todo --help and README.md for more details

# Example task format:
#    ✔ @due(10-31) get holloween costume @spooky
#    ☐ @due(12-25) get christmas gift @hohoho

# Prefix for tasks
upcoming = '☐'
completed = '✔'

# The .todo file to open (~/tasks.todo)
# (-f --file) [Default: os.path.join(os.environ['HOME'], 'tasks.todo')]
todo_file = os.path.join(os.environ['HOME'], 'tasks.todo')

# Number of days to due date until todo considers an unfinished task urgent
# [Default = Assignment:1, Quiz:2, Exam:3]
assignment_urgency = 2
quiz_urgency = 3
exam_urgency = 5

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
