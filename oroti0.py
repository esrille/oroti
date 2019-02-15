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

import re
import sys

tr = str.maketrans('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
                   'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
                   '０１２３４５６７８９：；！＋－＊／％＜＞＆｜＾～＝（）［］｛｝',
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   'abcdefghijklmnopqrstuvwxyz'
                   '0123456789:;!+-*/%<>&|^~=()[]{}',
                   '\n')


class Emitter:

    def __init__(self):
        self.indent = 0
        self.mode = 0
        self.subject = ''
        self.nl_count = 0
        self.function_target = ''
        self.function_name = ''
        self.function_indent = 0
        self.function_arguments = []
        self.function_params = {}
        self.strings = []
        self.count = 0

    def adjust(self, n):
        self.indent += n

    def reset(self):
        self.indent = 0
        self.mode = 0
        self.subject = ""

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

    def flush(self):
        if self.function_name and self.indent <= self.function_indent:
            buffer = self.function_target + "." + self.function_name + "("
            s = ''
            for arg in self.function_arguments:
                buffer += s + arg
                s = ", "
            for param, value in self.function_params.items():
                buffer += s + param + '=' + value
                s = ", "
            buffer += ')'
            buffer = self.unescape(buffer)
            print(buffer, end='')
            self.function_name = ''
            self.function_arguments = []
            self.function_params = {}
            return True
        return False

    def emit_subject(self, subject):
        if self.flush():
            print()
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
        buffer = ''.join(args)
        buffer = self.unescape(buffer)
        print(buffer, end='')

    def nl(self, n=1):
        if self.flush():
            print()
        if self.nl_count < n:
            n -= self.nl_count
            print('\n' * n, end='')
            self.nl_count += n

    def emit_indent(self):
        self.nl_count = 0
        if self.mode == 1:
            self.mode = 2
            print()
            self.emit_indent()
            print("def default(self):")
            self.indent += 4
        if self.flush():
            print()
        print(' ' * self.indent, end='')

    def emitnb(self, *args):
        self.emit_indent()
        buffer = ''.join(args)
        buffer = self.unescape(buffer)
        print(buffer, end='')

    def emit(self, *args):
        self.emitnb(*args)
        print()

    def emit_call(self, method):
        if self.flush():
            print()
        self.function_target = method[0]
        self.function_name = method[1]
        self.function_arguments = method[2]
        self.function_indent = self.indent

    def emit_argument(self, name, value):
        self.function_params[name] = value

    def escape(self, line):
        s = ''
        d = ''
        l = ''
        skip = False
        for c in line:
            if not d:
                i = "\'\"「『".find(c)
                if 0 <= i:
                    s = "\'\"\'\""[i]
                    l += '＄' + str(self.count) + '＄'
                    d = "\'\"」』"[i]
                    self.count += 1
                else:
                    l += c.translate(tr)
            elif skip:
                if c == '」' or c == '』':
                    s += c
                else:
                    s += '\\' + c
                skip = False
            elif c == '\\':
                skip = True
            elif c == d:
                i = "\'\"」』".find(c)
                s += "\'\"\'\""[i]
                self.strings.append(s)
                s = ''
                d = ''
            else:
                s += c
        return l

    def unescape(self, value):
        s = ''
        while value:
            pos = value.find('＄')
            if pos < 0:
                s += value
                value = ''
                break
            s += value[:pos]
            value = value[pos + 1:]
            pos = value.find('＄')
            assert 0 <= pos, 'internal error'
            count = value[:pos]
            s += self.strings[int(count)]
            value = value[pos + 1:]
        return s

    def function_mode(self):
        return self.function_name and self.function_indent < self.indent


