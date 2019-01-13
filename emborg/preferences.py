# Avendesora Password Generator Settings
#
# Copyright (C) 2018 Kenneth S. Kundert

# License {{{1
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# Imports {{{1
from appdirs import user_config_dir, user_data_dir
from textwrap import dedent

# Preferences {{{1
PROGRAM_NAME = 'emborg'
DEFAULT_COMMAND = 'create'
ENCODING = 'utf-8'
INDENT = '    '

CONFIG_DIR = user_config_dir(PROGRAM_NAME)

SETTINGS_FILE = 'settings'
LOG_FILE = '{config_name}.log'
PREV_LOG_FILE = '{config_name}.log.prev'
LOCK_FILE = '{config_name}.lock'
DATE_FILE = '{config_name}.lastbackup'

CONFIGS_SETTING = 'configurations'
DEFAULT_CONFIG_SETTING = 'default_configuration'
INCLUDE_SETTING = 'include'

EMBORG_SETTINGS = dict(
    archive = 'template Borg should use when creating archive names',
    avendesora_account = 'account name that holds passphrase for encryption key in Avendesora',
    check_after_create = 'run check as the last step of an archive creation',
    config_name = 'name of active configuration (set by program)',
    configurations = 'available emborg configurations',
    default_configuration = 'default emborg configuration',
    encryption = 'encryption method (see borg documentation)',
    excludes = 'list of glob strings of files or directories to skip',
    must_exist = 'if set, each of these files or directorys must exist or create will quit with an error',
    needs_ssh_agent = 'if set, emborg will complain if ssh_agent is not available',
    notifier = 'notification program',
    notify = 'email address to notify when things go wrong',
    passphrase = 'passphrase for encryption key (if specified, Avendesora is not used)',
    prune_after_create = 'run prune as the last step of an archive creation',
    repository = 'path to remote directory that contains repository',
    run_after_backup = 'command to run after archive has been created',
    run_before_backup = 'command to run before archive is to be created',
    src_dirs = 'the directories to archive',
)
    # Any setting found in the users settings files that is not found in
    # EMBORG_SETTINGS or BORG_SETTINGS is highlighted as a unknown setting by
    # the settings command.

BORG_SETTINGS = dict(
    append_only = dict(
        cmds = 'init',
        desc = 'create an append-only mode repository'
    ),
    compression = dict(
        cmds = 'create',
        arg = 'COMPRESSION',
        desc = 'compression algorithm'
    ),
    exclude_caches = dict(
        cmds = 'create',
        desc = 'exclude directories that contain a CACHEDIR.TAG file'
    ),
    exclude_if_present = dict(
        cmds = 'create',
        arg = 'NAME',
        desc = 'exclude directories that are tagged by containing a filesystem object with the given NAME'
    ),
    lock_wait = dict(
        cmds = 'all',
        arg = 'SECONDS',
        desc = 'wait at most SECONDS for acquiring a repository/cache lock (default: 1)'
    ),
    keep_within = dict(
        cmds = 'prune',
        arg = 'INTERVAL',
        desc = 'keep all archives within this time interval'
    ),
    keep_last = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of the most recent archives to keep'
    ),
    keep_minutely = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of minutely archives to keep'
    ),
    keep_hourly = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of hourly archives to keep'
    ),
    keep_daily = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of daily archives to keep'
    ),
    keep_weekly = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of weekly archives to keep'
    ),
    keep_monthly = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of monthly archives to keep'
    ),
    keep_yearly = dict(
        cmds = 'prune',
        arg = 'NUM',
        desc = 'number of yearly archives to keep'
    ),
    one_file_system = dict(
        cmds = 'create',
        desc = 'stay in the same file system and do not store mount points of other file systems'
    ),
    remote_path = dict(
        cmds = 'all',
        arg = 'CMD',
        desc = 'name of borg executable on remote platform',
    ),
    remote_ratelimit = dict(
        cmds = 'all',
        arg = 'RATE',
        desc = 'set remote network upload rate limit in kiB/s (deefault: 0=unlimited)'
    ),
    umask = dict(
        cmds = 'all',
        arg = 'M',
        desc = 'set umask to M (local and remote, default: 0077)'
    ),
)

# convert args to lists
for opt, attrs in BORG_SETTINGS.items():
    attrs['cmds'] = attrs['cmds'].split()

# utility function that converts setting names to borg option names
def convert_name_to_option(name):
    return '--' + name.replace('_', '-')

INITIAL_SETTINGS_FILE_CONTENTS = dedent("""
    # These settings are common to all configurations

    # configurations
    configurations = '<<list your configurations here>>'
    default_configuration = '<<default-config>>'

    # passcode
    # specify either passphrase or avendesora_account
    passphrase = '<<passcode>>'              # passphrase for encryption key
    avendesora_account = '<<account-name>>'  # avendesora account holding encryption key
    encryption = '<<encryption>>'            # borg encryption method
        # Common choices are 'repokey' and 'keyfile'.
        # With 'repokey' the encryption key is copied into repository, use this
        # only if the remote repository is owned by you and is secure.
        # With 'keyfile' the encryption key is only stored locally. Be sure to
        # export it and save a copy in a safe place, otherwise you may not be
        # able to access your backups if you lose your disk.

    # basic settings
    # specify notify if batch and notifier if interactive
    notify = "<<your-email-address>>"        # who to notify when things go wrong
    notifier = 'notify-send -u normal {prog_name} "{msg}"'
                                             # interactive notifier program
    needs_ssh_agent = True
    remote_ratelimit = 2000                  # bandwidth limit in kbps

    # repository settings
    compression = 'lz4'
    repository = '<<host>>:<<path>>/{host_name}-{user_name}-{config_name}'
    archive = '{host_name}-{{now}}'
        # These may contain {<name>} where name is any of host_name, user_name,
        # prog_name config_name, or any of the user specified settings.
        # Double up the braces to specify parameters that should be interpreted
        # by borg.

    # filter settings
    exclude_if_present = '.nobackup'
    one_file_system = True
    exclude_caches = True

    # prune settings
    keep_within = 1d                         # keep all archives created in interval
    keep_hourly = 24                         # number of hourly archives to keep
    keep_daily = 7                           # number of daily archives to keep
    keep_weekly = 4                          # number of weekly archives to keep
    keep_monthly = 12                        # number of monthly archives to keep
    keep_yearly = 1                          # number of yearly archives to keep
""").lstrip()

INITIAL_ROOT_CONFIG_FILE_CONTENTS = dedent("""
    # Settings for root configuration
    src_dirs = '/'.split()   # absolute path to directory to be backed up
    excludes = '''
        /dev
        /home/*/.cache
        /lost+found
        /mnt
        /proc
        /root/.cache
        /run
        /sys
        /tmp
        /var/cache
        /var/lock
        /var/log
        /var/run
        /var/spool
        /var/tmp
    '''.split()              # list of files or directories to skip
""").lstrip()

INITIAL_HOME_CONFIG_FILE_CONTENTS = dedent("""
    src_dirs = '~'.split()   # absolute path to directory to be backed up
    excludes = '''
        ~/**/__pycache__
        ~/**/*.pyc
        ~/**/.*.swp
        ~/**/.*.swo
    '''.split()
""").lstrip()
