import os, subprocess, dotbot
from enum import Enum

class PkgStatus(Enum):
    UP_TO_DATE = 'Already up to date'
    INSTALLED = 'Newly installed'

    NOT_FOUND = 'Not found'
    NOT_SURE = 'Could not determine'

class Yaourt(dotbot.Plugin):
    _directive = 'apt-get'

    def __init__(self, context):
        super(Yaourt, self).__init__(self)
        self._context = context
        self._strings = {}
        self._strings[PkgStatus.UP_TO_DATE] = "is already the newest"
        self._strings[PkgStatus.INSTALLED] = ""
        self._strings[PkgStatus.NOT_FOUND] = "Unable to locate package"

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

        # apt-get update
        self._update_index()

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
            self._log.info('All packages installed successfully')
            success = True
        else:
            success = False

        for status, amount in results.items():
            log = self._log.info if status in successful else self._log.error
            log('{} {}'.format(amount ,status.value))

        return success

    def _update_index(self):
        cmd = 'yaourt --noconfirm --aur -Syu'
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        out = process.stdout.read()
        process.stdout.close()

    def _install(self, pkg):
        cmd = 'yaourt --noconfirm -S {}'.format(pkg)
        process = subprocess.Popen(cmd, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = process.stdout.read()
        process.stdout.close()

        for item in self._strings.keys():
            if out.find(self._strings[item]) >= 0:
                return item

        self._log.warn("Could not determine what happened with package {}".format(pkg))
        return PkgStatus.NOT_SURE
