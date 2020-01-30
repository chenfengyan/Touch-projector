#!/usr/bin/env python
# -*- coding:utf-8 -*-


class _const:
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value

const = _const()
const.MY_DEVICE_ID_1 = ''  # enter your device id catching by 'adb devices'
const.MY_DEVICE_ID_2 = ''
const.DEVICE_ID = const.MY_DEVICE_ID_1