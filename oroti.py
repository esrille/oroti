#!/usr/bin/python3
# -*- coding: utf-8 -*-

真 = True
偽 = False


# 主体: ファイル
class ファイル:

    # ファイルを　ひらきます、とは。
    # 引数: ファイル名
    def ひらきます(self, ファイル名):
        self.file = open(ファイル名)

    # ファイルを　とじます、とは。
    def とじます(self):
        self.file.close()

    def __iter__(self):
        return self.file.__iter__()

    def __next__(self):
        return self.file.__next__()

import sys


# 主体: プログラム
class プログラム:

    # 属性: 引数
    引数 = sys.argv

    # プログラムを　おえます、とは。
    # 引数: ステータス
    def おえます(self, ステータス=0):
        sys.exit(ステータス)


プログラム = プログラム()
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

全角半角表 = str.maketrans('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
                   'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ'
                   '０１２３４５６７８９：；！＋－＊／％＜＞＆｜＾～＝（）［］｛｝',
                   'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                   'abcdefghijklmnopqrstuvwxyz'
                   '0123456789:;!+-*/%<>&|^~=()[]{}',
                   '\n')


class 出力:

    def __init__(self):
        self.インデント = 0
        self.モード = 0
        self.主体 = ''
        self.改行数 = 0
        self.メソッドターゲット = ''
        self.メソッド名 = ''
        self.メソッドインデント = 0
        self.メソッド引数 = []
        self.キーワード引数 = {}
        self.文字列集 = []
        self.文字列カウント = 0

    def ずらします(self, 桁):
        self.インデント = self.インデント + 桁

    def リセットします(self):
        self.インデント = 0
        self.モード = 0
        self.主体 = ''

    def モードをリセットします(self):
        self.モード = 0

    def あわせます(self, 行):
        スペース = 0
        while 行 and 行[0] == '　':
            スペース = スペース + 2
            行 = 行[1:]
        self.インデント = len(行)
        行 = 行.lstrip()
        self.インデント = self.インデント - len(行)
        self.インデント = self.インデント + スペース
        if self.主体:
            self.インデント = self.インデント + 4
        if self.モード == 2:
            self.インデント = self.インデント + 4

    def フラッシュします(self):
        if self.メソッド名 and self.インデント <= self.メソッドインデント:
            バッファー = self.メソッドターゲット + '.' + self.メソッド名 + '('
            くぎり = ''
            for 引数 in self.メソッド引数:
                バッファー = バッファー + くぎり + 引数
                くぎり = ', '
            for なまえ, 値 in self.キーワード引数.items():
                バッファー = バッファー + くぎり + なまえ + '=' + 値
                くぎり = ', '
            バッファー = バッファー + ')'
            バッファー = self.もどします(バッファー)
            print(バッファー, end='')
            self.メソッド名 = ''
            self.メソッド引数 = []
            self.キーワード引数 = {}
            return 真
        return 偽

    def クラスとしてかきだします(self, 主体):
        if self.フラッシュします():
            print()
        assert 主体 != ''
        if self.主体:
            self.インデント = self.インデント - 4
        if self.モード == 2:
            self.インデント = self.インデント - 4
        self.主体 = 主体
        self.あけます(2)
        self.モード = 0
        self.おくりだします('class ', 主体, ':')
        self.モード = 1

    def かきます(self, *引数):
        self.改行数 = 0
        バッファー = ''.join(引数)
        バッファー = self.もどします(バッファー)
        print(バッファー, end='')

    def あけます(self, 行):
        if self.フラッシュします():
            print()
        if self.改行数 < 行:
            行 = 行 - self.改行数
            print('\n' * 行, end='')
            self.改行数 = self.改行数 + 行

    def 字さげします(self):
        self.改行数 = 0
        if self.モード == 1:
            self.モード = 2
            print()
            self.字さげします()
            print('def default(self):')
            self.インデント = self.インデント + 4
        if self.フラッシュします():
            print()
        print(' ' * self.インデント, end='')

    def うちだします(self, *引数):
        self.字さげします()
        バッファー = ''.join(引数)
        バッファー = self.もどします(バッファー)
        print(バッファー, end='')

    def おくりだします(self, *引数):
        self.うちだします(*引数)
        print()

    def よびだしをだします(self, メソッド):
        if self.フラッシュします():
            print()
        self.メソッドターゲット = メソッド[0]
        self.メソッド名 = メソッド[1]
        self.メソッド引数 = メソッド[2]
        self.メソッドインデント = self.インデント

    def 引数としてわたします(self, キーワード, 値):
        self.キーワード引数[キーワード] = 値

    def ととのえます(self, 行):
        文字列 = ''
        カッコ = ''
        結果 = ''
        エスケープ = 偽
        for 字 in 行:
            if not カッコ:
                i = '\'"「『'.find(字)
                if 0 <= i:
                    文字列 = '\'"\'"'[i]
                    結果 = 結果 + '＄' + str(self.文字列カウント) + '＄'
                    カッコ = '\'"」』'[i]
                    self.文字列カウント = self.文字列カウント + 1
                else:
                    字 = 字.translate(全角半角表)
                    結果 = 結果 + 字
            elif エスケープ:
                if 字 == '」' or 字 == '』':
                    文字列 = 文字列 + 字
                else:
                    文字列 = 文字列 + '\\' + 字
                エスケープ = 偽
            elif 字 == '\\':
                エスケープ = 真
            elif 字 == カッコ:
                i = '\'"」』'.find(字)
                文字列 = 文字列 + '\'"\'"'[i]
                self.文字列集.append(文字列)
                文字列 = ''
                カッコ = ''
            else:
                文字列 = 文字列 + 字
        return 結果

    def もどします(self, 値):
        文字列 = ''
        while 値:
            位置 = 値.find('＄')
            if 位置 < 0:
                文字列 = 文字列 + 値
                値 = ''
                break
            文字列 = 文字列 + 値[:位置]
            値 = 値[位置 + 1:]
            位置 = 値.find('＄')
            assert 0 <= 位置
            カウント = 値[:位置]
            文字列 = 文字列 + self.文字列集[int(カウント)]
            値 = 値[位置 + 1:]
        return 文字列

    def メソッドを出力しています(self):
        if self.メソッド名 and self.メソッドインデント < self.インデント:
            return 真
        return 偽


