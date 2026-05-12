from __future__ import annotations
from collections.abc import Callable
from typing import Any
from fable_library.array_ import (filter, skip, truncate, map as map_1, indexed, map_indexed, empty, try_find, contains, update_at, initialize, fold, pairwise)
from fable_library.array_ import (Array, Int32ArrayCons)
from fable_library.core import (int32, float64)
from fable_library.list import (average, of_array)
from fable_library.option import (map, erase, default_arg, value as value_4)
from fable_library.util import (UNIT, max, compare_primitives, min, equals, to_enumerable, Unit, structural_hash, string_hash)

def Array_count[T](projection: Callable[[T], bool], array: Array[T]) -> int32:
    return int32(len(filter(projection, array)))


def Array_trySkip[T](count: int32, array: Array[T]) -> Array[T] | None:
    if count > int32(len(array)):
        return None

    else:
        return skip(count, array, None)



def Array_tryMid[T](start: int32, len_1: int32, array: Array[T]) -> Array[T] | None:
    def mapping(array_2: Array[T], len_1: Any=len_1) -> Array[T]:
        return truncate(len_1, array_2)

    return erase(map(mapping, Array_trySkip(start, array)))


def Tuple_map[T, U](mapping: Callable[[T], U], x: T, y: T) -> tuple[U, U]:
    return (mapping(x), mapping(y))


def StringMetric_midStart(start: int32, range: int32) -> int32:
    return max(compare_primitives, int32.ZERO, start - range)


def StringMetric_midLen(start: int32, range: int32) -> int32:
    return min(compare_primitives, (range * int32.TWO) + int32.ONE, (start + range) + int32.ONE)


