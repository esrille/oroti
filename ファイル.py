# -*- coding: utf-8 -*-


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