class Dictionary:

    # {
    #       "メソッド名": ["method name", ['を', 'で'], [なになに]],
    #       "メソッド名": ["method name", ['が'], []],
    # }

    def __init__(self):
        self.brackets = re.compile(r'(\[.+\])+$')
        self.particles = set()
        self.classes = set()
        self.methods = {}
        self.properties = set()
        self.properties.add('ながさ')
        self.subject = ""

    def set_subject(self, name):
        self.subject = name
        self.classes.add(name)

    def add_method(self, name, method):
        # TODO: Check python methods first
        self.methods[name] = method
        for p in method[1]:
            self.particles.add(p)

    def split2(self, s, pp):
        result = []
        if not s:
            return result
        if not pp:
            result.append([s])
            return result
        for p in pp:
            qq = pp.copy()
            qq.remove(p)
            i = 0
            while True:
                pos = s.find(p, i)
                if pos < 1 or len(s) <= pos + len(p):
                    break
                rest = self.split2(s[pos+len(p):], qq)
                for r in rest:
                    t = [s[:pos], p]
                    t.extend(r)
                    result.append(t)
                i = pos + 1
        return result

    def lookup_method(self, s):
        method = ''
        count = 0
        separated = []
        particles = sorted(self.particles, key=lambda p: len(p), reverse=True)
        for p in particles:
            i = 0
            while True:
                i = s.find(p, i + 1)
                if i == -1:
                    break
                target = s[:i]
                m = s[i + len(p):]
                if m in self.methods:
                    pp = self.methods[m][1]
                else:
                    continue
                if p not in pp:
                    continue
                if len(m) < len(method):
                    continue

                pp = pp.copy()
                pp.remove(p)
                if not pp:
                    target = self.property_form(target)
                    if target == self.subject:
                        target = 'self'
                    if len(method) < len(m) or count == 0:
                        separated = [target, p]
                        method = m
                    continue

                result = self.split2(target, pp)
                if not result:
                    continue

                c = 0
                for candidate in result:
                    a = []
                    for term in candidate:
                        pair = self.expression2(term)
                        c += pair[1]
                        a.append(pair[0])
                    a.append(p)
                    if len(method) < len(m) or count <= c:
                        separated = a
                        method = m
        if not separated:
            return separated
        arguments = []
        for p in self.methods[method][1]:
            for i in range(1, len(separated), 2):
                if separated[i] == p:
                    arguments.append(separated[i - 1])
                    break
        if arguments[0] == self.subject:
            arguments[0] = 'self'

        v = []
        for i in arguments:
            v.extend(i.split('、'))
        return v[0], self.methods[method][0], v[1:]

    def lookup_class(self, s, particle='は'):
        if s in self.classes:
            return s
        pos = len(s)
        while True:
            pos = s.rfind(particle, 0, pos)
            if pos == -1:
                break
            name = s[:pos]
            if name in self.classes:
                return name
        return None

    # [N1]の[N2]の[N3]...
    def property_form2(self, s):
        count = 0
        pos = len(s)
        while True:
            pos = s.rfind('の', 0, pos)
            if pos == -1:
                break
            property = s[pos + 1:]
            suffix = ""
            bracket = property.find('[')
            if 0 <= bracket:
                suffix = dictionary.expression(property[bracket:])
                property = property[:bracket]
            if property in self.properties:
                pair = self.property_form2(s[:pos])
                count = pair[1] + 1
                if not suffix and property == 'ながさ':
                    return "len(" + pair[0] + ')', count
                else:
                    return pair[0] + '.' + property + suffix, count
            elif s[:pos] == self.subject:
                self.properties.add(property)
                return "self." + property + suffix, count
        if s == self.subject:
            s = "self"
        return s, count

    def property_form(self, s):
        return self.property_form2(s)[0]

    def expression2(self, s):
        count = 0
        delim = " ,+-*/%<>&|^~!()[:]"
        for pos in range(len(s)):
            if s[pos] not in delim:
                break
        if s[pos] in delim:
            return s, count
        t = s[:pos]
        s = s[pos:]
        for pos in range(len(s)):
            if s[pos] in delim:
                term = s[:pos]
                l = self.property_form2(term)
                r = self.expression2(s[pos:])
                s = t + l[0] + r[0]
                count += l[1] + r[1]
                return s, count
        pair = self.property_form2(s)
        return t + pair[0], count + pair[1]

    def expression(self, s):
        return self.expression2(s)[0]

    def split(self, str, sep):
        count = 0
        left = str
        right = ''
        pos = 0
        while True:
            pos = str.find(sep, pos)
            if pos == -1:
                return left, right
            cnt = 1
            pair = self.expression2(str[:pos])
            l = pair[0]
            cnt += pair[1]
            pair = self.expression2(str[pos + len(sep):])
            r = pair[0]
            cnt += pair[1]
            if count < cnt:
                count = cnt
                left = l
                right = r
            pos += 1
        return left, right

    def parse_def(self, line):
        assert line.endswith("、とは。"), 'parse_def'
        line = line[:-4].strip()
        assert self.subject == line[:len(self.subject)], 'syntax error: invalid method definition'
        line = line[len(self.subject):].strip()
        pos = line.rfind('　')
        assert 0 < pos, 'syntax error: invalid method definition'
        method = line[pos+1:]
        line = line[:pos].strip()
        particles = []
        arguments = []
        while line:
            pos = line.find('(')
            if pos < 0:
                particles.append(line)
                line = ''
            else:
                particle = line[:pos].strip()
                particles.append(particle)
                line = line[pos+1:].strip()
                pos = line.find(')')
                assert 0 < pos, 'syntax error: invalid method definition'
                argument = line[:pos].strip()
                arguments.append(argument)
                line = line[pos+1:].strip()
        if method == "はじめにととのえます":
            method = "__init__"
        return method, particles, arguments

    def dump(self):
        print("主体一覧: ", ' '.join(self.classes), sep='')
        print("助詞一覧: ", ' '.join(sorted(self.particles, key=lambda p: len(p), reverse=True)), sep='')
        print("述語一覧:")
        for method, p in self.methods.items():
            print(method, p)