def StringMetric_rangef(s1: str, s2: str) -> int32:
    return max(compare_primitives, int32.ZERO, (max(compare_primitives, int32(len(s1)), int32(len(s2))) // int32.TWO) - int32.ONE)


def StringMetric_midChars[T](index: int32, range: int32, array: Array[T]) -> Array[T] | None:
    return erase(Array_tryMid(StringMetric_midStart(index, range), StringMetric_midLen(index, range), array))


def StringMetric_candidateIndexes[T](c: T, ics: Array[tuple[int32, T]] | None=None) -> Array[int32] | None:
    def _arrow27(arg: Array[tuple[int32, T]], c: Any=c) -> Array[int32]:
        def mapping(tuple: tuple[int32, T]) -> int32:
            return tuple[0]

        def predicate(tupled_arg: tuple[int32, T]) -> bool:
            c_0027: Any = tupled_arg[1]
            return equals(c_0027, c)

        return map_1(mapping, filter(predicate, arg), Int32ArrayCons)

    return erase(map(_arrow27, ics))


def StringMetric_candidatesArrayf(s1: str, s2: str) -> Array[Array[int32]]:
    range: int32 = StringMetric_rangef(s1, s2)
    s2indexed: Array[tuple[int32, str]] = indexed(Array[Any](to_enumerable(s2)))
    def mid_chars_0027(index: int32) -> Array[tuple[int32, str]] | None:
        return erase(StringMetric_midChars(index, range, s2indexed))

    def mapping_1(tupled_arg: tuple[str, Array[tuple[int32, str]] | None]) -> Array[int32] | None:
        return erase(StringMetric_candidateIndexes(tupled_arg[0], tupled_arg[1]))

    def mapping(i: int32, c: str) -> tuple[str, Array[tuple[int32, str]] | None]:
        return (c, mid_chars_0027(i))

    array_3 = map_1(mapping_1, map_indexed(mapping, Array[Any](to_enumerable(s1)), None), None)
    def _arrow29(__unit: Unit=UNIT) -> Callable[[Array[int32] | None], Array[int32]]:
        value: Array[int32] = empty()
        def _arrow28(option: Array[int32] | None=None) -> Array[int32]:
            return default_arg(option, value)

        return _arrow28

    return map_1(_arrow29(), array_3, None)


def StringMetric_folder(matchings: Array[int32 | None], index: int32, candidates: Array[int32]) -> Array[int32 | None]:
    def predicate(x: int32, matchings: Any=matchings, index: Any=index) -> bool:
        class ObjectExpr30:
            def Equals(self, x_1: int32 | None=None, y: int32 | None=None) -> bool:
                return equals(x_1, y)

            def GetHashCode(self, x_1: int32 | None=None) -> int32:
                return structural_hash(x_1)

        if contains(x, matchings, ObjectExpr30()) == False:
            return equals(matchings[index], None)

        else:
            return False


    available_index: int32 | None = erase(try_find(predicate, candidates))
    if available_index is None:
        return matchings

    else:
        x_2: int32 = available_index
        return update_at(index, x_2, matchings, None)



def StringMetric_matchingsf(s: str, candidates_array: Array[Array[int32]]) -> Array[int32 | None]:
    def _arrow31(_arg: int32) -> int32 | None:
        return None

    initial_matchings = initialize(int32(len(s)), _arrow31, None)
    def _arrow32(matchings: Array[int32 | None], tupled_arg: tuple[int32, Array[int32]]) -> Array[int32 | None]:
        return StringMetric_folder(matchings, tupled_arg[0], tupled_arg[1])

    return fold(_arrow32, initial_matchings, indexed(candidates_array))


def StringMetric_jaroSimilarity(s1: str, s2: str) -> float64:
    if True if (int32(len(s1)) == int32.ZERO) else (int32(len(s2)) == int32.ZERO):
        return float64(0.0)

    else:
        candidates_array: Array[Array[int32]] = StringMetric_candidatesArrayf(s1, s2)
        matchings = StringMetric_matchingsf(s1, candidates_array)
        def predicate(option: int32 | None=None) -> bool:
            return option is not None

        matched_indexes: Array[int32] = map_1(value_4, filter(predicate, matchings), Int32ArrayCons)
        m: int32 = int32(len(matched_indexes))
        def projection(tupled_arg: tuple[int32, int32]) -> bool:
            x: int32 = tupled_arg[0]
            y: int32 = tupled_arg[1]
            return x > y

        t: int32 = Array_count(projection, pairwise(matched_indexes))
        if m == int32.ZERO:
            return float64(0.0)

        else:
            s1f: float64 = float64(int32(len(s1)))
            s2f: float64 = float64(int32(len(s2)))
            mf: float64 = float64(m)
            tf: float64 = float64(t)
            return (((mf / s1f) + (mf / s2f)) + ((mf - tf) / mf)) / float64(3.0)




def StringMetric_jarotaidalogSimilarity(s1: str, s2: str) -> float64:
    if True if (int32(len(s1)) == int32.ZERO) else (int32(len(s2)) == int32.ZERO):
        return float64(0.0)

    else:
        w1: float64
        tupled_arg_1: tuple[float64, float64]
        tupled_arg: tuple[str, str] = (s1, s2)
        def mapping(arg: str) -> float64:
            return float64(int32(len(arg)))

        tupled_arg_1 = Tuple_map(mapping, tupled_arg[0], tupled_arg[1])
        x_1: float64 = tupled_arg_1[0]
        w1 = float64(1.0) - abs((x_1 - tupled_arg_1[1]) / x_1)
        def predicate(c: str, s2: Any=s2) -> bool:
            class ObjectExpr33:
                def Equals(self, x_2: str, y_2: str) -> bool:
                    return x_2 == y_2

                def GetHashCode(self, x_2: str) -> int32:
                    return string_hash(x_2)

            return contains(c, Array[Any](to_enumerable(s2)), ObjectExpr33())

        def _arrow34(s1: Any=s1, s2: Any=s2) -> Array[str]:
            array: Array[str] = Array[Any](to_enumerable(s1))
            return truncate(int32(len(s2)), array)

        w2: float64 = float64(int32(len(filter(predicate, _arrow34())))) / float64(int32(len(s2)))
        class ObjectExpr35:
            def GetZero(self, __unit: Unit=UNIT) -> float64:
                return float64(0.0)

            def Add(self, x_5: float64, y_3: float64) -> float64:
                return x_5 + y_3

            def DivideByInt(self, x_4: float64, i: int32) -> float64:
                return x_4 / i

        return StringMetric_jaroSimilarity(s1, s2) * average(of_array(Array[float64]([w1, w2])), ObjectExpr35())



