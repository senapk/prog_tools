## Soma

```hs
soma 4 5 == 9
soma 3 6 == 9
soma -1 4 == 3
```

<!--MAIN_BEGIN-->
### Main
```hs
main = do
    a <- readLn :: IO Int
    b <- readLn :: IO Int
    print $ soma a b

```
<!--MAIN_END-->
