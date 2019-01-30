#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Esrille Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

tr = str.maketrans('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
                   'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
                   '０１２３４５６７８９：；',
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   'abcdefghijklmnopqrstuvwxyz'
                   '0123456789:;',
                   '\n')


class Emitter:
    indent = 0
    mode = 0
    subject = ''
    nl_count = 0

    def adjust(self, n):
        self.indent += n

    def reset(self):
        self.indent = 0
        self.mode = 0
        self.subject = ''

    def reset_mode(self):
        self.mode = 0

    def set(self, line):
        sp = 0
        while line and line[0] == '　':
            sp += 2
            line = line[1:]
        self.indent = len(line)
        line = line.lstrip()
        self.indent -= len(line)
        self.indent += sp
        if self.subject:
            self.indent += 4
        if self.mode == 2:
            self.indent += 4

    def emit_subject(self, subject):
        assert subject != "", 'internal error: empty subject'
        if self.subject:
            self.indent -= 4
        if self.mode == 2:
            self.indent -= 4
        self.subject = subject
        self.nl(2)
        self.mode = 0
        self.emit("class ", subject, ":")
        self.mode = 1

    def raw(self, *args):
        self.nl_count = 0
        print(*args, sep='', end='')

    def nl(self, n=1):
        if self.nl_count < n:
            n -= self.nl_count
            print('\n' * n, end='')
            self.nl_count += n

    def emit(self, *args):
        self.nl_count = 0
        if self.mode == 1:
            print('\n', ' ' * self.indent, "def default(self):", sep='')
            self.mode = 2
            self.indent += 4
        print(' ' * self.indent, *args, sep='')


emitter = Emitter()


class Dictionary:

    def __init__(self):
        self.dict = {}
        self.methods = set()
        self.properties = set()
        self.actors = set()

    def add_subject(self, name):
        self.dict[name] = list()

    def add_method(self, method):
        self.methods.add(method)

    def add_actor(self, name):
        self.actors.add(name)

    # an actor has the default method.
    def is_actor(self, name):
        return name in self.actors

    def add(self, name, method):
        self.dict[name].append(method)
        self.methods.add(method)

    def has(self, subject, method):
        if subject not in self.dict:
            return False
        if method in self.dict[subject]:
            return True
        return False

    # [主語]がV
    # [目的語]をV
    # [目的語]を[補語]にV
    # N１がN２です。
    def lookup_method(self, s, particle='が'):
        index = -1
        while True:
            index = s.find(particle, index + 1)
            if index == -1:
                break
            method = s[index + 1:]
            if method in self.methods:
                return s[:index], method
        return None

    def lookup_class(self, s, particle='は'):
        if s in self.dict:
            return s
        index = len(s)
        while True:
            index = s.rfind(particle, 0, index)
            if index == -1:
                break
            name = s[:index]
            if name in self.dict:
                return name
        return None

    # [N1]の[N2]
    def property_form(self, subject, s):
        if subject and s.startswith(subject + 'の'):
            property = s[len(subject) + 1:]
            self.properties.add(property)
            return "self." + property
        index = -1
        while True:
            index = s.find('の', index + 1)
            if index == -1:
                break
            property = s[index + 1:]
            if property in self.properties:
                return self.property_form(subject, s[:index]) + '.' + property
        return s

    def include(self, name):
        with open(name + '.py', 'r') as file:
            for line in file:
                if line.startswith('#!'):
                    continue
                if line.startswith('# -*- coding:'):
                    continue
                emitter.raw(line)
                line = line.translate(tr).strip()
                if not line.startswith('#'):
                    continue
                line = line[1:].strip()
                if line.endswith("、とは、"):
                    line = line[:-4].strip()
                    self.add_method(line)

    def dump(self):
        print("主体一覧: ", ' '.join(self.dict), sep='')
        print("述語一覧: ", ' '.join(self.methods), sep='')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(0)

    emitter.raw('#!/usr/bin/python3\n')
    emitter.raw('# -*- coding: utf-8 -*-\n')

    dictionary = Dictionary()

    # Populate the dictionary
    subject = ""
    with open(sys.argv[1], 'r') as file:
        for line in file:
            line = line.translate(tr).strip()
            if line.startswith("ライブラリ:"):
                line = line[6:].strip()
                names = line.split('、')
                for name in names:
                    dictionary.include(name)
            elif line.startswith("主体:"):
                subject = line[3:].strip()
                dictionary.add_subject(subject)
            elif line.endswith("、とは、"):
                line = line[:-4].strip()
                dictionary.add(subject, line)
            else:
                pass

    actors = list()

    # Translate the program
    with open(sys.argv[1], 'r') as file:
        subject = ''
        let_mode = False
        for line in file:
            if line.startswith("ーー"):
                continue
            line = line.translate(tr)
            if line.startswith("ライブラリ:"):
                continue
            emitter.set(line)
            line = line.strip()

            if emitter.mode == 2:
                dictionary.add_actor(subject)

            # Construction lists
            if let_mode:
                if line == "をつかいます。":
                    let_mode = False
                    emitter.nl()
                    continue
                emitter.adjust(-4)
                name = dictionary.lookup_class(line)
                if name == line:
                    emitter.emit(name, " = ", name, "()")
                    if dictionary.is_actor(name):
                        actors.append(name)
                else:
                    line = line[len(name) + 1:].strip('、')
                    names = line.split('、')
                    for i in names:
                        emitter.emit(i, " = ", name, "()")
                        if dictionary.is_actor(name):
                            actors.append(i)
                continue

            # Statements
            if line.startswith("主体:"):
                subject = line[3:].strip()
                emitter.emit_subject(subject)
            elif line == "はじめに:":
                subject = ''
                emitter.reset()
                emitter.nl(2)
            elif line == "ここでは、":
                let_mode = True
            elif line.endswith("ましたら、"):
                line = line[:-5].strip()
                found = dictionary.lookup_method(line + "ます", 'が')
                if found:
                    emitter.emit("if ", found[0], ".", found[1], "():")
            elif line == "そうでなければ、":
                emitter.emit("else:")
            elif line.endswith("、とは、"):
                line = line[:-4].strip()
                emitter.nl()
                emitter.reset_mode()
                emitter.emit("def ", line, "(self):")
            elif line.endswith("ます。"):
                line = line[:-1].strip()
                found = dictionary.lookup_method(line, 'を')
                if found:
                    target = dictionary.property_form(subject, found[0])
                    emitter.emit(target, ".", found[1], "()")
                elif line.endswith("にします"):
                    # [目的語]を[補語]にV
                    line = line[:-4].strip()
                    complement = line.find('を')
                    if 0 <= complement:
                        target = dictionary.property_form(subject, line[:complement].strip())
                        emitter.emit(target, " = ", line[complement + 1:].strip())
                else:
                    pass
            elif line.endswith("です。"):
                line = line[:-1].strip()
                found = dictionary.lookup_method(line, 'が')
                if found:
                    target = dictionary.property_form(subject, found[0])
                    emitter.emit("return ", target, ".", found[1], "()")
            elif line:
                emitter.emit(line)
            else:
                emitter.nl()

    emitter.reset()
    if actors:
        emitter.nl()
        emitter.emit("while True:")
        emitter.adjust(4)
        for i in actors:
            emitter.emit(i, ".default()")

    sys.exit(0)