class 辞書:

    def __init__(self):
        self.助詞一覧 = set()
        self.クラス一覧 = set()
        self.メソッド集 = {}
        self.属性一覧 = set()
        self.属性一覧.add('ながさ')
        self.主体 = ''

    def 主体にします(self, なまえ):
        self.主体 = なまえ
        if なまえ:
            self.クラス一覧.add(なまえ)

    def 定義します(self, なまえ, メソッド):
        self.メソッド集[なまえ] = メソッド
        for 助詞 in メソッド[1]:
            self.助詞一覧.add(助詞)

    def わけます(self, 文字列, 助詞列):
        結果 = []
        if not 文字列:
            return 結果
        if not 助詞列:
            結果.append([文字列])
            return 結果
        for 助詞 in 助詞列:
            列 = 助詞列.copy()
            列.remove(助詞)
            i = 0
            while 真:
                位置 = 文字列[i:].find(助詞)
                if 位置 < 1:
                    break
                位置 = 位置 + i
                if len(文字列) <= 位置 + len(助詞):
                    break
                のこり = self.わけます(文字列[位置 + len(助詞):], 列)
                for わけかた in のこり:
                    リスト = [文字列[:位置], 助詞]
                    リスト.extend(わけかた)
                    結果.append(リスト)
                i = 位置 + 1
        return 結果

    def メソッドをみつけます(self, 文字列):
        メソッド = ''
        カウント = 0
        項 = []
        助詞列 = sorted(self.助詞一覧, key=lambda p: len(p), reverse=True)
        for 助詞 in 助詞列:
            i = 0
            while 真:
                j = 文字列[i + 1:].find(助詞)
                if j == -1:
                    break
                i = i + 1 + j
                ターゲット = 文字列[:i]
                なまえ = 文字列[i + len(助詞):]
                if self.メソッド集.__contains__(なまえ):
                    列 = self.メソッド集[なまえ][1]
                else:
                    continue
                if not 列.__contains__(助詞):
                    continue
                if len(なまえ) < len(メソッド):
                    continue

                列 = 列.copy()
                列.remove(助詞)
                if not 列:
                    ターゲット = self.属性形にします(ターゲット)
                    if ターゲット == self.主体:
                        ターゲット = 'self'
                    if len(メソッド) < len(なまえ) or カウント == 0:
                        項 = [ターゲット, 助詞]
                        メソッド = なまえ
                    continue

                結果 = self.わけます(ターゲット, 列)
                if not 結果:
                    continue

                c = 0
                for 候補 in 結果:
                    a = []
                    for 項 in 候補:
                        ペア = self.式2にします(項)
                        c = c + ペア[1]
                        a.append(ペア[0])
                    a.append(助詞)
                    if len(メソッド) < len(なまえ) or カウント <= c:
                        項 = a
                        メソッド = なまえ
        if not 項:
            return 項
        引数 = []
        for 助詞 in self.メソッド集[メソッド][1]:
            for i in range(1, len(項), 2):
                if 項[i] == 助詞:
                    引数.append(項[i - 1])
                    break
        if 引数[0] == self.主体:
            引数[0] = 'self'

        可変長引数 = []
        for 値 in 引数:
            値 = 値.split('、')
            可変長引数.extend(値)

        return 可変長引数[0], self.メソッド集[メソッド][0], 可変長引数[1:]

    def クラスをみつけます(self, 文字列):
        if self.クラス一覧.__contains__(文字列):
            return 文字列
        助詞 = 'は'
        位置 = len(文字列)
        while 真:
            位置 = 文字列.rfind(助詞, 0, 位置)
            if 位置 == -1:
                break
            なまえ = 文字列[:位置]
            if self.クラス一覧.__contains__(なまえ):
                return なまえ
        return ''

    # '[N1]の[N2]の[N3]...', カウント

    def 属性形2にします(self, 文字列):
        カウント = 0
        位置 = len(文字列)
        while 真:
            位置 = 文字列.rfind('の', 0, 位置)
            if 位置 == -1:
                break
            属性 = 文字列[位置 + 1:]
            カッコ = ''
            カッコ位置 = 属性.find('[')
            if 0 <= カッコ位置:
                カッコ = self.式にします(属性[カッコ位置:])
                属性 = 属性[:カッコ位置]
            if self.属性一覧.__contains__(属性):
                ペア = self.属性形2にします(文字列[:位置])
                カウント = ペア[1] + 1
                if not カッコ and 属性 == 'ながさ':
                    return 'len(' + ペア[0] + ')', カウント
                else:
                    return ペア[0] + '.' + 属性 + カッコ, カウント
            elif 文字列[:位置] == self.主体:
                self.属性一覧.add(属性)
                return 'self.' + 属性 + カッコ, カウント
        if 文字列 == self.主体:
            文字列 = 'self'
        return 文字列, カウント

    def 属性形にします(self, 文字列):
        ペア = self.属性形2にします(文字列)
        return ペア[0]

    def 式2にします(self, 文字列):
        カウント = 0
        くぎり = '" ,+-*/%<>&|^~!()[:]'
        for 位置 in range(len(文字列)):
            if not くぎり.__contains__(文字列[位置]):
                break
        if くぎり.__contains__(文字列[位置]):
            return 文字列, カウント
        でだし = 文字列[:位置]
        文字列 = 文字列[位置:]
        for 位置 in range(len(文字列)):
            if くぎり.__contains__(文字列[位置]):
                項 = 文字列[:位置]
                左 = self.属性形2にします(項)
                右 = self.式2にします(文字列[位置:])
                文字列 = でだし + 左[0] + 右[0]
                カウント = 左[1] + 右[1] + カウント
                return 文字列, カウント
        ペア = self.属性形2にします(文字列)
        return でだし + ペア[0], カウント + ペア[1]

    def 式にします(self, 文字列):
        ペア = self.式2にします(文字列)
        return ペア[0]

    def くぎります(self, 文字列, くぎり):
        カウント = 0
        左がわ = 文字列
        右がわ = ''
        位置 = 0
        while 真:
            位置2 = 文字列[位置:].find(くぎり)
            if 位置2 == -1:
                return 左がわ, 右がわ
            位置 = 位置 + 位置2
            cnt = 1
            ペア = self.式2にします(文字列[:位置])
            左 = ペア[0]
            cnt = cnt + ペア[1]
            ペア = self.式2にします(文字列[位置 + len(くぎり):])
            右 = ペア[0]
            cnt = cnt + ペア[1]
            if カウント < cnt:
                カウント = cnt
                左がわ = 左
                右がわ = 右
            位置 = 位置 + 1
        return 左がわ, 右がわ

    def 定義としてよみます(self, 行):
        assert 行.endswith('、とは。')
        行 = 行[:-4].strip()
        assert self.主体 == 行[:len(self.主体)]
        行 = 行[len(self.主体):]
        位置 = 行.rfind('　')
        assert 0 < 位置
        メソッド = 行[位置 + 1:]
        行 = 行[:位置].strip()
        助詞列 = []
        引数 = []
        while 行:
            位置 = 行.find('(')
            if 位置 < 0:
                助詞列.append(行)
                行 = ''
            else:
                助詞 = 行[:位置].strip()
                助詞列.append(助詞)
                行 = 行[位置 + 1:].strip()
                位置 = 行.find(')')
                assert 0 < 位置
                項 = 行[:位置].strip()
                引数.append(項)
                行 = 行[位置 + 1:].strip()
        if メソッド == "はじめにととのえます":
            メソッド = '__init__'
        return メソッド, 助詞列, 引数

    def かきだします(self):
        一覧 = ' '.join(self.クラス一覧)
        print('主体一覧: ', 一覧)
        一覧 = ' '.join(sorted(self.助詞一覧, key=lambda p: len(p), reverse=True))
        print('助詞一覧: ', 一覧)
        print('述語一覧:', end='')
        for なまえ, メソッド in self.メソッド集.items():
            print(なまえ, メソッド)


