# from talon import Module, actions
import time

# mod = Module()


# @mod.action_class
# class Actions:
#     def test():
#         """random"""
#         return 0

# t1 = time.perf_counter()
# for i in range(100000):
#     actions.user.test()
# print((time.perf_counter() - t1)*1000)

# import random
# t1 = time.perf_counter()
# for i in range(10000000):
#     random.random()
# print((time.perf_counter() - t1) * 1000)


# ctx.action_class("user", {
#     test() {
#         return 1;
#     },
# });

# const t1 = Date.now();
# for (let i = 0; i < 10; ++i) {
#     actions.user.test();
# }
# print(Date.now() - t1);

# const t1 = Date.now();
# for (let i = 0; i < 10000000; ++i) {
#     Math.random();
# }
# print(Date.now() - t1);


# action call. 100000 iterations
# py -> py: 950 ms
# py -> js: 1410 ms
# js -> py: 3900 ms
# js -> js: talon.lib.js.JSException: InternalError: wrong js.Context for callback thread

# random. 10000000 iterations
# py random.random(): 365 ms
# js Math.random(): 360 ms
