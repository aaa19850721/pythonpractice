# coding=utf-8
import copy

"""
@author:  xueyun
@license: Apache Licence
@contact: znmei12@gmail.com
@site: http://www.cloudgrassland.com
@file: bucket_state.py
@time: 2015/12/28 10:37
"""

BUCKET_CAPICITY = [8, 5, 3]
BUCKET_INIT_STATE = [8, 0, 0]
BUCKET_FINAL_STATE = [4, 4, 0]


class TagAction:
    def __init__(self, water,bucket_from, bucket_to):
        self.water = water
        self.bucket_from = bucket_from
        self.bucket_to = bucket_to



class BucketState:
    def __init__(self, bucket_s=BUCKET_INIT_STATE, state=None):
        if state is None:
            self.bucket_s = bucket_s
            self.cur_action = TagAction(8, -1, 0)
        else:
            self.bucket_s = state.bucket_s
            self.cur_action = copy.deepcopy(state.cur_action)

    def deep_copy_state(self, state):
        self.bucket_s = copy.deepcopy(state.bucket_s)
        self.cur_action = copy.deepcopy(state.cur_action)

    def is_same_state(self, bucket_s):
        for i in range(0, 3):
            if self.bucket_s[i] != bucket_s[i]:
                return False
        return True

    def is_bucket_empty(self, bucket):
        assert 0 <= bucket < 3
        return self.bucket_s[bucket] == 0

    def is_bucket_full(self, bucket):
        assert 0 <= bucket < 3
        return self.bucket_s[bucket] >= BUCKET_CAPICITY[bucket]

    def print_states(self):
        print("Dump " + str(self.cur_action.water) + " water from " + str(int(self.cur_action.bucket_from)+1) +
              " to " + str(self.cur_action.bucket_to+1) + ",", end='')
        print("bucket water states is :", end='')

        for i in range(0, 3):
            print(str(self.bucket_s[i]) + " ", end='')

        print()

    def is_final_state(self):
        return self.is_same_state(BUCKET_FINAL_STATE)

    def can_task_dump_action(self, bucket_from, bucket_to):
        assert 0 <= bucket_from < 3
        assert 0 <= bucket_to < 3
        if bucket_from != bucket_to and not self.is_bucket_empty(bucket_from) and not self.is_bucket_full(bucket_to):
            return True
        return False

    def dump_water(self, bucket_from, bucket_to, next):
        next.bucket_s = copy.deepcopy(self.bucket_s)
        dump_water = BUCKET_CAPICITY[bucket_to] - next.bucket_s[bucket_to]
        if next.bucket_s[bucket_from] >= dump_water:
            next.bucket_s[bucket_to] += dump_water
            next.bucket_s[bucket_from] -= dump_water
        else:
            next.bucket_s[bucket_to] += next.bucket_s[bucket_from]
            dump_water = next.bucket_s[bucket_from]
            next.bucket_s[bucket_from] = 0
        if dump_water > 0:
            next.cur_action = TagAction( dump_water,bucket_from, bucket_to)
            return True
        return False