namespace Taidalog

[<RequireQualifiedAccess>]
module Array =
    let count (projection: 'T -> bool) (array: 'T array) : int =
        array |> Array.filter projection |> Array.length

    let trySkip (count: int) (array: 'T array) : 'T array option =
        if count > (array |> Array.length) then
            None
        else
            Array.skip count array |> Some

    let tryMid (start: int) (len: int) (array: 'T array) : 'T array option =
        array |> trySkip start |> Option.map (Array.truncate len)

[<RequireQualifiedAccess>]
module Tuple =
    let map (mapping: 'T -> 'U) (x: 'T, y: 'T) : 'U * 'U = mapping x, mapping y

module StringMetric =
    let midStart (start: int) (range: int) : int = max 0 (start - range)
    let midLen (start: int) (range: int) : int = min (range * 2 + 1) (start + range + 1)

    let rangef (s1: string) (s2: string) : int =
        max (String.length s1) (String.length s2) / 2 - 1 |> max 0

    let midChars (index: int) (range: int) (array: 'T array) : 'T array option =
        Array.tryMid (midStart index range) (midLen index range) array

    let candidateIndexes (c: 'T, ics: (int * 'T) array option) : int array option =
        Option.map (Array.filter (fun (_, c') -> c' = c) >> Array.map fst) ics

    let candidatesArrayf (s1: string) (s2: string) : int array array =
        let range: int = rangef s1 s2
        let s2Indexed = s2 |> Seq.toArray |> Array.indexed
        let midChars' (index: int) : (int * char) array option = midChars index range s2Indexed

        s1
        |> Seq.toArray
        |> Array.mapi (fun i c -> c, midChars' i)
        |> Array.map candidateIndexes
        |> Array.map (Option.defaultValue Array.empty)

    let folder (matchings: int option array) (index: int, candidates: int array) : int option array =
        let availableIndex =
            candidates
            |> Array.tryFind (fun x -> Array.contains (Some x) matchings = false && Array.item index matchings = None)

        match availableIndex with
        | Some x -> Array.updateAt index (Some x) matchings
        | None -> matchings

    let matchingsf (s: string) (candidatesArray: int array array) : int option array =
        // let initialMatchings: int option array = Array.replicate (String.length s) None
        let initialMatchings: int option array =
            Array.init (String.length s) (fun _ -> None)

        candidatesArray |> Array.indexed |> Array.fold folder initialMatchings

    let jaroSimilarity (s1: string) (s2: string) : float =
        if String.length s1 = 0 || String.length s2 = 0 then
            0.
        else
            let candidatesArray: int array array = candidatesArrayf s1 s2
            let matchings: int option array = matchingsf s1 candidatesArray

            let matchedIndexes: int array =
                matchings |> Array.filter Option.isSome |> Array.map Option.get

            let m: int = Array.length matchedIndexes
            let t: int = matchedIndexes |> Array.pairwise |> Array.count (fun (x, y) -> x > y)

            if m = 0 then
                0.
            else
                let s1f: float = s1 |> String.length |> float
                let s2f: float = s2 |> String.length |> float
                let mf = float m
                let tf = float t
                (mf / s1f + mf / s2f + (mf - tf) / mf) / 3.

    let jarotaidalogSimilarity (s1: string) (s2: string) : float =
        if String.length s1 = 0 || String.length s2 = 0 then
            0.
        else
            let w1: float =
                (s1, s2)
                |> Tuple.map (String.length >> float)
                ||> fun x y -> 1. - ((x - y) / x |> abs)

            let w2: float =
                s1
                |> Seq.toArray
                |> Array.truncate (String.length s2)
                |> Array.filter (fun c -> s2 |> Seq.toArray |> Array.contains c)
                |> Array.length
                |> float
                |> fun x -> x / (s2 |> String.length |> float)

            jaroSimilarity s1 s2 * List.average [ w1; w2 ]