class トランスパイラー:

    def とりこみます(self, ソース名):
        ソース = ファイル()
        ライブラリ = ファイル()
        ソース.ひらきます(ファイル名=ソース名)
        行番号 = 0
        for 行 in ソース:
            行番号 = 行番号 + 1
            行 = 行.translate(全角半角表)
            行 = 行.strip()
            if 行.startswith('ライブラリ:'):
                行 = 行[6:].strip()
                リスト = 行.split('、')
                for ライブラリ名 in リスト:
                    辞書.主体にします('')
                    ライブラリ.ひらきます(ファイル名=ライブラリ名 + '.py')
                    for 行 in ライブラリ:
                        if 行.startswith('#!'):
                            continue
                        if 行.startswith('# -*- coding:'):
                            continue
                        出力.うちだします(行)
                        行 = 行.translate(全角半角表)
                        行 = 行.strip()
                        if not 行.startswith('#'):
                            continue
                        行 = 行[1:].strip()
                        if 行.endswith('、とは。'):
                            メソッド = 辞書.定義としてよみます(行)
                            辞書.定義します(メソッド[0], メソッド)
                        elif 行.startswith('主体:'):
                            行 = 行[3:].strip()
                            辞書.主体にします(行)
                        elif 行.startswith('属性:'):
                            行 = 行[3:].strip()
                            辞書.属性一覧.add(行)
                    ライブラリ.とじます()
                    辞書.主体にします('')
            elif 行.startswith('主体:'):
                行 = 行[3:].strip()
                辞書.主体にします(行)
            elif 行.endswith('、とは。'):
                メソッド = 辞書.定義としてよみます(行)
                assert len(メソッド[1]) == len(set(メソッド[1]))
                辞書.定義します(メソッド[0], メソッド)
        ソース.とじます()

    def 条件節に訳します(self, 行):
        リスト = 行.split('、')
        for 条件 in リスト:
            メソッド = []
            条件 = 条件.strip()
            if 条件 == 'または':
                出力.かきます(' or')
            elif 条件 == 'そして':
                出力.かきます(' and')
            elif 条件.endswith('ましたら'):
                条件 = 条件[:-4] + 'ます'
                メソッド = 辞書.メソッドをみつけます(条件)
            elif 条件.endswith('ませんでしたら'):
                条件 = 条件[:-7] + 'ます'
                メソッド = 辞書.メソッドをみつけます(条件)
                出力.かきます(' not')
            elif 条件.endswith('でしたら'):
                条件 = 条件[:-4].strip()
                条件 = 辞書.式にします(条件)
                出力.かきます(' ', 条件)
            elif 条件.endswith('でないなら'):
                条件 = 条件[:-5].strip()
                条件 = 辞書.式にします(条件)
                出力.かきます(' not ', 条件)
            if メソッド:
                出力.かきます(' ')
                出力.よびだしをだします(メソッド)
                出力.フラッシュします()

    # '～ます。'.訳します(おわる行)

    def 文に訳します(self, 行):
        メソッド = 辞書.メソッドをみつけます(行)
        if メソッド:
            出力.字さげします()
            if self.アサート:
                出力.かきます('assert ')
            出力.よびだしをだします(メソッド)
        elif 行 == 'うちきります':
            出力.おくりだします('break')
        elif 行.endswith('をかえします'):
            行 = 行[:-6].strip()
            リスト = 行.split('、')
            引数 = []
            for 値 in リスト:
                値 = 辞書.式にします(値)
                引数.append(値)
            引数 = ', '.join(引数)
            出力.おくりだします('return ', 引数)
        elif 行.endswith('をうちだします'):
            行 = 行[:-7].strip()
            リスト = 行.split('、')
            引数 = []
            for 値 in リスト:
                値 = 辞書.式にします(値)
                引数.append(値)
            引数 = ', '.join(引数)
            出力.おくりだします('print(', 引数, ", end='')")
        elif 行.endswith('おくりだします'):
            行 = 行[:-7].strip()
            if not 行:
                出力.おくりだします('print()')
            else:
                assert 行[-1] == 'を'
                リスト = 行[:-1].split('、')
                引数 = []
                for 値 in リスト:
                    値 = 辞書.式にします(値)
                    引数.append(値)
                引数 = ', '.join(引数)
                出力.おくりだします('print(', 引数, ')')
        elif 行.endswith('について、くりかえします'):
            行 = 行[:-12].strip()
            位置 = 行.find('それぞれの')
            assert 0 <= 位置
            ターゲット = 行[位置 + 5:].strip()
            ターゲット = ターゲット.split('、')
            ターゲット = ', '.join(ターゲット)
            行 = 行[:位置].strip()
            if 行[-1] == 'の':
                行 = 行[:-1].strip()
                リスト = 辞書.式にします(行)
                出力.おくりだします('for ', ターゲット, ' in ', リスト, ":")
            else:
                assert 行.endswith('まして、')
                行 = 行[:-4] + 'ます'
                メソッド = 辞書.メソッドをみつけます(行)
                assert メソッド
                出力.うちだします('for ', ターゲット, ' in ')
                出力.よびだしをだします(メソッド)
                出力.フラッシュします()
                出力.かきます(':\n')
        elif 行.endswith('ら、くりかえします'):
            出力.うちだします('while')
            行 = 行[:-8].strip()
            self.条件節に訳します(行)
            出力.かきます(':\n')
        elif 行.endswith('にいれます'):
            行 = 行[:-5].strip()
            位置 = 行.rfind('まして、')
            if 0 <= 位置:
                ターゲット = 行[位置 + 4:].strip()
                ターゲット = 辞書.属性形にします(ターゲット)
                行 = 行[:位置] + 'ます'
                主体 = ''
                if 行.startswith('あたらしい') and 行.endswith('をつくります'):
                    主体 = 行[5:-6]
                if 辞書.クラス一覧.__contains__(主体):
                    if self.アクター主体一覧.__contains__(主体):
                        self.アクター一覧.append(ターゲット)
                    出力.おくりだします(ターゲット, ' = ', 主体, '()')
                else:
                    メソッド = 辞書.メソッドをみつけます(行)
                    assert メソッド
                    出力.うちだします(ターゲット, ' = ')
                    出力.よびだしをだします(メソッド)
                    if 出力.フラッシュします():
                        print()
            else:
                ペア = 辞書.くぎります(行, 'を')
                式 = 辞書.式にします(ペア[0])
                出力.おくりだします(ペア[1], ' = ', 式)

    def 訳します(self, ソース名):
        ソース = ファイル()
        self.アクター主体一覧 = set()
        self.アクター一覧 = []

        ソース.ひらきます(ファイル名=ソース名)
        行番号 = 0
        for 行 in ソース:
            行番号 = 行番号 + 1
            if 行.startswith('－－'):
                continue
            行 = 出力.ととのえます(行)
            if 行.startswith('ライブラリ:'):
                continue
            出力.あわせます(行)
            行 = 行.strip()

            if 出力.モード == 2:
                self.アクター主体一覧.add(辞書.主体)

            if 行.startswith('チェック:'):
                行 = 行[5:].strip()
                self.アサート = 真
            else:
                self.アサート = 偽

            if 行.startswith('主体:'):
                行 = 行[3:].strip()
                辞書.主体にします(行)
                出力.クラスとしてかきだします(辞書.主体)
            elif 行.startswith('はじめに:'):
                辞書.主体にします('')
                出力.リセットします()
                出力.あけます(2)
            elif 行.endswith('ら、'):
                出力.字さげします()
                if 行.startswith('あるいは、'):
                    出力.かきます('elif')
                    行 = 行[5:].strip()
                else:
                    出力.かきます('if')
                行 = 行[:-1].strip()
                self.条件節に訳します(行)
                出力.かきます(':\n')
            elif 行 == 'そうでなければ、':
                出力.おくりだします('else:')
            elif 行 == 'つぎへ。':
                出力.おくりだします('continue')
            elif 行.endswith('、とは。'):
                メソッド = 辞書.定義としてよみます(行)
                出力.あけます(1)
                出力.モードをリセットします()
                出力.うちだします('def ', メソッド[0], '(self')
                if メソッド[2]:
                    引数 = ', '.join(メソッド[2])
                    出力.かきます(', ', 引数)
                出力.かきます('):\n')
            elif 行.endswith('ます。'):
                行 = 行[:-1].strip()
                self.文に訳します(行)
            elif 行.endswith('です。'):
                行 = 行[:-1].strip()
                if 出力.メソッドを出力しています():
                    行 = 行[:-2].strip()
                    ペア = 辞書.くぎります(行, 'は')
                    出力.引数としてわたします(ペア[0], ペア[1])
                else:
                    メソッド = 辞書.メソッドをみつけます(行)
                    assert メソッド
                    出力.うちだします('return ', メソッド[0], '.', メソッド[1], '()')
            elif 行:
                行 = 辞書.式にします(行)
                if self.アサート:
                    出力.おくりだします('assert ', 行)
                else:
                    出力.おくりだします(行)
            else:
                出力.あけます(1)
        ソース.とじます()

        if 出力.フラッシュします():
            print()
        出力.リセットします()

        if self.アクター一覧:
            出力.あけます(1)
            出力.おくりだします('while True:')
            出力.ずらします(4)
            for アクター in self.アクター一覧:
                出力.おくりだします(アクター, '.default()')


if len(プログラム.引数) < 2:
    プログラム.おえます()

出力 = 出力()
辞書 = 辞書()

出力.かきます('#!/usr/bin/python3\n')
出力.かきます('# -*- coding: utf-8 -*-\n')
出力.かきます('\n')
出力.かきます('真 = True\n')
出力.かきます('偽 = False\n')

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

for なまえ, メソッド in python_methods.items():
    辞書.定義します(なまえ, メソッド)

トランスパイラー = トランスパイラー()
トランスパイラー.とりこみます(プログラム.引数[1])
トランスパイラー.訳します(プログラム.引数[1])
