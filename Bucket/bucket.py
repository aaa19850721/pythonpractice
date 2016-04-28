# coding=utf-8
"""
@author:  xueyun
@license: Apache Licence 
@contact: znmei12@gmail.com
@site: http://www.cloudgrassland.com
@file: bucket.py
@time: 2015/12/28 10:37
"""
from collections import deque
from bucket_state import BucketState


def is_same_bucket_state(state1, state2):
    return state1.is_same_state(state2.bucket_s)


def is_processed_state(states, new_state):
    it = len(states)
    for i in range(0, len(states)):
        if is_same_bucket_state(states[i], new_state):
            it = i
            break
    return it != len(states)


def print_result(states):
    print("Find Result")
    for i in range(0, len(states)):
        states[i].print_states()
    print("\n" + "\n")


def search_state(states):
    current = states[-1]
    if current.is_final_state():
        print_result(states)
        return
    for j in range(0, 3):
        for i in range(0, 3):
            search_state_on_action(states, current, i, j)


def search_state_on_action(states, current, bucket_from, bucket_to):
    if current.can_task_dump_action(bucket_from, bucket_to):
        next = BucketState()
        bucket_dump = current.dump_water(bucket_from, bucket_to, next)
        if bucket_dump and not is_processed_state(states,next):
            states.append(next)
            search_state(states)
            states.pop()


if __name__ == '__main__':
    init = BucketState()
    states = []
    states.append(init)
    search_state(states)
    assert states.__len__() == 1


