exception Uneven
let rec rev_k_groups l k =
    try
        let (rest, acc) = go l k (fun x -> x) in
        acc (rev_k_groups rest k)
    with
    | Uneven -> l
and go l k acc =
    if k = 0 then (l, acc) else
        match l with
        | [] -> raise Uneven
        | x::xs -> go xs (k-1) (fun l -> x :: acc l)

let ex = [1;2;3;4;5]
let r = rev_k_groups ex 2
