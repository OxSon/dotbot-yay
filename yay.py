import subprocess
import time
from collections import OrderedDict
from enum import Enum

import dotbot


class PkgStatus(Enum):
    # These names will be displayed
    UP_TO_DATE = "Up to date"
    INSTALLED = "Installed"
    UPDATED = "Updated"
    NOT_FOUND = "Not Found"
    PACMAN_ERROR = "Pacman error, make sure pacman dbs are synced by running pacman -Sy"
    ERROR = "Error"
    NOT_SURE = "Could not determine"


class Yay(dotbot.Plugin):
    _directive = "yay"

    def __init__(self, context):
        super(Yay, self).__init__(self)
        self._context = context
        self._strings = OrderedDict()

        # Names to search the query string for
        self._strings[PkgStatus.ERROR] = "aborting"
        self._strings[
            PkgStatus.PACMAN_ERROR
        ] = "Errors occurred, no packages were upgraded"
        self._strings[PkgStatus.NOT_FOUND] = "Could not find all required packages"
        self._strings[PkgStatus.UPDATED] = "Net Upgrade Size:"
        self._strings[PkgStatus.INSTALLED] = "Total Installed Size:"
        self._strings[PkgStatus.UP_TO_DATE] = "is up to date -- skipping"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError(f"Yay cannot handle directive {directive}")
        return self._process(data)

    def _process(self, packages):
        defaults = self._context.defaults().get("yay", {})
        results = {}
        successful = [PkgStatus.UP_TO_DATE, PkgStatus.UPDATED, PkgStatus.INSTALLED]

        for pkg in packages:
            if isinstance(pkg, dict):
                self._log.error("Incorrect format")
            elif isinstance(pkg, list):
                # self._log.error('Incorrect format')
                pass
            else:
                pass
            result = self._install(pkg)
            results[result] = results.get(result, 0) + 1
            if result not in successful:
                self._log.error(f"Could not install package '{pkg}'")

        if all([result in successful for result in results.keys()]):
            self._log.info("\nAll packages installed successfully")
            success = True
        else:
            success = False

        for status, amount in results.items():
            log = self._log.info if status in successful else self._log.error
            log(f"{amount} {status.value}")

        return success

    def _install(self, pkg):
        # to have a unified string which we can query
        # we need to execute the command with LANG=en_US
        cmd = f"LANG=en_US yay --needed --noconfirm -S {pkg}"

        self._log.info(f'Installing "{pkg}". Please wait...')

        # needed to avoid conflicts due to locking
        time.sleep(1)

        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        assert proc.stdout is not None
        out = proc.stdout.read()
        proc.stdout.close()

        self._log.debug(out.decode("utf-8"))

        for item in self._strings.keys():
            if out.decode("utf-8").find(self._strings[item]) >= 0:
                return item

        self._log.warning(f"Could not determine what happened with package {pkg}")
        return PkgStatus.NOT_SURE