python_methods = {
    "あります": ["__contains__", ['に', 'が'], ['item']],
    "くわえます": ["add", ['に', 'を'], ['elem']],
    "つけくわえます": ["append", ['に', 'を'], ['x']],
    "コピーします": ["copy", ['を'], []],
    "おわります": ["endswith", ['が', 'で'], ['suffix']],
    "まぜます": ["extend", ['に', 'を'], ['iterable']],
    "みつけます": ["find", ['から', 'を'], ['sub']],
    "項目でみます": ["items", ['を'], []],
    "つなげます": ["join", ['で', 'を'], ['x']],
    "とりのぞきます": ["remove", ['から', 'を'], ['item']],
    "うしろからみつけます": ["rfind", ['から', 'を'], ['sub']],
    "きりわけます": ["split", ['を', 'で'], ['sep']],
    "はじまります": ["startswith", ['が', 'で'], ['prefix']],
    "余白をとります": ["strip", ['から'], []],
    "いれかえます": ["translate", ['を', 'で'], ['table']],
    "値でみます": ["values", ['を'], []],
}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(0)

    emitter = Emitter()
    emitter.raw('#!/usr/bin/python3\n')
    emitter.raw('# -*- coding: utf-8 -*-\n')
    emitter.raw('\n')
    emitter.raw('真 = True\n')
    emitter.raw('偽 = False\n')

    dictionary = Dictionary()
    for name, method in python_methods.items():
        dictionary.add_method(name, method)

    # Populate the dictionary
    with open(sys.argv[1], 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1
            line = line.translate(tr).strip()
            if line.startswith("ライブラリ:"):
                line = line[6:].strip()
                names = line.split('、')
                for name in names:
                    dictionary.set_subject("")
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
                            if line.endswith("、とは。"):
                                method = dictionary.parse_def(line)
                                dictionary.add_method(method[0], method)
                            elif line.startswith("主体:"):
                                dictionary.set_subject(line[3:].strip())
                            elif line.startswith("属性:"):
                                line = line[3:].strip()
                                dictionary.properties.add(line)
            elif line.startswith("主体:"):
                dictionary.set_subject(line[3:].strip())
            elif line.endswith("、とは。"):
                method = dictionary.parse_def(line)
                assert len(method[1]) == len(set(method[1])), lineno
                dictionary.add_method(method[0], method)

    actor_subjects = set()
    actors = []

    # Translate the program
    with open(sys.argv[1], 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            if line.startswith("－－"):
                continue
            line = emitter.escape(line)
            if line.startswith("ライブラリ:"):
                continue
            emitter.set(line)
            line = line.strip()

            if emitter.mode == 2:
                actor_subjects.add(dictionary.subject)

            # Assertion
            if line.startswith("チェック:"):
                line = line[5:].strip()
                assertion = True
            else:
                assertion = False

            # Statements
            if line.startswith("主体:"):
                dictionary.set_subject(line[3:].strip())
                emitter.emit_subject(dictionary.subject)
            elif line == "はじめに:":
                dictionary.set_subject('')
                emitter.reset()
                emitter.nl(2)
            elif line.endswith("ら、"):
                # if statement
                emitter.emit_indent()
                if line.startswith("あるいは、"):
                    emitter.raw("elif")
                    line = line[5:].strip()
                else:
                    emitter.raw("if")
                line = line[:-1].strip()
                cond = line.split('、')
                for p in cond:
                    found = []
                    p = p.strip()
                    if p == 'または':
                        emitter.raw(" or")
                    elif p == 'そして':
                        emitter.raw(" and")
                    elif p.endswith("ましたら"):
                        p = p[:-4] + "ます"
                        found = dictionary.lookup_method(p)
                    elif p.endswith("ませんでしたら"):
                        p = p[:-7] + "ます"
                        found = dictionary.lookup_method(p)
                        emitter.raw(" not")
                    elif p.endswith("でしたら"):
                        p = p[:-4].strip()
                        emitter.raw(" ", dictionary.expression(p))
                    elif p.endswith("でないなら"):
                        p = p[:-5].strip()
                        emitter.raw(" not ", dictionary.expression(p))
                    if found:
                        emitter.raw(" ")
                        emitter.emit_call(found)
                        emitter.flush()
                emitter.raw(":\n")
            elif line == "そうでなければ、":
                emitter.emit("else:")
            elif line == "つぎへ。":
                emitter.emit("continue")
            elif line.endswith("、とは。"):
                method = dictionary.parse_def(line)
                emitter.nl()
                emitter.reset_mode()
                emitter.emitnb("def ", method[0], "(self")
                if method[2]:
                    emitter.raw(', ', ", ".join(method[2]))
                emitter.raw("):\n")
            elif line.endswith("ます。"):
                line = line[:-1].strip()
                found = dictionary.lookup_method(line)
                if found:
                    emitter.emit_indent()
                    if assertion:
                        emitter.raw("assert ")
                    emitter.emit_call(found)
                elif line == "うちきります":
                    emitter.emit("break")
                elif line.endswith("をかえします"):
                    line = line[:-6].strip()
                    values = line.split('、')
                    values = [dictionary.expression(x) for x in values]
                    emitter.emit("return ", ", ".join(values))
                elif line.endswith("をうちだします"):
                    line = line[:-7].strip()
                    values = line.split('、')
                    values = [dictionary.expression(x) for x in values]
                    emitter.emit("print(", ", ".join(values), ", end='')")
                elif line.endswith("おくりだします"):
                    line = line[:-7].strip()
                    if not line:
                        emitter.emit("print()")
                    else:
                        assert line[-1] == 'を', lineno
                        values = line[:-1].split('、')
                        values = [dictionary.expression(x) for x in values]
                        emitter.emit("print(", ", ".join(values), ')')
                elif line.endswith("について、くりかえします"):
                    line = line[:-12].strip()
                    pos = line.find('それぞれの')
                    assert 0 <= pos, lineno
                    target = line[pos+5:].strip()
                    target = ", ".join(target.split('、'))
                    line = line[:pos].strip()
                    if line[-1] == 'の':
                        line = line[:-1].strip()
                        list = dictionary.expression(line)
                        emitter.emit("for ", target, " in ", list, ":")
                    else:
                        assert line.endswith("まして、"), lineno
                        line = line[:-4] + "ます"
                        found = dictionary.lookup_method(line)
                        assert found,  lineno
                        emitter.emitnb("for ", target, " in ")
                        emitter.emit_call(found)
                        emitter.flush()
                        emitter.raw(":\n")
                elif line.endswith("ら、くりかえします"):
                    # while statement
                    emitter.emitnb("while")
                    line = line[:-8].strip()
                    cond = line.split('、')
                    for p in cond:
                        found = []
                        p = p.strip()
                        if p == 'または':
                            emitter.raw(" or")
                        elif p == 'そして':
                            emitter.raw(" and")
                        elif p.endswith("ましたら"):
                            p = p[:-4].strip() + "ます"
                            found = dictionary.lookup_method(p)
                        elif p.endswith("ませんでしたら"):
                            p = p[:-7].strip() + "ます"
                            found = dictionary.lookup_method(p)
                            emitter.raw(" not")
                        elif p.endswith("でしたら"):
                            p = p[:-4].strip()
                            emitter.raw(" ", dictionary.expression(p))
                        elif p.endswith("でないなら"):
                            p = p[:-5].strip()
                            emitter.raw(" not ", dictionary.expression(p))
                        if found:
                            emitter.raw(" ")
                            emitter.emit_call(found)
                            emitter.flush()
                    emitter.raw(":\n")
                elif line.endswith("にいれます"):
                    # assignment
                    line = line[:-5].strip()
                    pos = line.rfind("まして、")
                    if 0 <= pos:
                        target = dictionary.property_form(line[pos + 4:].strip())
                        line = line[:pos] + "ます"
                        if line.startswith("あたらしい") and line.endswith("をつくります"):
                            subject = line[5:-6]
                            if subject in dictionary.classes:
                                if subject in actor_subjects:
                                    actors.append(target)
                                emitter.emit(target, " = ", subject, "()")
                                continue
                        found = dictionary.lookup_method(line)
                        assert found, lineno
                        emitter.emitnb(target, " = ")
                        emitter.emit_call(found)
                        if emitter.flush():
                            print()
                    else:
                        pair = dictionary.split(line, 'を')
                        emitter.emit(pair[1], " = ", dictionary.expression(pair[0]))
            elif line.endswith("です。"):
                line = line[:-1].strip()
                if emitter.function_mode():
                    line = line[:-2].strip()
                    pair = dictionary.split(line, 'は')
                    emitter.emit_argument(pair[0], pair[1])
                else:
                    found = dictionary.lookup_method(line)
                    assert method, lineno
                    target = found[0]
                    emitter.emit("return ", target, ".", found[1], "()")
            elif line:
                line = dictionary.expression(line)
                if assertion:
                    emitter.emit("assert ", line)
                else:
                    emitter.emit(line)
            else:
                emitter.nl()
    if emitter.flush():
        print()

    emitter.reset()
    if actors:
        emitter.nl()
        emitter.emit("while True:")
        emitter.adjust(4)
        for actor in actors:
            emitter.emit(actor, ".default()")

    sys.exit(0)
