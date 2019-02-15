# -*- coding: utf-8 -*-

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
