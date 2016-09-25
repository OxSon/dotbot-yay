import os, subprocess, dotbot, time
from enum import Enum

class PkgStatus(Enum):
    # These names will be displayed
    UP_TO_DATE = 'Up to date'
    INSTALLED = 'Installed'
    NOT_FOUND = 'Not Found'
    ERROR = "Build Error"
    NOT_SURE = 'Could not determine'

class Yaourt(dotbot.Plugin):
    _directive = 'yaourt'

    def __init__(self, context):
        super(Yaourt, self).__init__(self)
        self._context = context
        self._strings = {}

        # Names to search the query string for
        self._strings[PkgStatus.UP_TO_DATE] = "there is nothing to do"
        self._strings[PkgStatus.INSTALLED] = "Optional dependencies for"
        self._strings[PkgStatus.NOT_FOUND] = "target not found"
        self._strings[PkgStatus.ERROR] = "==> ERROR:"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Yaourt cannot handle directive %s' %
                directive)
        return self._process(data)

    def _process(self, packages):
        defaults = self._context.defaults().get('yaourt', {})
        results = {}
        successful = [PkgStatus.UP_TO_DATE, PkgStatus.INSTALLED]

        for pkg in packages:
            if isinstance(pkg, dict):
                self._log.error('Incorrect format')
            elif isinstance(pkg, list):
                # self._log.error('Incorrect format')
                pass
            else:
                pass
            result = self._install(pkg)
            results[result] = results.get(result, 0) + 1
            if result not in successful:
                self._log.error("Could not install package '{}'".format(pkg))


        if all([result in successful for result in results.keys()]):
            self._log.info('\nAll packages installed successfully')
            success = True
        else:
            success = False

        for status, amount in results.items():
            log = self._log.info if status in successful else self._log.error
            log('{} {}'.format(amount, status.value))

        return success

    def _install(self, pkg):
        # to have a unified string which we can query
        # we need to execute the command with LANG=en_US.UTF-8
        cmd = 'LANG=en_US.UTF-8 yaourt --needed --noconfirm -S {}'.format(pkg)

        self._log.info("Installing \"{}\". Please wait...".format(pkg))
        
        # needed to avoid conflicts due to locking
        time.sleep(1)

        proc = subprocess.Popen(cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.read()
        proc.stdout.close()

        for item in self._strings.keys():
            if out.decode("utf-8").find(self._strings[item]) >= 0:
                return item

        self._log.warn("Could not determine what happened with package {}".format(pkg))
        return PkgStatus.NOT_SURE
